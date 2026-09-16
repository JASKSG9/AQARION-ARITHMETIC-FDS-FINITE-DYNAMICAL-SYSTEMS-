#!/usr/bin/env python3
"""aqreplay minimal CLI — init / capture / verify / explain / closure / diff"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))


def cmd_init():
    for d in ["claims", "runs", "RECEIPTS", "FIXTURES", "ENGINES"]:
        (ROOT / d).mkdir(exist_ok=True)
    print("Initialized skeleton under", ROOT)


def cmd_capture(args):
    from capture import run_claim

    if len(args) < 3 or args[2] != "--":
        print("Usage: aqreplay capture CLAIM RUN -- command...")
        sys.exit(2)
    sys.exit(run_claim(args[0], args[1], args[3:], workdir=ROOT))


def cmd_verify(run_id: str):
    p = ROOT / "runs" / run_id / "receipt.json"
    if not p.exists():
        print("No receipt")
        sys.exit(1)
    data = json.loads(p.read_text())
    req = ["receipt_id", "claim_id", "exit_code", "verdict", "promotion_allowed"]
    miss = [k for k in req if k not in data]
    if miss:
        print("INVALID", miss)
        sys.exit(1)
    print(
        f"OK verdict={data['verdict']} exit={data['exit_code']} "
        f"promotion={data['promotion_allowed']}"
    )
    if data.get("residual"):
        print("RESIDUAL:", data["residual"])


def cmd_explain(run_id: str):
    p = ROOT / "runs" / run_id / "receipt.json"
    if not p.exists():
        print("No receipt")
        sys.exit(1)
    print(p.read_text())


def cmd_closure(claim_id: str):
    claim = ROOT / "claims" / f"{claim_id}.yaml"
    report = {"claim_id": claim_id, "parts": {}}
    report["parts"]["claim_yaml"] = "RESOLVED" if claim.exists() else "MISSING"
    engine = None
    if claim.exists():
        for line in claim.read_text().splitlines():
            if line.startswith("engine:"):
                engine = line.split(":", 1)[1].strip()
    eng_path = ROOT / engine if engine else None
    report["parts"]["engine"] = (
        "RESOLVED" if eng_path and eng_path.exists() else "MISSING"
    )
    matched = []
    for r in (ROOT / "RECEIPTS").glob("AQ-RPL-*.json"):
        try:
            d = json.loads(r.read_text())
            if d.get("claim_id") == claim_id:
                matched.append(r.name)
        except Exception:
            pass
    report["parts"]["receipt"] = (
        f"RESOLVED ({len(matched)})" if matched else "MISSING"
    )
    report["parts"]["lean"] = "OPEN"
    report["parts"]["promotion"] = "BLOCKED"
    closed = all(
        str(v).startswith("RESOLVED")
        for k, v in report["parts"].items()
        if k not in ("lean", "promotion")
    )
    report["object_status"] = "REPLAY_CLOSED" if closed else "INCOMPLETE"
    print(json.dumps(report, indent=2))


def cmd_diff(run_a: str, run_b: str):
    def load(rid):
        p = ROOT / "runs" / rid / "receipt.json"
        if not p.exists():
            print(f"Missing receipt: {rid}")
            sys.exit(1)
        return json.loads(p.read_text())

    a, b = load(run_a), load(run_b)
    keys = [
        "source_sha256",
        "stdout_sha256",
        "stderr_sha256",
        "exit_code",
        "verdict",
        "claim_id",
    ]
    print(f"DIFF {run_a} vs {run_b}")
    for k in keys:
        va, vb = a.get(k), b.get(k)
        mark = "SAME" if va == vb else "CHANGED"
        print(f"  {k}: {mark}")
        if va != vb:
            print(f"    A: {va}")
            print(f"    B: {vb}")
    ra, rb = a.get("residual"), b.get("residual")
    if ra or rb:
        print("  residual:")
        print(f"    A: {ra}")
        print(f"    B: {rb}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    c = sys.argv[1]
    if c == "init":
        cmd_init()
    elif c == "capture":
        cmd_capture(sys.argv[2:])
    elif c == "verify" and len(sys.argv) > 2:
        cmd_verify(sys.argv[2])
    elif c == "explain" and len(sys.argv) > 2:
        cmd_explain(sys.argv[2])
    elif c == "closure" and len(sys.argv) > 2:
        cmd_closure(sys.argv[2])
    elif c == "diff" and len(sys.argv) > 3:
        cmd_diff(sys.argv[2], sys.argv[3])
  
... 
