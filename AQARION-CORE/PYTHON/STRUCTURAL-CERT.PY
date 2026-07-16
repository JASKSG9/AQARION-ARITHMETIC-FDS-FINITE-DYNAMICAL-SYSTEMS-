
# PHASE 2 — STRUCTURAL CERTIFICATION

structural_code = '''"""
AQARION J15.LEAN — Structural Certification Module
PHASE 2: Structural Certification

Depends on: PHASE 1 (koopman_core.py)
"""

import numpy as np
from fractions import Fraction
from typing import Dict, List, Set, Tuple
from collections import defaultdict

from koopman_core import (
    koopman_pullback,
    projection_matrix,
    compute_depths,
    assert_only_fixed_point_cycles,
    exact_rank
)


# 2.1 Functional Graph Canonicalization

def decompose_functional_graph(T: Dict[int, int]) -> Dict:
    """
    2.1 FUNCTIONAL GRAPH CANONICALIZATION
    
    Decompose a functional graph into:
    - fixed_points: list of fixed points (cycles of length 1)
    - trees: mapping from each fixed point to its basin of attraction
    - depths: depth assignment for all states
    
    All downstream logic MUST use this structure.
    No duplicate depth logic permitted.
    """
    # Enforce cycle constraint first
    assert_only_fixed_point_cycles(T)
    
    fixed = [x for x in T if T[x] == x]
    depth = compute_depths(T)
    
    # Build trees: each fixed point is root of its basin
    trees = {f: [] for f in fixed}
    
    # Group states by their root (nearest fixed point)
    def find_root(x: int, T: Dict[int, int]) -> int:
        """Follow T until reaching a fixed point."""
        visited = set()
        current = x
        while current not in visited:
            if T[current] == current:
                return current
            visited.add(current)
            current = T[current]
        raise AssertionError(f"Cycle detected in find_root for {x}")
    
    for x in T:
        root = find_root(x, T)
        trees[root].append(x)
    
    # Sort trees for determinism
    for f in trees:
        trees[f].sort()
    
    return {
        "fixed_points": sorted(fixed),
        "trees": trees,
        "depths": depth
    }


# 2.2 Image Filtration Certification

def compute_image_chain(T: Dict[int, int]) -> List[int]:
    """
    Compute the image chain: |T^k(X)| for k = 0, 1, 2, ...
    """
    n = len(T)
    states = set(T.keys())
    chain = [len(states)]
    
    current = states.copy()
    seen = [frozenset(current)]
    
    while True:
        next_set = {T[x] for x in current}
        if frozenset(next_set) in seen:
            break
        seen.append(frozenset(next_set))
        chain.append(len(next_set))
        current = next_set
    
    return chain


def certify_image_filtration(T: Dict[int, int]) -> List[int]:
    """
    2.2 IMAGE FILTRATION CERTIFICATION
    
    Verify:
    1. Image chain is non-increasing: |T^k(X)| >= |T^{k+1}(X)|
    2. Terminal value equals number of fixed points
    """
    chain = compute_image_chain(T)
    
    # Verify non-increasing
    for i in range(len(chain) - 1):
        assert chain[i] >= chain[i + 1], \
            f"Image chain not non-increasing at step {i}: {chain[i]} < {chain[i+1]}"
    
    # Verify terminal value
    fixed_count = sum(1 for x in T if T[x] == x)
    assert chain[-1] == fixed_count, \
        f"Terminal image chain value {chain[-1]} != fixed point count {fixed_count}"
    
    return chain


# 2.3 Minimal Polynomial Verification

def matrix_power(M: np.ndarray, k: int) -> np.ndarray:
    """Compute M^k with exact Fraction arithmetic."""
    n = M.shape[0]
    result = np.eye(n, dtype=object)
    for i in range(n):
        for j in range(n):
            result[i, j] = Fraction(1) if i == j else Fraction(0)
    
    base = M.copy()
    while k > 0:
        if k % 2 == 1:
            result = result @ base
            for i in range(n):
                for j in range(n):
                    result[i, j] = Fraction(result[i, j]).limit_denominator()
        base = base @ base
        for i in range(n):
            for j in range(n):
                base[i, j] = Fraction(base[i, j]).limit_denominator()
        k //= 2
    
    return result


def verify_min_poly(K: np.ndarray, k: int) -> None:
    """
    2.3 MINIMAL POLYNOMIAL VERIFICATION
    
    Verify that K^k (K - I) = 0 for the validated nilpotent index k.
    
    For functional graphs with only fixed point cycles, the Koopman operator
    satisfies (K - I)^k = 0 where k is the maximum depth + 1.
    """
    n = K.shape[0]
    I = np.eye(n, dtype=object)
    for i in range(n):
        for j in range(n):
            I[i, j] = Fraction(1) if i == j else Fraction(0)
    
    K_minus_I = K - I
    for i in range(n):
        for j in range(n):
            K_minus_I[i, j] = Fraction(K_minus_I[i, j]).limit_denominator()
    
    # Compute (K - I)^k
    A = matrix_power(K_minus_I, k)
    
    # Verify all entries are zero
    for i in range(n):
        for j in range(n):
            val = Fraction(A[i, j]).limit_denominator()
            assert val == 0, \
                f"Minimal polynomial verification failed at ({i},{j}): {val}"


def compute_jordan_blocks(K: np.ndarray, max_depth: int) -> List[Tuple[int, int]]:
    """
    Compute Jordan block structure from nilpotent operator (K - I).
    
    Returns list of (size, count) for each Jordan block size.
    """
    n = K.shape[0]
    I = np.eye(n, dtype=object)
    for i in range(n):
        for j in range(n):
            I[i, j] = Fraction(1) if i == j else Fraction(0)
    
    N = K - I
    for i in range(n):
        for j in range(n):
            N[i, j] = Fraction(N[i, j]).limit_denominator()
    
    blocks = []
    for size in range(1, max_depth + 2):
        # Count Jordan blocks of this size
        N_power = matrix_power(N, size)
        N_power_next = matrix_power(N, size + 1)
        
        rank_current = exact_rank(N_power)
        rank_next = exact_rank(N_power_next)
        
        count = rank_current - rank_next
        if count > 0:
            blocks.append((size, count))
    
    return blocks


# Export
__all__ = [
    'decompose_functional_graph',
    'compute_image_chain',
    'certify_image_filtration',
    'matrix_power',
    'verify_min_poly',
    'compute_jordan_blocks'
]
'''

with open('/mnt/agents/output/J15/structural_cert.py', 'w') as f:
    f.write(structural_code)

print("PHASE 2 complete — structural_cert.py written")
print(f"Size: {len(structural_code)} bytes")
