
# [7] Kaprekar benchmark — the first standard test system

kaprekar_py = '''"""Kaprekar Benchmark for AQARION.

The Kaprekar routine is a canonical finite dynamical system:
- States: 4-digit numbers (0000-9999), excluding repdigits
- Dynamics: f(n) = sort_desc(n) - sort_asc(n)
- Fixed point: 6174 (Kaprekar's constant)

This serves as Paper I's primary example: a well-known system
where exact quotients and defect geometry can be computed explicitly.
"""

import numpy as np
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from aqarion.core import (
    build_K, proj, obstruction_D, D_norm,
    is_exact_quotient, compute_canonical_quotient, invariant_passport
)


def kaprekar_step(n: int, digits: int = 4) -> int:
    """Single Kaprekar step.
    
    Args:
        n: Integer state (0 to 10^digits - 1)
        digits: Number of digits (default 4)
    
    Returns:
        Next state via Kaprekar routine.
    """
    s = f"{n:0{digits}d}"
    desc = int("".join(sorted(s, reverse=True)))
    asc = int("".join(sorted(s)))
    return desc - asc


def build_kaprekar_system(digits: int = 4):
    """Build the full Kaprekar FDDS.
    
    Returns:
        T: Transition map (list of next states)
        state_map: dict mapping state value → index
    """
    max_n = 10 ** digits
    # Filter out repdigits (all same digit) — they map to 0
    states = [n for n in range(max_n) if len(set(f"{n:0{digits}d}")) > 1]
    # Include 0 as absorbing state for repdigits
    if 0 not in states:
        states.append(0)
    states = sorted(set(states))
    
    state_map = {n: i for i, n in enumerate(states)}
    n_states = len(states)
    
    T = [0] * n_states
    for val, idx in state_map.items():
        next_val = kaprekar_step(val, digits)
        if next_val in state_map:
            T[idx] = state_map[next_val]
        else:
            # Repdigit → 0
            T[idx] = state_map[0]
    
    return T, state_map


def kaprekar_attractor_partition(T, state_map, digits: int = 4):
    """Create partition by attractor basin.
    
    For Kaprekar, the attractor is 6174 (for 4-digit).
    All states eventually flow to 6174.
    """
    inv_map = {v: k for k, v in state_map.items()}
    n = len(T)
    
    # Find attractor (fixed point)
    attractors = []
    for i in range(n):
        if T[i] == i:
            attractors.append(i)
    
    # Basin partition: group by attractor
    basins = defaultdict(list)
    for i in range(n):
        # Trace orbit
        visited = set()
        curr = i
        while curr not in visited:
            visited.add(curr)
            curr = T[curr]
        # curr is on a cycle
        basins[curr].append(i)
    
    return list(basins.values())


def run_kaprekar_benchmark(digits: int = 4):
    """Run full Kaprekar benchmark and generate passport."""
    print(f"=== Kaprekar Benchmark ({digits}-digit) ===")
    
    T, state_map = build_kaprekar_system(digits)
    n = len(T)
    print(f"States: {n}")
    
    # Attractor partition
    part = kaprekar_attractor_partition(T, state_map, digits)
    print(f"Attractor blocks: {len(part)}")
    
    # Check exactness
    exact = is_exact_quotient(part, T)
    print(f"Exact quotient? {exact}")
    
    # Compute canonical quotient
    canon = compute_canonical_quotient(T)
    print(f"Canonical quotient blocks: {len(canon)}")
    print(f"Canonical exact? {is_exact_quotient(canon, T)}")
    
    # Defect analysis
    K = build_K(T)
    P = proj(part, n)
    D = obstruction_D(P, K)
    norm_fro = D_norm(D, "fro")
    norm_op = D_norm(D, "op")
    
    print(f"Defect Frobenius norm: {norm_fro:.6f}")
    print(f"Defect operator norm: {norm_op:.6f}")
    print(f"Defect rank: {np.linalg.matrix_rank(D, tol=1e-10)}")
    
    # Passport
    passport = invariant_passport(T, part)
    print(f"\nPassport (selected fields):")
    print(f"  State count: {passport['state_count']}")
    print(f"  Observable dim: {passport['observable_dimension']}")
    print(f"  Defect rank: {passport['defect_rank']}")
    print(f"  Certification: {passport['certification_status']}")
    
    return {
        "digits": digits,
        "states": n,
        "attractor_blocks": len(part),
        "exact": exact,
        "canonical_blocks": len(canon),
        "defect_fro": norm_fro,
        "defect_op": norm_op,
        "passport": passport,
    }


if __name__ == "__main__":
    results = run_kaprekar_benchmark(4)
    print("\n=== Benchmark Complete ===")
'''

with open(ROOT / "benchmarks/kaprekar_benchmark.py", "w") as f:
    f.write(kaprekar_py)

print("✅ benchmarks/kaprekar_benchmark.py")

# Now list ALL files created
print("\n" + "=" * 70)
print("COMPLETE FILE INVENTORY")
print("=" * 70)

def list_files(path, prefix=""):
    for item in sorted(path.iterdir()):
        rel = item.relative_to(ROOT)
        if item.is_dir():
            print(f"{prefix}📁 {rel}/")
            list_files(item, prefix + "  ")
        else:
            size = item.stat().st_size
            print(f"{prefix}📄 {rel} ({size:,} bytes)")

list_files(ROOT)✅ benchmarks/kaprekar_benchmark.py

======================================================================
COMPLETE FILE INVENTORY
======================================================================
📁 .github/
  📁 .github/workflows/
    📄 .github/workflows/aqarion_ci.yml (579 bytes)
📄 .gitignore (613 bytes)
📄 README.md (4,197 bytes)
📁 benchmarks/
  📄 benchmarks/kaprekar_benchmark.py (4,402 bytes)
📁 claims/
  📄 claims/CLAIMS_REGISTRY.md (5,949 bytes)
  📄 claims/COUNTEREXAMPLES.md (4,275 bytes)
  📄 claims/JUNE-CHECKPOINT.MD (2,259 bytes)
📁 docs/
  📄 docs/invariant_passport.md (1,981 bytes)
📁 lean/
  📄 lean/API.lean (1,823 bytes)
📄 pyproject.toml (1,699 bytes)
📁 src/
  📁 src/aqarion/
    📄 src/aqarion/__init__.py (500 bytes)
    📄 src/aqarion/core.py (7,810 bytes)
📁 verification/
  📄 verification/RUN-ALL.sh (889 bytes)
  📁 verification/counterexamples/
  📁 verification/reference_data/
  📁 verification/reports/
  📄 verification/run_all.py (7,137 bytes)
  📁 verification/tests/
    📄 verification/tests/test_core.py (7,100 bytes)
    📄 verification/tests/test_counterexamples.py (7,271 bytes)
    📄 verification/tests/test_theorems.py (6,955 bytes)
  📄 verification/verify_hashes.py (2,801 bytes)
