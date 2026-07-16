
# Create test_registry_loader.py
test_py = '''#!/usr/bin/env python3
"""AQTC-002 Test: Claim Registry Loader

Verifies:
  - all claims load
  - schema passes
  - IDs unique
  - report generated
  - hash generated
  - repeated runs produce identical hash
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
REPORTS_DIR = ROOT / "reports"
CERT_DIR = ROOT / "certificates"


def run_registry():
    """Run aq.py registry and return parsed report."""
    result = subprocess.run(
        [sys.executable, str(ROOT / "aq.py"), "registry"],
        capture_output=True, text=True, cwd=str(ROOT)
    )
    if result.returncode != 0:
        print(f"STDOUT:\n{result.stdout}")
        print(f"STDERR:\n{result.stderr}")
        raise RuntimeError(f"aq.py registry failed with code {result.returncode}")
    with open(REPORTS_DIR / "claim_registry_report.json", "r") as f:
        report = json.load(f)
    return report


def test_all_claims_load():
    report = run_registry()
    assert report["claims_loaded"] == 3, f"Expected 3 claims, got {report['claims_loaded']}"
    assert set(report["claims"]) == {"TEST-001", "AQ001", "PHI377"}
    print("PASS: all claims load")


def test_schema_passes():
    report = run_registry()
    assert report["schema_errors"] == 0, f"Schema errors: {report['schema_error_messages']}"
    print("PASS: schema passes")


def test_ids_unique():
    report = run_registry()
    assert report["duplicates"] == 0, f"Duplicates found: {report['duplicate_ids']}"
    print("PASS: IDs unique")


def test_report_generated():
    report = run_registry()
    assert REPORTS_DIR.joinpath("claim_registry_report.json").exists()
    assert report["status"] == "PASS"
    print("PASS: report generated")


def test_hash_generated():
    run_registry()
    cert_path = CERT_DIR / "claim_registry.sha256"
    assert cert_path.exists(), "Certificate file not found"
    content = cert_path.read_text()
    assert "AQARION_CLAIM_REGISTRY" in content
    assert "SHA256:" in content
    print("PASS: hash generated")


def test_deterministic_hash():
    hashes = []
    for run in [1, 2, 3]:
        report = run_registry()
        hashes.append(report["hash"])
        print(f"  Run {run}: {report['hash']}")
    assert len(set(hashes)) == 1, f"Hash drift detected: {hashes}"
    print("PASS: repeated runs produce identical hash")


def main():
    print("=" * 60)
    print("AQTC-002 TEST: Claim Registry Loader")
    print("=" * 60)

    test_all_claims_load()
    test_schema_passes()
    test_ids_unique()
    test_report_generated()
    test_hash_generated()
    test_deterministic_hash()

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)

    # Print final artifacts
    print("\n--- claim_registry_report.json ---")
    with open(REPORTS_DIR / "claim_registry_report.json") as f:
        print(json.dumps(json.load(f), indent=2))

    print("\n--- claim_registry.sha256 ---")
    print((CERT_DIR / "claim_registry.sha256").read_text())


if __name__ == "__main__":
    main()
'''

with open(TESTS_DIR / "test_registry_loader.py", "w") as f:
    f.write(test_py)

print("test_registry_loader.py created.")test_registry_loader.py created.
