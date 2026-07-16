
from pathlib import Path
import json
import hashlib
import subprocess
import sys

ROOT = Path("/mnt/agents/output/AQARION-TOOL-CHAIN")

# ============================================================
# Step 1: Audit all claims against evidence levels
# ============================================================

def load_claims():
    claims = {}
    for fpath in sorted((ROOT / "claims").glob("*.json")):
        with open(fpath, "r") as f:
            data = json.load(f)
        claims[data["claim_id"]] = data
    return claims

def load_evidence():
    evidence = {}
    if not (ROOT / "evidence").exists():
        return evidence
    for fpath in sorted((ROOT / "evidence").glob("*.json")):
        with open(fpath, "r") as f:
            data = json.load(f)
        cid = data.get("claim_id")
        if cid not in evidence:
            evidence[cid] = []
        evidence[cid].append(data)
    return evidence

claims = load_claims()
evidence = load_evidence()

print("=== CLAIM-EVIDENCE AUDIT ===\n")
mismatches = []
for cid, cdata in claims.items():
    level = cdata["evidence_level"]
    ev_list = evidence.get(cid, [])
    
    # Check consistency
    if level == "FV" and cdata["status"] != "PROVED":
        mismatches.append(f"{cid}: FV but status={cdata['status']}")
    if level == "CV" and cdata["status"] not in ("VERIFIED", "PROVED"):
        mismatches.append(f"{cid}: CV but status={cdata['status']}")
    if level == "OPEN" and cdata["status"] != "OPEN":
        mismatches.append(f"{cid}: OPEN but status={cdata['status']}")
    
    # Check evidence presence
    if level in ("CV", "FV") and not ev_list:
        mismatches.append(f"{cid}: level={level} but no evidence files")
    
    print(f"{cid}: {level} | status={cdata['status']} | evidence={len(ev_list)} files | deps={cdata['dependencies']}")

if mismatches:
    print(f"\nMISMATCHES: {len(mismatches)}")
    for m in mismatches:
        print(f"  {m}")
else:
    print("\nAll claims consistent with evidence levels.")=== CLAIM-EVIDENCE AUDIT ===

ALG-TEST: ALG | status=OPEN | evidence=0 files | deps=['TEST-001']
AQ001: FV | status=PROVED | evidence=2 files | deps=['TEST-001']
PHI377: OPEN | status=OPEN | evidence=0 files | deps=['AQ001']
TEST-001: CV | status=VERIFIED | evidence=0 files | deps=[]

MISMATCHES: 1
  TEST-001: level=CV but no evidence files
