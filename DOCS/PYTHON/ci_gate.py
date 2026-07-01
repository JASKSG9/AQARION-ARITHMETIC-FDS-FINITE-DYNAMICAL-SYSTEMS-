# ci_gate.py
# SINGLE TRUTH GATE FOR AQARION
# FAIL-FAST, NO SKIPS, NO SUBPROCESS RELIANCE

import sys
import traceback
from core import build_system
from invariants import validate_system

def fail(msg):
    print("\n[CI GATE FAILED]")
    print(msg)
    sys.exit(1)

def pass_gate():
    print("\n[CI GATE PASSED]")

def main():
    try:
        # 1. BUILD SYSTEM (single execution context)
        T = build_system()

        if T is None or len(T) == 0:
            fail("System build returned empty or None state")

        # 2. VALIDATION (single source of truth)
        report = validate_system(T)

        # 3. HARD REQUIREMENTS (NO SOFT PASS)
        required_keys = ["deterministic", "fixed_points"]

        for k in required_keys:
            if k not in report:
                fail(f"Missing invariant check: {k}")

        if report["deterministic"] is not True:
            fail("Determinism invariant FAILED")

        if report["fixed_points"] is None:
            fail("Fixed point computation invalid")

        # 4. NO SILENT SKIPS POLICY
        # (if your future suite adds skips, they must surface here)
        if hasattr(report, "skipped") and report["skipped"]:
            fail(f"Skipped tests detected: {report['skipped']}")

        pass_gate()

    except Exception as e:
        print("\n[CI GATE CRASHED]")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
