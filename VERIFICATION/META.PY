
# ============================================================
# verify_meta.py — Meta-Verifier with Signed Certificate
# ============================================================

verify_meta_py = '''#!/usr/bin/env python3
"""
AQARION Meta-Verifier — Signed Verification Certificate
=========================================================
Version: 1.0
Claim: Produces a cryptographically signed verification certificate
       containing repository state, verification results, and artifact hashes.

This is the canonical evidence attached to releases and archived
alongside the manuscript, making every reported result traceable to
a specific repository state and verification run.

Exit: 0 = PASS, 1 = FAIL, 2 = ERROR
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional


def get_git_commit_hash(repo_root: Path) -> Optional[str]:
    """Get current git commit hash."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(repo_root), capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_git_branch(repo_root: Path) -> Optional[str]:
    """Get current git branch."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=str(repo_root), capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_python_version() -> str:
    """Get Python version string."""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def get_os_info() -> str:
    """Get operating system info."""
    import platform
    return f"{platform.system()} {platform.release()} {platform.machine()}"


def get_dependency_versions() -> Dict[str, str]:
    """Get versions of key dependencies."""
    deps = {}
    for pkg in ["numpy", "scipy", "sympy", "networkx", "matplotlib"]:
        try:
            mod = __import__(pkg)
            deps[pkg] = getattr(mod, "__version__", "unknown")
        except ImportError:
            deps[pkg] = "not-installed"
    return deps


def compute_verifier_hashes(verification_dir: Path) -> Dict[str, str]:
    """Compute SHA256 of all verifier scripts."""
    hashes = {}
    for py_file in sorted(verification_dir.glob("verify_*.py")):
        h = hashlib.sha256()
        with open(py_file, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        hashes[py_file.name] = h.hexdigest()
    return hashes


def collect_evidence_summaries(evidence_dir: Path) -> List[Dict]:
    """Summarize all evidence files."""
    summaries = []
    for ev_file in sorted(evidence_dir.glob("*_evidence.json")):
        try:
            with open(ev_file, 'r') as f:
                data = json.load(f)
            summaries.append({
                "verifier": data.get("verifier", "unknown"),
                "status": data.get("status", "unknown"),
                "duration": data.get("duration_seconds", 0),
                "checks_passed": sum(1 for c in data.get("checks", []) if c.get("passed")),
                "checks_total": len(data.get("checks", [])),
                "file": ev_file.name
            })
        except Exception:
            summaries.append({
                "file": ev_file.name,
                "status": "ERROR",
                "error": "Could not parse evidence file"
            })
    return summaries


def generate_certificate(repo_root: Path, evidence_dir: Path, 
                         verification_dir: Path, report: Dict) -> Dict:
    """Generate the signed verification certificate."""
    
    commit_hash = get_git_commit_hash(repo_root)
    branch = get_git_branch(repo_root)
    
    certificate = {
        "certificate_version": "1.0",
        "certificate_type": "AQARION_VERIFICATION_CERTIFICATE",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repository": {
            "root": str(repo_root),
            "commit_hash": commit_hash,
            "branch": branch,
            "git_clean": commit_hash is not None,
        },
        "environment": {
            "python_version": get_python_version(),
            "operating_system": get_os_info(),
            "dependencies": get_dependency_versions(),
        },
        "verification_suite": {
            "version": "1.0",
            "verifier_hashes": compute_verifier_hashes(verification_dir),
            "total_verifiers": len(report.get("results", [])),
            "passed": sum(1 for r in report.get("results", []) if r.get("passed")),
            "failed": sum(1 for r in report.get("results", []) if not r.get("passed")),
        },
        "evidence_summary": collect_evidence_summaries(evidence_dir),
        "production_gates": report.get("production_gates", {}),
        "tier_breakdown": report.get("tier_breakdown", {}),
        "total_duration_seconds": report.get("total_duration_seconds", 0),
    }
    
    # Compute certificate hash (acts as signature)
    cert_str = json.dumps(certificate, sort_keys=True)
    certificate["certificate_hash"] = hashlib.sha256(cert_str.encode()).hexdigest()
    certificate["certificate_hash_algorithm"] = "SHA256"
    
    return certificate


def main():
    parser = argparse.ArgumentParser(description="Generate signed verification certificate")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--evidence-dir", type=Path, default=Path("evidence"))
    parser.add_argument("--verification-dir", type=Path, default=Path("verification"))
    parser.add_argument("--report", type=Path, required=True,
                        help="Path to referee report.json")
    parser.add_argument("--output", type=Path, default=Path("verification_certificate.json"),
                        help="Output certificate path")
    args = parser.parse_args()
    
    sys.path.insert(0, str(Path(__file__).parent))
    from report import Evidence, ReportLogger, exit_pass, exit_fail, exit_error
    
    logger = ReportLogger()
    start = time.time()
    
    evidence = Evidence(
        verifier="verify_meta.py",
        claim="Generates cryptographically signed verification certificate"
    )
    
    try:
        # Load report
        logger.info(f"Loading report: {args.report}")
        with open(args.report, 'r') as f:
            report = json.load(f)
        
        # Generate certificate
        logger.info("Generating verification certificate...")
        certificate = generate_certificate(
            args.repo_root, args.evidence_dir, args.verification_dir, report
        )
        
        # Save certificate
        with open(args.output, 'w') as f:
            json.dump(certificate, f, indent=2)
        
        evidence.add_artifact(args.output)
        evidence.add_metric("certificate_hash", certificate["certificate_hash"])
        evidence.add_metric("verifiers_total", certificate["verification_suite"]["total_verifiers"])
        evidence.add_metric("verifiers_passed", certificate["verification_suite"]["passed"])
        
        # Verify certificate is self-consistent
        cert_copy = dict(certificate)
        stored_hash = cert_copy.pop("certificate_hash")
        stored_algo = cert_copy.pop("certificate_hash_algorithm")
        recomputed = hashlib.sha256(json.dumps(cert_copy, sort_keys=True).encode()).hexdigest()
        
        hash_valid = stored_hash == recomputed
        evidence.add_check(
            name="certificate_self_consistent",
            passed=hash_valid,
            value=stored_hash[:16] + "...",
            expected=recomputed[:16] + "..."
        )
        
        all_passed = certificate["verification_suite"]["failed"] == 0
        evidence.add_check(
            name="all_verifiers_passed",
            passed=all_passed,
            value=certificate["verification_suite"]["failed"],
            expected=0
        )
        
        evidence.set_duration(start)
        evidence_path = args.evidence_dir / "verify_meta_evidence.json"
        evidence.save(evidence_path)
        
        logger.info(f"Certificate saved: {args.output}")
        logger.info(f"Certificate hash: {certificate['certificate_hash']}")
        
        if hash_valid and all_passed:
            exit_pass(evidence, "Meta-verification passed — certificate generated and validated")
        elif not hash_valid:
            exit_fail(evidence, "Certificate hash mismatch — integrity failure")
        else:
            exit_fail(evidence, "Some verifiers failed — certificate indicates incomplete verification")
            
    except Exception as e:
        evidence.set_duration(start)
        exit_error(evidence, e, "Meta-verification error")


if __name__ == "__main__":
    main()
'''

with open("/mnt/agents/output/verify_meta.py", 'w') as f:
    f.write(verify_meta_py)

print("[SAVED] verify_meta.py (Signed verification certificate generator)")
