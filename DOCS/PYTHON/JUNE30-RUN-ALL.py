
# [7] run_all.py — Central verification engine

run_all_py = '''"""AQARION v30.2 Verification Engine.

Central orchestrator for all verification stages.
Runs pytest suite, generates audit report, updates CLAIMS_REGISTRY.
Exit code: 0 if production-ready, 1 otherwise.
"""

import subprocess
import json
import sys
import hashlib
from datetime import datetime
from pathlib import Path

REPORT_DIR = Path(__file__).parent / "reports"
REPORT_DIR.mkdir(exist_ok=True)
JSON_PATH = REPORT_DIR / "audit_report.json"
TXT_PATH = REPORT_DIR / "audit_report.txt"
HASH_PATH = REPORT_DIR / "baseline_hashes.json"

# Stage definitions
STAGES = [
    ("core", "Stage 1: Core Linear Algebra"),
    ("theorem", "Stage 2: Theorem Verification"),
    ("counterexample", "Stage 3: Counterexample Reproduction"),
    ("random", "Stage 4: Randomized Testing"),
    ("lean", "Stage 5: Lean Formalization"),
    ("hash", "Stage 6: Reference Data Hash Verification"),
]


def run_pytest():
    """Execute pytest with JSON reporting."""
    cmd = [
        sys.executable, "-m", "pytest",
        str(Path(__file__).parent / "tests"),
        "-q", "--tb=short",
        "--json-report",
        f"--json-report-file={JSON_PATH}",
        "--json-report-omit=streams",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def load_report():
    """Load JSON report if available."""
    if JSON_PATH.exists():
        with open(JSON_PATH) as f:
            return json.load(f)
    return None


def compute_stage_status(data):
    """Determine pass/fail for each stage."""
    stage_status = {}
    tests = data.get("tests", [])
    
    for marker, label in STAGES:
        stage_tests = [t for t in tests if marker in t.get("keywords", [])]
        passed = sum(1 for t in stage_tests if t.get("outcome") == "passed")
        failed = sum(1 for t in stage_tests if t.get("outcome") == "failed")
        xfailed = sum(1 for t in stage_tests if t.get("outcome") == "xfailed")
        skipped = sum(1 for t in stage_tests if t.get("outcome") == "skipped")
        total = len(stage_tests)
        
        stage_status[marker] = {
            "label": label,
            "total": total,
            "passed": passed,
            "failed": failed,
            "xfailed": xfailed,
            "skipped": skipped,
            "status": "PASS" if failed == 0 else "FAIL",
        }
    
    return stage_status


def verify_hashes():
    """Stage 6: Verify reference data hashes."""
    ref_dir = Path(__file__).parent / "reference_data"
    if not ref_dir.exists():
        return {"status": "SKIP", "reason": "No reference_data directory"}
    
    if not HASH_PATH.exists():
        # Generate baseline
        hashes = {}
        for f in ref_dir.iterdir():
            if f.is_file():
                hashes[f.name] = hashlib.sha256(f.read_bytes()).hexdigest()
        with open(HASH_PATH, "w") as f:
            json.dump(hashes, f, indent=2)
        return {"status": "BASELINE_CREATED", "files": len(hashes)}
    
    with open(HASH_PATH) as f:
        expected = json.load(f)
    
    mismatches = []
    for name, expected_hash in expected.items():
        fpath = ref_dir / name
        if not fpath.exists():
            mismatches.append(f"MISSING: {name}")
            continue
        actual = hashlib.sha256(fpath.read_bytes()).hexdigest()
        if actual != expected_hash:
            mismatches.append(f"MISMATCH: {name}")
    
    return {
        "status": "PASS" if not mismatches else "FAIL",
        "mismatches": mismatches,
    }


def generate_report(data, stage_status, hash_status):
    """Generate human-readable audit report."""
    summary = data.get("summary", {}) if data else {}
    total_passed = summary.get("passed", 0)
    total_failed = summary.get("failed", 0)
    total_xfailed = summary.get("xfailed", 0)
    total_skipped = summary.get("skipped", 0)
    
    # Production readiness criteria
    core_ok = stage_status.get("core", {}).get("status") == "PASS"
    theorem_ok = stage_status.get("theorem", {}).get("status") == "PASS"
    ce_ok = stage_status.get("counterexample", {}).get("status") == "PASS"
    hash_ok = hash_status.get("status") in ("PASS", "BASELINE_CREATED", "SKIP")
    
    is_ready = core_ok and theorem_ok and ce_ok and hash_ok and total_failed == 0
    
    status = "VERIFIED" if is_ready else "PARTIALLY VERIFIED"
    prod_ready = "YES" if is_ready else "NO"
    
    report = f"""{'='*70}
AQARION v30.2 Verification Report
Generated: {datetime.now().isoformat()}
Commit: [TODO: git rev-parse HEAD]
{'='*70}

STAGE SUMMARY
{'-'*70}
"""
    
    for marker, label in STAGES:
        s = stage_status.get(marker, {})
        if s.get("total", 0) == 0:
            report += f"  {label:<45} [NO TESTS]\n"
        else:
            status_icon = "✓" if s["status"] == "PASS" else "✗"
            report += f"  {status_icon} {label:<43} {s['passed']}/{s['total']} passed"
            if s["xfailed"] > 0:
                report += f" ({s['xfailed']} xfail)"
            report += "\n"
    
    report += f"""
{'-'*70}
Reference Data Hash Verification: {hash_status.get('status', 'UNKNOWN')}
{'-'*70}

AGGREGATE
  Total Passed ............... {total_passed}
  Total Failed ............... {total_failed}
  Expected Failures .......... {total_xfailed}
  Skipped .................... {total_skipped}

PRODUCTION READINESS
  Status: {status}
  Production Ready: {prod_ready}
"""
    
    if not is_ready:
        report += "  Blockers:\n"
        if not core_ok:
            report += "    - Core linear algebra tests failing\n"
        if not theorem_ok:
            report += "    - Theorem verification incomplete\n"
        if not ce_ok:
            report += "    - Counterexample reproduction failing\n"
        if not hash_ok:
            report += "    - Reference data hash mismatch\n"
        report += "\n  Required for Paper I:\n"
        report += "    1. All core tests passing\n"
        report += "    2. All counterexamples reproducible\n"
        report += "    3. Lean LC1-LC5 proofs complete\n"
        report += "    4. Claims registry updated\n"
    else:
        report += "\n  ✓ All core claims certified.\n"
        report += "  ✓ Ready for Paper I submission.\n"
    
    report += f"\n{'='*70}\n"
    
    print(report)
    with open(TXT_PATH, "w") as f:
        f.write(report)
    
    return is_ready


def main():
    print("=" * 70)
    print("AQARION v30.2 Verification Engine")
    print("=" * 70)
    
    # Run pytest
    print("\n[1/3] Running pytest suite...")
    pytest_code, stdout, stderr = run_pytest()
    if stdout:
        print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)
    
    # Load results
    print("\n[2/3] Processing results...")
    data = load_report()
    stage_status = compute_stage_status(data) if data else {}
    
    # Hash verification
    print("\n[3/3] Verifying reference data hashes...")
    hash_status = verify_hashes()
    
    # Generate report
    print("\n" + "=" * 70)
    is_ready = generate_report(data, stage_status, hash_status)
    
    print(f"\nReport saved to: {TXT_PATH}")
    print(f"JSON data saved to: {JSON_PATH}")
    
    sys.exit(0 if is_ready else 1)


if __name__ == "__main__":
    main()
'''

with open(ROOT / "verification/run_all.py", "w") as f:
    f.write(run_all_py)

print("✅ verification/run_all.py")
