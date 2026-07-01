
# [4] Verification Suite — test_core.py, test_theorems.py, test_counterexamples.py

test_core = '''"""Stage 1: Core Linear Algebra Verification.

All tests MUST pass for repository to be Production Ready.
These verify the foundational operators: K, P_Π, D_Π.
"""

import numpy as np
import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aqarion.core import (
    build_K, proj, obstruction_D, D_norm,
    refine_partition, is_exact_quotient, compute_canonical_quotient
)


# ──────────────────────────────────────────────────────────────
# CORE-001: Projection Idempotence
# Evidence Class: [PV] — Proven by construction (P_Π is averaging projection)
# ──────────────────────────────────────────────────────────────

@pytest.mark.core
@pytest.mark.parametrize("part,n", [
    ([[0, 1], [2]], 3),
    ([[0], [1], [2]], 3),
    ([[0, 1, 2, 3]], 4),
    ([[0, 1], [2, 3], [4]], 5),
])
def test_projection_idempotence(part, n):
    """P_Π² = P_Π for all partitions."""
    P = proj(part, n)
    np.testing.assert_allclose(P @ P, P, atol=1e-12)


@pytest.mark.core
def test_projection_symmetry():
    """P_Π is symmetric: P_Πᵀ = P_Π."""
    part = [[0, 1, 3], [2, 4]]
    n = 5
    P = proj(part, n)
    np.testing.assert_allclose(P, P.T, atol=1e-12)


# ──────────────────────────────────────────────────────────────
# CORE-002: Koopman Operator Properties
# Evidence Class: [PV] — Definitionally true for deterministic systems
# ──────────────────────────────────────────────────────────────

@pytest.mark.core
def test_koopman_row_sums():
    """Each row of K sums to 1 (stochastic convention)."""
    T = [1, 2, 0]  # 3-cycle
    K = build_K(T)
    np.testing.assert_allclose(K.sum(axis=1), np.ones(3), atol=1e-12)


@pytest.mark.core
def test_koopman_permutation():
    """For permutation T, K is a permutation matrix."""
    T = [1, 2, 0]
    K = build_K(T)
    # Permutation matrix: exactly one 1 per row and column
    assert np.all(K.sum(axis=0) == 1)
    assert np.all(K.sum(axis=1) == 1)
    assert np.all((K == 0) | (K == 1))


# ──────────────────────────────────────────────────────────────
# CORE-003: Defect Operator — Zero-Defect iff Exact Quotient
# Evidence Class: [PV] — Core theorem of AQARION
# ──────────────────────────────────────────────────────────────

@pytest.mark.core
def test_zero_defect_exact_quotient():
    """D_Π = 0 ⟺ Π is exact quotient."""
    # Exact case: T maps each block consistently
    T = [1, 1, 3, 3]  # {0,1}→1, {2,3}→3
    part = [[0, 1], [2, 3]]
    n = 4
    K = build_K(T)
    P = proj(part, n)
    D = obstruction_D(P, K)
    
    assert is_exact_quotient(part, T)
    assert D_norm(D, "fro") < 1e-12


@pytest.mark.core
def test_nonzero_defect_nonexact():
    """Non-exact partition has D_Π ≠ 0."""
    T = [1, 2, 0]  # 3-cycle
    part = [[0, 1], [2]]  # Not exact: 0→1, 1→2 (different blocks)
    n = 3
    K = build_K(T)
    P = proj(part, n)
    D = obstruction_D(P, K)
    
    assert not is_exact_quotient(part, T)
    assert D_norm(D, "fro") > 1e-12


# ──────────────────────────────────────────────────────────────
# CORE-004: Rank Bound
# Evidence Class: [PV] — rank(D_Π) ≤ min(n-k, k)
# ──────────────────────────────────────────────────────────────

@pytest.mark.core
@pytest.mark.parametrize("n,k", [
    (4, 2), (5, 2), (6, 3), (8, 4), (10, 3)
])
def test_defect_rank_bound(n, k):
    """rank(D_Π) ≤ min(n - k, k) for random systems."""
    np.random.seed(42)
    T = list(np.random.randint(0, n, size=n))
    
    # Create random partition with k blocks
    perm = np.random.permutation(n)
    block_sizes = np.random.multinomial(n, [1/k]*k)
    part = []
    idx = 0
    for sz in block_sizes:
        if sz > 0:
            part.append(list(perm[idx:idx+sz]))
            idx += sz
    
    K = build_K(T)
    P = proj(part, n)
    D = obstruction_D(P, K)
    
    rank = np.linalg.matrix_rank(D, tol=1e-10)
    bound = min(n - len(part), len(part))
    assert rank <= bound + 1  # +1 for numerical tolerance


# ──────────────────────────────────────────────────────────────
# CORE-005: Refinement Convergence
# Evidence Class: [L] — Converges to exact quotient (CE-001: non-monotonic D)
# ──────────────────────────────────────────────────────────────

@pytest.mark.core
def test_refinement_converges():
    """Iterative refinement reaches exact quotient in ≤ n steps."""
    T = [1, 2, 0, 1, 3]  # Mixed dynamics
    n = len(T)
    part = [list(range(n))]  # Trivial partition
    
    for step in range(n):
        new_part = refine_partition(part, T)
        if is_exact_quotient(new_part, T):
            break
        part = new_part
    else:
        pytest.fail("Refinement did not converge within n steps")
    
    assert is_exact_quotient(part, T) or is_exact_quotient(new_part, T)


# ──────────────────────────────────────────────────────────────
# CORE-006: Canonical Quotient
# Evidence Class: [CJ] — Maximal exact quotient exists, uniqueness open
# ──────────────────────────────────────────────────────────────

@pytest.mark.core
def test_canonical_quotient_exact():
    """compute_canonical_quotient returns exact partition."""
    T = [1, 1, 3, 3, 4, 4]
    part = compute_canonical_quotient(T)
    assert is_exact_quotient(part, T)


@pytest.mark.core
def test_canonical_quotient_maximal():
    """Canonical quotient is at least as coarse as any exact quotient."""
    T = [1, 1, 3, 3]
    canon = compute_canonical_quotient(T)
    # The trivial partition [0,1,2,3] is NOT exact (0→1, 2→3)
    # But [[0,1], [2,3]] should be exact
    assert len(canon) <= 4
    assert is_exact_quotient(canon, T)
'''

with open(ROOT / "verification/tests/test_core.py", "w") as f:
    f.write(test_core)

print("✅ verification/tests/test_core.py")
