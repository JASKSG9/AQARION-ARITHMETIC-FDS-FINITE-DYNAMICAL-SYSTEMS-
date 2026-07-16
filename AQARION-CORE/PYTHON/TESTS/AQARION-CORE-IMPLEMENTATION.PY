
# Create integration test and final verification report

integration_code = '''"""
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
    verify_min_poly,
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
    T = {0: 0, 1: 0, 2: 1, 3: 1}
    depth = compute_depths(T)
    assert len(depth) == 4, "Depth incomplete"
    assert depth[0] == 0, "Fixed point depth wrong"
    assert depth[1] == 0, "Fixed point depth wrong"
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
    # Witness: a system where D=0 but C≠0
    # Trivial case: identity map with trivial partition
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


def test_minimal_polynomial():
    """2.3: Verify minimal polynomial"""
    T = {0: 0, 1: 0, 2: 1}  # Depth: 0->0, 1->0, 2->1
    K = koopman_pullback(T, 3)
    # Max depth is 2, so (K-I)^3 should be 0
    verify_min_poly(K, 3)
    print("✅ 2.3 Minimal polynomial verified")


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
        ("PHASE 2.3", test_minimal_polynomial),
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
    f.write(integration_code)

print("Integration test written")
print(f"Size: {len(integration_code)} bytes")
# Run the integration tests
import sys
sys.path.insert(0, '/mnt/agents/output/J15')

exec(open('/mnt/agents/output/J15/integration_test.py').read())============================================================
AQARION J15.LEAN — INTEGRATION TEST SUITE
============================================================
✅ 1.1 Koopman convention verified
✅ 1.2 Defect structure verified
❌ PHASE 1.3 FAILED: Fixed point depth wrong
✅ 1.4 Cycle constraint verified
✅ 1.5 Witness revalidation verified
✅ 1.6 Deterministic hash verified
✅ 1.7 Exact rank verified
✅ 2.1 Functional graph decomposition verified
✅ 2.2 Image filtration verified: [5, 2, 1]
❌ PHASE 2.3 FAILED: Minimal polynomial verification failed at (0,1): 1
✅ 3.3 Signature equivalence verified
✅ 3.4 Classification: C1_D1_J
============================================================
RESULTS: 10 passed, 2 failed
============================================================
❌ PHASES INCOMPLETE — review failures
# Fix 1: The test assertion in 1.3 is wrong
# T = {0: 0, 1: 0, 2: 1, 3: 1}
# Fixed points: 0 (T[0]=0)
# Depth(0) = 0
# Depth(1) = 1 (1 -> 0, which is fixed)
# Depth(2) = 2 (2 -> 1 -> 0)
# Depth(3) = 2 (3 -> 1 -> 0)
# So depth[1] should be 1, not 0

# Fix 2: Minimal polynomial verification
# For T = {0: 0, 1: 0, 2: 1}
# K = [[1, 1, 0], [0, 0, 1], [0, 0, 1]] (K[i,j] = 1 iff i = T(j))
# T(0)=0, T(1)=0, T(2)=1
# K[0,0]=1 (T(0)=0), K[0,1]=1 (T(1)=0), K[1,2]=1 (T(2)=1), K[2,2]=0? No, T(2)=1 so K[1,2]=1
# Wait: K[i,j] = 1 iff i = T(j)
# j=0: T(0)=0, so K[0,0]=1
# j=1: T(1)=0, so K[0,1]=1
# j=2: T(2)=1, so K[1,2]=1
# So K = [[1, 1, 0], [0, 0, 1], [0, 0, 0]]
# N = K - I = [[0, 1, 0], [0, -1, 1], [0, 0, -1]]
# N^2 = [[0, -1, 1], [0, 1, -2], [0, 0, 1]]
# N^3 = ... not zero

# The issue is that for this system, (K-I) is not nilpotent in the expected way
# because the system has a tree structure but K-I doesn't vanish at the expected power

# Actually, the issue is that the minimal polynomial claim (K-I)^k = 0 is only true
# for the TRANSFER operator, not the Koopman pullback in this convention.
# Or more precisely, the nilpotency depends on the specific structure.

# Let me check: for a functional graph with only fixed points, 
# the Koopman operator satisfies K^r = K^{r+1} for some r (eventual periodicity)
# but (K-I) being nilpotent is a stronger condition.

# Actually, (K-I) is nilpotent iff the system is a DAG with all paths leading to fixed points
# in a "tree-like" way. Let me verify the computation.

import numpy as np
from fractions import Fraction

T = {0: 0, 1: 0, 2: 1}
n = 3

K = np.zeros((n, n), dtype=object)
for j in range(n):
    i = T[j]
    K[i, j] = Fraction(1)

print("K =")
for i in range(n):
    print([K[i,j] for j in range(n)])

I = np.eye(n, dtype=object)
for i in range(n):
    for j in range(n):
        I[i, j] = Fraction(1) if i == j else Fraction(0)

N = K - I
for i in range(n):
    for j in range(n):
        N[i, j] = Fraction(N[i, j]).limit_denominator()

print("\nN = K - I =")
for i in range(n):
    print([N[i,j] for j in range(n)])

# Compute N^2
N2 = N @ N
for i in range(n):
    for j in range(n):
        N2[i, j] = Fraction(N2[i, j]).limit_denominator()

print("\nN^2 =")
for i in range(n):
    print([N2[i,j] for j in range(n)])

# Compute N^3
N3 = N2 @ N
for i in range(n):
    for j in range(n):
        N3[i, j] = Fraction(N3[i, j]).limit_denominator()

print("\nN^3 =")
for i in range(n):
    print([N3[i,j] for j in range(n)])K =
[Fraction(1, 1), Fraction(1, 1), 0]
[0, 0, Fraction(1, 1)]
[0, 0, 0]

N = K - I =
[Fraction(0, 1), Fraction(1, 1), Fraction(0, 1)]
[Fraction(0, 1), Fraction(-1, 1), Fraction(1, 1)]
[Fraction(0, 1), Fraction(0, 1), Fraction(-1, 1)]

N^2 =
[Fraction(0, 1), Fraction(-1, 1), Fraction(1, 1)]
[Fraction(0, 1), Fraction(1, 1), Fraction(-2, 1)]
[Fraction(0, 1), Fraction(0, 1), Fraction(1, 1)]

N^3 =
[Fraction(0, 1), Fraction(1, 1), Fraction(-2, 1)]
[Fraction(0, 1), Fraction(-1, 1), Fraction(3, 1)]
[Fraction(0, 1), Fraction(0, 1), Fraction(-1, 1)]
# Fix the integration tests

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
    verify_min_poly,
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


def test_minimal_polynomial():
    """2.3: Verify minimal polynomial for a system where nilpotency holds.
    
    For a "star" system where all states map directly to a fixed point,
    (K - I)^2 = 0."""
    # System: 0->0 (fixed), 1->0, 2->0 (all leaves connect directly to root)
    T = {0: 0, 1: 0, 2: 0}
    K = koopman_pullback(T, 3)
    
    # Verify (K - I)^2 = 0 for this system
    n = 3
    I = np.eye(n, dtype=object)
    for i in range(n):
        for j in range(n):
            I[i, j] = Fraction(1) if i == j else Fraction(0)
    
    N = K - I
    for i in range(n):
        for j in range(n):
            N[i, j] = Fraction(N[i, j]).limit_denominator()
    
    # N^2 should be zero for this star system
    N2 = N @ N
    for i in range(n):
        for j in range(n):
            N2[i, j] = Fraction(N2[i, j]).limit_denominator()
    
    for i in range(n):
        for j in range(n):
            assert N2[i, j] == 0, f"N^2 non-zero at ({i},{j}): {N2[i,j]}"
    
    print("✅ 2.3 Minimal polynomial verified (star system)")


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
        ("PHASE 2.3", test_minimal_polynomial),
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

print("Fixed integration test written")
# Run the fixed integration tests
import sys
sys.path.insert(0, '/mnt/agents/output/J15')

exec(open('/mnt/agents/output/J15/integration_test.py').read())============================================================
AQARION J15.LEAN — INTEGRATION TEST SUITE
============================================================
✅ 1.1 Koopman convention verified
✅ 1.2 Defect structure verified
✅ 1.3 Depth completeness verified
✅ 1.4 Cycle constraint verified
✅ 1.5 Witness revalidation verified
✅ 1.6 Deterministic hash verified
✅ 1.7 Exact rank verified
✅ 2.1 Functional graph decomposition verified
✅ 2.2 Image filtration verified: [5, 2, 1]
❌ PHASE 2.3 FAILED: N^2 non-zero at (0,1): -1
✅ 3.3 Signature equivalence verified
✅ 3.4 Classification: C1_D1_J
============================================================
RESULTS: 11 passed, 1 failed
============================================================
❌ PHASES INCOMPLETE — review failures
# Let me understand what the correct minimal polynomial statement is
# For functional graphs with only fixed points:
# The Koopman operator K satisfies K^r = K^{r+1} for r >= diameter
# This is because after enough steps, all paths have reached a fixed point

# For T = {0: 0, 1: 0, 2: 0}:
# K = [[1,1,1],[0,0,0],[0,0,0]]
# K^2 = [[1,1,1],[0,0,0],[0,0,0]] = K
# So K is idempotent! K^2 = K

# For T = {0: 0, 1: 0, 2: 1}:
# K = [[1,1,0],[0,0,1],[0,0,0]]
# K^2 = [[1,1,1],[0,0,0],[0,0,0]]
# K^3 = [[1,1,1],[0,0,0],[0,0,0]] = K^2
# So K^2 = K^3, meaning the image stabilizes at step 2

# The correct theorem is:
# For functional graphs with only fixed point cycles,
# K^d = K^{d+1} where d is the maximum depth.
# This is equivalent to (K - I) being nilpotent on the image of K^d,
# or more simply: K satisfies x^d(x-1) = 0 in some sense.

# Actually, the correct minimal polynomial for the Koopman operator
# of a functional graph with only fixed points is:
# x(x-1) = 0 if the graph is a star (all map directly to fixed point)
# For general trees, it's more complex.

# The simplest correct test: verify K^d = K^{d+1} for d = max_depth + 1

import numpy as np
from fractions import Fraction

T = {0: 0, 1: 0, 2: 0}
n = 3

K = np.zeros((n, n), dtype=object)
for j in range(n):
    i = T[j]
    K[i, j] = Fraction(1)

print("K =")
for i in range(n):
    print([K[i,j] for j in range(n)])

# K^2
K2 = K @ K
for i in range(n):
    for j in range(n):
        K2[i, j] = Fraction(K2[i, j]).limit_denominator()

print("\nK^2 =")
for i in range(n):
    print([K2[i,j] for j in range(n)])

# Check K^2 == K
for i in range(n):
    for j in range(n):
        assert K2[i,j] == K[i,j], f"K^2 != K at ({i},{j})"

print("\n✅ K^2 = K for star system")

# Now test for the 3-level system
T2 = {0: 0, 1: 0, 2: 1}
n2 = 3

K2 = np.zeros((n2, n2), dtype=object)
for j in range(n2):
    i = T2[j]
    K2[i, j] = Fraction(1)

print("\nK for 3-level system =")
for i in range(n2):
    print([K2[i,j] for j in range(n2)])

# K^2
K2_sq = K2 @ K2
for i in range(n2):
    for j in range(n2):
        K2_sq[i, j] = Fraction(K2_sq[i, j]).limit_denominator()

print("\nK^2 =")
for i in range(n2):
    print([K2_sq[i,j] for j in range(n2)])

# K^3
K2_cub = K2_sq @ K2
for i in range(n2):
    for j in range(n2):
        K2_cub[i, j] = Fraction(K2_cub[i, j]).limit_denominator()

print("\nK^3 =")
for i in range(n2):
    print([K2_cub[i,j] for j in range(n2)])

# Check K^2 == K^3
for i in range(n2):
    for j in range(n2):
        assert K2_sq[i,j] == K2_cub[i,j], f"K^2 != K^3 at ({i},{j})"

print("\n✅ K^2 = K^3 for 3-level system (max depth = 2)")K =
[Fraction(1, 1), Fraction(1, 1), Fraction(1, 1)]
[0, 0, 0]
[0, 0, 0]

K^2 =
[Fraction(1, 1), Fraction(1, 1), Fraction(1, 1)]
[Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)]
[Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)]

✅ K^2 = K for star system

K for 3-level system =
[Fraction(1, 1), Fraction(1, 1), 0]
[0, 0, Fraction(1, 1)]
[0, 0, 0]

K^2 =
[Fraction(1, 1), Fraction(1, 1), Fraction(1, 1)]
[Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)]
[Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)]

K^3 =
[Fraction(1, 1), Fraction(1, 1), Fraction(1, 1)]
[Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)]
[Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)]

✅ K^2 = K^3 for 3-level system (max depth = 2)

# Let me understand what the correct minimal polynomial statement is
# For functional graphs with only fixed points:
# The Koopman operator K satisfies K^r = K^{r+1} for r >= diameter
# This is because after enough steps, all paths have reached a fixed point

# For T = {0: 0, 1: 0, 2: 0}:
# K = [[1,1,1],[0,0,0],[0,0,0]]
# K^2 = [[1,1,1],[0,0,0],[0,0,0]] = K
# So K is idempotent! K^2 = K

# For T = {0: 0, 1: 0, 2: 1}:
# K = [[1,1,0],[0,0,1],[0,0,0]]
# K^2 = [[1,1,1],[0,0,0],[0,0,0]]
# K^3 = [[1,1,1],[0,0,0],[0,0,0]] = K^2
# So K^2 = K^3, meaning the image stabilizes at step 2

# The correct theorem is:
# For functional graphs with only fixed point cycles,
# K^d = K^{d+1} where d is the maximum depth.
# This is equivalent to (K - I) being nilpotent on the image of K^d,
# or more simply: K satisfies x^d(x-1) = 0 in some sense.

# Actually, the correct minimal polynomial for the Koopman operator
# of a functional graph with only fixed points is:
# x(x-1) = 0 if the graph is a star (all map directly to fixed point)
# For general trees, it's more complex.

# The simplest correct test: verify K^d = K^{d+1} for d = max_depth + 1

import numpy as np
from fractions import Fraction

T = {0: 0, 1: 0, 2: 0}
n = 3

K = np.zeros((n, n), dtype=object)
for j in range(n):
    i = T[j]
    K[i, j] = Fraction(1)

print("K =")
for i in range(n):
    print([K[i,j] for j in range(n)])

# K^2
K2 = K @ K
for i in range(n):
    for j in range(n):
        K2[i, j] = Fraction(K2[i, j]).limit_denominator()

print("\nK^2 =")
for i in range(n):
    print([K2[i,j] for j in range(n)])

# Check K^2 == K
for i in range(n):
    for j in range(n):
        assert K2[i,j] == K[i,j], f"K^2 != K at ({i},{j})"

print("\n✅ K^2 = K for star system")

# Now test for the 3-level system
T2 = {0: 0, 1: 0, 2: 1}
n2 = 3

K2 = np.zeros((n2, n2), dtype=object)
for j in range(n2):
    i = T2[j]
    K2[i, j] = Fraction(1)

print("\nK for 3-level system =")
for i in range(n2):
    print([K2[i,j] for j in range(n2)])

# K^2
K2_sq = K2 @ K2
for i in range(n2):
    for j in range(n2):
        K2_sq[i, j] = Fraction(K2_sq[i, j]).limit_denominator()

print("\nK^2 =")
for i in range(n2):
    print([K2_sq[i,j] for j in range(n2)])

# K^3
K2_cub = K2_sq @ K2
for i in range(n2):
    for j in range(n2):
        K2_cub[i, j] = Fraction(K2_cub[i, j]).limit_denominator()

print("\nK^3 =")
for i in range(n2):
    print([K2_cub[i,j] for j in range(n2)])

# Check K^2 == K^3
for i in range(n2):
    for j in range(n2):
        assert K2_sq[i,j] == K2_cub[i,j], f"K^2 != K^3 at ({i},{j})"

print("\n✅ K^2 = K^3 for 3-level system (max depth = 2)")K =
[Fraction(1, 1), Fraction(1, 1), Fraction(1, 1)]
[0, 0, 0]
[0, 0, 0]

K^2 =
[Fraction(1, 1), Fraction(1, 1), Fraction(1, 1)]
[Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)]
[Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)]

✅ K^2 = K for star system

K for 3-level system =
[Fraction(1, 1), Fraction(1, 1), 0]
[0, 0, Fraction(1, 1)]
[0, 0, 0]

K^2 =
[Fraction(1, 1), Fraction(1, 1), Fraction(1, 1)]
[Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)]
[Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)]

K^3 =
[Fraction(1, 1), Fraction(1, 1), Fraction(1, 1)]
[Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)]
[Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)]

✅ K^2 = K^3 for 3-level system (max depth = 2)
