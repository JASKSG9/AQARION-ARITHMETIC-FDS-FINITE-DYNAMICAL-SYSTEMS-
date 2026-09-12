#!/usr/bin/env python3
"""aq fixture-replay — independent DSU + matrix check of a published transport fixture.

Governance: reports MATCH/DIVERGE only. Never promotes status.
Hash of fixture file is recorded; status field inside JSON is ignored for promotion.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path


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
    return d.nblocks()


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
    return d.nblocks()


def matrix_close(parts, T_list, n):
    R = [[0] * n for _ in range(n)]
    for i in range(n):
        R[i][i] = 1
    for block in parts:
        bl = list(block)
        for i in bl:
            for j in bl:
                R[i][j] = 1
    for _ in range(n + 2):
        for i in range(n):
            for j in range(n):
                if R[i][j]:
                    R[T_list[i]][T_list[j]] = 1
        # symmetrize
        for i in range(n):
            for j in range(n):
                if R[i][j]:
                    R[j][i] = 1
        # transitive step
        N = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if R[i][j]:
                    for k in range(n):
                        if R[j][k]:
                            N[i][k] = 1
        for i in range(n):
            N[i][i] = 1
            for j in range(n):
                if N[i][j]:
                    R[i][j] = 1
    seen = set()
    comps = 0
    for i in range(n):
        if i not in seen:
            comps += 1
            stack = [i]
            while stack:
                u = stack.pop()
                if u in seen:
                    continue
                seen.add(u)
                for v in range(n):
                    if R[u][v] and v not in seen:
                        stack.append(v)
    return comps


def replay(path: Path) -> dict:
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)
    T_list = data["permutation_T"]
    n = len(T_list)
    X = list(range(n))
    T = {i: T_list[i] for i in X}
    P = [set(b) for b in data["P"]]
    Q = [set(b) for b in data["Q"]]
    exp = data["expected"]

    M = meet(P, Q)
    nP, nQ, nM, nU = len(P), len(Q), len(M), join_parts(X, P, Q)
    jp = orbit_close(X, T, P)
    jq = orbit_close(X, T, Q)
    jm = orbit_close(X, T, M)
    ju = orbit_close(X, T, [set(X)])  # join is X in this family; recompute via join_parts value
    # use join block count for ju via dynamical close of U partition as singleton block of all
    U_parts = []
    dU0 = DSU(X)
    for part in (P, Q):
        for block in part:
            it = iter(block)
            a = next(it)
            for b in it:
                dU0.union(a, b)
    # rebuild U parts
    buckets = defaultdict(set)
    for x in X:
        buckets[dU0.find(x)].add(x)
    U_parts = list(buckets.values())
    nU = len(U_parts)
    ju = orbit_close(X, T, U_parts)

    dP, dQ, dM, dU = nP - jp, nQ - jq, nM - jm, nU - ju
    s0 = nM + nU - nP - nQ
    delta = dP + dQ - dM - dU
    kappa = nP + nQ - nM - nU

    jp2 = matrix_close(P, T_list, n)
    jq2 = matrix_close(Q, T_list, n)
    jm2 = matrix_close(M, T_list, n)
    ju2 = matrix_close(U_parts, T_list, n)

    computed = {
        "block_P": nP,
        "block_Q": nQ,
        "block_M": nM,
        "block_U": nU,
        "J_P": jp,
        "J_Q": jq,
        "J_M": jm,
        "J_U": ju,
        "dP": dP,
        "dQ": dQ,
        "dM": dM,
        "dU": dU,
        "s0": s0,
        "delta": delta,
        "kappaS": kappa,
        "mT_all_J_one": jp == jq == jm == ju == 1,
    }
    checks = {
        "block_P": nP == exp["block_P"],
        "block_Q": nQ == exp["block_Q"],
        "block_M": nM == exp["block_M"],
        "block_U": nU == exp["block_U"],
        "s0": s0 == exp["s0"],
        "dP": dP == exp["dP"],
        "dQ": dQ == exp["dQ"],
        "dM": dM == exp["dM"],
        "dU": dU == exp["dU"],
        "delta": delta == exp["delta"],
        "kappaS": kappa == exp["kappaS"],
        "mT": (jp == jq == jm == ju == 1) and exp.get("mT", 0) == 0,
        "DSU_eq_matrix": (jp, jq, jm, ju) == (jp2, jq2, jm2, ju2),
    }
    return {
        "fixture_id": data.get("fixture_id"),
        "fixture_sha256": digest,
        "json_status_field": data.get("status"),
        "computed": computed,
        "checks": checks,
        "all_pass": all(checks.values()),
        "promotion": "BLOCKED",
        "note": "Replay MATCH is computational agreement, not a Lean receipt and not a promotion.",
    }


def render(rep: dict) -> str:
    lines = [
        "AQARION FIXTURE REPLAY",
        f"FIXTURE: {rep['fixture_id']}",
        f"SHA256:  {rep['fixture_sha256']}",
        f"JSON status field (ignored for promotion): {rep['json_status_field']}",
        "─" * 40,
        "COMPUTED:",
    ]
    for k, v in rep["computed"].items():
        lines.append(f"  {k:<16} {v}")
    lines.append("CHECKS:")
    for k, v in rep["checks"].items():
        lines.append(f"  {k:<16} {'PASS' if v else 'FAIL'}")
    lines.append("─" * 40)
    lines.append(f"ALL_PASS:  {rep['all_pass']}")
    lines.append(f"PROMOTION: {rep['promotion']}")
    lines.append(rep["note"])
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("fixture_json")
    args = p.parse_args()
    rep = replay(Path(args.fixture_json))
    print(render(rep))
    return 0 if rep["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
