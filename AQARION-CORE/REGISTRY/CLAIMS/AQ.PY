
# Create aq.py
aq_py = '''#!/usr/bin/env python3
"""AQARION Tool Chain (AQTC) — Main Entry Point

Commands:
    registry    Scan claims/, validate schema, build registry, generate audit report.
"""

import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.resolve()
CLAIMS_DIR = ROOT / "claims"
CERT_DIR = ROOT / "certificates"
REPORTS_DIR = ROOT / "reports"

ALLOWED_EVIDENCE_LEVELS = {"ALG", "CV", "FV", "OPEN"}
REQUIRED_FIELDS = {"claim_id", "description", "evidence_level", "status", "dependencies", "artifacts"}


def load_claims():
    """Scan claims/ and load all JSON files."""
    claims = []
    errors = []
    if not CLAIMS_DIR.exists():
        errors.append(f"Claims directory not found: {CLAIMS_DIR}")
        return claims, errors

    for fpath in sorted(CLAIMS_DIR.glob("*.json")):
        try:
            with open(fpath, "r") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                errors.append(f"{fpath.name}: root must be an object")
                continue
            claims.append(data)
        except json.JSONDecodeError as e:
            errors.append(f"{fpath.name}: invalid JSON — {e}")
        except Exception as e:
            errors.append(f"{fpath.name}: {e}")
    return claims, errors


def validate_schema(claims):
    """Validate claim schema and evidence levels."""
    errors = []
    for claim in claims:
        missing = REQUIRED_FIELDS - set(claim.keys())
        if missing:
            errors.append(f"{claim.get('claim_id', '?')}: missing fields {sorted(missing)}")
        if claim.get("evidence_level") not in ALLOWED_EVIDENCE_LEVELS:
            errors.append(
                f"{claim.get('claim_id', '?')}: invalid evidence_level "
                f"'{claim.get('evidence_level')}' (allowed: {sorted(ALLOWED_EVIDENCE_LEVELS)})"
            )
        if not isinstance(claim.get("dependencies", []), list):
            errors.append(f"{claim.get('claim_id', '?')}: dependencies must be a list")
        if not isinstance(claim.get("artifacts", []), list):
            errors.append(f"{claim.get('claim_id', '?')}: artifacts must be a list")
    return errors


def detect_duplicates(claims):
    """Detect duplicate claim_id values."""
    seen = {}
    duplicates = []
    for claim in claims:
        cid = claim.get("claim_id")
        if cid in seen:
            duplicates.append(cid)
        else:
            seen[cid] = claim
    return duplicates


def build_registry(claims):
    """Build deterministic registry index."""
    registry = {
        "object": "AQARION_CLAIM_REGISTRY",
        "version": "1.0",
        "timestamp": "2026-07-16T00:00:00+00:00",  # deterministic for reproducibility
        "claims": sorted(claims, key=lambda c: c.get("claim_id", "")),
    }
    return registry


def compute_registry_hash(registry):
    """Compute SHA-256 of canonical JSON representation."""
    canonical = json.dumps(registry, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def write_certificate(registry_hash):
    """Write SHA-256 certificate file."""
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    cert_path = CERT_DIR / "claim_registry.sha256"
    content = (
        "OBJECT:\\n"
        "AQARION_CLAIM_REGISTRY\\n"
        "\\n"
        "VERSION:\\n"
        "1.0\\n"
        "\\n"
        f"SHA256:\\n"
        f"{registry_hash}\\n"
    )
    with open(cert_path, "w") as f:
        f.write(content)
    return cert_path


def write_report(registry, registry_hash, schema_errors, duplicates):
    """Write audit report."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "status": "PASS" if not schema_errors and not duplicates else "FAIL",
        "claims_loaded": len(registry["claims"]),
        "duplicates": len(duplicates),
        "schema_errors": len(schema_errors),
        "claims": [c.get("claim_id") for c in registry["claims"]],
        "duplicate_ids": duplicates,
        "schema_error_messages": schema_errors,
        "hash": registry_hash,
        "timestamp": registry["timestamp"],
    }
    report_path = REPORTS_DIR / "claim_registry_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    return report_path


def cmd_registry():
    """Execute registry command."""
    print("=" * 60)
    print("AQARION CLAIM REGISTRY")
    print("=" * 60)

    claims, load_errors = load_claims()
    if load_errors:
        for e in load_errors:
            print(f"LOAD ERROR: {e}")
        sys.exit(1)

    print(f"Claims loaded: {len(claims)}")

    schema_errors = validate_schema(claims)
    if schema_errors:
        for e in schema_errors:
            print(f"SCHEMA ERROR: {e}")
        schema_pass = False
    else:
        schema_pass = True
    print(f"Schema: {'PASS' if schema_pass else 'FAIL'}")

    duplicates = detect_duplicates(claims)
    if duplicates:
        print(f"Duplicates: {len(duplicates)} — {duplicates}")
    else:
        print("Duplicates: 0")

    registry = build_registry(claims)
    registry_hash = compute_registry_hash(registry)
    print(f"Registry: {'PASS' if schema_pass and not duplicates else 'FAIL'}")
    print(f"Hash: {registry_hash}")

    cert_path = write_certificate(registry_hash)
    report_path = write_report(registry, registry_hash, schema_errors, duplicates)
    print(f"Certificate: {cert_path}")
    print(f"Report: {report_path}")

    if schema_errors or duplicates:
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: aq.py <command>")
        print("Commands: registry")
        sys.exit(1)

    command = sys.argv[1]
    if command == "registry":
        cmd_registry()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
'''

with open(ROOT / "aq.py", "w") as f:
    f.write(aq_py)

print("aq.py created.")aq.py created.
