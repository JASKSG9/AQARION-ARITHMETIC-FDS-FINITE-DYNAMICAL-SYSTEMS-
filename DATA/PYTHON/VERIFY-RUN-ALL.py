#!/usr/bin/env python3
"""
AQARION Test Suite v3.0 — Production Grade
Node #10878 | 2026‑07‑05

Convention: PULLBACK Koopman, K[i, T[i]] = 1  (Kf)(x) = f(T(x))
This is the unique convention for which D=0 ⟺ congruence holds exactly.
"""
import sys, argparse
from itertools import product as iprod
from typing import List, Dict, Tuple
import numpy as np

# ═══════════════════════════════════════════════════════════════
# CORE OPERATORS
# ═══════════════════════════════════════════════════════════════
def koopman(T: List[int]) -> np.ndarray:
    """Pullback Koopman: K[i, T[i]] = 1."""
    n = len(T)
    K = np.zeros((n, n))
    for i, t in enumerate(T):
        K[i, t] = 1.0
    return K

def projection(blocks: List[List[int]], n: int) -> np.ndarray:
    """Orthogonal averaging projection onto functions constant on each block."""
    P = np.zeros((n, n))
    for block in blocks:
        s = len(block)
        for i in block:
            for j in block:
                P[i, j] = 1.0 / s
    return P

def obstruction(P: np.ndarray, K: np.ndarray) -> np.ndarray:
    """D = (I − P) K P"""
    return (np.eye(P.shape[0]) - P) @ K @ P

def commutator(P: np.ndarray, K: np.ndarray) -> np.ndarray:
    """C = PK − KP"""
    return P @ K - K @ P

def is_zero(A: np.ndarray, tol: float = 1e-10) -> bool:
    return float(np.max(np.abs(A))) < tol

# ═══════════════════════════════════════════════════════════════
# PARTITION UTILITIES
# ═══════════════════════════════════════════════════════════════
def all_partitions(n: int):
    if n == 0:
        yield []
        return
    def helper(remaining, current):
        if not remaining:
            yield [b[:] for b in current]
            return
        first = remaining[0]
        rest  = remaining[1:]
        for i, block in enumerate(current):
            new = [b[:] for b in current]
            new[i].append(first)
            yield from helper(rest, new)
        yield from helper(rest, current + [[first]])
    yield from helper(list(range(1, n)), [[0]])

def label_vector(partition: List[List[int]], n: int) -> List[int]:
    labels = [0] * n
    for idx, block in enumerate(partition):
        for x in block:
            labels[x] = idx
    return labels

def is_congruence(T: List[int], partition: List[List[int]]) -> bool:
    lab = label_vector(partition, len(T))
    for block in partition:
        imgs = {lab[T[x]] for x in block}
        if len(imgs) > 1:
            return False
    return True

# ═══════════════════════════════════════════════════════════════
# KAPREKAR 55‑STATE FIXTURE
# ═══════════════════════════════════════════════════════════════
def kaprekar_step(n: int) -> int:
    s = f"{n:04d}"
    return int("".join(sorted(s, reverse=True))) - int("".join(sorted(s)))

def gap_pair(n: int) -> Tuple[int, int]:
    d = sorted(int(c) for c in f"{n:04d}")
    return (d[3] - d[0], d[2] - d[1])

def build_55_transition() -> List[int]:
    pairs = [(gb, gs) for gb in range(10) for gs in range(gb + 1)]
    idx   = {p: i for i, p in enumerate(pairs)}
    fibers: Dict = {}
    for n in range(10000):
        g = gap_pair(n)
        fibers.setdefault(g, n)
    return [idx[gap_pair(kaprekar_step(fibers[p]))] for p in pairs]

def nullity_seq(K: np.ndarray, max_h: int = 12) -> List[int]:
    n, seq, Kh = K.shape[0], [0], np.eye(K.shape[0])
    for h in range(1, max_h + 1):
        Kh = Kh @ K
        seq.append(n - int(np.linalg.matrix_rank(Kh, tol=1e-10)))
        if h > 1 and seq[-1] == seq[-2]:
            while len(seq) < max_h + 1:
                seq.append(seq[-1])
            break
    return seq

def jordan_from_nullity(nulls: List[int]) -> Dict[int, int]:
    blocks = {}
    for k in range(1, len(nulls) - 1):
        v = 2 * nulls[k] - nulls[k-1] - nulls[k+1]
        if v > 0:
            blocks[k] = int(v)
    return blocks

KAPREKAR_FIXTURE = {
    "n":               55,
    "nullity_sequence":[0, 34, 40, 44, 47, 50, 53, 53],
    "jordan_blocks":   {1: 28, 2: 2, 3: 1, 6: 3},
    "fixed_points":    2,
    "nilpotent_index": 6,
}

# ═══════════════════════════════════════════════════════════════
# TESTS — LAYER 1: ALGEBRAIC INVARIANTS
# ═══════════════════════════════════════════════════════════════
def test_projection_axioms() -> Tuple[bool, str]:
    np.random.seed(42)
    for _ in range(30):
        n = np.random.randint(2, 9)
        labels = list(np.random.randint(0, max(1, n // 2 + 1), size=n))
        bd: Dict = {}
        for i, l in enumerate(labels):
            bd.setdefault(int(l), []).append(i)
        P = projection(list(bd.values()), n)
        if not np.allclose(P @ P, P):
            return False, f"P² ≠ P for n={n}"
        if not np.allclose(P.T, P):
            return False, f"Pᵀ ≠ P for n={n}"
    return True, "P² = P and Pᵀ = P (30 random partitions)"

def test_structural_identities() -> Tuple[bool, str]:
    fail = {"PD=0": 0, "D(I-P)=0": 0, "DP=D": 0, "D2=0": 0}
    for n in range(1, 4):
        for T in iprod(range(n), repeat=n):
            T = list(T)
            K = koopman(T)
            I = np.eye(n)
            for part in all_partitions(n):
                P = projection(part, n)
                D = obstruction(P, K)
                if not is_zero(P @ D):            fail["PD=0"]    += 1
                if not is_zero(D @ (I - P)):      fail["D(I-P)=0"]+= 1
                if not np.allclose(D @ P, D):     fail["DP=D"]    += 1
                if not is_zero(D @ D):            fail["D2=0"]    += 1
    ok = all(v == 0 for v in fail.values())
    return ok, f"All four identities: {fail}"

def test_koopman_consistency() -> Tuple[bool, str]:
    np.random.seed(43)
    for _ in range(50):
        n = np.random.randint(2, 8)
        T = [int(v) for v in np.random.randint(0, n, size=n)]
        K = koopman(T)
        f = np.random.randn(n)
        expected = np.array([f[T[i]] for i in range(n)])
        if not np.allclose(K @ f, expected):
            return False, f"K@f != f∘T for T={T}"
    return True, "K@f == f∘T (50 random maps, pullback convention)"

def test_commutator_fallacy() -> Tuple[bool, str]:
    T = [4, 1, 3, 3, 4, 1]
    partition = [[0, 4], [1], [2, 3], [5]]
    n = 6
    K = koopman(T)
    P = projection(partition, n)
    D = obstruction(P, K)
    C = commutator(P, K)
    d_zero = is_zero(D)
    c_zero = is_zero(C)
    if not d_zero:
        return False, f"Witness has D≠0 (norm={np.linalg.norm(D,'fro'):.2e})"
    if c_zero:
        return False, "Witness has [P,K]=0 — fallacy not demonstrated"
    return True, f"D=0 (norm={np.linalg.norm(D,'fro'):.1e}) but [P,K]≠0 (norm={np.linalg.norm(C,'fro'):.3f})"

# ═══════════════════════════════════════════════════════════════
# TESTS — LAYER 2: DYNAMICAL EXPERIMENTS
# ═══════════════════════════════════════════════════════════════
def test_D0_iff_congruence_exhaustive() -> Tuple[bool, str]:
    mismatches = 0
    total = 0
    for n in range(1, 5):
        for T in iprod(range(n), repeat=n):
            T = list(T)
            K = koopman(T)
            for part in all_partitions(n):
                P = projection(part, n)
                D = obstruction(P, K)
                if is_zero(D) != is_congruence(T, part):
                    mismatches += 1
                total += 1
    ok = mismatches == 0
    return ok, f"D=0 ⟺ congruence: {total} cases, {mismatches} mismatches (pullback K)"

def test_pushforward_breaks_biconditional() -> Tuple[bool, str]:
    mismatches = 0
    for n in range(1, 5):
        for T in iprod(range(n), repeat=n):
            T = list(T)
            K_push = np.zeros((n, n))
            for j, t in enumerate(T):
                K_push[t, j] = 1.0
            for part in all_partitions(n):
                P = projection(part, n)
                D = obstruction(P, K_push)
                if is_zero(D) != is_congruence(T, part):
                    mismatches += 1
    ok = mismatches > 0
    return ok, f"Push‑forward K has {mismatches} D=0⟺cong violations → confirms pullback is canonical"

def test_random_map_stress() -> Tuple[bool, str]:
    np.random.seed(44)
    failures = 0
    for trial in range(1000):
        n = 8
        T = [int(v) for v in np.random.randint(0, n, size=n)]
        K = koopman(T)
        labels = list(np.random.randint(0, max(1, n // 3 + 1), size=n))
        bd: Dict = {}
        for i, l in enumerate(labels):
            bd.setdefault(int(l), []).append(i)
        partition = list(bd.values())
        P = projection(partition, n)
        D = obstruction(P, K)
        if is_zero(D) != is_congruence(T, partition):
            failures += 1
    ok = failures == 0
    return ok, f"Random maps: 1000 trials, {failures} failures"

def test_kaprekar_fixture() -> Tuple[bool, str]:
    T  = build_55_transition()
    n  = len(T)
    K  = koopman(T)
    nulls  = nullity_seq(K, max_h=12)
    jordan = jordan_from_nullity(nulls)
    fpts   = sum(1 for i, t in enumerate(T) if t == i)
    fx = KAPREKAR_FIXTURE
    ok = (n == fx["n"] and
          nulls[:len(fx["nullity_sequence"])] == fx["nullity_sequence"] and
          jordan == fx["jordan_blocks"] and
          fpts == fx["fixed_points"])
    return ok, f"n={n}, nullity={nulls[:8]}, Jordan={jordan}, fixed_pts={fpts}"

def test_kaprekar_basin() -> Tuple[bool, str]:
    depths = []
    for n in range(10000):
        x, d = n, 0
        seen = set()
        while x not in seen:
            seen.add(x)
            if x == 0 or x == 6174:
                break
            x = kaprekar_step(x)
            d += 1
            if d > 10:
                break
        depths.append(d if x in (0, 6174) else 99)
    max_depth = max(depths)
    all_reach = max_depth <= 7
    return all_reach, f"Max depth={max_depth}, all 10000 reach {{0,6174}}"

def test_gap_fiber_lumpability() -> Tuple[bool, str]:
    fibers: Dict = {}
    for n in range(10000):
        g = gap_pair(n)
        fibers.setdefault(g, []).append(n)
    violations = 0
    for g, states in fibers.items():
        next_gaps = {gap_pair(kaprekar_step(s)) for s in states}
        if len(next_gaps) > 1:
            violations += 1
    ok = violations == 0
    return ok, f"55 fibers, {violations} violations of lumpability"

# ═══════════════════════════════════════════════════════════════
# TESTS — LAYER 3: SPECTRAL STABILITY
# ═══════════════════════════════════════════════════════════════
def test_nullity_monotone() -> Tuple[bool, str]:
    np.random.seed(46)
    for _ in range(50):
        n = np.random.randint(2, 8)
        T = [int(v) for v in np.random.randint(0, n, size=n)]
        K = koopman(T)
        nulls = nullity_seq(K, max_h=8)
        for i in range(1, len(nulls)):
            if nulls[i] < nulls[i-1]:
                return False, f"Nullity decreased: {nulls}"
    return True, "Non‑decreasing nullity: 50 random pullback systems"

def test_jordan_reconstruction() -> Tuple[bool, str]:
    np.random.seed(47)
    for _ in range(30):
        n = np.random.randint(2, 10)
        J = np.random.randn(n, n) * 0.1
        for i in range(n):
            for j in range(i+1):
                J[i, j] = 0
        nulls = [0]
        Jh = np.eye(n)
        for h in range(1, n+2):
            Jh = Jh @ J
            nulls.append(n - int(np.linalg.matrix_rank(Jh, tol=1e-8)))
            if h > 1 and nulls[-1] == nulls[-2]:
                while len(nulls) < n+2:
                    nulls.append(nulls[-1])
                break
        blocks = jordan_from_nullity(nulls)
        total = sum(k * v for k, v in blocks.items())
        if total > n:
            return False, f"Jordan reconstruction failed: total={total}, n={n}"
    return True, "Jordan reconstruction: 30 random nilpotent matrices"

# ═══════════════════════════════════════════════════════════════
# RUNNER
# ═══════════════════════════════════════════════════════════════
ALL_TESTS = [
    ("projection_axioms", test_projection_axioms),
    ("structural_identities (4 laws)", test_structural_identities),
    ("koopman_consistency", test_koopman_consistency),
    ("commutator_fallacy (witness)", test_commutator_fallacy),
    ("D=0⟺congruence exhaustive n≤4", test_D0_iff_congruence_exhaustive),
    ("pushforward_breaks_biconditional", test_pushforward_breaks_biconditional),
    ("random_map_stress", test_random_map_stress),
    ("kaprekar_55_fixture", test_kaprekar_fixture),
    ("kaprekar_basin", test_kaprekar_basin),
    ("gap_fiber_lumpability", test_gap_fiber_lumpability),
    ("nullity_monotone", test_nullity_monotone),
    ("jordan_reconstruction", test_jordan_reconstruction),
]

def run(skip_slow: bool = False) -> bool:
    print("\n🧪  AQARION Test Suite v3.0  —  Node #10878")
    print("    Convention: pullback K, K[i,T[i]]=1, (Kf)(x)=f(T(x))")
    print("=" * 62)
    passed = True
    for label, fn in ALL_TESTS:
        if skip_slow and "exhaustive" in label:
            print(f"⏭   SKIP: {label}")
            continue
        try:
            ok, msg = fn()
            print(f"{'✅' if ok else '❌'}  {label}")
            print(f"    {msg}")
            if not ok:
                passed = False
        except Exception as e:
            import traceback
            print(f"⚠️  ERROR: {label}")
            traceback.print_exc()
            passed = False
    print("=" * 62)
    print(f"  {'ALL PASS ✅' if passed else 'FAILURES ❌'}")
    return passed

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fast", action="store_true")
    args = parser.parse_args()
    sys.exit(0 if run(skip_slow=args.fast) else 1)
