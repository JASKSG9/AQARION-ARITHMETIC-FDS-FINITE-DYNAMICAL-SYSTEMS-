#!/usr/bin/env python3
"""AQ-S9-DRIFT engine: detect source/manifest variable alignment."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "FIXTURES" / "s9_manifest.json").read_text())
mvar = manifest["variable"]


def check(source_path: Path):
    text = source_path.read_text()
    m = re.search(r'variable\s*=\s*["\'](\w+)["\']', text)
    svar = m.group(1) if m else "UNKNOWN"
    if svar == mvar:
        return {
            "status": "ALIGNED",
            "residual": None,
            "manifest": mvar,
            "source": svar,
        }
    return {
        "status": "SOURCE_MANIFEST_DRIFT",
        "residual": {
            "expression": f"{mvar} - {svar}",
            "manifest": mvar,
            "source": svar,
        },
        "repair": {
            "candidate": f"{svar} = {mvar}",
            "proof_status": "OPEN",
            "auto_apply": False,
        },
        "promotion_allowed": False,
    }


clean = check(ROOT / "FIXTURES" / "s9_source_clean.py")
drift = check(ROOT / "FIXTURES" / "s9_source_drift.py")

report = {
    "claim_id": "AQ-S9-DRIFT",
    "clean": clean,
    "drift": drift,
    "status": (
        "PASS"
        if clean["status"] == "ALIGNED" and drift["status"] == "SOURCE_MANIFEST_DRIFT"
        else "FAIL"
    ),
}
print(json.dumps(report, indent=2))
sys.exit(0 if report["status"] == "PASS" else 1)
