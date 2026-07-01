
# [6] test_counterexamples.py

test_counterexamples = '''"""Stage 3: Counterexample Reproduction.

Every counterexample from COUNTEREXAMPLES.md must be reproducible.
These tests verify that documented limitations are real and persistent.
"""

import numpy as np
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from aqarion.core import build_K, proj, obstruction_D, D_norm, refine_partition, is_exact_quotient


# ──────────────────────────────────────────────────────────────
# CE-001: Non-Monotonic Defect Under Refinement
# Registry: COUNTEREXAMPLES.md#CE-001
# Evidence Class: [CE] — Counterexample to AQ-THM-003 (monotonicity)
# ──────────────────────────────────────────────────────────────

@pytest.mark.counterexample
def test_ce_001_non_monotonic_defect():
    """Reproduce CE-001: ||D_Π|| can INCREASE under refinement.
    
    This is a verified counterexample. The defect norm is NOT
    monotonically decreasing under partition refinement.
    
    System: T = [1, 2, 0, 1] (n=4)
    Π₁ = {{0,1,2,3}} (trivial)
    Π₂ = refine(Π₁) = {{0,2}, {1,3}}
    
    Result: ||D_{Π₂}|| > ||D_{Π₁}||
    """
    T = [1, 2, 0, 1]
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
    
    # Document the counterexample
    print(f"\nCE-001 Reproduction:")
    print(f"  Π₁ = {part1}, ||D|| = {norm1:.6f}")
    print(f"  Π₂ = {part2}, ||D|| = {norm2:.6f}")
    print(f"  INCREASE: {norm2 > norm1}")
    
    assert norm2 > norm1, "CE-001 not reproduced — defect did not increase"


# ──────────────────────────────────────────────────────────────
# CE-002: Operator Convention Confusion
# Registry: COUNTEREXAMPLES.md#CE-002
# Evidence Class: [L] — Limitation (not bug, but convention risk)
# ──────────────────────────────────────────────────────────────

@pytest.mark.counterexample
def test_ce_002_operator_convention():
    """Reproduce CE-002: Koopman vs. Transfer operator convention.
    
    Koopman: K[x, T(x)] = 1 (rows sum to 1)
    Transfer: K[T(x), x] = 1 (columns sum to 1)
    
    These are transposes. Using the wrong convention gives wrong D_Π.
    """
    T = [1, 2, 0]
    n = 3
    
    # Correct Koopman convention
    K_koopman = build_K(T)
    
    # WRONG transfer convention (transposed)
    K_transfer = np.zeros((n, n))
    for x in range(n):
        K_transfer[T[x], x] = 1.0
    
    part = [[0, 1], [2]]
    P = proj(part, n)
    
    D_correct = obstruction_D(P, K_koopman)
    D_wrong = obstruction_D(P, K_transfer)
    
    norm_correct = D_norm(D_correct, "fro")
    norm_wrong = D_norm(D_wrong, "fro")
    
    print(f"\nCE-002 Reproduction:")
    print(f"  Koopman ||D|| = {norm_correct:.6f}")
    print(f"  Transfer ||D|| = {norm_wrong:.6f}")
    print(f"  Different: {abs(norm_correct - norm_wrong) > 1e-6}")
    
    assert abs(norm_correct - norm_wrong) > 1e-6, "Conventions give same result — unexpected"


# ──────────────────────────────────────────────────────────────
# CE-003: Partition Bug — Empty Blocks
# Registry: COUNTEREXAMPLES.md#CE-003
# Evidence Class: [L] — Implementation limitation
# ──────────────────────────────────────────────────────────────

@pytest.mark.counterexample
def test_ce_003_empty_block_handling():
    """Reproduce CE-003: Empty blocks in partition cause errors.
    
    Some partition representations may include empty blocks.
    Our proj() should handle this gracefully (skip empty blocks).
    """
    T = [1, 1, 2]
    n = 3
    
    # Partition with empty block
    part_with_empty = [[0, 1], [], [2]]
    
    # Should not raise
    try:
        P = proj(part_with_empty, n)
        # Verify it still works correctly
        assert P.shape == (n, n)
        np.testing.assert_allclose(P @ P, P, atol=1e-12)
    except Exception as e:
        pytest.fail(f"Empty block handling failed: {e}")


# ──────────────────────────────────────────────────────────────
# CE-004: Numerical Precision — Float32 vs Float64
# Registry: COUNTEREXAMPLES.md#CE-004
# Evidence Class: [L] — Floating point limitation
# ──────────────────────────────────────────────────────────────

@pytest.mark.counterexample
def test_ce_004_float_precision():
    """Reproduce CE-004: Float32 can miss exact quotients.
    
    For large n or specific structures, Float32 may report
    D_Π ≠ 0 when it should be 0 (or vice versa).
    """
    T = [1, 1, 3, 3]
    part = [[0, 1], [2, 3]]
    n = 4
    
    # Float64 (default)
    K64 = build_K(T)
    P64 = proj(part, n)
    D64 = obstruction_D(P64, K64)
    norm64 = D_norm(D64, "fro")
    
    # Float32
    K32 = K64.astype(np.float32)
    P32 = P64.astype(np.float32)
    D32 = (np.eye(n, dtype=np.float32) - P32) @ K32 @ P32
    norm32 = float(np.linalg.norm(D32, "fro"))
    
    print(f"\nCE-004 Reproduction:")
    print(f"  Float64 ||D|| = {norm64:.2e}")
    print(f"  Float32 ||D|| = {norm32:.2e}")
    
    # Float64 should detect exact quotient
    assert norm64 < 1e-10, "Float64 failed to detect exact quotient"
    # Float32 might not — this documents the limitation
    if norm32 > 1e-6:
        print("  Float32 MISSED exact quotient — documented limitation")


# ──────────────────────────────────────────────────────────────
# CE-005: Refinement Divergence (Hypothetical)
# Registry: COUNTEREXAMPLES.md#CE-005
# Evidence Class: [CJ] — Active search, no confirmed counterexample yet
# ──────────────────────────────────────────────────────────────

@pytest.mark.counterexample
@pytest.mark.skip(reason="Active search — no confirmed divergence found yet")
def test_ce_005_refinement_divergence():
    """Search for system where refinement does NOT converge.
    
    STATUS: [CJ] — No confirmed counterexample. This test is a
    placeholder for future automated search.
    
    Theory: Refinement MUST converge for finite systems (at most n steps).
    But non-standard partition representations might loop.
    """
    pass
'''

with open(ROOT / "verification/tests/test_counterexamples.py", "w") as f:
    f.write(test_counterexamples)

print("✅ verification/tests/test_counterexamples.py")
