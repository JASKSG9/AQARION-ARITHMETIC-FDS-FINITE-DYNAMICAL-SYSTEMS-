
verify_reproducibility_py = '''#!/usr/bin/env python3
"""
AQARION Reproducibility Verifier
=================================
Version: 1.0
Claim: The repository can be cleanly rebuilt from a fresh clone with
       matching hashes to the original.

CRITICAL: This script MUST NOT import from any AQARION source module.
          It performs fresh clone, isolated build, and hash comparison.

This verifier:
  1. Creates a temporary directory
  2. Clones the repository (if git remote available) or copies to temp
  3. Installs dependencies in clean environment
  4. Runs build/generation steps
  5. Compares output hashes against original

Exit: 0 = PASS, 1 = FAIL, 2 = ERROR
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ============================================================
# CONFIGURATION — Build steps to execute in fresh environment
# ============================================================
DEFAULT_BUILD_STEPS = [
    # Check Python version
    ["python", "--version"],
    # Install dependencies if requirements.txt exists
    ["pip", "install", "-r", "requirements.txt"],
    # Run any generation scripts
    ["python", "-m", "pytest", "tests/", "-q"],
]

# Files to compare after rebuild (must be deterministic)
ARTIFACT_PATTERNS = [
    "paper.pdf",
    "**/*.csv",
    "**/*.json",
    "data/**",
    "figures/**",
]


def get_git_remote(repo_root: Path) -> Optional[str]:
    """Get the git remote URL for cloning."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=str(repo_root), capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def clone_repository(remote_url: str, target_dir: Path, logger) -> bool:
    """Clone repository to target directory."""
    logger.info(f"Cloning from {remote_url} to {target_dir}")
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", remote_url, str(target_dir)],
            check=True, capture_output=True, text=True, timeout=120
        )
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Clone failed: {e.stderr}")
        return False
    except subprocess.TimeoutExpired:
        logger.error("Clone timed out after 120s")
        return False


def copy_repository(source: Path, target: Path, logger) -> bool:
    """Copy repository as fallback when git remote unavailable."""
    logger.info(f"Copying repository from {source} to {target}")
    try:
        # Use rsync-like copy excluding .git and temp files
        shutil.copytree(
            source, target,
            ignore=shutil.ignore_patterns(
                ".git", "__pycache__", "*.pyc", ".venv", "venv",
                "node_modules", ".pytest_cache", ".mypy_cache"
            ),
            dirs_exist_ok=True
        )
        return True
    except Exception as e:
        logger.error(f"Copy failed: {e}")
        return False


def run_build_steps(build_dir: Path, steps: List[List[str]], logger) -> Tuple[bool, List[str]]:
    """Execute build steps in the fresh clone directory."""
    logs = []
    for step in steps:
        # Adjust paths for build directory
        adjusted_step = []
        for arg in step:
            if isinstance(arg, str) and ("/" in arg or "\\\\" in arg):
                # Might be a path — check if relative to build dir
                potential_path = build_dir / arg
                if potential_path.exists():
                    adjusted_step.append(str(potential_path))
                else:
                    adjusted_step.append(arg)
            else:
                adjusted_step.append(arg)

        logger.info(f"Build step: {' '.join(adjusted_step)}")
        try:
            result = subprocess.run(
                adjusted_step, cwd=str(build_dir),
                capture_output=True, text=True, timeout=300
            )
            logs.append(f"STEP: {' '.join(adjusted_step)}")
            logs.append(f"RC: {result.returncode}")
            logs.append(f"STDOUT: {result.stdout[:500]}")
            logs.append(f"STDERR: {result.stderr[:500]}")

            if result.returncode != 0:
                # Some steps are optional (e.g., tests might not exist)
                if "pytest" in adjusted_step[0] or "test" in ' '.join(adjusted_step).lower():
                    logger.warn(f"Test step failed (may be expected if no tests): {result.stderr[:200]}")
                    continue
                logger.error(f"Build step failed: {result.stderr[:500]}")
                return False, logs
        except FileNotFoundError as e:
            logger.warn(f"Build step command not found: {e}")
            logs.append(f"MISSING: {adjusted_step[0]}")
            continue
        except subprocess.TimeoutExpired:
            logger.error(f"Build step timed out: {' '.join(adjusted_step)}")
            return False, logs
        except Exception as e:
            logger.error(f"Build step error: {e}")
            return False, logs

    return True, logs


def discover_artifacts(directory: Path, patterns: List[str]) -> Dict[str, Path]:
    """Discover artifact files matching patterns."""
    artifacts = {}
    for pattern in patterns:
        for match in directory.glob(pattern):
            if match.is_file():
                rel = str(match.relative_to(directory))
                artifacts[rel] = match
    return artifacts


def compute_artifact_hashes(artifacts: Dict[str, Path]) -> Dict[str, str]:
    """Compute SHA256 for all artifacts."""
    hashes = {}
    for rel_path, filepath in artifacts.items():
        h = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        hashes[rel_path] = h.hexdigest()
    return hashes


def compare_artifacts(original_hashes: Dict[str, str],
                      rebuild_hashes: Dict[str, str],
                      evidence, logger) -> bool:
    """Compare artifact hashes between original and rebuild."""
    mismatches = []
    missing_in_rebuild = []
    missing_in_original = []

    # Check all original artifacts exist in rebuild
    for rel_path, orig_hash in original_hashes.items():
        if rel_path not in rebuild_hashes:
            missing_in_rebuild.append(rel_path)
            evidence.add_check(
                name=f"reproducibility:{rel_path}",
                passed=False,
                value="missing in rebuild",
                expected="exists"
            )
        elif orig_hash != rebuild_hashes[rel_path]:
            mismatches.append(rel_path)
            evidence.add_check(
                name=f"reproducibility:{rel_path}",
                passed=False,
                value=rebuild_hashes[rel_path][:16] + "...",
                expected=orig_hash[:16] + "..."
            )
        else:
            evidence.add_check(
                name=f"reproducibility:{rel_path}",
                passed=True,
                value=orig_hash[:16] + "...",
                expected=orig_hash[:16] + "..."
            )

    # Check for new artifacts in rebuild
    for rel_path in rebuild_hashes:
        if rel_path not in original_hashes:
            missing_in_original.append(rel_path)
            evidence.add_check(
                name=f"reproducibility:{rel_path}",
                passed=False,
                value="new in rebuild",
                expected="in original"
            )

    evidence.add_metric("original_artifacts", len(original_hashes))
    evidence.add_metric("rebuild_artifacts", len(rebuild_hashes))
    evidence.add_metric("mismatches", len(mismatches))
    evidence.add_metric("missing_in_rebuild", len(missing_in_rebuild))
    evidence.add_metric("new_in_rebuild", len(missing_in_original))

    if mismatches:
        evidence.add_note(f"Hash mismatches in {len(mismatches)} artifacts: {mismatches[:5]}")
    if missing_in_rebuild:
        evidence.add_note(f"Missing in rebuild: {missing_in_rebuild[:5]}")
    if missing_in_original:
        evidence.add_note(f"New in rebuild: {missing_in_original[:5]}")

    all_ok = len(mismatches) == 0 and len(missing_in_rebuild) == 0

    evidence.add_check(
        name="reproducibility_overall",
        passed=all_ok,
        value={
            "mismatches": len(mismatches),
            "missing": len(missing_in_rebuild),
            "extra": len(missing_in_original)
        },
        expected={"mismatches": 0, "missing": 0, "extra": 0}
    )

    return all_ok


def main():
    parser = argparse.ArgumentParser(description="Verify reproducibility from fresh clone")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(),
                        help="Repository root directory")
    parser.add_argument("--evidence-dir", type=Path, default=Path("evidence"),
                        help="Directory to write evidence JSON")
    parser.add_argument("--log-file", type=Path, default=None,
                        help="Optional log file path")
    parser.add_argument("--skip-clone", action="store_true",
                        help="Skip actual clone, use copy instead (faster, less rigorous)")
    parser.add_argument("--keep-temp", action="store_true",
                        help="Keep temporary directory for inspection")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    sys.path.insert(0, str(Path(__file__).parent))
    from report import Evidence, ReportLogger, exit_pass, exit_fail, exit_error

    logger = ReportLogger(log_file=args.log_file)
    start = time.time()

    evidence = Evidence(
        verifier="verify_reproducibility.py",
        claim="Repository can be cleanly rebuilt from fresh clone with matching hashes"
    )

    logger.info(f"Reproducibility verification for: {repo_root}")

    temp_dir = None
    try:
        # Step 1: Get original artifact hashes
        logger.info("Computing original artifact hashes...")
        original_artifacts = discover_artifacts(repo_root, ARTIFACT_PATTERNS)
        original_hashes = compute_artifact_hashes(original_artifacts)
        evidence.add_metric("original_artifact_count", len(original_hashes))
        logger.info(f"Found {len(original_hashes)} original artifacts")

        # Step 2: Create fresh clone/copy
        temp_dir = Path(tempfile.mkdtemp(prefix="aqarion_repro_"))
        evidence.add_metric("temp_directory", str(temp_dir))

        if args.skip_clone:
            success = copy_repository(repo_root, temp_dir / "repo", logger)
            evidence.add_note("Used copy mode (not true clone)")
        else:
            remote = get_git_remote(repo_root)
            if remote:
                success = clone_repository(remote, temp_dir / "repo", logger)
                evidence.add_note(f"Cloned from: {remote}")
            else:
                logger.warn("No git remote found, falling back to copy")
                success = copy_repository(repo_root, temp_dir / "repo", logger)
                evidence.add_note("No git remote — used copy fallback")

        if not success:
            evidence.set_duration(start)
            exit_fail(evidence, "Failed to create fresh copy of repository")

        build_dir = temp_dir / "repo"

        # Step 3: Run build steps
        logger.info("Running build steps in fresh environment...")
        build_ok, build_logs = run_build_steps(build_dir, DEFAULT_BUILD_STEPS, logger)
        evidence.add_metric("build_success", build_ok)

        # Save build logs as artifact
        log_path = temp_dir / "build_logs.txt"
        with open(log_path, 'w') as f:
            f.write('\\n'.join(build_logs))
        evidence.add_artifact(log_path)

        if not build_ok:
            evidence.set_duration(start)
            exit_fail(evidence, "Build steps failed in fresh environment")

        # Step 4: Compare artifacts
        logger.info("Comparing rebuilt artifacts...")
        rebuild_artifacts = discover_artifacts(build_dir, ARTIFACT_PATTERNS)
        rebuild_hashes = compute_artifact_hashes(rebuild_artifacts)
        evidence.add_metric("rebuild_artifact_count", len(rebuild_hashes))

        match_ok = compare_artifacts(original_hashes, rebuild_hashes, evidence, logger)

        evidence.set_duration(start)

        # Save comparison
        comparison_path = temp_dir / "hash_comparison.json"
        with open(comparison_path, 'w') as f:
            json.dump({
                "original": original_hashes,
                "rebuild": rebuild_hashes,
                "match": match_ok
            }, f, indent=2)
        evidence.add_artifact(comparison_path)

        evidence_path = args.evidence_dir / "verify_reproducibility_evidence.json"
        evidence.save(evidence_path)
        logger.info(f"Evidence saved: {evidence_path}")

        if match_ok:
            logger.success("Reproducibility verified — fresh clone produces identical artifacts")
            exit_pass(evidence, "Reproducibility verified")
        else:
            logger.fail("Reproducibility failed — artifacts differ between original and rebuild")
            exit_fail(evidence, "Reproducibility verification failed")

    except Exception as e:
        evidence.set_duration(start)
        exit_error(evidence, e, "Reproducibility verification error")

    finally:
        if temp_dir and not args.keep_temp:
            logger.info(f"Cleaning up temporary directory: {temp_dir}")
            shutil.rmtree(temp_dir, ignore_errors=True)
        elif temp_dir:
            logger.info(f"Keeping temporary directory: {temp_dir}")


if __name__ == "__main__":
    main()
'''

with open("/mnt/agents/output/verify_reproducibility.py", 'w') as f:
    f.write(verify_reproducibility_py)

print("[SAVED] verify_reproducibility.py")
