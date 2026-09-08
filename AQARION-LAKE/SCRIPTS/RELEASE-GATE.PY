#!/usr/bin/env python3

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "Evidence" / "EXP-001C_EXECUTION.json"

if not PATH.exists():
    print("RELEASE BLOCKED: execution receipt missing")
    raise SystemExit(2)

data = json.loads(PATH.read_text(encoding="utf-8"))
tests = data.get("tests", {})

required = [f"T{i}" for i in range(1, 14)]

missing = [
    test for test in required
    if tests.get(test, {}).get("status") == "PENDING"
]

if missing:
    print("RELEASE BLOCKED")
    print("Pending:", ", ".join(missing))
    raise SystemExit(3)

failed = [
    test for test in required
    if tests.get(test, {}).get("status", "").endswith("FAIL")
]

if failed:
    print("RELEASE BLOCKED")
    print("Failed:", ", ".join(failed))
    raise SystemExit(4)

if data.get("status") != "VERIFIED":
    print(
        "RELEASE BLOCKED: experiment status is "
        + repr(data.get("status"))
    )
    raise SystemExit(5)

print("AQARION LAKE RELEASE GATE: PASS")
