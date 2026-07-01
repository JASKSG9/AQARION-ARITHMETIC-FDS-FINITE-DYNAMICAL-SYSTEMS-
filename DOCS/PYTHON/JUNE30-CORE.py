
# [3] Core Python module: src/aqarion/__init__.py and core.py

init_py = '''"""AQARION — Certification theory for finite observable dynamical systems.

Version: 30.2.0 (July Freeze)
"""

__version__ = "30.2.0"

from .core import (
    build_K,
    proj,
    obstruction_D,
    D_norm,
    refine_partition,
    is_exact_quotient,
    compute_canonical_quotient,
    invariant_passport,
)

__all__ = [
    "build_K",
    "proj",
    "obstruction_D",
    "D_norm",
    "refine_partition",
    "is_exact_quotient",
    "compute_canonical_quotient",
    "invariant_passport",
]
'''

core_py = '''"""AQARION Core — Finite Deterministic Dynamical Systems (FDDS).

Implements the central operators:
- K: Koopman operator (stochastic convention)
- P_Π: Averaging projection for partition Π
- D_Π = (I - P_Π) K P_Π: Defect / obstruction operator

All functions operate on 0-based indexing (Python convention).
Julia parity: use 1-based wrappers.
"""

import numpy as np
from typing import List, Tuple, Dict, Any
import hashlib
import json


def build_K(T: List[int]) -> np.ndarray:
    """Build Koopman operator K for deterministic map T.
    
    Convention: K[x, T[x]] = 1.0 (rows sum to 1).
    This is the stochastic / Perron-Frobenius convention.
    
    Args:
        T: State transition map, T[x] = next state of x.
           Must be 0-based indexing.
    
    Returns:
        n×n numpy array (Float64).
    """
    n = len(T)
    K = np.zeros((n, n), dtype=np.float64)
    for x in range(n):
        K[x, T[x]] = 1.0
    return K


def proj(part: List[List[int]], n: int) -> np.ndarray:
    """Build averaging projection matrix P_Π for partition Π.
    
    For each block b in partition, P[i,j] = 1/|b| if i,j ∈ b, else 0.
    Properties: P² = P (idempotent), Pᵀ = P (symmetric).
    
    Args:
        part: Partition as list of blocks (each block is list of state indices).
        n: Total number of states.
    
    Returns:
        n×n numpy array (Float64).
    """
    P = np.zeros((n, n), dtype=np.float64)
    for b in part:
        sz = len(b)
        val = 1.0 / sz
        for i in b:
            for j in b:
                P[i, j] = val
    return P


def obstruction_D(P: np.ndarray, K: np.ndarray) -> np.ndarray:
    """Compute defect operator D_Π = (I - P_Π) K P_Π.
    
    Measures failure of observable Π to define an exact dynamical quotient.
    D_Π = 0  ⟺  Π is an exact quotient (Markovian/lumpable).
    
    Args:
        P: Projection matrix (from proj()).
        K: Koopman operator (from build_K()).
    
    Returns:
        n×n numpy array (Float64).
    """
    I = np.eye(P.shape[0], dtype=np.float64)
    return (I - P) @ K @ P


def D_norm(D: np.ndarray, ord: str = "fro") -> float:
    """Compute norm of defect operator.
    
    Default: Frobenius norm (||D||_F = sqrt(Σ|d_ij|²)).
    Also supports 'op' (operator 2-norm) and 'nuc' (nuclear).
    
    Args:
        D: Defect operator matrix.
        ord: Norm order ('fro', 'op', 'nuc').
    
    Returns:
        Scalar norm value.
    """
    if ord == "fro":
        return float(np.linalg.norm(D, "fro"))
    elif ord == "op":
        return float(np.linalg.norm(D, 2))
    elif ord == "nuc":
        return float(np.linalg.norm(D, "nuc"))
    else:
        raise ValueError(f"Unknown norm order: {ord}")


def refine_partition(part: List[List[int]], T: List[int]) -> List[List[int]]:
    """One-step partition refinement by image consistency.
    
    Split each block b into sub-blocks where T maps consistently.
    This is the standard exact-quotient refinement (coarsest exact refinement).
    
    Args:
        part: Current partition.
        T: State transition map.
    
    Returns:
        Refined partition (list of blocks sorted by minimum element).
    """
    block_map = {}
    for b_idx, b in enumerate(part):
        for x in b:
            block_map[x] = b_idx
    
    new_blocks: Dict[Tuple[int, int], List[int]] = {}
    for b in part:
        for x in b:
            curr = block_map[x]
            fut = block_map[T[x]]
            key = (curr, fut)
            if key not in new_blocks:
                new_blocks[key] = []
            new_blocks[key].append(x)
    
    next_part = list(new_blocks.values())
    next_part.sort(key=lambda b: min(b))
    return next_part


def is_exact_quotient(part: List[List[int]], T: List[int]) -> bool:
    """Check if partition defines an exact dynamical quotient.
    
    Exact quotient: for every block b, all x ∈ b map to the same future block.
    Equivalent to D_Π = 0 (numerically, ||D_Π|| < ε).
    
    Args:
        part: Partition to test.
        T: State transition map.
    
    Returns:
        True if exact quotient, False otherwise.
    """
    block_map = {}
    for b_idx, b in enumerate(part):
        for x in b:
            block_map[x] = b_idx
    
    for b in part:
        futures = {block_map[T[x]] for x in b}
        if len(futures) > 1:
            return False
    return True


def compute_canonical_quotient(T: List[int]) -> List[List[int]]:
    """Compute the maximal exact quotient (coarsest exact partition).
    
    Iteratively refines until fixed point. Guaranteed to converge
    for finite systems (at most n refinements).
    
    Args:
        T: State transition map.
    
    Returns:
        Maximal exact quotient partition.
    """
    n = len(T)
    # Start with trivial partition (one block)
    part = [list(range(n))]
    
    for _ in range(n):  # Upper bound on iterations
        new_part = refine_partition(part, T)
        if len(new_part) == len(part):
            # Check if actually fixed (refine_partition may not change count)
            # but block contents changed
            if all(sorted(a) == sorted(b) for a, b in zip(part, new_part)):
                break
        part = new_part
    
    return part


def invariant_passport(T: List[int], part: List[List[int]]) -> Dict[str, Any]:
    """Generate the AQARION Invariant Passport for a system + observable.
    
    17-field characterization schema. See docs/invariant_passport.md.
    
    Args:
        T: State transition map.
        part: Observable partition.
    
    Returns:
        Dictionary with all 17 passport fields.
    """
    n = len(T)
    k = len(part)
    K = build_K(T)
    P = proj(part, n)
    D = obstruction_D(P, K)
    
    # Spectral properties
    s = np.linalg.svd(D, compute_uv=False)
    spectral_radius = float(max(abs(np.linalg.eigvals(K))))
    
    # Automorphism group (trivial for generic FDDS, but compute)
    # For small n, brute-force permutation check
    automorphism_group = []
    if n <= 6:
        import itertools
        for perm in itertools.permutations(range(n)):
            sigma = list(perm)
            if all(T[sigma[x]] == sigma[T[x]] for x in range(n)):
                automorphism_group.append(sigma)
    
    # Leakage entropy
    D_abs = np.abs(D)
    total = np.sum(D_abs)
    if total > 1e-15:
        probs = D_abs.flatten() / total
        probs = probs[probs > 1e-15]
        leakage_entropy = float(-np.sum(probs * np.log2(probs)))
    else:
        leakage_entropy = 0.0
    
    passport = {
        "state_count": n,
        "observable_dimension": k,
        "partition_size": k,
        "behavioral_dimension": int(np.linalg.matrix_rank(K)),
        "defect_rank": int(np.linalg.matrix_rank(D)),
        "defect_norm_fro": round(D_norm(D, "fro"), 12),
        "defect_norm_op": round(D_norm(D, "op"), 12),
        "leakage_entropy": round(leakage_entropy, 12),
        "support_graph_edges": int(np.count_nonzero(D_abs > 1e-12)),
        "transient_depth": None,  # Requires filtration computation
        "filtration_height": None,  # Requires hitting-time analysis
        "spectral_radius": round(spectral_radius, 12),
        "nilpotent_index": None,  # Requires transient block analysis
        "automorphism_group_order": len(automorphism_group),
        "transformation_monoid_size": None,  # Requires semigroup computation
        "certification_status": "EXACT" if is_exact_quotient(part, T) else "DEFECTIVE",
        "benchmark_status": "PENDING",
        "lean_status": "NOT_FORMALIZED",
    }
    return passport


def hash_system(T: List[int], part: List[List[int]]) -> str:
    """Generate SHA-256 hash for a system + observable pair.
    
    Used for regression testing and reference data verification.
    """
    data = json.dumps({"T": T, "part": part}, sort_keys=True)
    return hashlib.sha256(data.encode()).hexdigest()[:16]
'''

with open(ROOT / "src/aqarion/__init__.py", "w") as f:
    f.write(init_py)

with open(ROOT / "src/aqarion/core.py", "w") as f:
    f.write(core_py)

print("✅ src/aqarion/__init__.py")
print("✅ src/aqarion/core.py")
