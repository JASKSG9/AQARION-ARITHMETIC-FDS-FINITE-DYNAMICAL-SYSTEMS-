
report_py = '''#!/usr/bin/env python3
"""
AQARION Shared Reporting Utilities
==================================
Version: 1.0
Purpose: Common output formatting, evidence serialization, and log handling
         for ALL verification scripts.

CRITICAL: This module MUST NOT import from any AQARION source code.
          It uses only Python standard library.

Usage in verifiers:
    from report import Evidence, ReportLogger, exit_pass, exit_fail, exit_error
"""

import json
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class Evidence:
    """
    Standardized evidence container for a single verification check.
    Each verifier produces one Evidence instance, serialized to JSON.
    """
    __slots__ = ("verifier", "claim", "status", "checks", "metrics",
                 "artifacts", "timestamp", "duration", "notes")

    def __init__(self, verifier: str, claim: str, status: str = "PENDING"):
        self.verifier = verifier
        self.claim = claim
        self.status = status          # PASS, FAIL, ERROR, SKIP
        self.checks: List[Dict[str, Any]] = []
        self.metrics: Dict[str, Union[int, float, str]] = {}
        self.artifacts: List[str] = []
        self.timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.duration: float = 0.0
        self.notes: List[str] = []

    def add_check(self, name: str, passed: bool, value: Any = None,
                  tolerance: Optional[float] = None, expected: Any = None) -> None:
        """Record a single sub-check with optional tolerance comparison."""
        entry = {
            "name": name,
            "passed": passed,
            "value": self._serialize_value(value),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        if expected is not None:
            entry["expected"] = self._serialize_value(expected)
        if tolerance is not None:
            entry["tolerance"] = tolerance
            if value is not None and expected is not None:
                try:
                    entry["within_tolerance"] = abs(float(value) - float(expected)) <= tolerance
                except (TypeError, ValueError):
                    entry["within_tolerance"] = None
        self.checks.append(entry)

    def add_metric(self, name: str, value: Union[int, float, str]) -> None:
        """Record a quantitative metric (e.g., matrix rank, computation time)."""
        self.metrics[name] = value

    def add_artifact(self, path: Union[str, Path]) -> None:
        """Record a path to an artifact produced during verification."""
        self.artifacts.append(str(path))

    def add_note(self, note: str) -> None:
        """Add a free-text note for the audit trail."""
        self.notes.append(note)

    def set_duration(self, start_time: float) -> None:
        """Set duration from a start timestamp."""
        self.duration = time.time() - start_time

    def all_checks_passed(self) -> bool:
        """Return True only if all sub-checks passed."""
        return all(c["passed"] for c in self.checks)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "verifier": self.verifier,
            "claim": self.claim,
            "status": self.status,
            "timestamp": self.timestamp,
            "duration_seconds": round(self.duration, 6),
            "checks": self.checks,
            "metrics": self.metrics,
            "artifacts": self.artifacts,
            "notes": self.notes,
        }

    def save(self, output_path: Union[str, Path]) -> Path:
        """Serialize evidence to JSON file."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        return path

    @staticmethod
    def _serialize_value(value: Any) -> Any:
        """Handle numpy types and other non-JSON-serializable values."""
        if value is None:
            return None
        # Handle numpy scalars/arrays if present (verifiers may use numpy)
        module_name = type(value).__module__
        if module_name and module_name.startswith("numpy"):
            try:
                return float(value) if hasattr(value, "item") else value.tolist()
            except Exception:
                return str(value)
        if isinstance(value, Path):
            return str(value)
        return value


class ReportLogger:
    """
    Simple structured logger for verification output.
    Writes to both stdout and an optional log file.
    """
    def __init__(self, log_file: Optional[Path] = None):
        self.log_file = log_file
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            # Clear existing log
            open(log_file, 'w').close()

    def info(self, message: str) -> None:
        self._write("INFO", message)

    def warn(self, message: str) -> None:
        self._write("WARN", message)

    def error(self, message: str) -> None:
        self._write("ERROR", message)

    def success(self, message: str) -> None:
        self._write("PASS", message)

    def fail(self, message: str) -> None:
        self._write("FAIL", message)

    def _write(self, level: str, message: str) -> None:
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        line = f"[{timestamp}] [{level}] {message}"
        print(line)
        if self.log_file:
            with open(self.log_file, 'a') as f:
                f.write(line + "\\n")


def exit_pass(evidence: Evidence, message: str = "Verification passed") -> None:
    """Standard exit for successful verification."""
    evidence.status = "PASS"
    print(f"\\n✅ {message}")
    print(f"    Checks passed: {sum(1 for c in evidence.checks if c['passed'])}/{len(evidence.checks)}")
    print(f"    Duration: {evidence.duration:.3f}s")
    sys.exit(0)


def exit_fail(evidence: Evidence, message: str = "Verification failed") -> None:
    """Standard exit for failed verification."""
    evidence.status = "FAIL"
    print(f"\\n❌ {message}")
    print(f"    Checks passed: {sum(1 for c in evidence.checks if c['passed'])}/{len(evidence.checks)}")
    failed_checks = [c["name"] for c in evidence.checks if not c["passed"]]
    if failed_checks:
        print(f"    Failed checks: {', '.join(failed_checks)}")
    print(f"    Duration: {evidence.duration:.3f}s")
    sys.exit(1)


def exit_error(evidence: Evidence, exception: Exception,
               message: str = "Verification error") -> None:
    """Standard exit for infrastructure/exception errors."""
    evidence.status = "ERROR"
    evidence.add_note(f"Exception: {type(exception).__name__}: {exception}")
    evidence.add_note(traceback.format_exc())
    print(f"\\n💥 {message}")
    print(f"    Exception: {type(exception).__name__}: {exception}")
    print(f"    Duration: {evidence.duration:.3f}s")
    sys.exit(2)
'''

with open("/mnt/agents/output/report.py", 'w') as f:
    f.write(report_py)

print("[SAVED] report.py")
