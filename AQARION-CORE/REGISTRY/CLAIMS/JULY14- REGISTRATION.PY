
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path("/mnt/agents/output/AQARION-TOOL-CHAIN")
CLAIMS_DIR = ROOT / "claims"
CERT_DIR = ROOT / "certificates"
REPORTS_DIR = ROOT / "reports"
TESTS_DIR = ROOT / "tests"

# Ensure directories exist
for d in [CLAIMS_DIR, CERT_DIR, REPORTS_DIR, TESTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Create sample claim files
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
# Print all claim files for verification
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

Hash: `9bf22540c65da58570a8759911646f1485f1070515cf91798fcf26606e542c8f`

---

Directory Structure

```
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
```

---

Command

```
python aq.py registry
```

Output:

```
AQARION CLAIM REGISTRY
Claims loaded: 3
Schema: PASS
Duplicates: 0
Registry: PASS
Hash: 9bf22540c65da58570a8759911646f1485f1070515cf91798fcf26606e542c8f
```

---

Artifacts

- [aq.py](sandbox:///mnt/agents/output/AQARION-TOOL-CHAIN/aq.py)
- [claims/AQ001.json](sandbox:///mnt/agents/output/AQARION-TOOL-CHAIN/claims/AQ001.json)
- [claims/PHI377.json](sandbox:///mnt/agents/output/AQARION-TOOL-CHAIN/claims/PHI377.json)
- [claims/TEST-001.json](sandbox:///mnt/agents/output/AQARION-TOOL-CHAIN/claims/TEST-001.json)
- [certificates/claim_registry.sha256](sandbox:///mnt/agents/output/AQARION-TOOL-CHAIN/certificates/claim_registry.sha256)
- [reports/claim_registry_report.json](sandbox:///mnt/agents/output/AQARION-TOOL-CHAIN/reports/claim_registry_report.json)
- [tests/test_registry_loader.py](sandbox:///mnt/agents/output/AQARION-TOOL-CHAIN/tests/test_registry_loader.py)

---

Next: AQTC-003

Claim Registry → Dependency Graph Generator

Output: nodes, edges, cycles, dependency order.
