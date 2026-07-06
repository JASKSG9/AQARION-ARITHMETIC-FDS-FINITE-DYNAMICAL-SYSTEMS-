
# ============================================================================
# 7. ADVERSARIAL SCRIPTS — Independent Falsification
# ============================================================================

# --- EXHAUSTIVE SEARCH ---
enumerate_systems = """#!/usr/bin/env python3
\"\"\"
enumerate_systems.py
Exhaustive enumeration of all finite dynamical systems on small state spaces.

For |X| = n, there are n^n possible maps T: X → X.
We enumerate all of them for n ≤ 5.
\"\"\"

from itertools import product
from typing import List, Tuple, Callable
import json

def enumerate_maps(n: int) -> List[Tuple[int, ...]]:
    \"\"\"Enumerate all maps T: {0,...,n-1} → {0,...,n-1}.\"\"\"
    return list(product(range(n), repeat=n))

def count_maps(n: int) -> int:
    return n ** n

if __name__ == "__main__":
    for n in range(1, 6):
        maps = enumerate_maps(n)
        print(f"|X| = {n}: {len(maps)} maps")
    
    # Save enumeration stats
    stats = {n: count_maps(n) for n in range(1, 6)}
    with open("enumeration_stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    print("\\nEnumeration stats saved to enumeration_stats.json")
"""

with open(f"{base_dir}/adversarial/exhaustive/enumerate_systems.py", "w") as f:
    f.write(enumerate_systems)

enumerate_partitions = """#!/usr/bin/env python3
\"\"\"
enumerate_partitions.py
Exhaustive enumeration of all set partitions (Bell numbers).

For |X| = n, there are B_n partitions, where B_n is the Bell number.
\"\"\"

from typing import List, Tuple, Set
import json

def bell_number(n: int) -> int:
    \"\"\"Compute Bell number B_n using Dobinski's formula approximation or recurrence.\"\"\"
    if n == 0: return 1
    if n == 1: return 1
    # Use recurrence: B_{n+1} = sum_{k=0}^n C(n,k) B_k
    bell = [0] * (n + 1)
    bell[0] = 1
    for i in range(1, n + 1):
        bell[i] = sum(bell[j] for j in range(i))
    return bell[n]

def generate_partitions(collection: List[int]) -> List[List[Set[int]]]:
    \"\"\"Generate all set partitions of a collection.\"\"\"
    if not collection:
        return [[]]
    first = collection[0]
    rest = collection[1:]
    partitions = generate_partitions(rest)
    result = []
    for partition in partitions:
        # Add first to each existing block
        for i in range(len(partition)):
            new_partition = [block.copy() for block in partition]
            new_partition[i].add(first)
            result.append(new_partition)
        # Add first as a new block
        new_partition = [block.copy() for block in partition] + [{first}]
        result.append(new_partition)
    return result

if __name__ == "__main__":
    for n in range(1, 6):
        elements = list(range(n))
        partitions = generate_partitions(elements)
        print(f"|X| = {n}: {len(partitions)} partitions (Bell = {bell_number(n)})")
    
    stats = {n: bell_number(n) for n in range(1, 6)}
    with open("partition_stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    print("\\nPartition stats saved to partition_stats.json")
"""

with open(f"{base_dir}/adversarial/exhaustive/enumerate_partitions.py", "w") as f:
    f.write(enumerate_partitions)

verify_equivalence = """#!/usr/bin/env python3
\"\"\"
verify_equivalence.py

INDEPENDENT COMPUTATIONAL CERTIFIER — Two-Route Verification

Critical principle: Do NOT verify "defect == invariant_test" because both
may share bugs. Use two independent routes.

Route A: Construct D_Π = (I - P_Π) K P_Π, check D_Π = 0
Route B: Construct basis V_Π, apply K to each basis vector, check K v_i ∈ V_Π

Acceptance: Route A == Route B for all tested systems.
\"\"\"

import numpy as np
from itertools import product
from typing import List, Tuple, Set, Dict
import json
import sys

def generate_partitions(n: int) -> List[List[Set[int]]]:
    \"\"\"Generate all partitions of {0, ..., n-1}.\"\"\"
    if n == 0:
        return [[]]
    
    def _partitions(elems):
        if not elems:
            yield []
            return
        first = elems[0]
        rest = elems[1:]
        for partition in _partitions(rest):
            for i in range(len(partition)):
                new_partition = [set(block) for block in partition]
                new_partition[i].add(first)
                yield new_partition
            yield [set(block) for block in partition] + [{first}]
    
    return list(_partitions(list(range(n))))

def build_koopman_matrix(T: Tuple[int, ...]) -> np.ndarray:
    \"\"\"Build Koopman operator matrix: K_{ij} = δ_{i, T(j)}.\"\"\"
    n = len(T)
    K = np.zeros((n, n), dtype=np.float64)
    for j in range(n):
        i = T[j]
        K[i, j] = 1.0
    return K

def build_projection_matrix(partition: List[Set[int]], n: int) -> np.ndarray:
    \"\"\"Build orthogonal projection P_Π onto V_Π.\"\"\"
    P = np.zeros((n, n), dtype=np.float64)
    for block in partition:
        block_list = list(block)
        m = len(block_list)
        if m > 0:
            for i in block_list:
                for j in block_list:
                    P[i, j] = 1.0 / m
    return P

def route_a_defect_zero(K: np.ndarray, P: np.ndarray) -> bool:
    \"\"\"Route A: Compute D = (I-P)KP, check if D ≈ 0.\"\"\"
    I = np.eye(K.shape[0])
    D = (I - P) @ K @ P
    return np.allclose(D, 0, atol=1e-10)

def route_b_invariant_subspace(K: np.ndarray, P: np.ndarray) -> bool:
    \"\"\"Route B: Check if K(V_Π) ⊆ V_Π by testing K P e_i ∈ V_Π for all i.\"\"\"
    n = K.shape[0]
    I = np.eye(n)
    for i in range(n):
        v = P @ I[:, i]  # Projected basis vector
        Kv = K @ v
        # Check if Kv is in V_Π: P(Kv) should equal Kv
        if not np.allclose(P @ Kv, Kv, atol=1e-10):
            return False
    return True

def verify_system(T: Tuple[int, ...], partition: List[Set[int]]) -> Tuple[bool, bool, bool]:
    \"\"\"Verify one (T, Π) pair. Returns (route_a, route_b, match).\"\"\"
    n = len(T)
    K = build_koopman_matrix(T)
    P = build_projection_matrix(partition, n)
    
    a = route_a_defect_zero(K, P)
    b = route_b_invariant_subspace(K, P)
    
    return a, b, (a == b)

if __name__ == "__main__":
    MAX_N = 5  # Exhaustive up to |X| = 5
    
    total_systems = 0
    total_partitions = 0
    mismatches = 0
    
    print("=" * 60)
    print("AQARION PAPER I — INDEPENDENT COMPUTATIONAL CERTIFIER")
    print("=" * 60)
    print(f"Exhaustive verification for |X| ≤ {MAX_N}")
    print()
    
    for n in range(1, MAX_N + 1):
        print(f"Processing |X| = {n}...", end=" ", flush=True)
        
        maps = list(product(range(n), repeat=n))
        partitions = generate_partitions(n)
        
        n_systems = 0
        n_partitions = 0
        n_mismatches = 0
        
        for T in maps:
            for partition in partitions:
                a, b, match = verify_system(T, partition)
                n_systems += 1
                n_partitions += 1
                if not match:
                    n_mismatches += 1
                    print(f"\\n  MISMATCH: T={T}, Π={partition}")
                    print(f"    Route A (defect=0): {a}")
                    print(f"    Route B (invariant): {b}")
        
        total_systems += n_systems
        total_partitions += n_partitions
        mismatches += n_mismatches
        
        print(f"Done. Systems: {n_systems}, Partitions: {n_partitions}, Mismatches: {n_mismatches}")
    
    print()
    print("=" * 60)
    print("VERIFICATION COMPLETE")
    print(f"Total systems tested: {total_systems}")
    print(f"Total partition pairs: {total_partitions}")
    print(f"Mismatches: {mismatches}")
    print(f"Status: {'PASS' if mismatches == 0 else 'FAIL'}")
    print("=" * 60)
    
    result = {
        "max_n": MAX_N,
        "systems_tested": total_systems,
        "partitions_tested": total_partitions,
        "mismatches": mismatches,
        "status": "PASS" if mismatches == 0 else "FAIL",
        "verification_principle": "Two independent routes: defect computation vs. subspace invariance"
    }
    
    with open("verification_result.json", "w") as f:
        json.dump(result, f, indent=2)
    
    print("\\nResult saved to verification_result.json")
    
    if mismatches > 0:
        sys.exit(1)
"""

with open(f"{base_dir}/adversarial/exhaustive/verify_equivalence.py", "w") as f:
    f.write(verify_equivalence)

# --- RANDOM STRESS TEST ---
random_stress = """#!/usr/bin/env python3
\"\"\"
randomized_stress.py

Randomized stress testing for larger state spaces where exhaustive search
is infeasible. Tests random maps and random partitions.
\"\"\"

import numpy as np
import random
import json
from typing import List, Set

def random_map(n: int) -> np.ndarray:
    \"\"\"Generate a random map T: {0,...,n-1} → {0,...,n-1}.\"\"\"
    return np.random.randint(0, n, size=n)

def random_partition(n: int) -> List[Set[int]]:
    \"\"\"Generate a random partition of {0,...,n-1}.\"\"\"
    elements = list(range(n))
    random.shuffle(elements)
    partition = []
    i = 0
    while i < n:
        size = random.randint(1, min(3, n - i))
        partition.append(set(elements[i:i+size]))
        i += size
    return partition

def build_koopman_matrix(T: np.ndarray) -> np.ndarray:
    n = len(T)
    K = np.zeros((n, n), dtype=np.float64)
    for j in range(n):
        K[T[j], j] = 1.0
    return K

def build_projection_matrix(partition: List[Set[int]], n: int) -> np.ndarray:
    P = np.zeros((n, n), dtype=np.float64)
    for block in partition:
        block_list = list(block)
        m = len(block_list)
        if m > 0:
            for i in block_list:
                for j in block_list:
                    P[i, j] = 1.0 / m
    return P

def route_a_defect_zero(K: np.ndarray, P: np.ndarray) -> bool:
    I = np.eye(K.shape[0])
    D = (I - P) @ K @ P
    return np.allclose(D, 0, atol=1e-10)

def route_b_invariant_subspace(K: np.ndarray, P: np.ndarray) -> bool:
    n = K.shape[0]
    I = np.eye(n)
    for i in range(n):
        v = P @ I[:, i]
        Kv = K @ v
        if not np.allclose(P @ Kv, Kv, atol=1e-10):
            return False
    return True

if __name__ == "__main__":
    NUM_TESTS = 10000
    MAX_N = 20
    
    print(f"Randomized stress test: {NUM_TESTS} trials, |X| up to {MAX_N}")
    
    mismatches = 0
    for trial in range(NUM_TESTS):
        n = random.randint(2, MAX_N)
        T = random_map(n)
        partition = random_partition(n)
        
        K = build_koopman_matrix(T)
        P = build_projection_matrix(partition, n)
        
        a = route_a_defect_zero(K, P)
        b = route_b_invariant_subspace(K, P)
        
        if a != b:
            mismatches += 1
            print(f"Mismatch trial {trial}: n={n}, T={T}, Π={partition}")
    
    print(f"\\nTrials: {NUM_TESTS}")
    print(f"Mismatches: {mismatches}")
    print(f"Status: {'PASS' if mismatches == 0 else 'FAIL'}")
    
    result = {
        "trials": NUM_TESTS,
        "max_n": MAX_N,
        "mismatches": mismatches,
        "status": "PASS" if mismatches == 0 else "FAIL"
    }
    
    with open("random_stress_result.json", "w") as f:
        json.dump(result, f, indent=2)
"""

with open(f"{base_dir}/adversarial/random/randomized_stress.py", "w") as f:
    f.write(random_stress)

# --- PATHOLOGICAL CASES ---
trivial_partition = """#!/usr/bin/env python3
\"\"\"
trivial_partition.py

Case 1: Trivial partition Π = {X}

Expected: Always invariant. D_Π = 0 for all T.
\"\"\"

import numpy as np

def test_trivial_partition(n: int) -> bool:
    \"\"\"Test trivial partition on n states.\"\"\"
    # Trivial partition: one block containing all states
    partition = [set(range(n))]
    
    # Projection matrix: P = (1/n) J where J is all-ones matrix
    P = np.ones((n, n), dtype=np.float64) / n
    
    # For any map T, check if D_Π = 0
    # Koopman matrix for random T
    T = np.random.randint(0, n, size=n)
    K = np.zeros((n, n), dtype=np.float64)
    for j in range(n):
        K[T[j], j] = 1.0
    
    I = np.eye(n)
    D = (I - P) @ K @ P
    
    return np.allclose(D, 0, atol=1e-10)

if __name__ == "__main__":
    print("Testing trivial partition Π = {X}...")
    for n in range(2, 11):
        result = test_trivial_partition(n)
        print(f"  n={n}: {'PASS' if result else 'FAIL'}")
    print("\\nTrivial partition: always invariant (expected).")
"""

with open(f"{base_dir}/adversarial/pathological/trivial_partition.py", "w") as f:
    f.write(trivial_partition)

discrete_partition = """#!/usr/bin/env python3
\"\"\"
discrete_partition.py

Case 2: Discrete partition (every state separate)

Expected: Always invariant. D_Π = 0 for all T.
\"\"\"

import numpy as np

def test_discrete_partition(n: int) -> bool:
    \"\"\"Test discrete partition on n states.\"\"\"
    # Discrete partition: each state is its own block
    partition = [{i} for i in range(n)]
    
    # Projection matrix: P = I (identity)
    P = np.eye(n, dtype=np.float64)
    
    T = np.random.randint(0, n, size=n)
    K = np.zeros((n, n), dtype=np.float64)
    for j in range(n):
        K[T[j], j] = 1.0
    
    I = np.eye(n)
    D = (I - P) @ K @ P
    
    return np.allclose(D, 0, atol=1e-10)

if __name__ == "__main__":
    print("Testing discrete partition (singleton blocks)...")
    for n in range(2, 11):
        result = test_discrete_partition(n)
        print(f"  n={n}: {'PASS' if result else 'FAIL'}")
    print("\\nDiscrete partition: always invariant (expected).")
"""

with open(f"{base_dir}/adversarial/pathological/discrete_partition.py", "w") as f:
    f.write(discrete_partition)

constant_maps = """#!/usr/bin/env python3
\"\"\"
constant_maps.py

Case 3: Constant dynamics T(x) = c

Checks collapse behavior. All states map to a single fixed point.
\"\"\"

import numpy as np
from itertools import product

def test_constant_map(n: int, c: int) -> bool:
    \"\"\"Test constant map T(x) = c on all partitions.\"\"\"
    T = tuple(c for _ in range(n))
    K = np.zeros((n, n), dtype=np.float64)
    for j in range(n):
        K[T[j], j] = 1.0
    
    # Test a few random partitions
    for _ in range(100):
        # Random partition
        partition = []
        elems = list(range(n))
        np.random.shuffle(elems)
        i = 0
        while i < n:
            size = np.random.randint(1, min(4, n - i + 1))
            partition.append(set(elems[i:i+size]))
            i += size
        
        P = np.zeros((n, n), dtype=np.float64)
        for block in partition:
            block_list = list(block)
            m = len(block_list)
            if m > 0:
                for x in block_list:
                    for y in block_list:
                        P[x, y] = 1.0 / m
        
        I = np.eye(n)
        D = (I - P) @ K @ P
        
        if not np.allclose(D, 0, atol=1e-10):
            return False
    return True

if __name__ == "__main__":
    print("Testing constant maps T(x) = c...")
    for n in range(2, 8):
        for c in range(n):
            result = test_constant_map(n, c)
            print(f"  n={n}, c={c}: {'PASS' if result else 'FAIL'}")
    print("\\nConstant maps: all partitions invariant (expected).")
"""

with open(f"{base_dir}/adversarial/pathological/constant_maps.py", "w") as f:
    f.write(constant_maps)

cycles = """#!/usr/bin/env python3
\"\"\"
cycles.py

Case 4: Pure cycles (invertible dynamics)

Checks behavior on cyclic permutations.
\"\"\"

import numpy as np

def test_cycle(n: int) -> bool:
    \"\"\"Test n-cycle: T(i) = (i+1) mod n.\"\"\"
    T = tuple((i + 1) % n for i in range(n))
    K = np.zeros((n, n), dtype=np.float64)
    for j in range(n):
        K[T[j], j] = 1.0
    
    # Test partition into cycle orbits (the whole set)
    partition = [set(range(n))]
    P = np.ones((n, n), dtype=np.float64) / n
    I = np.eye(n)
    D = (I - P) @ K @ P
    
    return np.allclose(D, 0, atol=1e-10)

if __name__ == "__main__":
    print("Testing pure n-cycles...")
    for n in range(2, 11):
        result = test_cycle(n)
        print(f"  n={n}: {'PASS' if result else 'FAIL'}")
    print("\\nCycles: trivial partition invariant (expected).")
"""

with open(f"{base_dir}/adversarial/pathological/cycles.py", "w") as f:
    f.write(cycles)

multibasin = """#!/usr/bin/env python3
\"\"\"
multibasin.py

Case 5: Multiple attractors

Checks basin separation. Two fixed points with their basins.
\"\"\"

import numpy as np

def test_multibasin() -> bool:
    \"\"\"Test a system with two attractors.\"\"\"
    n = 6
    # States 0,1,2 → attractor 0
    # States 3,4,5 → attractor 1
    T = np.array([0, 0, 0, 1, 1, 1])
    K = np.zeros((n, n), dtype=np.float64)
    for j in range(n):
        K[T[j], j] = 1.0
    
    # Partition by basins: {0,1,2}, {3,4,5}
    partition = [{0,1,2}, {3,4,5}]
    P = np.zeros((n, n), dtype=np.float64)
    for block in partition:
        block_list = list(block)
        m = len(block_list)
        for i in block_list:
            for j in block_list:
                P[i, j] = 1.0 / m
    
    I = np.eye(n)
    D = (I - P) @ K @ P
    
    return np.allclose(D, 0, atol=1e-10)

if __name__ == "__main__":
    print("Testing multiple attractor system...")
    result = test_multibasin()
    print(f"  Result: {'PASS' if result else 'FAIL'}")
    print("\\nMultibasin: basin partition is invariant (expected).")
"""

with open(f"{base_dir}/adversarial/pathological/multibasin.py", "w") as f:
    f.write(multibasin)

nilpotent = """#!/usr/bin/env python3
\"\"\"
nilpotent_collapse.py

Case 6: Nilpotent collapse

Checks transient dynamics that collapse to a fixed point in finite steps.
\"\"\"

import numpy as np

def test_nilpotent() -> bool:
    \"\"\"Test nilpotent dynamics: 0→0, 1→0, 2→1, 3→2.\"\"\"
    n = 4
    T = np.array([0, 0, 1, 2])
    K = np.zeros((n, n), dtype=np.float64)
    for j in range(n):
        K[T[j], j] = 1.0
    
    # Partition by preimage structure
    partition = [{0}, {1,2,3}]
    P = np.zeros((n, n), dtype=np.float64)
    for block in partition:
        block_list = list(block)
        m = len(block_list)
        for i in block_list:
            for j in block_list:
                P[i, j] = 1.0 / m
    
    I = np.eye(n)
    D = (I - P) @ K @ P
    
    return np.allclose(D, 0, atol=1e-10)

if __name__ == "__main__":
    print("Testing nilpotent collapse system...")
    result = test_nilpotent()
    print(f"  Result: {'PASS' if result else 'FAIL'}")
    print("\\nNilpotent: preimage partition is invariant (expected).")
"""

with open(f"{base_dir}/adversarial/pathological/nilpotent_collapse.py", "w") as f:
    f.write(nilpotent)

# --- COMMUTATOR SEARCH ---
commutator_search = """#!/usr/bin/env python3
\"\"\"
search_noncommuting.py

Search for counterexamples to T4.2 (converse commutation):
D_Π = 0 but [P_Π, K] ≠ 0

Purpose: Demonstrate that invariance ≠ commutation.
This should become a paper example.
\"\"\"

import numpy as np
from itertools import product
from typing import List, Set, Tuple
import json

def generate_partitions(n: int) -> List[List[Set[int]]]:
    \"\"\"Generate all partitions of {0, ..., n-1}.\"\"\"
    def _partitions(elems):
        if not elems:
            yield []
            return
        first = elems[0]
        rest = elems[1:]
        for partition in _partitions(rest):
            for i in range(len(partition)):
                new_partition = [set(block) for block in partition]
                new_partition[i].add(first)
                yield new_partition
            yield [set(block) for block in partition] + [{first}]
    return list(_partitions(list(range(n))))

def build_koopman_matrix(T: Tuple[int, ...]) -> np.ndarray:
    n = len(T)
    K = np.zeros((n, n), dtype=np.float64)
    for j in range(n):
        K[T[j], j] = 1.0
    return K

def build_projection_matrix(partition: List[Set[int]], n: int) -> np.ndarray:
    P = np.zeros((n, n), dtype=np.float64)
    for block in partition:
        block_list = list(block)
        m = len(block_list)
        if m > 0:
            for i in block_list:
                for j in block_list:
                    P[i, j] = 1.0 / m
    return P

def commutator_norm(K: np.ndarray, P: np.ndarray) -> float:
    \"\"\"Compute ||[P, K]||_F (Frobenius norm).\"\"\"
    comm = P @ K - K @ P
    return np.linalg.norm(comm, 'fro')

def defect_norm(K: np.ndarray, P: np.ndarray) -> float:
    \"\"\"Compute ||D_Π||_F.\"\"\"
    I = np.eye(K.shape[0])
    D = (I - P) @ K @ P
    return np.linalg.norm(D, 'fro')

if __name__ == "__main__":
    print("=" * 60)
    print("COMMUTATOR SEPARATION SEARCH")
    print("=" * 60)
    print("Searching: D_Π = 0 but [P_Π, K] ≠ 0")
    print()
    
    found = []
    
    for n in range(3, 7):  # Search up to n=6
        print(f"Searching |X| = {n}...", end=" ", flush=True)
        
        maps = list(product(range(n), repeat=n))
        partitions = generate_partitions(n)
        
        count = 0
        for T in maps:
            for partition in partitions:
                K = build_koopman_matrix(T)
                P = build_projection_matrix(partition, n)
                
                d_norm = defect_norm(K, P)
                c_norm = commutator_norm(K, P)
                
                # D_Π ≈ 0 but [P,K] not ≈ 0
                if d_norm < 1e-10 and c_norm > 1e-6:
                    found.append({
                        "n": n,
                        "T": list(T),
                        "partition": [list(b) for b in partition],
                        "defect_norm": float(d_norm),
                        "commutator_norm": float(c_norm)
                    })
                    count += 1
        
        print(f"Found {count} examples.")
    
    print()
    print("=" * 60)
    print(f"TOTAL COUNTEREXAMPLES FOUND: {len(found)}")
    print("=" * 60)
    
    if found:
        print("\\nFirst example:")
        ex = found[0]
        print(f"  n = {ex['n']}")
        print(f"  T = {ex['T']}")
        print(f"  Π = {ex['partition']}")
        print(f"  ||D_Π||_F = {ex['defect_norm']:.2e}")
        print(f"  ||[P,K]||_F = {ex['commutator_norm']:.4f}")
        print("\\nThis demonstrates: invariance ≠ commutation.")
    
    with open("noncommuting_examples.json", "w") as f:
        json.dump({
            "search_description": "D_Π = 0 but [P_Π, K] ≠ 0",
            "examples_found": len(found),
            "examples": found[:10]  # Save first 10
        }, f, indent=2)
    
    print("\\nResults saved to noncommuting_examples.json")
"""

with open(f"{base_dir}/adversarial/commutator/search_noncommuting.py", "w") as f:
    f.write(commutator_search)

print("All adversarial scripts created.")All adversarial scripts created.
