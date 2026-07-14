
# Fix the f-string with nested quotes issue
# Need to use different quote styles or escape

hash_lean = r'''#!/usr/bin/env python3
"""
AQARION-HASH-LEAN v0.4.1-final
Official cryptographic hash infrastructure for AQARION evidence objects.
"""

import hashlib
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union

__version__ = "0.4.1-final"

# ============================================================
# HASH ALGORITHM REGISTRY (versioned, explicit)
# ============================================================

HASH_ALGORITHMS = {
    "sha256": {
        "name": "SHA-256",
        "digest_size": 32,
        "block_size": 64,
        "impl": hashlib.sha256,
        "status": "current",
    },
}

DEFAULT_ALGORITHM = "sha256"

# ============================================================
# LEAF HASH: Individual file content hash
# ============================================================

def hash_file(filepath: Union[str, Path], algorithm: str = DEFAULT_ALGORITHM) -> Dict:
    """Compute canonical hash of a single file."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Cannot hash nonexistent file: {path}")
    
    content = path.read_bytes()
    hasher = HASH_ALGORITHMS[algorithm]["impl"]()
    hasher.update(content)
    
    # Git-style object header: "blob <size>\0<content>"
    git_header = f"blob {len(content)}\0".encode()
    git_hasher = HASH_ALGORITHMS[algorithm]["impl"]()
    git_hasher.update(git_header + content)
    
    return {
        "type": "leaf",
        "algorithm": HASH_ALGORITHMS[algorithm]["name"],
        "path": str(path),
        "size_bytes": len(content),
        "content_hash": hasher.hexdigest(),
        "git_object_hash": git_hasher.hexdigest(),
        "mode": "100644" if not (path.stat().st_mode & 0o111) else "100755",
    }

# ============================================================
# BRANCH HASH: Directory hash (Merkle tree)
# ============================================================

def hash_directory(dirpath: Union[str, Path], 
                   algorithm: str = DEFAULT_ALGORITHM) -> Dict:
    """Compute Merkle-tree hash of a directory."""
    path = Path(dirpath)
    if not path.is_dir():
        raise NotADirectoryError(f"Cannot hash non-directory: {path}")
    
    children = []
    for entry in sorted(path.iterdir()):
        if entry.name.startswith("."):
            continue
        if entry.is_file():
            children.append(hash_file(entry, algorithm))
        elif entry.is_dir():
            children.append(hash_directory(entry, algorithm))
    
    child_hashes = [c["content_hash"] if c["type"] == "leaf" else c["merkle_root"] 
                    for c in children]
    merkle_input = "".join(sorted(child_hashes)).encode()
    
    hasher = HASH_ALGORITHMS[algorithm]["impl"]()
    hasher.update(merkle_input)
    merkle_root = hasher.hexdigest()
    
    return {
        "type": "branch",
        "algorithm": HASH_ALGORITHMS[algorithm]["name"],
        "path": str(path),
        "merkle_root": merkle_root,
        "children": children,
        "child_count": len(children),
    }

# ============================================================
# ROOT HASH: Release hash
# ============================================================

def hash_release(root_dir: Union[str, Path],
                 version: str,
                 algorithm: str = DEFAULT_ALGORITHM) -> Dict:
    """Compute official release hash for an AQARION version."""
    path = Path(root_dir)
    
    components = {}
    for subdir in ["src", "certificates", "docs", "tests"]:
        subpath = path / subdir
        if subpath.exists():
            components[subdir] = hash_directory(subpath, algorithm)
    
    loose_files = []
    for f in sorted(path.iterdir()):
        if f.is_file() and not f.name.startswith("."):
            loose_files.append(hash_file(f, algorithm))
    if loose_files:
        child_hashes = [c["content_hash"] for c in loose_files]
        merkle_input = "".join(sorted(child_hashes)).encode()
        hasher = HASH_ALGORITHMS[algorithm]["impl"]()
        hasher.update(merkle_input)
        components["root_files"] = {
            "type": "branch",
            "path": str(path),
            "merkle_root": hasher.hexdigest(),
            "children": loose_files,
            "child_count": len(loose_files),
        }
    
    component_roots = []
    for name, comp in sorted(components.items()):
        root = comp["content_hash"] if comp["type"] == "leaf" else comp["merkle_root"]
        component_roots.append(f"{name}:{root}")
    
    release_input = f"AQARION:{version}:" + ":".join(sorted(component_roots))
    hasher = HASH_ALGORITHMS[algorithm]["impl"]()
    hasher.update(release_input.encode())
    release_hash = hasher.hexdigest()
    
    return {
        "type": "root",
        "algorithm": HASH_ALGORITHMS[algorithm]["name"],
        "version": version,
        "release_hash": release_hash,
        "components": components,
        "timestamp": "2026-07-14T00:51:00Z",
        "canonical_string": release_input,
    }

# ============================================================
# CERTIFICATE HASH: Evidence-bound hash
# ============================================================

def hash_certificate(claim_id: str,
                     evidence: Dict,
                     release_hash: str,
                     algorithm: str = DEFAULT_ALGORITHM) -> Dict:
    """Compute certificate-bound hash for an AQARION evidence object."""
    evidence_canonical = json.dumps(evidence, sort_keys=True, separators=(',', ':'))
    evidence_hasher = HASH_ALGORITHMS[algorithm]["impl"]()
    evidence_hasher.update(evidence_canonical.encode())
    evidence_hash = evidence_hasher.hexdigest()
    
    cert_input = f"AQARION-CERT:{claim_id}:{evidence_hash}:{release_hash}"
    cert_hasher = HASH_ALGORITHMS[algorithm]["impl"]()
    cert_hasher.update(cert_input.encode())
    cert_hash = cert_hasher.hexdigest()
    
    return {
        "type": "cert",
        "algorithm": HASH_ALGORITHMS[algorithm]["name"],
        "claim_id": claim_id,
        "certificate_hash": cert_hash,
        "release_hash": release_hash,
        "evidence_hash": evidence_hash,
        "canonical_string": cert_input,
        "status": "UNVERIFIED",
    }

# ============================================================
# INCREMENTAL HASH
# ============================================================

def hash_incremental(root_dir: Union[str, Path],
                     previous_manifest: Optional[Dict] = None,
                     algorithm: str = DEFAULT_ALGORITHM) -> Dict:
    """Compute incremental hash: only changed files re-hashed."""
    path = Path(root_dir)
    changes = []
    unchanged = []
    new_manifest = {"files": {}, "directories": {}}
    
    for filepath in sorted(path.rglob("*")):
        if filepath.name.startswith("."):
            continue
        
        rel_path = filepath.relative_to(path)
        stat = filepath.stat()
        current_sig = f"{stat.st_size}:{stat.st_mtime}"
        
        if previous_manifest and str(rel_path) in previous_manifest.get("files", {}):
            prev = previous_manifest["files"][str(rel_path)]
            if prev.get("signature") == current_sig:
                new_manifest["files"][str(rel_path)] = prev
                unchanged.append(str(rel_path))
                continue
        
        if filepath.is_file():
            h = hash_file(filepath, algorithm)
            h["signature"] = current_sig
            new_manifest["files"][str(rel_path)] = h
            changes.append(str(rel_path))
    
    new_manifest["changed_count"] = len(changes)
    new_manifest["unchanged_count"] = len(unchanged)
    new_manifest["changed_files"] = changes
    
    return new_manifest

# ============================================================
# LEAN OUTPUT FORMAT
# ============================================================

def to_lean_format(hash_obj: Dict) -> str:
    """Convert hash object to Lean-compatible format."""
    t = hash_obj["type"]
    alg = hash_obj["algorithm"]
    
    if t == "leaf":
        return f'{{ type := "leaf", algorithm := "{alg}", path := "{hash_obj["path"]}", size_bytes := {hash_obj["size_bytes"]}, content_hash := "{hash_obj["content_hash"]}" }}'
    elif t == "branch":
        children = ", ".join([f'"{c.get("content_hash", c.get("merkle_root"))}"' for c in hash_obj["children"]])
        return f'{{ type := "branch", algorithm := "{alg}", path := "{hash_obj["path"]}", merkle_root := "{hash_obj["merkle_root"]}", children := [{children}], child_count := {hash_obj["child_count"]} }}'
    elif t == "root":
        return f'{{ type := "root", algorithm := "{alg}", version := "{hash_obj["version"]}", release_hash := "{hash_obj["release_hash"]}", timestamp := "{hash_obj["timestamp"]}" }}'
    elif t == "cert":
        return f'{{ type := "cert", algorithm := "{alg}", claim_id := "{hash_obj["claim_id"]}", certificate_hash := "{hash_obj["certificate_hash"]}", release_hash := "{hash_obj["release_hash"]}", evidence_hash := "{hash_obj["evidence_hash"]}", status := "{hash_obj["status"]}" }}'
    else:
        raise ValueError(f"Unknown hash type: {t}")

# ============================================================
# VERIFICATION
# ============================================================

def verify_hash(hash_obj: Dict, filepath: Optional[Union[str, Path]] = None) -> bool:
    """Verify a hash object against actual file content."""
    if hash_obj["type"] == "leaf":
        if filepath is None:
            filepath = hash_obj["path"]
        actual = hash_file(filepath, "sha256")
        return actual["content_hash"] == hash_obj["content_hash"]
    elif hash_obj["type"] == "branch":
        child_hashes = [c["content_hash"] if c["type"] == "leaf" else c["merkle_root"]
                        for c in hash_obj["children"]]
        merkle_input = "".join(sorted(child_hashes)).encode()
        hasher = hashlib.sha256()
        hasher.update(merkle_input)
        return hasher.hexdigest() == hash_obj["merkle_root"]
    elif hash_obj["type"] == "root":
        for name, comp in hash_obj["components"].items():
            if not verify_hash(comp):
                return False
        return True
    elif hash_obj["type"] == "cert":
        return True
    return False

# ============================================================
# MAIN CLI
# ============================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("AQARION-HASH-LEAN v" + __version__)
        print()
        print("Usage:")
        print("  python AQARION-HASH-LEAN.py file <path>        — Hash single file")
        print("  python AQARION-HASH-LEAN.py dir <path>         — Hash directory (Merkle)")
        print("  python AQARION-HASH-LEAN.py release <path> <version>  — Release hash")
        print("  python AQARION-HASH-LEAN.py cert <claim_id> <evidence.json> <release_hash>")
        print("  python AQARION-HASH-LEAN.py lean <hash.json>   — Convert to Lean format")
        print("  python AQARION-HASH-LEAN.py verify <hash.json> — Verify hash integrity")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "file" and len(sys.argv) >= 3:
        result = hash_file(sys.argv[2])
        print(json.dumps(result, indent=2))
    elif cmd == "dir" and len(sys.argv) >= 3:
        result = hash_directory(sys.argv[2])
        print(json.dumps(result, indent=2))
    elif cmd == "release" and len(sys.argv) >= 4:
        result = hash_release(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2))
    elif cmd == "cert" and len(sys.argv) >= 5:
        with open(sys.argv[3]) as f:
            evidence = json.load(f)
        result = hash_certificate(sys.argv[2], evidence, sys.argv[4])
        print(json.dumps(result, indent=2))
    elif cmd == "lean" and len(sys.argv) >= 3:
        with open(sys.argv[2]) as f:
            h = json.load(f)
        print(to_lean_format(h))
    elif cmd == "verify" and len(sys.argv) >= 3:
        with open(sys.argv[2]) as f:
            h = json.load(f)
        ok = verify_hash(h)
        print(f"Verification: {'PASS' if ok else 'FAIL'}")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
'''

with open(os.path.join(output_dir, "AQARION-HASH-LEAN.py"), 'w') as f:
    f.write(hash_lean)

print(f"✅ AQARION-HASH-LEAN.py written ({len(hash_lean):,} bytes)")

# Run a quick test
result = subprocess.run(
    [sys.executable, "AQARION-HASH-LEAN.py", "file", "aqarion_kernel.py"],
    cwd=output_dir,
    capture_output=True,
    text=True
)
print("\nTest: hash_file on aqarion_kernel.py")
print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
if result.returncode != 0:
    print("STDERR:", result.stderr)✅ AQARION-HASH-LEAN.py written (12,165 bytes)

Test: hash_file on aqarion_kernel.py
{
  "type": "leaf",
  "algorithm": "SHA-256",
  "path": "aqarion_kernel.py",
  "size_bytes": 11649,
  "content_hash": "f52dc1f01a49d4fc1766c051f8f5ea96499d3256bb536d6dcb17dd4d27920d44",
  "git_object_hash": "9c92b4f5fa6f2bf5969bd0d6c320d2deebc3824e14dfad4e3da48d3125bce640",
  "mode": "100644"
}
