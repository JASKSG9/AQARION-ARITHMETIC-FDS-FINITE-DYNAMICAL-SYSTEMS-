
verify_hashes_py = '''#!/usr/bin/env python3
"""
AQARION Hash Manifest Verifier
===============================
Version: 1.0
Claim: All artifacts (paper.pdf, datasets, figures, code, Lean files) have
       computed SHA256 hashes that match the manifest.

CRITICAL: This script MUST NOT import from any AQARION source module.
          It computes hashes independently and compares against manifest.

Exit: 0 = PASS, 1 = FAIL, 2 = ERROR
"""

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ============================================================
# CONFIGURATION — File patterns to hash
# ============================================================
DEFAULT_HASH_PATTERNS = [
    "paper.pdf",
    "**/*.csv",
    "**/*.json",
    "**/*.npy",
    "**/*.png",
    "**/*.jpg",
    "**/*.pdf",
    "**/*.lean",
    "**/*.py",
    "**/*.md",
    "**/*.yml",
    "**/*.yaml",
    "!**/__pycache__/**",
    "!**/.git/**",
    "!**/node_modules/**",
    "!**/.venv/**",
    "!**/venv/**",
    "!**/*.pyc",
]

MANIFEST_FILENAME = "hash_manifest.json"


def compute_sha256(filepath: Path) -> str:
    """Compute SHA256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def discover_files(repo_root: Path, patterns: List[str]) -> List[Path]:
    """Discover files matching patterns, excluding negated patterns."""
    include_patterns = [p for p in patterns if not p.startswith("!")]
    exclude_patterns = [p[1:] for p in patterns if p.startswith("!")]

    files = set()
    for pattern in include_patterns:
        for match in repo_root.glob(pattern):
            if match.is_file():
                files.add(match.resolve())

    # Apply exclusions
    excluded = set()
    for pattern in exclude_patterns:
        for match in repo_root.glob(pattern):
            if match.is_file():
                excluded.add(match.resolve())
            elif match.is_dir():
                for child in match.rglob("*"):
                    if child.is_file():
                        excluded.add(child.resolve())

    return sorted(files - excluded)


def load_manifest(repo_root: Path) -> Optional[Dict[str, str]]:
    """Load existing hash manifest if present."""
    manifest_path = repo_root / MANIFEST_FILENAME
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            return json.load(f)
    return None


def save_manifest(repo_root: Path, manifest: Dict[str, str]) -> Path:
    """Save hash manifest to repository root."""
    manifest_path = repo_root / MANIFEST_FILENAME
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
    return manifest_path


def verify_hashes(repo_root: Path, evidence, logger) -> Tuple[bool, Dict]:
    """
    Compute hashes for all tracked files and compare against manifest.
    If no manifest exists, generate one (first-run mode).
    """
    files = discover_files(repo_root, DEFAULT_HASH_PATTERNS)
    evidence.add_metric("files_discovered", len(files))
    logger.info(f"Discovered {len(files)} files for hashing")

    current_hashes = {}
    for filepath in files:
        rel_path = str(filepath.relative_to(repo_root))
        current_hashes[rel_path] = compute_sha256(filepath)

    manifest = load_manifest(repo_root)

    if manifest is None:
        logger.warn("No existing hash manifest found. Generating new manifest.")
        manifest_path = save_manifest(repo_root, current_hashes)
        evidence.add_check(
            name="manifest_exists",
            passed=True,  # We just created it
            value=str(manifest_path),
            expected="generated"
        )
        evidence.add_note(
            "First-run mode: Generated new hash_manifest.json. "
            "Future runs will verify against this baseline."
        )
        return True, current_hashes

    evidence.add_check(
        name="manifest_exists",
        passed=True,
        value=MANIFEST_FILENAME,
        expected="exists"
    )

    # Compare current hashes against manifest
    mismatches = []
    missing_in_manifest = []
    missing_in_filesystem = []

    # Check for files that exist now but aren't in manifest (new files)
    for rel_path in current_hashes:
        if rel_path not in manifest:
            missing_in_manifest.append(rel_path)
            evidence.add_check(
                name=f"hash_match:{rel_path}",
                passed=False,
                value="new file not in manifest",
                expected="in manifest"
            )
        elif current_hashes[rel_path] != manifest[rel_path]:
            mismatches.append({
                "file": rel_path,
                "current": current_hashes[rel_path],
                "manifest": manifest[rel_path]
            })
            evidence.add_check(
                name=f"hash_match:{rel_path}",
                passed=False,
                value=current_hashes[rel_path][:16] + "...",
                expected=manifest[rel_path][:16] + "..."
            )
        else:
            evidence.add_check(
                name=f"hash_match:{rel_path}",
                passed=True,
                value=current_hashes[rel_path][:16] + "...",
                expected=manifest[rel_path][:16] + "..."
            )

    # Check for files in manifest that no longer exist (deleted files)
    for rel_path in manifest:
        if rel_path not in current_hashes:
            missing_in_filesystem.append(rel_path)
            evidence.add_check(
                name=f"hash_match:{rel_path}",
                passed=False,
                value="file deleted",
                expected="exists"
            )

    evidence.add_metric("mismatches", len(mismatches))
    evidence.add_metric("missing_in_manifest", len(missing_in_manifest))
    evidence.add_metric("missing_in_filesystem", len(missing_in_filesystem))

    if mismatches:
        evidence.add_note(f"Hash mismatches detected in {len(mismatches)} files:")
        for m in mismatches[:5]:
            evidence.add_note(f"  - {m['file']}: hash changed")

    if missing_in_manifest:
        evidence.add_note(f"New files not in manifest: {missing_in_manifest[:5]}")

    if missing_in_filesystem:
        evidence.add_note(f"Files in manifest but missing: {missing_in_filesystem[:5]}")

    all_ok = len(mismatches) == 0 and len(missing_in_manifest) == 0 and len(missing_in_filesystem) == 0

    evidence.add_check(
        name="all_hashes_match",
        passed=all_ok,
        value={
            "mismatches": len(mismatches),
            "new_files": len(missing_in_manifest),
            "deleted_files": len(missing_in_filesystem)
        },
        expected={"mismatches": 0, "new_files": 0, "deleted_files": 0}
    )

    return all_ok, current_hashes


def main():
    parser = argparse.ArgumentParser(description="Verify artifact hashes")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(),
                        help="Repository root directory")
    parser.add_argument("--evidence-dir", type=Path, default=Path("evidence"),
                        help="Directory to write evidence JSON")
    parser.add_argument("--log-file", type=Path, default=None,
                        help="Optional log file path")
    parser.add_argument("--generate-manifest", action="store_true",
                        help="Force generation of new manifest (first run)")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    sys.path.insert(0, str(Path(__file__).parent))
    from report import Evidence, ReportLogger, exit_pass, exit_fail, exit_error

    logger = ReportLogger(log_file=args.log_file)
    start = time.time()

    evidence = Evidence(
        verifier="verify_hashes.py",
        claim="All artifacts have SHA256 hashes matching the manifest"
    )

    logger.info(f"Hash verification for: {repo_root}")

    try:
        passed, current_hashes = verify_hashes(repo_root, evidence, logger)
        evidence.set_duration(start)

        # Save updated manifest if in generate mode
        if args.generate_manifest:
            manifest_path = save_manifest(repo_root, current_hashes)
            logger.info(f"Generated manifest: {manifest_path}")
            evidence.add_artifact(manifest_path)

        evidence_path = args.evidence_dir / "verify_hashes_evidence.json"
        evidence.save(evidence_path)
        logger.info(f"Evidence saved: {evidence_path}")

        if passed:
            logger.success("All artifact hashes verified")
            exit_pass(evidence, "Hash verification passed")
        else:
            logger.fail("Hash verification failed — artifacts changed")
            exit_fail(evidence, "Hash verification failed")

    except Exception as e:
        evidence.set_duration(start)
        exit_error(evidence, e, "Hash verification error")


if __name__ == "__main__":
    main()
'''

with open("/mnt/agents/output/verify_hashes.py", 'w') as f:
    f.write(verify_hashes_py)

print("[SAVED] verify_hashes.py")
