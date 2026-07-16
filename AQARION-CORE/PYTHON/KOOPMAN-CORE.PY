
import os

# Create the J15.LEAN directory structure
os.makedirs('/mnt/agents/output/J15', exist_ok=True)

# PHASE 1 — CORE CORRECTION LOCK
# 1.1 Koopman Definition

koopman_code = '''"""
AQARION J15.LEAN — Koopman Operator Module
PHASE 1.1: Koopman Definition (MANDATORY REPLACEMENT)

Matrix convention (LOCKED):
    K[i, j] = 1  iff  i = T(j)

For a column vector f:
    (Kf)(j) = f(T(j))

This convention ensures:
    D = (I - P) K P = 0  ⇔  partition Π is T-congruence
"""

import numpy as np
from fractions import Fraction
from typing import Dict, List, Set, Tuple

def koopman_pullback(T: Dict[int, int], n: int) -> np.ndarray:
    """
    Construct Koopman pullback operator K.
    
    K[i, j] = 1  iff  i = T(j)
    
    For column vector f: (Kf)(j) = f(T(j))
    
    This is the ONLY accepted convention. No deviation.
    """
    K = np.zeros((n, n), dtype=object)
    for j in range(n):
        i = T[j]
        K[i, j] = Fraction(1)
    return K


def projection_matrix(partition_blocks: List[List[int]], n: int) -> np.ndarray:
    """
    Construct orthogonal projection P_Π onto block-constant functions.
    
    For block B: P_Π(f)(x) = (1/|B|) * Σ_{y∈B} f(y)  for x ∈ B
    """
    P = np.zeros((n, n), dtype=object)
    for block in partition_blocks:
        m = len(block)
        for x in block:
            for y in block:
                P[x, y] = Fraction(1, m)
    return P


def defect_operator(T: Dict[int, int], partition_blocks: List[List[int]], n: int) -> np.ndarray:
    """
    Compute defect operator D_Π = (I - P) K P
    
    D_Π = 0  ⇔  Π is a dynamical congruence for T
    """
    K = koopman_pullback(T, n)
    P = projection_matrix(partition_blocks, n)
    I = np.eye(n, dtype=object)
    for i in range(n):
        for j in range(n):
            if I[i, j] == 1:
                I[i, j] = Fraction(1)
    D = (I - P) @ K @ P
    # Ensure exact rational arithmetic
    for i in range(n):
        for j in range(n):
            D[i, j] = Fraction(D[i, j]).limit_denominator()
    return D


# 1.2 Defect Operator Structural Enforcement

def validate_defect_structure(D: np.ndarray, P: np.ndarray) -> None:
    """
    Enforce PDP = 0 invariant.
    
    The defect operator must satisfy P D P = 0 for all valid constructions.
    """
    test = P @ D @ P
    for i in range(test.shape[0]):
        for j in range(test.shape[1]):
            val = Fraction(test[i, j]).limit_denominator()
            if val != 0:
                raise AssertionError(
                    f"Defect operator violates PDP = 0 invariant at ({i},{j}): {val}"
                )


# 1.3 Depth Completeness Assertion

def compute_depths(T: Dict[int, int]) -> Dict[int, int]:
    """
    BFS-based depth computation with completeness assertion.
    
    Depth(x) = distance to nearest fixed point (cycle of length 1).
    """
    n = len(T)
    depth: Dict[int, int] = {}
    
    # Find fixed points (cycles of length 1)
    fixed = {x for x in T if T[x] == x}
    
    # BFS from fixed points
    from collections import deque
    queue = deque([(x, 0) for x in fixed])
    for x in fixed:
        depth[x] = 0
    
    while queue:
        x, d = queue.popleft()
        # Find predecessors
        for y in T:
            if T[y] == x and y not in depth:
                depth[y] = d + 1
                queue.append((y, d + 1))
    
    # 1.3 DEPTH COMPLETENESS ASSERTION
    if len(depth) != n:
        missing = set(T.keys()) - set(depth.keys())
        raise AssertionError(f"Depth assignment incomplete. Missing states: {missing}")
    
    return depth


# 1.4 Cycle Constraint Enforcement

def detect_cycles(T: Dict[int, int]) -> List[List[int]]:
    """Detect all cycles in the functional graph."""
    visited = set()
    cycles = []
    
    for start in T:
        if start in visited:
            continue
        path = []
        current = start
        while current not in visited:
            visited.add(current)
            path.append(current)
            current = T[current]
            if current in path:
                # Found cycle
                idx = path.index(current)
                cycle = path[idx:]
                cycles.append(cycle)
                break
    
    return cycles


def assert_only_fixed_point_cycles(T: Dict[int, int]) -> None:
    """
    1.4 CYCLE CONSTRAINT ENFORCEMENT
    
    All cycles must be of length 1 (fixed points).
    Non-trivial cycles are rejected before spectral computation.
    """
    cycles = detect_cycles(T)
    for c in cycles:
        if len(c) != 1:
            raise AssertionError(f"Non-trivial cycle detected: {c}")


# 1.5 Witness Revalidation (AQ-W-003)

def revalidate_witness(witness_T: Dict[int, int], witness_part: List[List[int]], n: int) -> None:
    """
    Revalidate AQ-W-003 witness under current conventions.
    
    Witness must satisfy:
    1. D = defect_operator(T, part) has all zeros
    2. C = KP - PK is non-zero (non-commutativity witness)
    """
    D = defect_operator(witness_T, witness_part, n)
    for i in range(n):
        for j in range(n):
            val = Fraction(D[i, j]).limit_denominator()
            assert val == 0, f"Witness defect non-zero at ({i},{j}): {val}"
    
    K = koopman_pullback(witness_T, n)
    P = projection_matrix(witness_part, n)
    C = K @ P - P @ K
    
    has_nonzero = False
    for i in range(n):
        for j in range(n):
            val = Fraction(C[i, j]).limit_denominator()
            if val != 0:
                has_nonzero = True
                break
        if has_nonzero:
            break
    
    assert has_nonzero, "Witness C = KP - PK is zero — witness invalid"


# 1.6 Deterministic Hash Fix

def deterministic_hash(file_list: List[str]) -> str:
    """
    1.6 DETERMINISTIC HASH FIX
    
    Exclude build_provenance.json from hash computation.
    """
    import hashlib
    hasher = hashlib.sha256()
    for fname in sorted(file_list):
        if fname == "build_provenance.json":
            continue
        hasher.update(fname.encode())
    return hasher.hexdigest()


# 1.7 Exact Rank Stabilization

def exact_rank(A: np.ndarray) -> int:
    """
    1.7 EXACT RANK STABILIZATION
    
    Fraction-based Gaussian elimination with exact arithmetic.
    No overflow-style expansion.
    """
    rows, cols = A.shape
    # Convert to Fraction matrix
    M = np.zeros((rows, cols), dtype=object)
    for i in range(rows):
        for j in range(cols):
            M[i, j] = Fraction(A[i, j]).limit_denominator()
    
    rank = 0
    for col in range(cols):
        # Find pivot
        pivot_row = None
        for r in range(rank, rows):
            if M[r, col] != 0:
                pivot_row = r
                break
        
        if pivot_row is None:
            continue
        
        # Swap
        M[[rank, pivot_row]] = M[[pivot_row, rank]]
        
        # Normalize pivot
        pivot_val = M[rank, col]
        for c in range(col, cols):
            M[rank, c] /= pivot_val
        
        # Eliminate
        for r in range(rows):
            if r != rank and M[r, col] != 0:
                factor = M[r, col]
                for c in range(col, cols):
                    M[r, c] -= factor * M[rank, c]
        
        rank += 1
    
    return rank


# Export all functions
__all__ = [
    'koopman_pullback',
    'projection_matrix', 
    'defect_operator',
    'validate_defect_structure',
    'compute_depths',
    'detect_cycles',
    'assert_only_fixed_point_cycles',
    'revalidate_witness',
    'deterministic_hash',
    'exact_rank'
]
'''

with open('/mnt/agents/output/J15/koopman_core.py', 'w') as f:
    f.write(koopman_code)

print("PHASE 1 complete — koopman_core.py written")
print(f"Size: {len(koopman_code)} bytes")
