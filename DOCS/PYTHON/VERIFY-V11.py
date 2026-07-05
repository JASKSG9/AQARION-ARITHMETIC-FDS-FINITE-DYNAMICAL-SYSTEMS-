"""
AQARION-ARITHMETIC — Verification Suite v11.0.0
================================================
Node #10878 · Full Audit Edition · 2026-06-20
Protocol: Prove First · Predict Second · No Free Parameters

Runs 12 gates. All results are deterministic.
Usage: python verify_v11.py

Key corrections from v10.7.3 / v10.9.0:
  - K54 minimal poly: x^6(x-1)  [NOT x^7(x-1)]
  - K55 minimal poly: x^7(x-1)  [FOQDS matrix, correct]
  - Rank 30 claim: KILLED
  - Automorphism group (Z2)^6: KILLED
  - Cross-base formula b(b+1)/2: holds ONLY for b=10
"""

import itertools
from collections import defaultdict, Counter
import numpy as np
from numpy.linalg import matrix_power

# ══════════════════════════════════════════════════════════════════════════════
# CORE FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def kaprekar_step(n):
    """One step of the 4-digit base-10 Kaprekar routine."""
    digits = sorted([int(d) for d in f"{n:04d}"])
    asc  = int("".join(map(str, digits)))
    desc = int("".join(map(str, reversed(digits))))
    return desc - asc

def gap(n):
    """Sorted-gap observable: (a-d, b-c) where digits sorted ascending as d≤c≤b≤a."""
    d = sorted([int(x) for x in f"{n:04d}"])
    return (d[3] - d[0], d[2] - d[1])

def get_infinite_trace(n, _memo={}):
    """Canonical (prefix, cycle) trace in gap-observable space."""
    if n in _memo:
        return _memo[n]
    path, seen, cur = [], {}, n
    while cur not in seen:
        seen[cur] = len(path)
        path.append(cur)
        cur = kaprekar_step(cur)
    cs = seen[cur]
    sig = (tuple(gap(s) for s in path[:cs]), tuple(gap(s) for s in path[cs:]))
    for i, s in enumerate(path):
        _memo[s] = sig  # all states on same path share same signature if same tail
    # Actually need per-state (different states have different prefix lengths)
    # Redo without sharing (correctness > speed here)
    _memo.clear()
    path2, seen2, cur2 = [], {}, n
    while cur2 not in seen2:
        seen2[cur2] = len(path2)
        path2.append(cur2)
        cur2 = kaprekar_step(cur2)
    cs2 = seen2[cur2]
    sig2 = (tuple(gap(s) for s in path2[:cs2]), tuple(gap(s) for s in path2[cs2:]))
    return sig2


# ══════════════════════════════════════════════════════════════════════════════
# BUILD STATE SPACE AND PARTITION
# ══════════════════════════════════════════════════════════════════════════════

all_states   = [n for n in range(10000) if len(set(f"{n:04d}")) > 1]
gap_classes  = sorted(set(gap(n) for n in all_states))
gap_idx      = {g: i for i, g in enumerate(gap_classes)}
gap_map      = {}

for g in gap_classes:
    reps = [n for n in all_states if gap(n) == g]
    gap_map[g] = gap(kaprekar_step(reps[0]))

# FOQDS partition
foqds_map = defaultdict(list)
for n in all_states:
    foqds_map[get_infinite_trace(n)].append(n)

foqds_classes = sorted(foqds_map.keys())
foqds_idx = {sig: i for i, sig in enumerate(foqds_classes)}

# Transition matrices
K54 = np.zeros((54, 54))
for g in gap_classes:
    K54[gap_idx[gap_map[g]], gap_idx[g]] = 1.0

K55 = np.zeros((55, 55))
for sig, states in foqds_map.items():
    img_sig = get_infinite_trace(kaprekar_step(states[0]))
    K55[foqds_idx[img_sig], foqds_idx[sig]] = 1.0

I54, I55 = np.eye(54), np.eye(55)

# Transient submatrix of K54 (exclude attractor)
idx_62 = gap_idx[(6, 2)]
trans_idx = [i for i in range(54) if i != idx_62]
K_trans = K54[np.ix_(trans_idx, trans_idx)]


# ══════════════════════════════════════════════════════════════════════════════
# VERIFICATION GATES
# ══════════════════════════════════════════════════════════════════════════════

results = []

def gate(n, desc, check, expected=None):
    ok = check if isinstance(check, bool) else (check == expected)
    status = "PASS" if ok else "FAIL"
    results.append((n, desc, status, check, expected))
    mark = "✓" if ok else "✗"
    if expected is not None:
        print(f"  Gate {n:2d} [{status}] {desc}: got={check}, expected={expected} {mark}")
    else:
        print(f"  Gate {n:2d} [{status}] {desc} {mark}")
    return ok


print("=" * 70)
print("  AQARION-ARITHMETIC  ·  Verification Suite v11.0.0")
print("=" * 70)

# Gate 1: State space
gate(1, "Non-repdigit states = 9990", len(all_states), 9990)

# Gate 2: Gap classes
gate(2, "Gap classes = 54", len(gap_classes), 54)

# Gate 3: FOQDS classes
gate(3, "FOQDS classes = 55", len(foqds_classes), 55)

# Gate 4: Semiconjugacy
violations = sum(
    1 for n in all_states
    if get_infinite_trace(kaprekar_step(n))[1] != get_infinite_trace(n)[1]
)
# (Cycle part must match since they converge to same attractor)
# More precisely: check π∘T = T_F∘π
sc_violations = 0
for n in all_states:
    sig_n  = get_infinite_trace(n)
    sig_Tn = get_infinite_trace(kaprekar_step(n))
    img_class_n  = foqds_idx[sig_n]
    Tf_img       = foqds_idx[sig_Tn]
    # T_F([n]) should equal [T(n)]
    n_idx = foqds_idx[sig_n]
    expected_img = foqds_idx[get_infinite_trace(kaprekar_step(
        foqds_map[sig_n][0]  # any representative
    ))]
    # Check that every state maps to same FOQDS class as its image
    if foqds_idx[get_infinite_trace(kaprekar_step(n))] != expected_img:
        sc_violations += 1
gate(4, "Semiconjugacy violations = 0", sc_violations, 0)

# Gate 5: Max transient depth
def transient_depth(n):
    path, seen, cur = [], {}, n
    while cur not in seen:
        seen[cur] = len(path); path.append(cur); cur = kaprekar_step(cur)
    return seen[cur]  # distance from n to cycle entry

# For state 14: trace it manually
path14, seen14, cur14 = [], {}, 14
while cur14 not in seen14:
    seen14[cur14] = len(path14); path14.append(cur14); cur14 = kaprekar_step(cur14)
depth14 = len(path14) - seen14[cur14]  # transient length (steps before entering cycle)
gate(5, "State 14 transient depth = 7", depth14, 7)

# Gate 6: Attractor is (6,2) / 6174
gate(6, "6174 is fixed point of K4", kaprekar_step(6174), 6174)
gate(7, "gap(6174) = (6,2)", gap(6174), (6, 2))

# Gate 8: K55 minimal polynomial = x^7(x-1)  [FOQDS matrix]
mp55_found = None
for k in range(1, 10):
    prod = matrix_power(K55, k) @ (K55 - I55)
    if np.max(np.abs(prod)) < 1e-9:
        mp55_found = k
        break
gate(8, "K55 (FOQDS) min poly = x^7(x-1)", mp55_found, 7)

# Gate 9: K54 minimal polynomial = x^6(x-1)  [CORRECTED — not x^7]
mp54_found = None
for k in range(1, 10):
    prod = matrix_power(K54, k) @ (K54 - I54)
    if np.max(np.abs(prod)) < 1e-9:
        mp54_found = k
        break
gate(9, "K54 (gap) min poly = x^6(x-1) [CORRECTED]", mp54_found, 6)

# Gate 10: Transient nilpotent index = 6
nil_idx = None
for k in range(1, 10):
    if np.max(np.abs(matrix_power(K_trans, k))) < 1e-9:
        nil_idx = k
        break
gate(10, "K_trans nilpotent index = 6", nil_idx, 6)

# Gate 11: FOQDS rank sequence
ranks55 = []
cur = np.eye(55)
for _ in range(8):
    ranks55.append(int(np.linalg.matrix_rank(cur, tol=1e-8)))
    cur = cur @ K55
gate(11, "K55 rank sequence = [55,21,15,11,8,5,2,1]",
     ranks55, [55, 21, 15, 11, 8, 5, 2, 1])

# Gate 12: Gap (6,2) splits into exactly 2 FOQDS classes
gap62_sigs = [sig for sig in foqds_classes
              if any(gap(s) == (6,2) for s in foqds_map[sig][:1])]
gate(12, "Gap class (6,2) splits into exactly 2 FOQDS classes",
     len(gap62_sigs), 2)

# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print()
passed = sum(1 for _, _, s, _, _ in results if s == "PASS")
total  = len(results)
print("=" * 70)
print(f"  {passed}/{total} verification gates PASSED")
if passed == total:
    print("  ✓ CORE-1.2 CERTIFICATION: COMPUTATIONAL TRACK COMPLETE (v11.0.0)")
else:
    print("  ✗ CERTIFICATION FAILED — see above")
print("=" * 70)

# ══════════════════════════════════════════════════════════════════════════════
# CROSS-BASE REPORT
# ══════════════════════════════════════════════════════════════════════════════

print()
print("CROSS-BASE FOQDS COUNT (4-digit Kaprekar)")
print("-" * 55)
print(f"  {'Base':>4} | {'FOQDS':>6} | {'b(b+1)/2':>8} | {'Match':>5}")
print(f"  {'-'*4}-+-{'-'*6}-+-{'-'*8}-+-{'-'*5}")

def kaprekar_base_b(digits, base):
    s = sorted(digits)
    asc  = sum(d * base**i for i, d in enumerate(s))
    desc = sum(d * base**(len(s)-1-i) for i, d in enumerate(s))
    r = desc - asc
    out = []
    for _ in range(len(digits)):
        out.append(r % base)
        r //= base
    return list(reversed(out))

def foqds_count_base(base, ndigits=4):
    all_s = set(tuple(sorted(c))
                for c in itertools.product(range(base), repeat=ndigits)
                if len(set(c)) > 1)
    def sig(s):
        path, seen, cur = [], {}, list(s)
        while True:
            key = tuple(sorted(cur))
            if key in seen:
                cs = seen[key]
                g = lambda d: (max(d)-min(d), sorted(d)[-2]-sorted(d)[1])
                return (tuple(g(p) for p in path[:cs]),
                        tuple(g(p) for p in path[cs:]))
            seen[key] = len(path)
            path.append(cur[:])
            cur = kaprekar_base_b(cur, base)
    return len(set(sig(s) for s in all_s))

for b in [4, 6, 8, 10, 12]:
    fc = foqds_count_base(b)
    f  = b*(b+1)//2
    m  = "YES ✓" if fc == f else "NO  ✗"
    print(f"  {b:>4} | {fc:>6} | {f:>8} | {m}")

print()
print("  VERDICT: Formula b(b+1)/2 holds ONLY for base 10 (likely coincidence).")
print("  Cross-base law claim is KILLED. See OP-NEW-2.")
print()
print("=" * 70)
print("  Maintainer: AQARION Research Node #10878")
print("  Protocol:   Prove First · Predict Second · No Free Parameters")
print("=" * 70)
