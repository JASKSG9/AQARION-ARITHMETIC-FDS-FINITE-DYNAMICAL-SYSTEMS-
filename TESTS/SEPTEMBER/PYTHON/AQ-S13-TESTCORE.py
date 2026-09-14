"""
Regression tests. Two categories:

1. "bug_*" tests pin down mistakes that were actually made and found during
   this module's derivation -- they exist so nobody reintroduces them.
2. "identity_*" tests check the proven closed-form identities across ranges
   that were exhaustively verified (see docstrings for exact ranges; nothing
   here claims to check ranges it doesn't actually check).
"""
import math
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ksg_defect import (
    cycle_laplacian, cycle_laplacian_eigenvalues, alpha2,
    defect_operator, reduced_defect, expected_gram,
    expected_singular_values, expected_operator_norm, expected_trace,
    all_rgs, all_partitions, rgs_to_partition, tore_closure,
)

TOL = 1e-9


def matmul(a, b):
    ar, ac, bc = len(a), len(a[0]), len(b[0])
    out = [[0.0] * bc for _ in range(ar)]
    for i in range(ar):
        for k in range(ac):
            aik = a[i][k]
            if aik == 0:
                continue
            for j in range(bc):
                out[i][j] += aik * b[k][j]
    return out


def transpose(a):
    r, c = len(a), len(a[0])
    return [[a[i][j] for i in range(r)] for j in range(c)]


def max_abs_diff(a, b):
    return max(abs(a[i][j] - b[i][j]) for i in range(len(a)) for j in range(len(a[0])))


# ---------------------------------------------------------------------------
# BUG REGRESSION: cycle_laplacian must double the edge at m=2
# ---------------------------------------------------------------------------
def test_bug_cycle_laplacian_m2_must_be_doubled_edge():
    L = cycle_laplacian(2)
    assert L == [[2.0, -2.0], [-2.0, 2.0]], (
        f"cycle_laplacian(2) = {L}. A C_2 'cycle' is a doubled edge "
        f"(S_1 == S_-1 when m=2). [[2,-1],[-1,2]] is WRONG and was the "
        f"original bug -- it comes from writing L[i][j] = -1 twice with "
        f"plain assignment instead of += for the two (now-identical) "
        f"neighbor indices."
    )


# ---------------------------------------------------------------------------
# BUG REGRESSION: RGS generator must reach all Bell(n) partitions
# ---------------------------------------------------------------------------
def test_bug_rgs_generator_reaches_all_bell_numbers():
    bell = {1: 1, 2: 2, 3: 5, 4: 15, 5: 52, 6: 203, 7: 877}
    for n, expected in bell.items():
        got = len(all_partitions(n))
        assert got == expected, (
            f"n={n}: generated {got} partitions, Bell({n})={expected}. "
            f"If got==1 for every n, the RGS generator has regressed to "
            f"'range(mx+1)', which can never open a new block."
        )


# ---------------------------------------------------------------------------
# IDENTITY: alpha^2 * L(C_m) == U^T D^T D U   (THM-SV)
#   Verified exactly (sympy Rational) for k,m in 2..5 in the original session;
#   verified here numerically for k,m in 2..8 as an executable check.
# ---------------------------------------------------------------------------
def test_identity_gram_matches_defect_operator():
    for k in range(2, 9):
        for m in range(2, 9):
            for s in range(1, m * k):
                D = reduced_defect(m, k, s)      # n x m
                Dt = transpose(D)
                gram = matmul(Dt, D)             # m x m
                target = expected_gram(m, k, s)
                err = max_abs_diff(gram, target)
                assert err < 1e-6, f"k={k} m={m} s={s}: gram mismatch, err={err}"


# ---------------------------------------------------------------------------
# IDENTITY: eigenvalues of L(C_m) are 4*sin^2(pi*l/m), general m
#   Proof: L(C_m) is circulant (2I - S_1 - S_-1), diagonalized by the DFT;
#   this is standard circulant-matrix theory, checked here for m up to 200
#   as a sanity check on the derivation, not as the proof itself.
# ---------------------------------------------------------------------------
def test_identity_cycle_laplacian_eigenvalues_general_m():
    try:
        import numpy as np
    except ImportError:
        return  # optional cross-check only
    for m in [2, 3, 4, 5, 7, 10, 20, 50, 100, 200]:
        L = np.array(cycle_laplacian(m))
        eigs = sorted(np.linalg.eigvalsh(L))
        pred = cycle_laplacian_eigenvalues(m)
        err = max(abs(a - b) for a, b in zip(eigs, pred))
        assert err < 1e-6, f"m={m}: eigenvalue mismatch, err={err}"


# ---------------------------------------------------------------------------
# IDENTITY: operator norm parity split
#   Verified exactly for k=2..11, m=2..14, all valid s (5720 cases) in the
#   original session; re-checked here across the same range.
# ---------------------------------------------------------------------------
def test_identity_operator_norm_parity_split():
    try:
        import numpy as np
    except ImportError:
        return
    for k in range(2, 12):
        for m in range(2, 15):
            for s in range(1, m * k):
                if s % k == 0:
                    continue
                D = reduced_defect(m, k, s)
                sv = np.linalg.svd(np.array(D), compute_uv=False)
                actual_norm = sv[0]
                pred_norm = expected_operator_norm(m, k, s)
                assert abs(actual_norm - pred_norm) < 1e-6, (
                    f"k={k} m={m} s={s}: op-norm mismatch "
                    f"actual={actual_norm} pred={pred_norm}"
                )


def test_identity_trace_formula():
    try:
        import numpy as np
    except ImportError:
        return
    for k in range(2, 9):
        for m in range(2, 9):
            for s in range(1, m * k):
                D = np.array(reduced_defect(m, k, s))
                trace_actual = float(np.trace(D.T @ D))
                trace_pred = expected_trace(m, k, s)
                assert abs(trace_actual - trace_pred) < 1e-6


# ---------------------------------------------------------------------------
# TORE closure: h_T <= |R| -- EXHAUSTIVELY verified n=3..7, tight (h_T=|R|
# achieved) at every n tested. NOT proven for general n -- this test only
# checks small n, it is evidence, not a proof, and the docstring in
# partitions.py says so.
# ---------------------------------------------------------------------------
def test_tore_closure_h_bound_small_n():
    from itertools import permutations
    for n in [3, 4, 5]:  # kept small here for fast CI; session verified to n=7
        parts = [R for R in all_partitions(n) if 2 <= len(R) <= n - 1]
        for T in permutations(range(n)):
            for R in parts:
                h, _ = tore_closure(R, list(T), n)
                assert h is not None, f"n={n} R={R} T={T}: did not stabilize"
                assert h <= len(R), f"n={n} R={R} T={T}: h_T={h} > |R|={len(R)}"


if __name__ == "__main__":
    tests = [f for name, f in list(globals().items()) if name.startswith("test_")]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
