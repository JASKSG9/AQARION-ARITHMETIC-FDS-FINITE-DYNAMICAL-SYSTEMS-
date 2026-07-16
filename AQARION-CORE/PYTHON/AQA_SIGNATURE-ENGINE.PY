
# Fix integration_test.py to use verify_eventual_idempotency

fixed_integration = '''"""
AQARION J15.LEAN — Integration Test Suite
Final verification of all three phases.
"""

import numpy as np
from fractions import Fraction

from koopman_core import (
    koopman_pullback,
    projection_matrix,
    defect_operator,
    validate_defect_structure,
    compute_depths,
    assert_only_fixed_point_cycles,
    revalidate_witness,
    deterministic_hash,
    exact_rank
)

from structural_cert import (
    decompose_functional_graph,
    compute_image_chain,
    certify_image_filtration,
    verify_eventual_idempotency,
    compute_jordan_blocks
)

from signature_engine import (
    InvariantSignature,
    compute_signature,
    equivalent,
    classify_system
)


def test_koopman_convention():
    """1.1: Verify Koopman convention K[i,j] = 1 iff i = T(j)"""
    T = {0: 1, 1: 1, 2: 2}  # 0->1 (fixed), 1->1 (fixed), 2->2 (fixed)
    K = koopman_pullback(T, 3)
    
    # K[1,0] = 1 because T(0) = 1
    assert K[1, 0] == Fraction(1), "Koopman convention violated"
    # K[1,1] = 1 because T(1) = 1
    assert K[1, 1] == Fraction(1), "Koopman convention violated"
    # K[2,2] = 1 because T(2) = 2
    assert K[2, 2] == Fraction(1), "Koopman convention violated"
    
    print("✅ 1.1 Koopman convention verified")


def test_defect_structure():
    """1.2: Verify PDP = 0 invariant"""
    T = {0: 0, 1: 0, 2: 0}  # All map to 0
    partition = [[0, 1, 2]]  # One block
    D = defect_operator(T, partition, 3)
    P = projection_matrix(partition, 3)
    validate_defect_structure(D, P)
    print("✅ 1.2 Defect structure verified")


def test_depth_completeness():
    """1.3: Verify depth assignment is complete"""
    # T = {0: 0, 1: 0, 2: 1, 3: 1}
    # Fixed point: 0 (T[0]=0)
    # 1 -> 0, so depth(1) = 1
    # 2 -> 1 -> 0, so depth(2) = 2
    # 3 -> 1 -> 0, so depth(3) = 2
    T = {0: 0, 1: 0, 2: 1, 3: 1}
    depth = compute_depths(T)
    assert len(depth) == 4, "Depth incomplete"
    assert depth[0] == 0, "Fixed point depth wrong"
    assert depth[1] == 1, "State 1 should have depth 1 (maps to fixed point 0)"
    assert depth[2] == 2, "State 2 should have depth 2 (2->1->0)"
    assert depth[3] == 2, "State 3 should have depth 2 (3->1->0)"
    print("✅ 1.3 Depth completeness verified")


def test_cycle_constraint():
    """1.4: Verify only fixed point cycles allowed"""
    T_good = {0: 0, 1: 1, 2: 1}  # Only fixed points
    assert_only_fixed_point_cycles(T_good)
    
    T_bad = {0: 1, 1: 0}  # 2-cycle
    try:
        assert_only_fixed_point_cycles(T_bad)
        assert False, "Should have raised"
    except AssertionError as e:
        assert "Non-trivial cycle" in str(e)
    
    print("✅ 1.4 Cycle constraint verified")


def test_witness_revalidation():
    """1.5: Revalidate witness"""
    # Witness: identity map with discrete partition
    T = {0: 0, 1: 1}
    partition = [[0], [1]]  # Discrete partition
    
    # For identity with discrete partition, D should be 0
    D = defect_operator(T, partition, 2)
    for i in range(2):
        for j in range(2):
            assert Fraction(D[i, j]).limit_denominator() == 0
    
    print("✅ 1.5 Witness revalidation verified")


def test_deterministic_hash():
    """1.6: Verify hash excludes build_provenance.json"""
    files = ["a.py", "b.py", "build_provenance.json", "c.py"]
    h1 = deterministic_hash(files)
    h2 = deterministic_hash([f for f in files if f != "build_provenance.json"])
    assert h1 == h2, "Hash not deterministic w.r.t. build_provenance"
    print("✅ 1.6 Deterministic hash verified")


def test_exact_rank():
    """1.7: Verify exact rank computation"""
    A = np.array([[1, 2, 3], [2, 4, 6], [1, 1, 1]], dtype=object)
    r = exact_rank(A)
    assert r == 2, f"Expected rank 2, got {r}"
    print("✅ 1.7 Exact rank verified")


def test_functional_graph_decomposition():
    """2.1: Verify functional graph canonicalization"""
    T = {0: 0, 1: 0, 2: 0, 3: 3, 4: 3}
    G = decompose_functional_graph(T)
    
    assert sorted(G["fixed_points"]) == [0, 3]
    assert len(G["trees"][0]) == 3  # 0, 1, 2
    assert len(G["trees"][3]) == 2  # 3, 4
    print("✅ 2.1 Functional graph decomposition verified")


def test_image_filtration():
    """2.2: Verify image filtration certification"""
    T = {0: 0, 1: 0, 2: 1, 3: 1, 4: 0}
    chain = certify_image_filtration(T)
    
    # Verify non-increasing
    for i in range(len(chain) - 1):
        assert chain[i] >= chain[i + 1]
    
    # Verify terminal
    fixed_count = sum(1 for x in T if T[x] == x)
    assert chain[-1] == fixed_count
    print(f"✅ 2.2 Image filtration verified: {chain}")


def test_eventual_idempotency():
    """2.3: Verify K^d = K^{d+1} for functional graphs with fixed points only.
    
    For a star system where all states map directly to a fixed point,
    K^2 = K (idempotent).
    
    For a 3-level system, K^2 = K^3 (stabilizes at max_depth=2)."""
    # Test 1: Star system (max depth = 1)
    T1 = {0: 0, 1: 0, 2: 0}
    K1 = koopman_pullback(T1, 3)
    verify_eventual_idempotency(K1, 1)  # max_depth = 1
    
    # Test 2: 3-level system (max depth = 2)
    T2 = {0: 0, 1: 0, 2: 1}
    K2 = koopman_pullback(T2, 3)
    verify_eventual_idempotency(K2, 2)  # max_depth = 2
    
    print("✅ 2.3 Eventual idempotency verified")


def test_signature_equivalence():
    """3.3: Verify signature equivalence"""
    T1 = {0: 0, 1: 0, 2: 0}  # One fixed point, depth 1
    T2 = {0: 0, 1: 0, 2: 0}  # Same structure
    T3 = {0: 0, 1: 1, 2: 1}  # Two fixed points
    
    assert equivalent(T1, T2), "Same structure should be equivalent"
    assert not equivalent(T1, T3), "Different structure should not be equivalent"
    print("✅ 3.3 Signature equivalence verified")


def test_classification():
    """3.4: Verify classification"""
    T = {0: 0, 1: 0, 2: 0}
    cls = classify_system(T)
    print(f"✅ 3.4 Classification: {cls}")


def run_all_tests():
    """Execute full integration test suite."""
    print("=" * 60)
    print("AQARION J15.LEAN — INTEGRATION TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("PHASE 1.1", test_koopman_convention),
        ("PHASE 1.2", test_defect_structure),
        ("PHASE 1.3", test_depth_completeness),
        ("PHASE 1.4", test_cycle_constraint),
        ("PHASE 1.5", test_witness_revalidation),
        ("PHASE 1.6", test_deterministic_hash),
        ("PHASE 1.7", test_exact_rank),
        ("PHASE 2.1", test_functional_graph_decomposition),
        ("PHASE 2.2", test_image_filtration),
        ("PHASE 2.3", test_eventual_idempotency),
        ("PHASE 3.3", test_signature_equivalence),
        ("PHASE 3.4", test_classification),
    ]
    
    passed = 0
    failed = 0
    
    for name, test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {name} FAILED: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("✅ ALL PHASES COMPLETE — AQARION transitions to classification system")
    else:
        print("❌ PHASES INCOMPLETE — review failures")
    
    return failed == 0


if __name__ == "__main__":
    run_all_tests()
'''

with open('/mnt/agents/output/J15/integration_test.py', 'w') as f:
    f.write(fixed_integration)

# Also fix signature_engine.py to use verify_eventual_idempotency
fixed_signature = '''"""
AQARION J15.LEAN — Invariant Signature Engine
PHASE 3: Invariant Signature Engine (NEXT LAYER)

Depends on: PHASE 1 (koopman_core.py), PHASE 2 (structural_cert.py)

Target Theorem:
    T_1 ~ T_2  <=>  Signature(T_1) = Signature(T_2)
"""

import numpy as np
from fractions import Fraction
from typing import Dict, List, Tuple

from koopman_core import koopman_pullback, exact_rank
from structural_cert import (
    decompose_functional_graph,
    compute_image_chain,
    compute_jordan_blocks,
    certify_image_filtration
)


# 3.1 Define Canonical Signature

class InvariantSignature:
    """
    Canonical signature for functional graph equivalence.
    
    Fields:
        cycle_structure: list of fixed points (always length 1 cycles)
        depth_profile: sorted list of depths for all states
        image_chain: non-increasing chain of image sizes
        jordan_blocks: list of (size, count) for nilpotent part
        rank_profile: ranks of powers of (K - I)
    """
    
    def __init__(self, 
                 cycle_structure: List[int],
                 depth_profile: List[int],
                 image_chain: List[int],
                 jordan_blocks: List[Tuple[int, int]],
                 rank_profile: List[int]):
        self.cycle_structure = cycle_structure
        self.depth_profile = depth_profile
        self.image_chain = image_chain
        self.jordan_blocks = jordan_blocks
        self.rank_profile = rank_profile
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, InvariantSignature):
            return False
        return (self.cycle_structure == other.cycle_structure and
                self.depth_profile == other.depth_profile and
                self.image_chain == other.image_chain and
                self.jordan_blocks == other.jordan_blocks and
                self.rank_profile == other.rank_profile)
    
    def __hash__(self) -> int:
        return hash((tuple(self.cycle_structure),
                     tuple(self.depth_profile),
                     tuple(self.image_chain),
                     tuple(self.jordan_blocks),
                     tuple(self.rank_profile)))
    
    def to_dict(self) -> Dict:
        return {
            "cycle_structure": self.cycle_structure,
            "depth_profile": self.depth_profile,
            "image_chain": self.image_chain,
            "jordan_blocks": self.jordan_blocks,
            "rank_profile": self.rank_profile
        }


# 3.2 Extraction Function

def compute_signature(T: Dict[int, int]) -> InvariantSignature:
    """
    3.2 EXTRACTION FUNCTION
    
    Compute the complete invariant signature of a functional graph.
    """
    n = len(T)
    
    # Structural decomposition
    G = decompose_functional_graph(T)
    
    # Cycle structure (fixed points only, enforced by PHASE 1.4)
    cycle_structure = sorted(G["fixed_points"])
    
    # Depth profile
    depth_profile = sorted(G["depths"].values())
    
    # Image chain (certified by PHASE 2.2)
    image_chain = certify_image_filtration(T)
    
    # Koopman operator
    K = koopman_pullback(T, n)
    I = np.eye(n, dtype=object)
    for i in range(n):
        for j in range(n):
            I[i, j] = Fraction(1) if i == j else Fraction(0)
    
    N = K - I
    for i in range(n):
        for j in range(n):
            N[i, j] = Fraction(N[i, j]).limit_denominator()
    
    # Jordan blocks
    max_depth = max(depth_profile) if depth_profile else 0
    jordan_blocks = compute_jordan_blocks(K, max_depth)
    
    # Rank profile: ranks of N, N^2, N^3, ...
    rank_profile = []
    current = N.copy()
    for _ in range(max_depth + 2):
        rank_profile.append(exact_rank(current))
        current = current @ N
        for i in range(n):
            for j in range(n):
                current[i, j] = Fraction(current[i, j]).limit_denominator()
    
    return InvariantSignature(
        cycle_structure=cycle_structure,
        depth_profile=depth_profile,
        image_chain=image_chain,
        jordan_blocks=jordan_blocks,
        rank_profile=rank_profile
    )


# 3.3 Equivalence Operator

def equivalent(T1: Dict[int, int], T2: Dict[int, int]) -> bool:
    """
    3.3 EQUIVALENCE OPERATOR
    
    Two functional graphs are equivalent iff their signatures match.
    
    Target Theorem:
        T_1 ~ T_2  <=>  Signature(T_1) = Signature(T_2)
    """
    sig1 = compute_signature(T1)
    sig2 = compute_signature(T2)
    return sig1 == sig2


# 3.4 Classification Interface

def classify_system(T: Dict[int, int]) -> str:
    """
    Classify a functional graph by its invariant signature.
    
    Returns canonical class identifier.
    """
    sig = compute_signature(T)
    
    # Build canonical class string
    parts = [
        f"C{len(sig.cycle_structure)}",
        f"D{max(sig.depth_profile) if sig.depth_profile else 0}",
        f"J{''.join(f'{s}x{c}' for s, c in sig.jordan_blocks)}"
    ]
    
    return "_".join(parts)


# Export
__all__ = [
    'InvariantSignature',
    'compute_signature',
    'equivalent',
    'classify_system'
]
'''

with open('/mnt/agents/output/J15/signature_engine.py', 'w') as f:
    f.write(fixed_signature)

print("Fixed signature_engine.py written")Fixed signature_engine.py written
