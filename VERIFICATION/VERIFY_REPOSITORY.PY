
verify_repository_py = '''#!/usr/bin/env python3
"""
AQARION Repository Integrity Verifier
======================================
Version: 1.0
Claim: The repository has complete directory structure, required files,
       no missing modules, no duplicate files, and no broken imports.

CRITICAL: This script MUST NOT import from any AQARION source module.
          It performs structural analysis using only filesystem inspection.

Exit: 0 = PASS, 1 = FAIL, 2 = ERROR
"""

import argparse
import ast
import sys
import time
from pathlib import Path

# ============================================================
# CONFIGURATION — Required repository structure
# ============================================================
REQUIRED_TOP_LEVEL_FILES = [
    "README.md",
    "LICENSE",
    "CITATION.cff",
    "CHANGELOG.md",
]

REQUIRED_DIRECTORIES = [
    "docs",
    "src",           # or equivalent source directory
    "verification",  # this suite
    "tests",         # unit tests
    "data",          # datasets, manifests
]

REQUIRED_VERIFICATION_FILES = [
    "verification/referee.py",
    "verification/report.py",
    "verification/verify_repository.py",
    "verification/verify_hashes.py",
    "verification/verify_reproducibility.py",
]

# Files that must exist if claims are made about them
CLAIM_DEPENDENT_FILES = {
    "Lean formalization": ["*.lean", "lakefile.lean", "lean-toolchain"],
    "CI pipeline": [".github/workflows/*.yml", ".github/workflows/*.yaml"],
    "Docker build": ["Dockerfile", "docker-compose.yml"],
    "Release metadata": ["CITATION.cff", "LICENSE"],
    "Python package": ["pyproject.toml", "setup.py", "setup.cfg"],
}

# Import ban check: these patterns indicate a verifier importing source code
BANNED_IMPORT_PATTERNS = [
    "from aqarion",
    "from src.",
    "import aqarion",
    "import src_",
]


def check_file_exists(repo_root: Path, rel_path: str, evidence) -> bool:
    """Check if a required file exists."""
    full_path = repo_root / rel_path
    exists = full_path.exists()
    evidence.add_check(
        name=f"file_exists:{rel_path}",
        passed=exists,
        value=str(full_path) if exists else None,
        expected="exists"
    )
    return exists


def check_directory_exists(repo_root: Path, dir_name: str, evidence) -> bool:
    """Check if a required directory exists."""
    full_path = repo_root / dir_name
    exists = full_path.exists() and full_path.is_dir()
    evidence.add_check(
        name=f"dir_exists:{dir_name}",
        passed=exists,
        value=str(full_path) if exists else None,
        expected="exists"
    )
    return exists


def check_duplicate_files(repo_root: Path, evidence) -> bool:
    """Detect duplicate filenames (potential copy-paste errors)."""
    from collections import defaultdict
    name_map = defaultdict(list)
    for path in repo_root.rglob("*"):
        if path.is_file() and ".git" not in str(path):
            name_map[path.name].append(str(path.relative_to(repo_root)))

    duplicates = {name: paths for name, paths in name_map.items() if len(paths) > 1}
    # Exclude common duplicates (like __init__.py, README.md in subdirs)
    meaningful_dups = {
        name: paths for name, paths in duplicates.items()
        if name not in {"__init__.py", "README.md", ".gitignore", "requirements.txt"}
    }

    passed = len(meaningful_dups) == 0
    evidence.add_check(
        name="no_duplicate_files",
        passed=passed,
        value=list(meaningful_dups.keys()) if meaningful_dups else [],
        expected=[]
    )
    if meaningful_dups:
        evidence.add_note(f"Duplicate files detected: {json.dumps(meaningful_dups, indent=2)}")
    return passed


def check_broken_imports(repo_root: Path, evidence) -> bool:
    """Scan Python files for import statements that reference non-existent modules."""
    broken = []
    py_files = list(repo_root.rglob("*.py"))
    evidence.add_metric("python_files_scanned", len(py_files))

    for py_file in py_files:
        if ".git" in str(py_file):
            continue
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=str(py_file))
        except SyntaxError as e:
            broken.append(f"Syntax error in {py_file.relative_to(repo_root)}: {e}")
            continue
        except Exception:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # Simple heuristic: if it's a local module, check existence
                    mod_name = alias.name.split('.')[0]
                    if mod_name not in sys.stdlib_module_names:
                        # Could be local — check if file or package exists
                        local_mod = repo_root / mod_name.replace('.', '/') / "__init__.py"
                        local_file = repo_root / (mod_name.replace('.', '/') + ".py")
                        if not local_mod.exists() and not local_file.exists():
                            # Might be an installed package — skip
                            pass
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    mod_name = node.module.split('.')[0]
                    if mod_name not in sys.stdlib_module_names:
                        local_mod = repo_root / mod_name.replace('.', '/') / "__init__.py"
                        local_file = repo_root / (mod_name.replace('.', '/') + ".py")
                        if not local_mod.exists() and not local_file.exists():
                            # Check if it's actually installed
                            try:
                                __import__(mod_name)
                            except ImportError:
                                rel_path = py_file.relative_to(repo_root)
                                broken.append(f"{rel_path}: cannot resolve '{node.module}'")

    passed = len(broken) == 0
    evidence.add_check(
        name="no_broken_imports",
        passed=passed,
        value=broken[:10] if broken else [],  # Limit output
        expected=[]
    )
    if broken:
        evidence.add_note(f"Found {len(broken)} broken import references (showing first 10)")
    return passed


def check_verifier_independence(repo_root: Path, evidence) -> bool:
    """
    CRITICAL CHECK: Ensure verification scripts do not import from source tree.
    This enforces the core principle: verifiers must be independent.
    """
    violations = []
    verification_dir = repo_root / "verification"
    if not verification_dir.exists():
        evidence.add_check(
            name="verifier_independence",
            passed=False,
            value="verification directory not found",
            expected="no banned imports"
        )
        return False

    for py_file in verification_dir.rglob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue

        for pattern in BANNED_IMPORT_PATTERNS:
            if pattern in content:
                rel = py_file.relative_to(repo_root)
                violations.append(f"{rel}: banned pattern '{pattern}'")

    passed = len(violations) == 0
    evidence.add_check(
        name="verifier_independence",
        passed=passed,
        value=violations[:10] if violations else [],
        expected=[]
    )
    if violations:
        evidence.add_note(
            f"VERIFIER INDEPENDENCE VIOLATION: {len(violations)} files import from source tree. "
            f"This INVALIDATES the audit. Verifiers must use only standard libraries."
        )
    return passed


def check_claim_dependent_files(repo_root: Path, evidence) -> bool:
    """Check for files that should exist based on claimed features."""
    all_passed = True
    for claim, patterns in CLAIM_DEPENDENT_FILES.items():
        found_any = False
        found_paths = []
        for pattern in patterns:
            matches = list(repo_root.glob(pattern))
            if matches:
                found_any = True
                found_paths.extend([str(m.relative_to(repo_root)) for m in matches])

        # Note: we don't FAIL if missing — we just record the gap
        evidence.add_check(
            name=f"claim_file_check:{claim}",
            passed=found_any,  # If claimed, should exist
            value=found_paths if found_any else f"No files matching {patterns}",
            expected=f"Files matching {patterns}"
        )
        if not found_any:
            evidence.add_note(f"Claim-dependent files missing for: {claim}")
            all_passed = False

    return all_passed


def main():
    parser = argparse.ArgumentParser(description="Verify repository integrity")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(),
                        help="Repository root directory")
    parser.add_argument("--evidence-dir", type=Path, default=Path("evidence"),
                        help="Directory to write evidence JSON")
    parser.add_argument("--log-file", type=Path, default=None,
                        help="Optional log file path")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    # Import report utilities (same directory, standard library only)
    sys.path.insert(0, str(Path(__file__).parent))
    from report import Evidence, ReportLogger, exit_pass, exit_fail, exit_error

    logger = ReportLogger(log_file=args.log_file)
    start = time.time()

    evidence = Evidence(
        verifier="verify_repository.py",
        claim="Repository has complete structure, no missing modules, no duplicates, no broken imports"
    )

    logger.info(f"Scanning repository: {repo_root}")
    evidence.add_metric("repo_root", str(repo_root))

    try:
        # Check 1: Required top-level files
        logger.info("Checking required top-level files...")
        files_ok = all(check_file_exists(repo_root, f, evidence) for f in REQUIRED_TOP_LEVEL_FILES)

        # Check 2: Required directories
        logger.info("Checking required directories...")
        dirs_ok = all(check_directory_exists(repo_root, d, evidence) for d in REQUIRED_DIRECTORIES)

        # Check 3: Duplicate files
        logger.info("Checking for duplicate files...")
        dups_ok = check_duplicate_files(repo_root, evidence)

        # Check 4: Broken imports
        logger.info("Checking for broken imports...")
        imports_ok = check_broken_imports(repo_root, evidence)

        # Check 5: Verifier independence (CRITICAL)
        logger.info("Checking verifier independence (CRITICAL)...")
        independence_ok = check_verifier_independence(repo_root, evidence)

        # Check 6: Claim-dependent files
        logger.info("Checking claim-dependent files...")
        claims_ok = check_claim_dependent_files(repo_root, evidence)

        evidence.set_duration(start)

        # Save evidence
        evidence_path = args.evidence_dir / "verify_repository_evidence.json"
        evidence.save(evidence_path)
        logger.info(f"Evidence saved: {evidence_path}")

        # Determine outcome
        if not independence_ok:
            logger.error("VERIFIER INDEPENDENCE VIOLATION — AUDIT INVALID")
            exit_fail(evidence, "Repository integrity: VERIFIER INDEPENDENCE VIOLATION")

        if all([files_ok, dirs_ok, dups_ok, imports_ok, claims_ok]):
            logger.success("All repository integrity checks passed")
            exit_pass(evidence, "Repository integrity verified")
        else:
            logger.fail("One or more repository integrity checks failed")
            exit_fail(evidence, "Repository integrity check failed")

    except Exception as e:
        evidence.set_duration(start)
        exit_error(evidence, e, "Repository integrity verification error")


if __name__ == "__main__":
    main()
'''

with open("/mnt/agents/output/verify_repository.py", 'w') as f:
    f.write(verify_repository_py)

print("[SAVED] verify_repository.py")
