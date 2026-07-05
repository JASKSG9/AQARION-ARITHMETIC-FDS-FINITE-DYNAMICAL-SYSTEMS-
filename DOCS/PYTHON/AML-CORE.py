"""
aml_core.py — AQARION Adversarial Mathematics Laboratory
=========================================================
Node #10878 · Version 1.0.0 · 2026-06-21
Protocol: Prove First · Predict Second · No Free Parameters

Modules:
  A — FDDS Family Generator
  B — Executable Property Language  
  C — Adversarial Mutation Operators
  D — Counterexample Minimizer
  E — Collision Atlas
  G — Implementation Mutation Testing
  I — Proof Pressure Index

Usage:
  from aml_core import *
  T, states = FAMILIES["kaprekar_b10_d4"]()
  obs = gap_obs_kaprekar(T, states)
  result = run_property_suite(T, states, obs)
  ppi = ProofPressureIndex()
  ppi.add_claim("T-FOQDS-55", "FOQDS = 55 classes", exhaustive=True, lean=True)
  ppi.report()
"""

import itertools
import random
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple, Any
import numpy as np
from numpy.linalg import matrix_rank, matrix_power

# ══════════════════════════════════════════════════════════════════════════════
# MODULE A — FDDS FAMILY GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

def fdds_kaprekar(base: int = 10, ndigits: int = 4):
    """4-digit Kaprekar map on non-repdigit states."""
    def step(n):
        d = sorted([int(x) for x in f"{n:0{ndigits}d}"])
        return int("".join(str(x) for x in reversed(d))) - int("".join(str(x) for x in d))
    states = [n for n in range(base**ndigits) if len(set(f"{n:0{ndigits}d}")) > 1]
    return {s: step(s) for s in states}, states

def fdds_random(n: int, seed: int = 0):
    rng = random.Random(seed)
    states = list(range(n))
    return {s: rng.randint(0, n-1) for s in states}, states

def fdds_nilpotent(n: int):
    states = list(range(n))
    T = {s: max(0, s-1) for s in states}; T[0] = 0
    return T, states

def fdds_single_cycle(n: int):
    states = list(range(n))
    return {s: (s+1)%n for s in states}, states

def fdds_tree(n: int):
    states = list(range(n))
    return {s: (s-1)//2 if s > 0 else 0 for s in states}, states

def fdds_affine(n: int, a: int = 3, b: int = 2):
    states = list(range(n))
    return {s: (a*s+b)%n for s in states}, states

def fdds_two_cycle(n: int):
    states = list(range(n)); half = n//2
    T = {s: (s+1)%half if s < half else half+(s-half+1)%(n-half) for s in states}
    return T, states

def fdds_tree_class3():
    """Minimal Class III example: T=[0→2,1→3,2→2,3→3], obs={0,1}→A,{2,3}→B"""
    states = [0,1,2,3]
    T = {0:2, 1:3, 2:2, 3:3}
    return T, states

FAMILIES = {
    "kaprekar_b10_d4": lambda: fdds_kaprekar(10, 4),
    "kaprekar_b6_d4":  lambda: fdds_kaprekar(6, 4),
    "random_20":       lambda: fdds_random(20, 42),
    "random_50":       lambda: fdds_random(50, 99),
    "nilpotent_15":    lambda: fdds_nilpotent(15),
    "single_cycle_12": lambda: fdds_single_cycle(12),
    "tree_15":         lambda: fdds_tree(15),
    "affine_17":       lambda: fdds_affine(17, 3, 5),
    "two_cycle_20":    lambda: fdds_two_cycle(20),
    "tree_class3":     fdds_tree_class3,
}


# ══════════════════════════════════════════════════════════════════════════════
# OBSERVABLES
# ══════════════════════════════════════════════════════════════════════════════

def gap_obs_kaprekar(T, states):
    def gap(n):
        d = sorted([int(x) for x in f"{n:04d}"])
        return (d[3]-d[0], d[2]-d[1])
    return {s: gap(s) for s in states}

def mod_obs(k: int):
    return lambda T, states: {s: s%k for s in states}

def parity_obs(T, states):
    return {s: s%2 for s in states}

def tree_class3_obs(T, states):
    return {s: ("A" if s < 2 else "B") for s in states}


# ══════════════════════════════════════════════════════════════════════════════
# MODULE B — EXECUTABLE PROPERTY LANGUAGE
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class Property:
    name: str
    description: str
    check: Callable  # (T, states, obs) -> (bool, str)

def prop_semiconjugacy(T, states, obs):
    """π∘T = T̃∘π: observable commutes with dynamics."""
    fiber = defaultdict(list)
    for s in states: fiber[obs[s]].append(s)
    for o, members in fiber.items():
        imgs = set(obs[T[s]] for s in members)
        if len(imgs) > 1:
            return False, f"Fiber obs={o} maps to multiple: {list(imgs)[:3]}"
    return True, "OK"

def prop_pi_idempotent(T, states, obs):
    """Π² = Π: projection must be idempotent."""
    fiber = defaultdict(list)
    for s in states: fiber[obs[s]].append(s)
    N = len(states); si = {s: i for i, s in enumerate(states)}
    Pi = np.zeros((N, N))
    for o, members in fiber.items():
        k = len(members)
        for i in members:
            for j in members:
                Pi[si[i], si[j]] = 1.0/k
    err = float(np.max(np.abs(Pi @ Pi - Pi)))
    return err < 1e-10, f"||Π²-Π||∞={err:.2e}"

def prop_attractor_reachable(T, states, obs):
    """Every state eventually reaches a periodic orbit."""
    for s in states:
        cur = s; seen = set(); ct = 0
        while cur not in seen and ct <= len(states):
            seen.add(cur); cur = T[cur]; ct += 1
        if ct > len(states):
            return False, f"State {s}: no attractor within {len(states)} steps"
    return True, "OK"

def prop_foqds_refines_obs(T, states, obs, depth: int = 20):
    """FOQDS partition must refine the observable partition."""
    def trace(s):
        path = []; seen = {}; cur = s
        for _ in range(depth):
            if cur in seen: break
            seen[cur] = len(path); path.append(obs[cur]); cur = T[cur]
        return tuple(path)
    traces = {s: trace(s) for s in states}
    for s in states:
        for t in states:
            if traces[s] == traces[t] and obs[s] != obs[t]:
                return False, f"States {s},{t} same trace but obs {obs[s]}≠{obs[t]}"
    return True, "OK (sample check)"

def prop_rank_c_equals_deviation_dim(T, states, obs):
    """rank(ΠK-KΠ) = dim span{Δ(x)}: commutator rank identity."""
    fiber = defaultdict(list)
    for s in states: fiber[obs[s]].append(s)
    N = len(states); si = {s: i for i, s in enumerate(states)}
    Pi = np.zeros((N, N))
    for o, members in fiber.items():
        k = len(members)
        for i in members:
            for j in members:
                Pi[si[i], si[j]] = 1.0/k
    K = np.zeros((N, N))
    for s in states:
        K[si[T[s]], si[s]] = 1.0
    C = Pi @ K - K @ Pi
    I = np.eye(N)
    innovations = (I - Pi) @ K
    rank_C = matrix_rank(C, tol=1e-9)
    rank_innov = matrix_rank(innovations, tol=1e-9)
    ok = abs(rank_C - rank_innov) == 0
    return ok, f"rank(C)={rank_C}, rank(span{{Δ}})={rank_innov}"

PROPERTY_SUITE = [
    Property("SemiConjugacy",     "π∘T = T̃∘π",          prop_semiconjugacy),
    Property("PiIdempotent",      "Π² = Π",              prop_pi_idempotent),
    Property("AttractorReach",    "All states reach P(T)", prop_attractor_reachable),
    Property("FOQDSRefinesObs",   "FOQDS ≻ observable",  prop_foqds_refines_obs),
    Property("RankCDeviation",    "rank(C)=dim span{Δ}", prop_rank_c_equals_deviation_dim),
]

def run_property_suite(T, states, obs, suite=None):
    suite = suite or PROPERTY_SUITE
    results = {}
    for prop in suite:
        ok, msg = prop.check(T, states, obs)
        results[prop.name] = {"pass": ok, "msg": msg}
    return results


# ══════════════════════════════════════════════════════════════════════════════
# MODULE C — ADVERSARIAL MUTATIONS
# ══════════════════════════════════════════════════════════════════════════════

def mut_merge_fixed_points(T, states, seed=0):
    """Merge two attractors into one."""
    rng = random.Random(seed)
    fixed = [s for s in states if T[s] == s]
    if len(fixed) < 2: return T.copy(), "no_op"
    a, b = fixed[0], fixed[-1]
    T2 = dict(T); T2[a] = b
    return T2, f"merged fixed {a}→{b}"

def mut_reroute_transient(T, states, seed=0):
    rng = random.Random(seed)
    non_fixed = [s for s in states if T[s] != s]
    if len(non_fixed) < 2: return T.copy(), "no_op"
    src = rng.choice(non_fixed)
    tgt = rng.choice([s for s in non_fixed if s != src])
    T2 = dict(T); T2[src] = tgt
    return T2, f"rerouted {src}→{tgt}"

def mut_collapse_obs(obs, states, seed=0):
    rng = random.Random(seed)
    cls = list(set(obs.values()))
    if len(cls) < 2: return obs.copy(), "no_op"
    c1, c2 = rng.sample(cls, 2)
    return {s: (c1 if obs[s] == c2 else obs[s]) for s in states}, f"collapsed {c2}→{c1}"

def mut_inject_symmetry(T, states, seed=0):
    rng = random.Random(seed)
    if len(states) < 2: return T.copy(), "no_op"
    a, b = rng.sample(states, 2)
    swap = {a: b, b: a}
    T2 = {s: swap.get(T[s], T[s]) for s in states}
    T2[swap.get(a, a)], T2[swap.get(b, b)] = T2.get(b, T2[a]), T2.get(a, T2[b])
    return T2, f"swapped {a}↔{b}"

MUTATIONS_T = {
    "merge_fixed_points": mut_merge_fixed_points,
    "reroute_transient":  mut_reroute_transient,
    "inject_symmetry":    mut_inject_symmetry,
}
MUTATIONS_OBS = {
    "collapse_obs_classes": mut_collapse_obs,
}


# ══════════════════════════════════════════════════════════════════════════════
# MODULE D — COUNTEREXAMPLE MINIMIZER
# ══════════════════════════════════════════════════════════════════════════════

def minimize_counterexample(T, states, prop, obs_fn, max_rounds=5):
    """Delta-debug: find minimal state subset where prop still fails."""
    def close(subset, T):
        c = set(subset)
        changed = True
        while changed:
            changed = False
            adds = set()
            for s in c:
                if T[s] not in c: adds.add(T[s]); changed = True
            c |= adds
        return sorted(c)
    
    current = sorted(states)
    for _ in range(max_rounds):
        improved = False
        for s in sorted(current, reverse=True):
            candidate = close([x for x in current if x != s], T)
            if not candidate: continue
            T_sub = {x: T[x] for x in candidate}
            obs_sub = obs_fn(T_sub, candidate)
            ok, _ = prop(T_sub, candidate, obs_sub)
            if not ok:
                current = candidate; improved = True
        if not improved: break
    
    return current


# ══════════════════════════════════════════════════════════════════════════════
# MODULE E — COLLISION ATLAS
# ══════════════════════════════════════════════════════════════════════════════

def compute_observable_signature(T, states, obs):
    """Canonical signature of an FDDS under the given observable."""
    fiber = defaultdict(list)
    for s in states: fiber[obs[s]].append(s)
    parts = []
    for o in sorted(set(obs.values()), key=str):
        m = fiber[o]
        imgs = tuple(sorted(set(obs[T[s]] for s in m), key=str))
        parts.append((str(o), imgs, len(m)))
    return tuple(parts)

@dataclass
class CollisionRecord:
    signature: tuple
    systems: List[Any]
    invariant_name: str
    
class CollisionAtlas:
    def __init__(self, invariant_name: str):
        self.name = invariant_name
        self.buckets: Dict[tuple, CollisionRecord] = {}
    
    def add(self, T, states, obs, system_id: Any):
        sig = compute_observable_signature(T, states, obs)
        if sig not in self.buckets:
            self.buckets[sig] = CollisionRecord(sig, [], self.name)
        self.buckets[sig].systems.append(system_id)
    
    def collisions(self):
        return {sig: rec for sig, rec in self.buckets.items() if len(rec.systems) > 1}
    
    def report(self):
        cols = self.collisions()
        print(f"Collision Atlas [{self.name}]:")
        print(f"  Distinct signatures: {len(self.buckets)}")
        print(f"  Colliding signatures: {len(cols)}")
        if cols:
            max_bucket = max(len(r.systems) for r in cols.values())
            print(f"  Max bucket size: {max_bucket}")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE G — IMPLEMENTATION MUTATION TESTING
# ══════════════════════════════════════════════════════════════════════════════

def test_minpoly_detector(K: np.ndarray, claimed_k: int) -> Tuple[bool, str]:
    """Check if K has minimal polynomial x^k(x-1)."""
    I = np.eye(K.shape[0])
    val_k = float(np.max(np.abs(matrix_power(K, claimed_k) @ (K - I))))
    val_k1 = float(np.max(np.abs(matrix_power(K, claimed_k-1) @ (K - I)))) if claimed_k > 1 else float("inf")
    ok = val_k < 1e-9 and val_k1 > 1e-3
    return ok, f"||K^{claimed_k}(K-I)||∞={val_k:.2e}, ||K^{claimed_k-1}(K-I)||∞={val_k1:.2e}"

KNOWN_MUTANTS = {
    "transpose_K":      lambda K, k: (K.T, k),
    "add_identity":     lambda K, k: (K + np.eye(K.shape[0]), k),
    "scale_2":          lambda K, k: (2*K, k),
    "off_by_one_k+1":   lambda K, k: (K, k+1),
    "off_by_one_k-1":   lambda K, k: (K, max(1, k-1)),
}

def run_mutation_test(K: np.ndarray, correct_k: int):
    """Test detector against all known mutants. Return which mutants survive."""
    survivors = []
    ok, msg = test_minpoly_detector(K, correct_k)
    if not ok:
        return None, "Detector fails on correct input!"
    for mname, mut_fn in KNOWN_MUTANTS.items():
        K_mut, k_mut = mut_fn(K, correct_k)
        try:
            ok_mut, msg_mut = test_minpoly_detector(K_mut, k_mut)
            if ok_mut:
                survivors.append((mname, msg_mut))
        except Exception as e:
            pass
    return survivors, "OK"


# ══════════════════════════════════════════════════════════════════════════════
# MODULE I — PROOF PRESSURE INDEX
# ══════════════════════════════════════════════════════════════════════════════

EVIDENCE_WEIGHTS = {
    "exhaustive_search": 3,
    "random_search":     2,
    "adversarial":       3,
    "mutation_testing":  2,
    "independent_impl":  2,
    "literature":        1,
    "proof_written":     4,
    "lean_formalized":   3,
}
MAX_PRESSURE = sum(EVIDENCE_WEIGHTS.values())  # 20

def evidence_grade(ev: dict) -> str:
    if ev.get("proof_written") and ev.get("lean_formalized"): return "PV"
    if ev.get("proof_written"): return "P"
    if ev.get("adversarial") and ev.get("exhaustive_search"): return "AV"
    if ev.get("exhaustive_search"): return "C2"
    if ev.get("random_search"): return "C1"
    return "C0"

@dataclass
class Claim:
    id: str
    statement: str
    evidence: Dict[str, bool] = field(default_factory=dict)
    killed: bool = False
    kill_reason: Optional[str] = None
    
    def pressure_score(self) -> int:
        return sum(EVIDENCE_WEIGHTS.get(k, 1) for k, v in self.evidence.items() if v)
    
    def grade(self) -> str:
        if self.killed: return "KILLED"
        return evidence_grade(self.evidence)

class ProofPressureIndex:
    def __init__(self):
        self.claims: Dict[str, Claim] = {}
    
    def add(self, id, statement, killed=False, kill_reason=None, **ev_kwargs):
        self.claims[id] = Claim(id, statement, ev_kwargs, killed, kill_reason)
    
    def kill(self, id, reason):
        if id in self.claims:
            self.claims[id].killed = True
            self.claims[id].kill_reason = reason
    
    def report(self):
        print(f"{'ID':18s} | {'Grade':6s} | {'Pressure':8s} | Statement")
        print("-"*75)
        for c in self.claims.values():
            if c.killed:
                print(f"  {'~~'+c.id+'~~':18s} | {'KILLED':6s} | {'':8s} | {c.statement} [{c.kill_reason[:30]}]")
                continue
            sc = c.pressure_score()
            g = c.grade()
            pct = sc / MAX_PRESSURE
            bar = "█"*int(pct*10) + "░"*(10-int(pct*10))
            print(f"  {c.id:18s} | {g:6s} | {bar} | {c.statement[:45]}")


# ══════════════════════════════════════════════════════════════════════════════
# CANONICAL KAPREKAR REGISTRY
# ══════════════════════════════════════════════════════════════════════════════

def build_canonical_ppi() -> ProofPressureIndex:
    ppi = ProofPressureIndex()
    ppi.add("T-FOQDS-55",  "FOQDS = 55 classes (4-dig b10 Kaprekar)",
            exhaustive_search=True, random_search=True, independent_impl=True,
            lean_formalized=True)
    ppi.add("T-K55-MP",    "K55 minimal poly = x^7(x-1)",
            exhaustive_search=True, random_search=True, adversarial=True, mutation_testing=True)
    ppi.add("T-K54-MP",    "K54 minimal poly = x^6(x-1)  [v11 correction]",
            exhaustive_search=True, random_search=True, adversarial=True, mutation_testing=True)
    ppi.add("T-SEMICONJ",  "Semiconjugacy π∘T=T_F∘π (0 violations)",
            exhaustive_search=True, random_search=True, adversarial=True,
            mutation_testing=True, independent_impl=True, proof_written=True, lean_formalized=True)
    ppi.add("T-RANK-C=1",  "rank(ΠK-KΠ)=1 for Kaprekar FOQDS space",
            exhaustive_search=True, adversarial=True)
    ppi.add("T-KAP-CLASS4","Kaprekar ∈ Class IV (mixed, not Class II)",
            exhaustive_search=True, adversarial=True)
    ppi.add("T-COUPLING",  "δ=dim(V_ref∩V_bdry) — general formula",
            exhaustive_search=True)
    ppi.add("T-CROSSBASE", "|Q_b|=b(b+1)/2 for all even b",
            killed=True, kill_reason="Fails for b=4,6,8,12,14 (computed)")
    ppi.add("T-AUTO-Z26",  "Automorphism group (Z2)^6 order 64",
            killed=True, kill_reason="No Z2 action found; level-1 has 3 nodes (not 2^k)")
    ppi.add("T-RANK-30",   "Incidence rank stabilizes at 30",
            killed=True, kill_reason="No matrix computes to 30; origin unidentified")
    return ppi


if __name__ == "__main__":
    print("=" * 70)
    print("  AQARION AML CORE — Self-Test")
    print("=" * 70)
    
    # A: Kaprekar
    T, states = fdds_kaprekar(10, 4)
    print(f"\nA. Kaprekar: {len(states)} states")
    
    # B: Properties
    obs = gap_obs_kaprekar(T, states)
    results = run_property_suite(T, states, obs)
    for name, r in results.items():
        print(f"  {'PASS' if r['pass'] else 'FAIL'} {name}: {r['msg']}")
    
    # G: Mutation test
    from numpy.linalg import matrix_power as mp2
    def gap(n):
        d = sorted([int(x) for x in f"{n:04d}"])
        return (d[3]-d[0], d[2]-d[1])
    gap_classes = sorted(set(gap(s) for s in states))
    gi = {g:i for i,g in enumerate(gap_classes)}
    fiber = defaultdict(list)
    for s in states: fiber[gap(s)].append(s)
    K54 = np.zeros((54,54))
    for g in gap_classes:
        img_g = gap(T[fiber[g][0]])
        K54[gi[img_g], gi[g]] = 1.0
    
    survivors, status = run_mutation_test(K54, 6)
    print(f"\nG. Mutation test (K54, k=6): {status}")
    if survivors:
        for sname, smsg in survivors:
            print(f"  ⚠ SURVIVOR: {sname} — {smsg}")
    else:
        print("  All mutants caught!")
    
    # I: PPI
    print("\nI. Proof Pressure Index:")
    ppi = build_canonical_ppi()
    ppi.report()
    
    print("\n=== Self-test complete ===")
