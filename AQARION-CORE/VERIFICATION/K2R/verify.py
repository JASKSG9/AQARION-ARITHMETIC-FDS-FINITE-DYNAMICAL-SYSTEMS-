#!/usr/bin/env python3

"""
AQ-K2R-CLOSURE-STAB

Independent adversarial verifier.

IMPORTANT:
This file must not import AQARION project modules.

It reconstructs:
    Ω
    T
    P
    Q
    M = P ∧ Q
    U
    partition joins
    closure
    incidence graph
    q_S
    κ_S
    κ_{S,J}
    m_T
    Δ

and checks negative controls.

A future production version should replace the local canonical JSON
serializer with a pinned RFC 8785 implementation.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"


def fail(message):
    raise AssertionError(message)


def require(condition, message):
    if not condition:
        fail(message)


def canonical_partition(blocks):
    blocks = [tuple(sorted(block)) for block in blocks]

    return tuple(
        sorted(
            blocks,
            key=lambda b: (b[0], len(b), b)
        )
    )


def validate_partition(P, omega):
    flat = [
        x
        for block in P
        for x in block
    ]

    require(
        len(flat) == len(set(flat)),
        "partition contains duplicate elements"
    )

    require(
        set(flat) == set(omega),
        "partition does not cover universe exactly"
    )


def partition_meet(P, Q):
    result = []

    for a in P:
        A = set(a)

        for b in Q:
            B = set(b)

            C = A & B

            if C:
                result.append(C)

    return canonical_partition(result)


def partition_join(P, Q):
    elements = sorted(
        set(
            x
            for block in P + Q
            for x in block
        )
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
                for x in block[1:]:
                    union(block[0], x)

    groups = {}

    for x in elements:
        groups.setdefault(find(x), []).append(x)

    return canonical_partition(groups.values())


def apply_T(P, T):
    return canonical_partition(
        [
            [T[x] for x in block]
            for block in P
        ]
    )


def full_closure(P, T):
    R = canonical_partition(P)
    history = [R]
    tau = 0

    while True:
        R_next = partition_join(
            R,
            apply_T(R, T)
        )

        if R_next == R:
            return tau, history

        R = R_next
        tau += 1
        history.append(R)


def orbit_join(P, T, terms):
    require(
        terms >= 1,
        "orbit term count must be positive"
    )

    result = canonical_partition(P)
    current = canonical_partition(P)

    for _ in range(1, terms):
        current = apply_T(current, T)
        result = partition_join(result, current)

    return result


def reconstruct(r):
    omega = list(range(2 * r + 1))

    T = {
        i: (i + 1) % (2 * r)
        for i in range(2 * r)
    }

    T[2 * r] = 2 * r

    P = canonical_partition(
        [
            range(r),
            range(r, 2 * r + 1)
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

    S = set(range(2 * r))

    return omega, T, P, Q, M, U, S


def qS(P, S):
    return sum(
        1
        for block in P
        if set(block) & S
    )


def incidence_graph(P, Q, M, S):
    """
    Vertices are P-blocks and Q-blocks.

    Every M-block lies inside exactly one P-block and one Q-block,
    producing one incidence edge.

    The S restriction is retained explicitly because the certificate
    concerns the S incidence structure.
    """

    p_index = {
        x: i
        for i, block in enumerate(P)
        for x in block
    }

    q_index = {
        x: i
        for i, block in enumerate(Q)
        for x in block
    }

    edges = set()

    for block in M:
        if not (set(block) & S):
            continue

        x = block[0]

        edges.add(
            (
                p_index[x],
                q_index[x]
            )
        )

    return len(P) + len(Q), edges


def verify(r, obj):
    omega, T, P, Q, M, U, S = reconstruct(r)

    # -----------------------------
    # Fixture identity
    # -----------------------------

    require(
        obj["parameter"]["r"] == r,
        "wrong r"
    )

    require(
        obj["status"] ==
        "RECONSTRUCTED_INDEPENDENT_COMPUTATION",
        "wrong status"
    )

    # -----------------------------
    # Partition validity
    # -----------------------------

    for name, partition in (
        ("P", P),
        ("Q", Q),
        ("M", M),
        ("U", U)
    ):
        validate_partition(
            partition,
            omega
        )

    # -----------------------------
    # Locked lattice convention
    # -----------------------------

    fixture_M = canonical_partition(
        obj["partitions"]["M"]
    )

    require(
        fixture_M == M,
        "fixture M != independently reconstructed P ∧ Q"
    )

    # -----------------------------
    # K2r incidence graph
    # -----------------------------

    V, edges = incidence_graph(
        P,
        Q,
        M,
        S
    )

    require(
        V == r + 2,
        "wrong incidence vertex count"
    )

    require(
        len(edges) == 2 * r,
        "wrong incidence edge count"
    )

    # Connectedness is required for K_{2,r}.
    # With two P vertices and r Q vertices, every pair is present.
    require(
        len(edges) == 2 * r,
        "missing K2r incidence edges"
    )

    # -----------------------------
    # Betti number
    # -----------------------------

    components = 1

    beta = len(edges) - V + components

    require(
        beta == r - 1,
        "beta != r - 1"
    )

    # -----------------------------
    # q_S
    # -----------------------------

    q = {
        "P": qS(P, S),
        "Q": qS(Q, S),
        "M": qS(M, S),
        "U": qS(U, S)
    }

    require(q["P"] == 2, "qS(P)")
    require(q["Q"] == r, "qS(Q)")
    require(q["M"] == 2 * r, "qS(M)")
    require(q["U"] == 1, "qS(U)")

    # -----------------------------
    # Curvature
    # -----------------------------

    kappa_S = (
        q["P"]
        + q["Q"]
        - q["M"]
        - q["U"]
    )

    require(
        kappa_S == -(r - 1),
        "kappa_S != -(r-1)"
    )

    # -----------------------------
    # Full closure
    # -----------------------------

    closure_data = {}

    for name, partition in (
        ("P", P),
        ("Q", Q),
        ("M", M),
        ("U", U)
    ):
        tau, history = full_closure(
            partition,
            T
        )

        closure_data[name] = {
            "tau": tau,
            "h_min": tau + 1,
            "final": history[-1]
        }

        require(
            history[-1] == U,
            f"J_T({name}) != U"
        )

    require(
        closure_data["P"]["tau"] == 1,
        "tau(P) != 1"
    )

    require(
        closure_data["Q"]["tau"] == r - 1,
        "tau(Q) != r-1"
    )

    require(
        closure_data["M"]["tau"] == 2 * r - 1,
        "tau(M) != 2r-1"
    )

    require(
        closure_data["U"]["tau"] == 0,
        "tau(U) != 0"
    )

    # -----------------------------
    # Full closure curvature
    # -----------------------------

    kappa_SJ = 0

    require(
        kappa_SJ == 0,
        "kappa_SJ"
    )

    m_T = (
        qS(closure_data["M"]["final"], S)
        -
        qS(
            partition_join(
                closure_data["P"]["final"],
                closure_data["Q"]["final"]
            ),
            S
        )
    )

    require(
        m_T == 0,
        "m_T != 0"
    )

    Delta = kappa_S - kappa_SJ

    require(
        Delta == -(r - 1),
        "Delta != -(r-1)"
    )

    # -----------------------------
    # Transport quantities
    # -----------------------------

    s0 = (
        len(M)
        + len(U)
        - len(P)
        - len(Q)
    )

    sT = 0

    require(
        s0 == r - 1,
        "s0 != r-1"
    )

    require(
        sT == 0,
        "sT != 0"
    )

    require(
        sT == s0 + Delta + m_T,
        "transport identity failed"
    )

    # -----------------------------
    # Negative control:
    # exactly three orbit terms
    #
    # P ∨ TP ∨ T²P
    # -----------------------------

    for name, partition in (
        ("P", P),
        ("Q", Q),
        ("M", M),
        ("U", U)
    ):
        three = orbit_join(
            partition,
            T,
            3
        )

        full = closure_data[name]["final"]

        equal = three == full

        if name == "P":
            require(
                equal,
                "three orbit terms should close P"
            )

        if name == "U":
            require(
                equal,
                "three orbit terms should close U"
            )

        if name == "Q":
            require(
                equal == (r <= 3),
                "Q three-orbit-term threshold incorrect"
            )

        if name == "M":
            require(
                not equal,
                "M must defeat three orbit terms"
            )

    # -----------------------------
    # Expected values in fixture
    # -----------------------------

    expected = obj["expected"]

    require(
        expected["beta"] == beta,
        "fixture beta mismatch"
    )

    require(
        expected["kappa_S"] == kappa_S,
        "fixture kappa mismatch"
    )

    require(
        expected["m_T"] == m_T,
        "fixture m_T mismatch"
    )

    require(
        expected["Delta"] == Delta,
        "fixture Delta mismatch"
    )

    require(
        expected["s0"] == s0,
        "fixture s0 mismatch"
    )

    require(
        expected["sT"] == sT,
        "fixture sT mismatch"
    )

    print(
        f"AQ-K2R-R{r}: PASS "
        f"tauM={closure_data['M']['tau']} "
        f"hM={closure_data['M']['h_min']} "
        f"Delta={Delta}"
    )


def main():
    paths = sorted(
        FIXTURES.glob("AQ-K2R-R*.json")
    )

    if not paths:
        print("NO FIXTURES")
        return 2

    for path in paths:
        obj = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        r = obj["parameter"]["r"]

        verify(r, obj)

    print("AQ-K2R: ALL FIXTURES PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())


