
# ============================================================
# 4. aq_verify — Independent Certificate Verifier
# ============================================================

aq_verify = '''#!/usr/bin/env python3
"""aq_verify — Independent Certificate Verification

Loads a certificate, recomputes all hashes from raw artifacts,
and reports PASS/FAIL. Never trusts the certificate itself.

Usage:
    aq_verify <certificate.json>
"""

import json
import hashlib
import sys
from pathlib import Path


def sha256_file(path: Path) -> str:
    """Compute SHA-256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_json(data: dict) -> str:
    """Compute SHA-256 of canonical JSON representation."""
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def verify_certificate(cert_path: Path) -> dict:
    """Verify a certification record independently."""
    errors = []
    
    # Load certificate
    with open(cert_path, "r") as f:
        cert = json.load(f)
    
    required = ["record_id", "claim_id", "artifact_hash", "graphs", 
                "evidence_level", "status", "timestamp", "certificate_hash"]
    for field in required:
        if field not in cert:
            errors.append("Missing field: " + field)
    
    if errors:
        return {"status": "FAIL", "errors": errors}
    
    # Recompute certificate hash from contents (excluding certificate_hash itself)
    cert_body = {k: v for k, v in cert.items() if k != "certificate_hash"}
    recomputed_cert_hash = sha256_json(cert_body)
    
    if recomputed_cert_hash != cert["certificate_hash"]:
        errors.append(
            "Certificate hash mismatch: stored=" + cert["certificate_hash"] +
            " recomputed=" + recomputed_cert_hash
        )
    
    # Verify graph hashes if artifacts exist
    root = cert_path.parent.parent  # Navigate to project root
    graphs = cert.get("graphs", {})
    for graph_name, stored_hash in graphs.items():
        graph_file = root / "graphs" / (graph_name + ".json")
        if graph_file.exists():
            recomputed = sha256_file(graph_file)
            if recomputed != stored_hash:
                errors.append(
                    "Graph hash mismatch for " + graph_name +
                    ": stored=" + stored_hash + " recomputed=" + recomputed
                )
        else:
            errors.append("Graph file not found: " + str(graph_file))
    
    # Verify claim exists in registry
    claim_file = root / "claims" / (cert["claim_id"] + ".json")
    if claim_file.exists():
        claim_hash = sha256_file(claim_file)
        if claim_hash != cert["artifact_hash"]:
            errors.append(
                "Claim hash mismatch: stored=" + cert["artifact_hash"] +
                " recomputed=" + claim_hash
            )
    else:
        errors.append("Claim file not found: " + str(claim_file))
    
    status = "PASS" if not errors else "FAIL"
    return {
        "status": status,
        "record_id": cert.get("record_id"),
        "claim_id": cert.get("claim_id"),
        "errors": errors,
        "recomputed_certificate_hash": recomputed_cert_hash,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: aq_verify <certificate.json>")
        sys.exit(1)
    
    cert_path = Path(sys.argv[1])
    if not cert_path.exists():
        print("FAIL: certificate not found: " + str(cert_path))
        sys.exit(1)
    
    result = verify_certificate(cert_path)
    print(json.dumps(result, indent=2, sort_keys=True))
    sys.exit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
'''

with open(ROOT / "aq_verify.py", "w") as f:
    f.write(aq_verify)

print("aq_verify.py written.")aq_verify.py written.
