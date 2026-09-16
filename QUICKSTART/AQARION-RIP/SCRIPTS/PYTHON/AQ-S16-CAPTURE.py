#!/usr/bin/env python3
"""AQARION capture — RPL-001: FAILED RUN ⇒ COMPLETE RECEIPT via direct returncode."""
from __future__ import annotations
import argparse
import datetime
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return "NO_SOURCE"
    return sha256_bytes(path.read_bytes())


def run_claim(claim_id: str, run_id: str, cmd: list[str], workdir: Path | None = None) -> int:
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    workdir = workdir or Path.cwd()
    out_dir = workdir / "runs" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    receipts_dir = workdir / "RECEIPTS"
    receipts_dir.mkdir(parents=True, exist_ok=True)

    try:
        proc = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=str(workdir)
        )
        exit_code = proc.returncode
        stdout = proc.stdout or b""
        stderr = proc.stderr or b""
    except Exception as e:
        exit_code = 127
        stdout = b""
        stderr = str(e).encode()

    (out_dir / "stdout.txt").write_bytes(stdout)
    (out_dir / "stderr.txt").write_bytes(stderr)

    source_sha = "NO_SOURCE"
    for arg in reversed(cmd):
        p = Path(arg)
        if p.suffix in {".py", ".lean", ".sh"} and p.exists():
            source_sha = sha256_file(p)
            break

    try:
        commit = subprocess.getoutput("git rev-parse HEAD 2>/dev/null")[:12] or "UNVERSIONED"
    except Exception:
        commit = "UNVERSIONED"

    residual = None
    if exit_code != 0:
        residual = {"expression": f"exit_code={exit_code}", "note": "non-zero exit"}

    receipt = {
        "receipt_id": f"AQ-RPL-{run_id}",
        "claim_id": claim_id,
        "run_id": run_id,
        "timestamp_utc": ts,
        "command": cmd,
        "exit_code": exit_code,
        "stdout_sha256": sha256_bytes(stdout) if stdout else "NO_STDOUT",
        "stderr_sha256": sha256_bytes(stderr) if stderr else "NO_STDERR",
        "source_sha256": source_sha,
        "commit": commit,
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "policy": {
            "filesystem": "workspace_only",
            "network": False,
            "external_actions": False,
        },
        "verdict": "FAILED" if exit_code != 0 else "COMPUTED",
        "residual": residual,
        "promotion_allowed": False,
        "independent_machine": False,
    }
    # INVARIANT: always write complete receipt
    (out_dir / "receipt.json").write_text(json.dumps(receipt, indent=2))
    (receipts_dir / f"{receipt['receipt_id']}.json").write_text(json.dumps(receipt, indent=2))
    print(json.dumps(receipt, indent=2))
    return exit_code


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("claim_id")
    p.add_argument("run_id")
    p.add_argument("cmd", nargs=argparse.REMAINDER)
    args = p.parse_args()
    cmd = list(args.cmd)
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    if not cmd:
        print(
            "Usage: capture.py CLAIM_ID RUN_ID [--] command [args...]",
            file=sys.stderr,
        )
        sys.exit(2)
    sys.exit(run_claim(args.claim_id, args.run_id, cmd))


if __name__ == "__main__":
    main()
