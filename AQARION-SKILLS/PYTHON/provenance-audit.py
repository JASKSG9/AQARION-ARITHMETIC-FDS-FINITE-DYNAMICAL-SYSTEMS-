#!/usr/bin/env python3
"""aq provenance-audit — detect session-echo / circular skill stubs.

Flags files whose content is too small, contains local workspace paths,
or matches known session-command fingerprints. Does not modify the remote repo.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

FINGERPRINTS = [
    r"/home/workdir/artifacts",
    r"from \.core import SemanticDiff",
    r"python3 aq/semantic_diff\.py",
    r"PYTHONPATH=\. python3 aq/",
    r"mkdir -p /home/workdir",
]


def audit(path: Path) -> dict:
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    hits = [fp for fp in FINGERPRINTS if re.search(fp, text)]
    return {
        "path": str(path),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "lines": text.count("\n") + (0 if text.endswith("\n") or not text else 1),
        "fingerprint_hits": hits,
        "verdict": "SESSION_ECHO_SUSPECT" if hits or len(raw) < 40 else "NO_LOCAL_FINGERPRINT",
        "promotion": "BLOCKED",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("files", nargs="+")
    args = p.parse_args()
    any_suspect = False
    for f in args.files:
        rep = audit(Path(f))
        print("AQARION PROVENANCE AUDIT")
        for k, v in rep.items():
            print(f"  {k}: {v}")
        print()
        if rep["verdict"] != "NO_LOCAL_FINGERPRINT":
            any_suspect = True
    return 1 if any_suspect else 0


if __name__ == "__main__":
    raise SystemExit(main())
