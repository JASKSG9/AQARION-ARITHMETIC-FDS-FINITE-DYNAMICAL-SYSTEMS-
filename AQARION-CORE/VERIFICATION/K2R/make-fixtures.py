#!/usr/bin/env python3

"""
AQ-K2R-CLOSURE-STAB

Independent fixture generator.

This generator deliberately does NOT import AQARION project code.
It reconstructs the mathematical family from the public specification.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FIXTURE_DIR = ROOT / "fixtures"

R_VALUES = (2, 3, 5, 6, 10, 15)


def canonical_partition(blocks):
    blocks = [tuple(sorted(block)) for block in blocks]
    return tuple(sorted(blocks, key=lambda b: (b[0], len(b), b)))


def partition_meet(P, Q):
    out = []

    for a in P:
        A = set(a)

        for b in Q:
            B = set(b)
            C = A & B

            if C:
                out.append(C)

    return canonical_partition(out)


def partition_join(P, Q):
    elements = sorted(
        set(x for block in P + Q for x in block)
    )

    parent = {x: x for x in elements}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        a = find(a)
        b = find(b)

        if a != b:
            parent[b] = a

    for partition in (P, Q):
        for block in partition:
            if len(block) > 1:
                root = block[0]

                for x in block[1:]:
                    union(root, x)

    groups = {}

    for x in elements:
        groups.setdefault(find(x), []).append(x)

    return canonical_partition(groups.values())


def apply_T(P, T):
    return canonical_partition(
        [[T[x] for x in block] for block in P]
    )


def closure(P, T):
    """
    Returns:

        tau,
        history

    where tau is the number of strict recurrence steps and
    history contains R_0 through the first stabilized state.
    """

    R = canonical_partition(P)
    history = [R]
    tau = 0

    while True:
        R_next = partition_join(R, apply_T(R, T))

        if R_next == R:
            return tau, history

        R = R_next
        tau += 1
        history.append(R)


def orbit_join(P, T, orbit_term_count):
    """
    Exact orbit-term truncation.

    orbit_term_count = 3 means:

        P ∨ T(P) ∨ T²(P)

    It does NOT mean three recurrence iterations.
    """

    if orbit_term_count < 1:
        raise ValueError("orbit_term_count must be >= 1")

    result = canonical_partition(P)
    current = canonical_partition(P)

    for _ in range(1, orbit_term_count):
        current = apply_T(current, T)
        result = partition_join(result, current)

    return result


def build_family(r):
    omega = list(range(2 * r + 1))

    T = {
        i: (i + 1) % (2 * r)
        for i in range(2 * r)
    }

    T[2 * r] = 2 * r

    P = canonical_partition(
        [
            range(r),
            range(r, 2 * r + 1),
        ]
    )

    Q = canonical_partition(
        [
            [i, r + 1 + i]
            for i in range(r - 1)
        ]
        +
        [
            [r - 1, r, 2 * r]
        ]
    )

    M = partition_meet(P, Q)

    U = canonical_partition([omega])

    S = list(range(2 * r))

    return omega, T, P, Q, M, U, S


def fixture(r):
    omega, T, P, Q, M, U, S = build_family(r)

    partitions = {
        "P": P,
        "Q": Q,
        "M": M,
        "U": U,
    }

    tau = {}
    h_min = {}

    for name, partition in partitions.items():
        t, _ = closure(partition, T)
        tau[name] = t
        h_min[name] = t + 1

    three_orbit_terms = {}

    for name, partition in partitions.items():
        truncated = orbit_join(partition, T, 3)
        full = closure(partition, T)[1][-1]
        three_orbit_terms[name] = truncated == full

    return {
        "schema_version": "AQ-K2R-CLOSURE-STAB-1.0",
        "fixture_id": f"AQ-K2R-R{r}",
        "status": "RECONSTRUCTED_INDEPENDENT_COMPUTATION",
        "parameter": {
            "r": r
        },
        "universe": {
            "omega": omega,
            "S": S
        },
        "action": {
            "cycle": list(range(2 * r)),
            "fixed": [2 * r]
        },
        "partitions": {
            "P": [list(x) for x in P],
            "Q": [list(x) for x in Q],
            "M": [list(x) for x in M],
            "U": [list(x) for x in U]
        },
        "semantic_contract": {
            "lattice_meet": "block_intersection",
            "lattice_join": "transitive_closure",
            "closure": "R[k+1] = R[k] join T(R[k])",
            "orbit_terms": "R[k] = join(T^i(R), i=0..k)",
            "truncation": "forbidden"
        },
        "expected": {
            "incidence_graph": "K_{2,r}",
            "V": r + 2,
            "E": 2 * r,
            "components": 1,
            "beta": r - 1,
            "qS": {
                "P": 2,
                "Q": r,
                "M": 2 * r,
                "U": 1
            },
            "kappa_S": -(r - 1),
            "kappa_SJ": 0,
            "m_T": 0,
            "Delta": -(r - 1),
            "s0": r - 1,
            "sT": 0,
            "tau": tau,
            "h_min": h_min,
            "three_orbit_terms": three_orbit_terms
        }
    }


def canonical_bytes(obj):
    """
    For this schema, all values are JSON-compatible integers,
    strings, booleans, arrays and objects, with no floating-point
    values requiring special JCS handling.

    Production verification should still use an actual RFC 8785
    implementation rather than relying on this equivalence.
    """

    return json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":")
    ).encode("utf-8")


def sha256(obj):
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def main():
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)

    manifest = {
        "schema_version": "AQ-K2R-CLOSURE-STAB-1.0",
        "canonicalization": "RFC8785-JCS",
        "hash": "SHA-256",
        "fixtures": {},
        "verifier": "verify.py"
    }

    for r in R_VALUES:
        obj = fixture(r)

        path = FIXTURE_DIR / f"AQ-K2R-R{r}.json"

        path.write_text(
            json.dumps(
                obj,
                ensure_ascii=False,
                indent=2
            )
            + "\n",
            encoding="utf-8"
        )

        digest = sha256(obj)

        manifest["fixtures"][path.name] = digest

        print(path.name, digest)

    manifest_path = ROOT / "canonical-hashes.json"

    manifest_path.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2
        )
        + "\n",
        encoding="utf-8"
    )


if __name__ == "__main__":
    main()


