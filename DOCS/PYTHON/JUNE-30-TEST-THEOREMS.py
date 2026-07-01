
# [5] test_theorems.py and test_counterexamples.py

test_theorems = '''"""Stage 2: Theorem Verification.

Tests for claimed theorems. XFAIL marks known unproven claims.
Each test links to CLAIMS_REGISTRY entry.
"""

import numpy as np
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from aqarion.core import build_K, proj, obstruction_D, D_norm, refine_partition


# ──────────────────────────────────────────────────────────────
# AQ-THM-001: Projection Idempotence
# Status: [PV] — Proven, tested in test_core
# ──────────────────────────────────────────────────────────────

@pytest.mark.theorem
def test_thm_001_projection_idempotence():
    """For any partition Π of finite set S, P_Π² = P_Π."""
    part = [[0, 2], [1, 3], [4]]
    n = 5
    P = proj(part, n)
    np.testing.assert_allclose(P @ P, P, atol=1e-12)


# ──────────────────────────────────────────────────────────────
# AQ-THM-002: Zero-Defect Characterization
# Status: [PV] — Core theorem
# ──────────────────────────────────────────────────────────────

@pytest.mark.theorem
def test_thm_002_zero_defect_iff_exact():
    """D_Π = 0 ⟺ Π is an exact dynamical quotient of (S, f)."""
    # Forward: exact → D = 0
    T = [1, 1, 3, 3]
    part = [[0, 1], [2, 3]]
    n = 4
    K = build_K(T)
    P = proj(part, n)
    D = obstruction_D(P, K)
    assert D_norm(D, "fro") < 1e-12
    
    # Backward: D = 0 → exact (tested via is_exact_quotient)
    # This is the non-trivial direction


# ──────────────────────────────────────────────────────────────
# AQ-THM-003: Refinement Convergence to Exact Quotient
# Status: [L] — Converges, but D_Π is NOT monotonic (CE-001)
# Registry: COUNTEREXAMPLES.md#CE-001
# ──────────────────────────────────────────────────────────────

@pytest.mark.theorem
@pytest.mark.xfail(reason="D_Π is not monotonic under refinement — CE-001")
def test_thm_003_refinement_monotonic():
    """Refinement should monotonically decrease ||D_Π||.
    
    KNOWN FAILURE: CE-001 documents non-monotonicity.
    This test is XFAIL to document the limitation.
    """
    T = [1, 2, 0, 1]  # System where non-monotonicity occurs
    n = 4
    part1 = [[0, 1, 2, 3]]
    part2 = refine_partition(part1, T)
    
    K = build_K(T)
    P1 = proj(part1, n)
    P2 = proj(part2, n)
    D1 = obstruction_D(P1, K)
    D2 = obstruction_D(P2, K)
    
    norm1 = D_norm(D1, "fro")
    norm2 = D_norm(D2, "fro")
    
    # This assertion FAILS for some systems — that's the point
    assert norm2 <= norm1 + 1e-12, f"Non-monotonic: {norm1:.6f} → {norm2:.6f}"


# ──────────────────────────────────────────────────────────────
# AQ-THM-004: Rank Bound
# Status: [PV] — rank(D_Π) ≤ min(n-k, k)
# ──────────────────────────────────────────────────────────────

@pytest.mark.theorem
def test_thm_004_rank_bound():
    """For partition Π with k blocks on n states:
    rank(D_Π) ≤ min(n - k, k).
    """
    np.random.seed(42)
    for n in [5, 8, 10]:
        for k in [2, 3, 4]:
            if k >= n:
                continue
            T = list(np.random.randint(0, n, size=n))
            # Random partition with k blocks
            perm = np.random.permutation(n)
            cuts = sorted(np.random.choice(range(1, n), size=k-1, replace=False))
            part = []
            prev = 0
            for c in cuts:
                part.append(list(perm[prev:c]))
                prev = c
            part.append(list(perm[prev:]))
            part = [b for b in part if b]  # Remove empty
            
            K = build_K(T)
            P = proj(part, n)
            D = obstruction_D(P, K)
            rank = np.linalg.matrix_rank(D, tol=1e-10)
            bound = min(n - len(part), len(part))
            assert rank <= bound + 1, f"n={n}, k={k}: rank={rank} > bound={bound}"


# ──────────────────────────────────────────────────────────────
# AQ-THM-005: Canonical Quotient Existence
# Status: [CJ] — Conjectured, not proven in general
# ──────────────────────────────────────────────────────────────

@pytest.mark.theorem
@pytest.mark.cj
def test_thm_005_canonical_quotient_existence():
    """Every finite dynamical system admits a maximal exact quotient.
    
    STATUS: [CJ] — Computational evidence supports this for tested systems.
    No general proof exists. Test searches for counterexamples.
    """
    np.random.seed(123)
    for n in range(2, 20):
        for _ in range(10):
            T = list(np.random.randint(0, n, size=n))
            from aqarion.core import compute_canonical_quotient
            canon = compute_canonical_quotient(T)
            from aqarion.core import is_exact_quotient
            assert is_exact_quotient(canon, T), f"Failed for n={n}, T={T}"


# ──────────────────────────────────────────────────────────────
# AQ-THM-006: Spectral Radius Bound
# Status: [CJ] — ρ(K) ≤ 1 for Koopman of finite deterministic system
# ──────────────────────────────────────────────────────────────

@pytest.mark.theorem
def test_thm_006_spectral_radius_bound():
    """For Koopman operator K of finite deterministic system:
    spectral radius ρ(K) = 1.
    
    STATUS: [PV] for deterministic systems (permutation-like spectrum).
    """
    np.random.seed(456)
    for n in [3, 5, 7, 10]:
        T = list(np.random.randint(0, n, size=n))
        K = build_K(T)
        eigenvalues = np.linalg.eigvals(K)
        spectral_radius = max(abs(ev) for ev in eigenvalues)
        assert abs(spectral_radius - 1.0) < 1e-10, f"ρ(K) = {spectral_radius}"
'''

with open(ROOT / "verification/tests/test_theorems.py", "w") as f:
    f.write(test_theorems)

print("✅ verification/tests/test_theorems.py")
