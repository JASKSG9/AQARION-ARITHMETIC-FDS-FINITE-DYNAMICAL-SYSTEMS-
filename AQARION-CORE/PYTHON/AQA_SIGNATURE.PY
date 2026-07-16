
# PHASE 3 — INVARIANT SIGNATURE ENGINE

signature_code = '''"""
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
    f.write(signature_code)

print("PHASE 3 complete — signature_engine.py written")
print(f"Size: {len(signature_code)} bytes")
