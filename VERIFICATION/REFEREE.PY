
referee_py = '''#!/usr/bin/env python3
"""
AQARION Master Referee — Production Verification Orchestrator
===============================================================
Version: 1.0
Principle: This script MUST NOT import from any AQARION source module.
           All verifiers are executed as independent subprocesses.
           Violation of this principle invalidates the entire audit.

Execution Tiers:
  Tier 1 (Gate):   Structural integrity, hashes, reproducibility, claims
  Tier 2 (Core):   Mathematical verifiers (projection, koopman, graph, etc.)
  Tier 3 (Deep):   Census, random testing, counterexamples
  Tier 4 (Formal): Lean build, paper artifacts, CI
  Tier 5 (Release): Final gating before tag

Usage:
  python referee.py [--tier 1|2|3|4|5] [--output-dir ./reports]

Exit Codes:
  0 = All checks passed
  1 = One or more checks failed
  2 = Infrastructure error (missing verifier, etc.)
"""

import argparse
import json
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ============================================================
# CONFIGURATION — Adjust for your repository layout
# ============================================================
VERIFICATION_DIR = Path(__file__).parent.resolve()
REPO_ROOT = VERIFICATION_DIR.parent.resolve()
EVIDENCE_DIR = VERIFICATION_DIR / "evidence"
LOG_DIR = VERIFICATION_DIR / "verification_logs"
REPORT_DIR = VERIFICATION_DIR / "reports"

# Tier definitions: ordered list of (tier_name, [verifier_scripts])
TIER_DEFINITIONS = {
    1: ("GATE", [
        "verify_repository.py",
        "verify_hashes.py",
        "verify_reproducibility.py",
        "verify_claims.py",
    ]),
    2: ("CORE_MATHEMATICS", [
        "verify_projection.py",
        "verify_koopman.py",
        "verify_graph.py",
        "verify_scc.py",
        "verify_cycles.py",
        "verify_kaprekar.py",
    ]),
    3: ("DEEP_AUDIT", [
        "verify_counterexamples.py",
        "verify_random_fdds.py",
        "verify_census.py",
    ]),
    4: ("FORMAL_PUBLICATION", [
        "verify_lean.py",
        "verify_no_sorry.py",
        "verify_figures.py",
        "verify_tables.py",
        "verify_papers.py",
    ]),
    5: ("RELEASE", [
        "verify_release.py",
        "verify_ci.py",
    ]),
}

# Production readiness gates — all must pass for a release tag
PRODUCTION_GATES = [
    "Repository integrity",
    "Artifact hash verification",
    "Clean reproducibility from fresh clone",
    "FDDS and partition verification",
    "Projection and obstruction verification",
    "Koopman operator identities",
    "Characteristic and minimal polynomial agreement",
    "Jordan reconstruction from kernel growth",
    "Functional graph invariants (SCCs, cycles, depth, condensation DAG)",
    "Kaprekar benchmark verification",
    "Multi-digit benchmark verification",
    "Counterexample census and regression tests",
    "Lean build with zero sorry, admit, or untrusted axioms",
    "Paper tables and figures regenerated from source data",
    "Claim compiler reports zero unsupported claims",
    "CI passes on all supported platforms",
    "Signed release with reproducible artifacts and hash manifest",
]


class VerificationResult:
    """Immutable result container for a single verifier execution."""
    __slots__ = ("script", "tier", "passed", "duration", "stdout", "stderr",
                 "returncode", "evidence_file", "timestamp")

    def __init__(self, script: str, tier: int, passed: bool, duration: float,
                 stdout: str, stderr: str, returncode: int,
                 evidence_file: Optional[Path] = None):
        self.script = script
        self.tier = tier
        self.passed = passed
        self.duration = duration
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.evidence_file = evidence_file
        self.timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ")

    def to_dict(self) -> dict:
        return {
            "script": self.script,
            "tier": self.tier,
            "tier_name": TIER_DEFINITIONS.get(self.tier, ("UNKNOWN", []))[0],
            "passed": self.passed,
            "duration_seconds": round(self.duration, 3),
            "returncode": self.returncode,
            "timestamp": self.timestamp,
            "evidence_file": str(self.evidence_file) if self.evidence_file else None,
            "stdout_preview": self.stdout[:500] if self.stdout else None,
            "stderr_preview": self.stderr[:500] if self.stderr else None,
        }


class Referee:
    """
    Master referee executing verifiers in tiered order.
    Stops on first failure within a tier if --strict is set.
    """

    def __init__(self, max_tier: int = 5, strict: bool = True,
                 output_dir: Optional[Path] = None):
        self.max_tier = max_tier
        self.strict = strict
        self.output_dir = output_dir or REPORT_DIR
        self.results: List[VerificationResult] = []
        self.gate_status: Dict[str, bool] = {g: False for g in PRODUCTION_GATES}

        # Ensure output directories exist
        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _run_verifier(self, script_name: str, tier: int) -> VerificationResult:
        """
        Execute a single verifier script as an isolated subprocess.
        The script is expected to:
          - Accept --evidence-dir and --log-dir arguments
          - Exit 0 on PASS, 1 on FAIL, 2 on ERROR
          - Write evidence.json to evidence_dir
        """
        script_path = VERIFICATION_DIR / script_name
        if not script_path.exists():
            return VerificationResult(
                script=script_name, tier=tier, passed=False,
                duration=0.0, stdout="", stderr=f"Script not found: {script_path}",
                returncode=2, evidence_file=None
            )

        evidence_out = EVIDENCE_DIR / f"{script_name.replace('.py', '')}_evidence.json"
        log_out = LOG_DIR / f"{script_name.replace('.py', '')}.log"

        cmd = [
            sys.executable,
            str(script_path),
            "--evidence-dir", str(EVIDENCE_DIR),
            "--log-file", str(log_out),
            "--repo-root", str(REPO_ROOT),
        ]

        start = time.time()
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=300,
                cwd=str(REPO_ROOT)
            )
            duration = time.time() - start
            passed = (proc.returncode == 0)

            # Load evidence if produced
            ev_file = evidence_out if evidence_out.exists() else None

            return VerificationResult(
                script=script_name, tier=tier, passed=passed,
                duration=duration, stdout=proc.stdout, stderr=proc.stderr,
                returncode=proc.returncode, evidence_file=ev_file
            )

        except subprocess.TimeoutExpired:
            duration = time.time() - start
            return VerificationResult(
                script=script_name, tier=tier, passed=False,
                duration=duration, stdout="", stderr="TIMEOUT after 300s",
                returncode=2, evidence_file=None
            )
        except Exception as e:
            duration = time.time() - start
            return VerificationResult(
                script=script_name, tier=tier, passed=False,
                duration=duration, stdout="", stderr=traceback.format_exc(),
                returncode=2, evidence_file=None
            )

    def run(self) -> Tuple[bool, dict]:
        """
        Execute all verifiers up to max_tier.
        Returns (all_passed, report_dict).
        """
        print("=" * 70)
        print("AQARION MASTER REFEREE — Tiered Verification Execution")
        print("=" * 70)
        print(f"Repository root: {REPO_ROOT}")
        print(f"Max tier: {self.max_tier} ({TIER_DEFINITIONS.get(self.max_tier, ('UNKNOWN', []))[0]})")
        print(f"Strict mode: {self.strict}")
        print()

        all_passed = True
        overall_start = time.time()

        for tier in range(1, self.max_tier + 1):
            tier_name, scripts = TIER_DEFINITIONS.get(tier, ("UNKNOWN", []))
            if not scripts:
                continue

            print(f"\n{'─' * 70}")
            print(f"TIER {tier}: {tier_name}")
            print(f"{'─' * 70}")

            tier_passed = True
            for script in scripts:
                print(f"  Running {script} ...", end=" ", flush=True)
                result = self._run_verifier(script, tier)
                self.results.append(result)

                status = "PASS" if result.passed else "FAIL"
                print(f"{status} ({result.duration:.2f}s)")

                if not result.passed:
                    tier_passed = False
                    all_passed = False
                    if self.strict:
                        print(f"  \n  STRICT MODE: Halting tier {tier} on first failure.")
                        break

            if self.strict and not tier_passed:
                print(f"\n  Tier {tier} FAILED. Stopping execution.")
                break

        overall_duration = time.time() - overall_start

        # Build report
        report = self._build_report(overall_duration)
        return all_passed, report

    def _build_report(self, total_duration: float) -> dict:
        """Compile final report structure."""
        report = {
            "referee_version": "1.0",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "repository_root": str(REPO_ROOT),
            "max_tier_executed": self.max_tier,
            "strict_mode": self.strict,
            "total_duration_seconds": round(total_duration, 3),
            "summary": {
                "total_verifiers": len(self.results),
                "passed": sum(1 for r in self.results if r.passed),
                "failed": sum(1 for r in self.results if not r.passed),
                "all_tiers_passed": all(r.passed for r in self.results),
            },
            "tier_breakdown": {},
            "production_gates": self.gate_status,
            "results": [r.to_dict() for r in self.results],
        }

        for tier in range(1, 6):
            tier_results = [r for r in self.results if r.tier == tier]
            if tier_results:
                report["tier_breakdown"][f"tier_{tier}"] = {
                    "name": TIER_DEFINITIONS[tier][0],
                    "total": len(tier_results),
                    "passed": sum(1 for r in tier_results if r.passed),
                    "failed": sum(1 for r in tier_results if not r.passed),
                }

        return report

    def save_reports(self, report: dict) -> None:
        """Write report.json, report.md, and evidence index."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")

        # JSON report
        json_path = self.output_dir / f"report_{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n[SAVED] JSON report: {json_path}")

        # Markdown report
        md_path = self.output_dir / f"report_{timestamp}.md"
        with open(md_path, 'w') as f:
            f.write(self._render_markdown(report))
        print(f"[SAVED] Markdown report: {md_path}")

        # Evidence manifest
        evidence_manifest = EVIDENCE_DIR / "evidence_manifest.json"
        evidence_files = [str(p.name) for p in EVIDENCE_DIR.glob("*_evidence.json")]
        with open(evidence_manifest, 'w') as f:
            json.dump({
                "timestamp": report["timestamp"],
                "evidence_files": evidence_files,
                "count": len(evidence_files)
            }, f, indent=2)

    def _render_markdown(self, report: dict) -> str:
        """Render human-readable markdown report."""
        lines = [
            "# AQARION Verification Report",
            "",
            f"**Generated:** {report['timestamp']}",
            f"**Referee Version:** {report['referee_version']}",
            f"**Repository:** `{report['repository_root']}`",
            f"**Max Tier:** {report['max_tier_executed']}",
            f"**Total Duration:** {report['total_duration_seconds']:.2f}s",
            "",
            "## Summary",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Verifiers | {report['summary']['total_verifiers']} |",
            f"| Passed | {report['summary']['passed']} |",
            f"| Failed | {report['summary']['failed']} |",
            f"| All Tiers Passed | {'YES ✅' if report['summary']['all_tiers_passed'] else 'NO ❌'} |",
            "",
            "## Tier Breakdown",
            "",
            "| Tier | Name | Total | Passed | Failed |",
            "|------|------|-------|--------|--------|",
        ]
        for tier_key, tier_data in report['tier_breakdown'].items():
            lines.append(
                f"| {tier_key} | {tier_data['name']} | {tier_data['total']} | "
                f"{tier_data['passed']} | {tier_data['failed']} |"
            )
        lines.append("")
        lines.append("## Individual Results")
        lines.append("")
        for r in report['results']:
            status_icon = "✅" if r['passed'] else "❌"
            lines.append(f"### {r['script']} {status_icon}")
            lines.append(f"- **Tier:** {r['tier']} ({r['tier_name']})")
            lines.append(f"- **Duration:** {r['duration_seconds']:.3f}s")
            lines.append(f"- **Return Code:** {r['returncode']}")
            if r['evidence_file']:
                lines.append(f"- **Evidence:** `{r['evidence_file']}`")
            if r['stdout_preview']:
                lines.append(f"- **Output Preview:** `{r['stdout_preview'][:200]}`")
            if r['stderr_preview']:
                lines.append(f"- **Error Preview:** `{r['stderr_preview'][:200]}`")
            lines.append("")
        return "\\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="AQARION Master Referee")
    parser.add_argument("--tier", type=int, default=5, choices=range(1, 6),
                        help="Maximum tier to execute (default: 5 = all)")
    parser.add_argument("--strict", action="store_true", default=True,
                        help="Halt on first failure within a tier (default: True)")
    parser.add_argument("--no-strict", dest="strict", action="store_false",
                        help="Continue despite failures")
    parser.add_argument("--output-dir", type=Path, default=None,
                        help="Directory for report output")
    args = parser.parse_args()

    referee = Referee(max_tier=args.tier, strict=args.strict,
                      output_dir=args.output_dir)
    all_passed, report = referee.run()
    referee.save_reports(report)

    print("\\n" + "=" * 70)
    if all_passed:
        print("RESULT: ALL CHECKS PASSED ✅")
        print("Repository is PRODUCTION READY for assessed tiers.")
        sys.exit(0)
    else:
        print("RESULT: ONE OR MORE CHECKS FAILED ❌")
        print("Repository is NOT production ready. Review reports for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
'''

with open("/mnt/agents/output/referee.py", 'w') as f:
    f.write(referee_py)

print("[SAVED] referee.py")
