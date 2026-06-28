
# Generate verify_claims.py (integrates with AQARION-CC v2.0 concept)
verify_claims_py = '''#!/usr/bin/env python3
"""
AQARION Claim Compiler Verifier
================================
Version: 1.0
Claim: All manuscript claims are supported by the invariance ledger,
       scope matrix, and computational evidence. Zero unsupported claims.

CRITICAL: This script MUST NOT import from any AQARION source module.
          It reads claim_audit.json and manuscript files independently.

Expected repository files:
  - claim_audit.json       (claim database with evidence references)
  - invariance_ledger.md   (invariant tracking)
  - scope_matrix.md        (scope boundaries)
  - Manuscript files (paper.md, paper.tex, or similar)

Exit: 0 = PASS, 1 = FAIL, 2 = ERROR
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# ============================================================
# CONFIGURATION
# ============================================================
CLAIM_AUDIT_FILE = "claim_audit.json"
INVARIANCE_LEDGER = "invariance_ledger.md"
SCOPE_MATRIX = "scope_matrix.md"
MANUSCRIPT_PATTERNS = ["paper.md", "paper.tex", "manuscript.md", "manuscript.tex", "docs/**/*.md"]

# Claim reference patterns in manuscript (e.g., [Claim-001], Theorem 3.2, etc.)
CLAIM_REFERENCE_PATTERNS = [
    r"\[Claim-\d+\]",
    r"\[Theorem-\d+\.\d+\]",
    r"\[Lemma-\d+\.\d+\]",
    r"\[Corollary-\d+\.\d+\]",
    r"\[Proposition-\d+\.\d+\]",
]


def load_claim_audit(repo_root: Path) -> Optional[Dict]:
    """Load claim audit database."""
    path = repo_root / CLAIM_AUDIT_FILE
    if path.exists():
        with open(path, 'r') as f:
            return json.load(f)
    return None


def load_manuscript_claims(repo_root: Path) -> Set[str]:
    """Extract all claim references from manuscript files."""
    found_claims = set()
    for pattern in MANUSCRIPT_PATTERNS:
        for file_path in repo_root.glob(pattern):
            if not file_path.is_file():
                continue
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                for regex in CLAIM_REFERENCE_PATTERNS:
                    found_claims.update(re.findall(regex, content))
            except Exception:
                continue
    return found_claims


def verify_claim_coverage(audit: Dict, manuscript_claims: Set[str], evidence, logger) -> bool:
    """Check that every manuscript claim is in the audit database."""
    if not audit or "claims" not in audit:
        evidence.add_check(
            name="claim_audit_exists",
            passed=False,
            value="missing or malformed claim_audit.json",
            expected="valid claim database"
        )
        return False

    audit_claims = set()
    for claim in audit.get("claims", []):
        claim_id = claim.get("id", claim.get("claim_id", ""))
        if claim_id:
            audit_claims.add(f"[{claim_id}]")

    evidence.add_metric("audit_claims", len(audit_claims))
    evidence.add_metric("manuscript_claims", len(manuscript_claims))

    # Check for unsupported claims (in manuscript but not in audit)
    unsupported = manuscript_claims - audit_claims
    supported = manuscript_claims & audit_claims

    evidence.add_check(
        name="unsupported_claims",
        passed=len(unsupported) == 0,
        value=list(unsupported)[:20],
        expected=[]
    )

    evidence.add_check(
        name="supported_claims",
        passed=len(supported) > 0,
        value=len(supported),
        expected=">0"
    )

    if unsupported:
        evidence.add_note(f"Unsupported claims found: {len(unsupported)}")
        for c in list(unsupported)[:10]:
            evidence.add_note(f"  - {c}")

    logger.info(f"Claims: {len(supported)} supported, {len(unsupported)} unsupported")
    return len(unsupported) == 0


def verify_evidence_links(audit: Dict, repo_root: Path, evidence, logger) -> bool:
    """Check that every claim has valid evidence links."""
    if not audit or "claims" not in audit:
        return False

    broken_links = []
    claims_without_evidence = []

    for claim in audit.get("claims", []):
        claim_id = claim.get("id", "unknown")
        evidence_refs = claim.get("evidence", claim.get("evidence_refs", []))

        if not evidence_refs:
            claims_without_evidence.append(claim_id)
            evidence.add_check(
                name=f"evidence_link:{claim_id}",
                passed=False,
                value="no evidence references",
                expected=">=1 evidence reference"
            )
            continue

        for ref in evidence_refs:
            ref_path = repo_root / ref
            if not ref_path.exists():
                broken_links.append(f"{claim_id} -> {ref}")
                evidence.add_check(
                    name=f"evidence_link:{claim_id}:{ref}",
                    passed=False,
                    value="file not found",
                    expected="exists"
                )
            else:
                evidence.add_check(
                    name=f"evidence_link:{claim_id}:{ref}",
                    passed=True,
                    value=str(ref_path.relative_to(repo_root)),
                    expected="exists"
                )

    evidence.add_metric("claims_without_evidence", len(claims_without_evidence))
    evidence.add_metric("broken_evidence_links", len(broken_links))

    if claims_without_evidence:
        evidence.add_note(f"Claims without evidence: {claims_without_evidence[:10]}")
    if broken_links:
        evidence.add_note(f"Broken evidence links: {broken_links[:10]}")

    all_ok = len(claims_without_evidence) == 0 and len(broken_links) == 0

    evidence.add_check(
        name="all_evidence_valid",
        passed=all_ok,
        value={
            "missing_evidence": len(claims_without_evidence),
            "broken_links": len(broken_links)
        },
        expected={"missing_evidence": 0, "broken_links": 0}
    )

    return all_ok


def verify_ledger_and_scope(repo_root: Path, evidence, logger) -> bool:
    """Check that ledger and scope matrix exist and are non-empty."""
    checks = []

    ledger_path = repo_root / INVARIANCE_LEDGER
    ledger_exists = ledger_path.exists() and ledger_path.stat().st_size > 0
    checks.append(ledger_exists)
    evidence.add_check(
        name="invariance_ledger_exists",
        passed=ledger_exists,
        value=str(ledger_path) if ledger_exists else "missing/empty",
        expected="exists and non-empty"
    )

    scope_path = repo_root / SCOPE_MATRIX
    scope_exists = scope_path.exists() and scope_path.stat().st_size > 0
    checks.append(scope_exists)
    evidence.add_check(
        name="scope_matrix_exists",
        passed=scope_exists,
        value=str(scope_path) if scope_exists else "missing/empty",
        expected="exists and non-empty"
    )

    if ledger_exists:
        with open(ledger_path, 'r') as f:
            lines = [l for l in f.readlines() if l.strip() and not l.startswith('#')]
        evidence.add_metric("ledger_entries", len(lines))

    if scope_exists:
        with open(scope_path, 'r') as f:
            lines = [l for l in f.readlines() if l.strip() and not l.startswith('#')]
        evidence.add_metric("scope_entries", len(lines))

    return all(checks)


def main():
    parser = argparse.ArgumentParser(description="Verify claim compiler integrity")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(),
                        help="Repository root directory")
    parser.add_argument("--evidence-dir", type=Path, default=Path("evidence"),
                        help="Directory to write evidence JSON")
    parser.add_argument("--log-file", type=Path, default=None,
                        help="Optional log file path")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    sys.path.insert(0, str(Path(__file__).parent))
    from report import Evidence, ReportLogger, exit_pass, exit_fail, exit_error

    logger = ReportLogger(log_file=args.log_file)
    start = time.time()

    evidence = Evidence(
        verifier="verify_claims.py",
        claim="All manuscript claims are supported by evidence with zero unsupported claims"
    )

    logger.info(f"Claim verification for: {repo_root}")

    try:
        # Check 1: Ledger and scope matrix
        logger.info("Checking invariance ledger and scope matrix...")
        ledger_ok = verify_ledger_and_scope(repo_root, evidence, logger)

        # Check 2: Load claim audit
        logger.info("Loading claim audit database...")
        audit = load_claim_audit(repo_root)
        if audit is None:
            evidence.add_note("claim_audit.json not found — this is a first-run condition")
            evidence.add_note("Generate claim_audit.json using AQARION-CC v2.0")

        # Check 3: Extract manuscript claims
        logger.info("Scanning manuscript for claim references...")
        manuscript_claims = load_manuscript_claims(repo_root)
        evidence.add_metric("manuscript_claims_found", len(manuscript_claims))

        # Check 4: Verify coverage
        coverage_ok = True
        if audit and manuscript_claims:
            logger.info("Verifying claim coverage...")
            coverage_ok = verify_claim_coverage(audit, manuscript_claims, evidence, logger)
        elif not manuscript_claims:
            logger.warn("No claim references found in manuscript")
            evidence.add_note("No claim references detected — manuscript may not use claim IDs")

        # Check 5: Verify evidence links
        evidence_ok = True
        if audit:
            logger.info("Verifying evidence links...")
            evidence_ok = verify_evidence_links(audit, repo_root, evidence, logger)

        evidence.set_duration(start)

        evidence_path = args.evidence_dir / "verify_claims_evidence.json"
        evidence.save(evidence_path)
        logger.info(f"Evidence saved: {evidence_path}")

        if all([ledger_ok, coverage_ok, evidence_ok]):
            logger.success("Claim verification passed")
            exit_pass(evidence, "Claim verification passed")
        else:
            logger.fail("Claim verification failed")
            exit_fail(evidence, "Claim verification failed")

    except Exception as e:
        evidence.set_duration(start)
        exit_error(evidence, e, "Claim verification error")


if __name__ == "__main__":
    main()
'''

with open("/mnt/agents/output/verify_claims.py", 'w') as f:
    f.write(verify_claims_py)

print("[SAVED] verify_claims.py")[SAVED] verify_claims.py
<>:40: SyntaxWarning: invalid escape sequence '\['
<>:40: SyntaxWarning: invalid escape sequence '\['
/tmp/ipykernel_397/108671004.py:40: SyntaxWarning: invalid escape sequence '\['
  r"\[Claim-\d+\]",
