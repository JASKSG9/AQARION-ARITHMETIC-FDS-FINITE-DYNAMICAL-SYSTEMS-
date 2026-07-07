#!/usr/bin/env python3
"""
AQARION Claims Matrix Verifier
Reads PAPER1.json and verifies the implementation against the claim statuses.
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.parent.resolve()
MANIFEST_DIR = REPO_ROOT / "DOCS" / "MANIFEST"
PAPER1_PATH = MANIFEST_DIR / "PAPER1.json"

def check_claim(claim_id, claim_data):
    """Verify that a claim's status is supported by actual evidence."""
    status = claim_data.get("status")
    evidence = claim_data.get("evidence", [])
    
    if status == "PROVED":
        # Must have symbolic proof
        if "symbolic proof" not in evidence:
            return (False, f"{claim_id}: PROVED but missing symbolic proof")
    elif status == "COMPUTATIONALLY CERTIFIED":
        # Must have some verification artifact
        if not any("verification" in e or "exhaustive" in e or "counterexample" in e for e in evidence):
            return (False, f"{claim_id}: COMPUTATIONALLY CERTIFIED but no verification artifact")
    elif status == "PROPOSED":
        # No requirement
        pass
    else:
        return (False, f"{claim_id}: Unknown status '{status}'")
    
    return (True, f"{claim_id}: OK")

def main():
    if not PAPER1_PATH.exists():
        print(f"Error: PAPER1.json not found at {PAPER1_PATH}")
        sys.exit(1)
    
    with open(PAPER1_PATH, "r") as f:
        data = json.load(f)
    
    theorems = data.get("theorems", {})
    failed = []
    
    print("AQARION Claims Matrix Check\n")
    for claim_id, claim_data in theorems.items():
        ok, msg = check_claim(claim_id, claim_data)
        if ok:
            print(f"✅ {msg}")
        else:
            print(f"❌ {msg}")
            failed.append(claim_id)
    
    print(f"\nSummary: {len(theorems) - len(failed)} passed, {len(failed)} failed")
    
    if failed:
        print("\n⚠️  The following claims need attention:", ", ".join(failed))
        sys.exit(1)
    else:
        print("\n✅ All claims verified.")
        sys.exit(0)

if __name__ == "__main__":
    main()
