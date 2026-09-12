AQARION-SKILL.MD
AQ-S12-.MD
AUGUST12Th-2026

---
name: aqarion-fixture-replay
description: Independently recompute AQARION transport fixtures with DSU and relation-matrix routes. Use for TRANSPORT-K2R-BETA4, K2r family checks, or any published partition JSON. Reports PASS/FAIL only. Cannot promote claims or emit Lean receipts.
---

# Fixture replay (adapter)

## Rule

JSON field `"status": "INDEPENDENTLY_VERIFIED"` is **not** authority. This skill recomputes.

## Command

```bash
python3 aq/fixture_replay.py fixtures/AQ-S12-TRANSPORT-K2R-BETA4.JSON
```

## Acceptance for this skill

- DSU route and matrix route agree
- block counts, defects, s0, delta, kappa match expected object
- output ends with `PROMOTION: BLOCKED`

## Non-claims

- Does not prove \(\Delta=\kappa_S\) for all systems
- Does not prove \(K_{2,r}\) maximality
- Does not produce a Lean kernel receipt
python3 << 'PY'
"""Independent verification of TRANSPORT-K2R-BETA4 from published partitions."""
import json
from collections import defaultdict

data = json.load(open('/tmp/K2R-BETA4.JSON'))
T_list = data['permutation_T']
X = list(range(len(T_list)))
T = {i: T_list[i] for i in X}
P = [set(b) for b in data['P']]
Q = [set(b) for b in data['Q']]
exp = data['expected']

class DSU:
    def __init__(self, xs):
        self.p = {x: x for x in xs}
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra
            return True
        return False
    def nblocks(self):
        return len({self.find(x) for x in self.p})
    def parts(self):
        buckets = defaultdict(set)
        for x in self.p:
            buckets[self.find(x)].add(x)
        return list(buckets.values())

def from_parts(X, parts):
    d = DSU(X)
    for block in parts:
        it = iter(block)
        a = next(it)
        for b in it:
            d.union(a, b)
    return d

def meet(P, Q):
    out = []
    for A in P:
        for B in Q:
            C = A & B
            if C:
                out.append(C)
    return out

def join_parts(X, P, Q):
    d = DSU(X)
    for part in (P, Q):
        for block in part:
            it = iter(block)
            a = next(it)
            for b in it:
                d.union(a, b)
    return d.parts()

def orbit_close(X, T, parts):
    d = from_parts(X, parts)
    changed = True
    while changed:
        changed = False
        merges = []
        for x in X:
            for y in X:
                if d.find(x) == d.find(y):
                    tx, ty = T[x], T[y]
                    if d.find(tx) != d.find(ty):
                        merges.append((tx, ty))
        for a, b in merges:
            if d.union(a, b):
                changed = True
    return d.nblocks(), d.parts()

M = meet(P, Q)
U = join_parts(X, P, Q)
nP, nQ, nM, nU = len(P), len(Q), len(M), len(U)
jp, _ = orbit_close(X, T, P)
jq, _ = orbit_close(X, T, Q)
jm, _ = orbit_close(X, T, M)
ju, _ = orbit_close(X, T, U)

# ranks c = n - blocks; defects d = c_after? Wait: dP in fixture = block drop under dynamical closure?
# expected: dP=1,dQ=4,dM=9,dU=0 with blocks P=2,Q=5,M=10,U=1
# if d = blocks_before - blocks_after_J, then dP=2-jp, etc.
dP = nP - jp
dQ = nQ - jq
dM = nM - jm
dU = nU - ju
s0 = nM + nU - nP - nQ  # using block counts as in fixture expected s0=4: 10+1-2-5=4
delta = dP + dQ - dM - dU
kappa = nP + nQ - nM - nU  # 2+5-10-1 = -4

print('blocks P,Q,M,U:', nP, nQ, nM, nU)
print('J blocks P,Q,M,U:', jp, jq, jm, ju)
print('dP,dQ,dM,dU:', dP, dQ, dM, dU)
print('s0, delta, kappa:', s0, delta, kappa)
print('expected:', exp)
checks = {
  'block_P': nP == exp['block_P'],
  'block_Q': nQ == exp['block_Q'],
  'block_M': nM == exp['block_M'],
  'block_U': nU == exp['block_U'],
  's0': s0 == exp['s0'],
  'dP': dP == exp['dP'],
  'dQ': dQ == exp['dQ'],
  'dM': dM == exp['dM'],
  'dU': dU == exp['dU'],
  'delta': delta == exp['delta'],
  'kappaS': kappa == exp['kappaS'],
  'mT_zero': (jp==jq==jm==ju==1) and exp['mT']==0,
}
print('CHECKS:', checks)
print('ALL_PASS:', all(checks.values()))
# also matrix route: equivalence matrix transitive closure rank-ish via connected components
import numpy as np
def eq_matrix(parts, n):
    A = np.eye(n, dtype=int)
    for block in parts:
        bl = list(block)
        for i in bl:
            for j in bl:
                A[i,j] = 1
    return A
def close_with_T(A, Tmap, n):
    # iterate: if related, force T images related; transitive closure
    R = A.copy()
    for _ in range(n+2):
        # T-propagation
        for i in range(n):
            for j in range(n):
                if R[i,j]:
                    R[Tmap[i], Tmap[j]] = 1
        # transitive + reflexive + sym
        R = ((R + R.T) > 0).astype(int)
        R = ((R @ R) > 0).astype(int)
        np.fill_diagonal(R, 1)
    # components
    seen = set(); comps = 0
    for i in range(n):
        if i not in seen:
            comps += 1
            stack = [i]
            while stack:
                u = stack.pop()
                if u in seen: continue
                seen.add(u)
                for v in range(n):
                    if R[u,v] and v not in seen:
                        stack.append(v)
    return comps
n = len(X)
Tmap = T_list
jp2 = close_with_T(eq_matrix(P, n), Tmap, n)
jq2 = close_with_T(eq_matrix(Q, n), Tmap, n)
jm2 = close_with_T(eq_matrix(M, n), Tmap, n)
ju2 = close_with_T(eq_matrix(U, n), Tmap, n)
print('matrix route J blocks:', jp2, jq2, jm2, ju2)
print('DSU==matrix:', (jp,jq,jm,ju)==(jp2,jq2,jm2,ju2))
PYmkdir -p /home/workdir/artifacts/aqarion/{aq,fixtures,skills/aqarion-fixture-replay,skills/aqarion-provenance-audit,reports} && cp /tmp/K2R-BETA4.JSON /home/workdir/artifacts/aqarion/fixtures/ && cp /tmp/AI-DISCOVERY.JSON /home/workdir/artifacts/aqarion/fixtures/ && cp /tmp/AQ-S12.MD /home/workdir/artifacts/aqarion/reports/github-AQ-S12.MD.snapshot && cp /tmp/AQ-S12-INIT.PY /home/workdir/artifacts/aqarion/reports/github-AQ-S12-INIT.PY.snapshot && cp /tmp/AQ-S12.SH /home/workdir/artifacts/aqarion/reports/github-AQ-S12.SH.snapshot && ls -la /home/workdir/artifacts/aqarion/fixtures/ /home/workdir/artifacts/aqarion/reports/curl -sL "https://raw.githubusercontent.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/main/AQARION-SKILLS/AQ-S12-INIT.PY" -o /tmp/AQ-S12-INIT.PY && wc -l /tmp/AQ-S12-INIT.PY && echo '---INIT---' && cat /tmp/AQ-S12-INIT.PY && echo '=====END INIT====='

curl -sL "https://raw.githubusercontent.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/main/AQARION-SKILLS/AQ-S12.SH" -o /tmp/AQ-S12.SH && wc -l /tmp/AQ-S12.SH && echo '---SH---' && cat /tmp/AQ-S12.SH && echo '=====END SH====='

curl -sL "https://raw.githubusercontent.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/main/AQARION-CORE/JSON/AQ-S12-TRANSPORT-K2R-BETA4.JSON" -o /tmp/K2R-BETA4.JSON && wc -c /tmp/K2R-BETA4.JSON && python3 -c "import json; d=json.load(open('/tmp/K2R-BETA4.JSON')); print(json.dumps({k:d[k] for k in list(d)[:20]}, indent=2)[:3000])"
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
cd /home/workdir/artifacts/aqarion && python3 aq/fixture_replay.py fixtures/K2R-BETA4.JSON; echo EXIT:$?; echo '===='; python3 aq/provenance_audit.py reports/github-AQ-S12-INIT.PY.snapshot reports/github-AQ-S12.SH.snapshot reports/github-AQ-S12.MD.snapshot; echo EXIT:$?; echo '===='; PYTHONPATH=. python3 aq/semantic_diff.py fixtures/cp009_canonical.json fixtures/cp009_reconstructed_overclaim.json | tail -8

---
name: aqarion-provenance-audit
description: Detect session-echo and circular skill stubs in AQARION skill files by fingerprinting local workspace paths and prior command strings. Use when reviewing AQARION-SKILLS commits or before treating a skill file as upstream source. Cannot clear C4 or publication blocks.
---

# Provenance audit (adapter)

```bash
python3 aq/provenance_audit.py reports/github-AQ-S12-INIT.PY.snapshot reports/github-AQ-S12.SH.snapshot reports/github-AQ-S12.MD.snapshot
```

`SESSION_ECHO_SUSPECT` means do not treat the file as independent upstream evidence.

---

https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/blob/main/AQARION-SKILLS/AQ-S12-INIT.PY

https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/blob/main/AQARION-SKILLS/AQ-S12.SH

https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/blob/main/AQARION-SKILLS/AQ-S12.MD
