
# ============================================================
# Step 5: Create a standalone reproducibility script
# ============================================================

repro_script = '''#!/usr/bin/env python3
"""reproduce.py — One-command reproducibility for AQARION

Runs the entire verification pipeline and reports PASS/FAIL.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()

def run(cmd, cwd=ROOT):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=str(cwd))
    return result.returncode == 0, result.stdout, result.stderr

def main():
    checks = []
    
    # 1. Registry
    ok, out, err = run("python aq.py registry")
    checks.append(("Registry load", ok))
    
    # 2. AQTC-002
    ok, out, err = run("python tests/test_registry_loader.py")
    checks.append(("AQTC-002 (Registry Loader)", ok))
    
    # 3. AQTC-003
    ok, out, err = run("python tests/test_graph_generator.py")
    checks.append(("AQTC-003 (Graph Generator)", ok))
    
    # 4. Independent verification
    ok, out, err = run("python aq_verify.py certificates/TEST-001_certificate.json")
    checks.append(("Independent verification", ok))
    
    # 5. Graph analysis
    ok, out, err = run("python aq_analyze.py all")
    checks.append(("Graph analysis", ok))
    
    # 6. Deterministic hash
    import json
    with open(ROOT / "reports" / "claim_registry_report.json") as f:
        h1 = json.load(f)["hash"]
    run("python aq.py registry > /dev/null")
    with open(ROOT / "reports" / "claim_registry_report.json") as f:
        h2 = json.load(f)["hash"]
    checks.append(("Deterministic hash", h1 == h2))
    
    print("=" * 60)
    print("AQARION REPRODUCIBILITY REPORT")
    print("=" * 60)
    all_pass = True
    for name, ok in checks:
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_pass = False
        print(f"  [{status}] {name}")
    print("=" * 60)
    print(f"OVERALL: {'PASS' if all_pass else 'FAIL'}")
    return 0 if all_pass else 1

if __name__ == "__main__":
    sys.exit(main())
'''

with open(ROOT / "reproduce.py", "w") as f:
    f.write(repro_script)

# Run it
result = subprocess.run(
    [sys.executable, str(ROOT / "reproduce.py")],
    capture_output=True, text=True, cwd=str(ROOT)
)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print("EXIT CODE:", result.returncode)============================================================
AQARION REPRODUCIBILITY REPORT
============================================================
  [PASS] Registry load
  [FAIL] AQTC-002 (Registry Loader)
  [PASS] AQTC-003 (Graph Generator)
  [FAIL] Independent verification
  [PASS] Graph analysis
  [PASS] Deterministic hash
============================================================
OVERALL: FAIL

EXIT CODE: 1
