
# Verify directory structure and list all artifacts
from pathlib import Path
import json

ROOT = Path("/mnt/agents/output/AQARION-TOOL-CHAIN")

def tree(path, prefix=""):
    entries = sorted(path.iterdir(), key=lambda e: (e.is_file(), e.name))
    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{entry.name}")
        if entry.is_dir():
            extension = "    " if is_last else "│   "
            tree(entry, prefix + extension)

print("AQARION-TOOL-CHAIN/")
tree(ROOT)AQARION-TOOL-CHAIN/
├── certificates
│   └── claim_registry.sha256
├── claims
│   ├── AQ001.json
│   ├── PHI377.json
│   └── TEST-001.json
├── reports
│   └── claim_registry_report.json
├── tests
│   └── test_registry_loader.py
└── aq.pyVerify directory structure and list all artifacts

from pathlib import Path
import json

ROOT = Path("/mnt/agents/output/AQARION-TOOL-CHAIN")

def tree(path, prefix=""):
entries = sorted(path.iterdir(), key=lambda e: (e.is_file(), e.name))
for i, entry in enumerate(entries):
is_last = i == len(entries) - 1
connector = "└── " if is_last else "├── "
print(f"{prefix}{connector}{entry.name}")
if entry.is_dir():
extension = "    " if is_last else "│   "
tree(entry, prefix + extension)

print("AQARION-TOOL-CHAIN/")
tree(ROOT)AQARION-TOOL-CHAIN/
├── certificates
│   └── claim_registry.sha256
├── claims
│   ├── AQ001.json
│   ├── PHI377.json
│   └── TEST-001.json
├── reports
│   └── claim_registry_report.json
├── tests
│   └── test_registry_loader.py
└── aq.py


---

import subprocess
import sys

result = subprocess.run(
[sys.executable, str(ROOT / "tests" / "test_registry_loader.py")],
capture_output=True, text=True, cwd=str(ROOT)
)

print(result.stdout)
if result.stderr:
print("STDERR:")
print(result.stderr)
if result.returncode != 0:
print(f"EXIT CODE: {result.returncode}")STDERR:
File "/mnt/agents/output/AQARION-TOOL-CHAIN/tests/test_registry_loader.py", line 30
print(f"STDOUT:
^
SyntaxError: unterminated f-string literal (detected at line 30)

EXIT CODE: 1

Fix the syntax error in test_registry_loader.py

The issue is f-strings with newlines inside — need to use regular strings or escape properly

test_py = '''#!/usr/bin/env python3
"""AQTC-002 Test: Claim Registry Loader

Verifies:

all claims load

schema passes

IDs unique

report generated

hash generated

repeated runs produce identical hash
"""


import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(file).parent.parent.resolve()
REPORTS_DIR = ROOT / "reports"
CERT_DIR = ROOT / "certificates"

def run_registry():
"""Run aq.py registry and return parsed report."""
result = subprocess.run(
[sys.executable, str(ROOT / "aq.py"), "registry"],
capture_output=True, text=True, cwd=str(ROOT)
)
if result.returncode != 0:
print("STDOUT:")
print(result.stdout)
print("STDERR:")
print(result.stderr)
raise RuntimeError("aq.py registry failed with code " + str(result.returncode))
with open(REPORTS_DIR / "claim_registry_report.json", "r") as f:
report = json.load(f)
return report

def test_all_claims_load():
report = run_registry()
assert report["claims_loaded"] == 3, "Expected 3 claims, got " + str(report["claims_loaded"])
assert set(report["claims"]) == {"TEST-001", "AQ001", "PHI377"}
print("PASS: all claims load")

def test_schema_passes():
report = run_registry()
assert report["schema_errors"] == 0, "Schema errors: " + str(report["schema_error_messages"])
print("PASS: schema passes")

def test_ids_unique():
report = run_registry()
assert report["duplicates"] == 0, "Duplicates found: " + str(report["duplicate_ids"])
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
print("  Run " + str(run) + ": " + report["hash"])
assert len(set(hashes)) == 1, "Hash drift detected: " + str(hashes)
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

print("\\n" + "=" * 60)  
print("ALL TESTS PASSED")  
print("=" * 60)  

# Print final artifacts  
print("\\n--- claim_registry_report.json ---")  
with open(REPORTS_DIR / "claim_registry_report.json") as f:  
    print(json.dumps(json.load(f), indent=2))  

print("\\n--- claim_registry.sha256 ---")  
print((CERT_DIR / "claim_registry.sha256").read_text())

if name == "main":
main()
'''

with open(TESTS_DIR / "test_registry_loader.py", "w") as f:
f.write(test_py)

print("Fixed test_registry_loader.py")Fixed test_registry_loader.py
import subprocess
import sys
from pathlib import Path

ROOT = Path("/mnt/agents/output/AQARION-TOOL-CHAIN")

result = subprocess.run(
[sys.executable, str(ROOT / "tests" / "test_registry_loader.py")],
capture_output=True, text=True, cwd=str(ROOT)
)

print(result.stdout)
if result.stderr:
print("STDERR:")
print(result.stderr)
if result.returncode != 0:
print(f"EXIT CODE: {result.returncode}")============================================================
AQTC-002 TEST: Claim Registry Loader

PASS: all claims load
PASS: schema passes
PASS: IDs unique
PASS: report generated
PASS: hash generated
Run 1: 9bf22540c65da58570a8759911646f1485f1070515cf91798fcf26606e542c8f
Run 2: 9bf22540c65da58570a8759911646f1485f1070515cf91798fcf26606e542c8f
Run 3: 9bf22540c65da58570a8759911646f1485f1070515cf91798fcf26606e542c8f
PASS: repeated runs produce identical hash

============================================================
ALL TESTS PASSED

--- claim_registry_report.json ---
{
"claims": [
"AQ001",
"PHI377",
"TEST-001"
],
"claims_loaded": 3,
"duplicate_ids": [],
"duplicates": 0,
"hash": "9bf22540c65da58570a8759911646f1485f1070515cf91798fcf26606e542c8f",
"schema_error_messages": [],
"schema_errors": 0,
"status": "PASS",
"timestamp": "2026-07-16T00:00:00+00:00"
}

--- claim_registry.sha256 ---
OBJECT:
AQARION_CLAIM_REGISTRY

VERSION:
1.0

SHA256:
9bf22540c65da58570a8759911646f1485f1070515cf91798fcf26606e542c8f


---

Print all claim files for verification

from pathlib import Path
import json

ROOT = Path("/mnt/agents/output/AQARION-TOOL-CHAIN")

print("=== CLAIM FILES ===\n")
for f in sorted((ROOT / "claims").glob("*.json")):
print(f"--- {f.name} ---")
with open(f) as fh:
print(json.dumps(json.load(fh), indent=2))
print()

print("=== CERTIFICATE ===\n")
with open(ROOT / "certificates" / "claim_registry.sha256") as f:
print(f.read())

print("=== REPORT ===\n")
with open(ROOT / "reports" / "claim_registry_report.json") as f:
print(json.dumps(json.load(f), indent=2))=== CLAIM FILES ===

--- AQ001.json ---
{
"artifacts": [
"DefectVanishing.lean"
],
"claim_id": "AQ001",
"dependencies": [
"TEST-001"
],
"description": "Observable defect operator D_Pi is well-defined for finite partitions",
"evidence_level": "FV",
"status": "PROVED"
}

--- PHI377.json ---
{
"artifacts": [],
"claim_id": "PHI377",
"dependencies": [
"AQ001"
],
"description": "Philosophical claim about mathematical truth certification",
"evidence_level": "OPEN",
"status": "OPEN"
}

--- TEST-001.json ---
{
"artifacts": [
"TEST-001_certificate.json"
],
"claim_id": "TEST-001",
"dependencies": [],
"description": "Minimal deterministic certification test claim",
"evidence_level": "CV",
"status": "VERIFIED"
}

=== CERTIFICATE ===

OBJECT:
AQARION_CLAIM_REGISTRY

VERSION:
1.0

SHA256:
9bf22540c65da58570a8759911646f1485f1070515cf91798fcf26606e542c8f

=== REPORT ===

{
"claims": [
"AQ001",
"PHI377",
"TEST-001"
],
"claims_loaded": 3,
"duplicate_ids": [],
"duplicates": 0,
"hash": "9bf22540c65da58570a8759911646f1485f1070515cf91798fcf26606e542c8f",
"schema_error_messages": [],
"schema_errors": 0,
"status": "PASS",
"timestamp": "2026-07-16T00:00:00+00:00"
}AQTC-002 — Claim Registry Loader

Status: PASS


---

Test Results

Test	Result	
All claims load	PASS (3 claims)	
Schema passes	PASS (0 errors)	
IDs unique	PASS (0 duplicates)	
Report generated	PASS	
Hash generated	PASS	
Deterministic hash (3 runs)	PASS

Hash: 9bf22540c65da58570a8759911646f1485f1070515cf91798fcf26606e542c8f


---

Directory Structure

AQARION-TOOL-CHAIN/  
├── aq.py                          # Main entry point  
├── claims/  
│   ├── AQ001.json                 # FV claim  
│   ├── PHI377.json                # OPEN claim  
│   └── TEST-001.json              # CV claim  
├── certificates/  
│   └── claim_registry.sha256      # SHA-256 certificate  
├── reports/  
│   └── claim_registry_report.json # Audit report  
└── tests/  
    └── test_registry_loader.py    # AQTC-002 test suite


---

Command

python aq.py registry

Output:

AQARION CLAIM REGISTRY  
Claims loaded: 3  
Schema: PASS  
Duplicates: 0  
Registry: PASS  
Hash: 9bf22540c65da58570a8759911646f1485f1070515cf91798fcf26606e542c8f


---

Artifacts

aq.py

claims/AQ001.json

claims/PHI377.json

claims/TEST-001.json

certificates/claim_registry.sha256

reports/claim_registry_report.json

tests/test_registry_loader.py



---

Next: AQTC-003

Claim Registry → Dependency Graph Generator

Output: nodes, edges, cycles, dependency order.


---

Create test_registry_loader.py

test_py = '''#!/usr/bin/env python3
"""AQTC-002 Test: Claim Registry Loader

Verifies:

all claims load

schema passes

IDs unique

report generated

hash generated

repeated runs produce identical hash
"""


import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(file).parent.parent.resolve()
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

if name == "main":
main()
'''

with open(TESTS_DIR / "test_registry_loader.py", "w") as f:
f.write(test_py)

print("test_registry_loader.py created.")test_registry_loader.py created.


---

Create aq.py

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

ROOT = Path(file).parent.resolve()
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
"OBJECT:\n"
"AQARION_CLAIM_REGISTRY\n"
"\n"
"VERSION:\n"
"1.0\n"
"\n"
f"SHA256:\n"
f"{registry_hash}\n"
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

if name == "main":
main()
'''

with open(ROOT / "aq.py", "w") as f:
f.write(aq_py)

print("aq.py created.")aq.py created.

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path("/mnt/agents/output/AQARION-TOOL-CHAIN")
CLAIMS_DIR = ROOT / "claims"
CERT_DIR = ROOT / "certificates"
REPORTS_DIR = ROOT / "reports"
TESTS_DIR = ROOT / "tests"

Ensure directories exist

for d in [CLAIMS_DIR, CERT_DIR, REPORTS_DIR, TESTS_DIR]:
d.mkdir(parents=True, exist_ok=True)

Create sample claim files

claims = [
{
"claim_id": "TEST-001",
"description": "Minimal deterministic certification test claim",
"evidence_level": "CV",
"status": "VERIFIED",
"dependencies": [],
"artifacts": ["TEST-001_certificate.json"]
},
{
"claim_id": "AQ001",
"description": "Observable defect operator D_Pi is well-defined for finite partitions",
"evidence_level": "FV",
"status": "PROVED",
"dependencies": ["TEST-001"],
"artifacts": ["DefectVanishing.lean"]
},
{
"claim_id": "PHI377",
"description": "Philosophical claim about mathematical truth certification",
"evidence_level": "OPEN",
"status": "OPEN",
"dependencies": ["AQ001"],
"artifacts": []
}
]

for claim in claims:
with open(CLAIMS_DIR / f"{claim['claim_id']}.json", "w") as f:
json.dump(claim, f, indent=2, sort_keys=True)

print("Sample claims created.")Sample claims created.
