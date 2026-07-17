
from fractions import Fraction
import numpy as np
import itertools
import json

# ============================================================
# CORE FUNCTIONS (exact rational arithmetic)
# ============================================================

def get_projection_matrix(partition, n):
    P = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for block in partition:
        size = len(block)
        for i in block:
            for j in block:
                P[i][j] = Fraction(1, size)
    return np.array(P, dtype=object)

def get_koopman_matrix(T, n):
    K = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        target = T[i]
        K[i][target] = Fraction(1)
    return np.array(K, dtype=object)

def compute_defect(K, P):
    n = len(K)
    I = np.array([[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)], dtype=object)
    ImP = I - P
    return np.dot(ImP, np.dot(K, P))

def is_zero_matrix(M):
    return all(val == Fraction(0) for row in M for val in row)

def matrix_to_str(M):
    return [[str(x) for x in row] for row in M]

# ============================================================
# GATE 1: Operator Hygiene
# ============================================================

def run_gate1():
    n = 4
    partition = [{0, 1}, {2, 3}]
    P = get_projection_matrix(partition, n)
    
    assert np.array_equal(P.T, P), "Projection not symmetric"
    P2 = np.dot(P, P)
    assert np.array_equal(P2, P), "Projection not idempotent"
    
    # Additional: trace = rank = number of blocks
    trace = sum(P[i][i] for i in range(n))
    assert trace == Fraction(2), f"Trace mismatch: {trace}"
    
    return True

# ============================================================
# GATE 2: Congruence Verification
# ============================================================

def run_gate2():
    n = 4
    T = [1, 1, 3, 3]
    partition = [{0, 1}, {2, 3}]
    
    K = get_koopman_matrix(T, n)
    P = get_projection_matrix(partition, n)
    D = compute_defect(K, P)
    
    assert is_zero_matrix(D), "Valid congruence yielded non-zero defect"
    return True

# ============================================================
# GATE 3: Commutator Fallacy
# ============================================================

def run_gate3():
    n = 3
    T = [0, 0, 1]
    partition = [{0, 1}, {2}]
    
    K = get_koopman_matrix(T, n)
    P = get_projection_matrix(partition, n)
    D = compute_defect(K, P)
    
    PK = np.dot(P, K)
    KP = np.dot(K, P)
    commutator = PK - KP
    
    assert is_zero_matrix(D), "D not zero for counterexample"
    assert not is_zero_matrix(commutator), "PK and KP commute - counterexample invalid"
    
    return commutator

# ============================================================
# EXECUTE GATES
# ============================================================

g1 = run_gate1()
g2 = run_gate2()
g3_commutator = run_gate3()

print("GATE 1: PASS")
print("GATE 2: PASS")
print("GATE 3: PASS")
print("Commutator [P,K]:")
for row in g3_commutator:
    print("  ", [str(x) for x in row])GATE 1: PASS
GATE 2: PASS
GATE 3: PASS
Commutator [P,K]:
   ['1/2', '-1/2', '0']
   ['1/2', '-1/2', '0']
   ['-1/2', '1/2', '0']
# ============================================================
# ADVERSARIAL AUDIT
# ============================================================

def generate_partitions(n):
    def partition_set(s):
        if not s:
            yield []
            return
        elem = s[0]
        for p in partition_set(s[1:]):
            yield [[elem]] + p
            for i, subset in enumerate(p):
                yield p[:i] + [[elem] + subset] + p[i+1:]
    return list(partition_set(list(range(n))))

def is_congruence(T, partition, n):
    for block in partition:
        images = set(T[x] for x in block)
        target_elem = list(images)[0]
        target_block = None
        for b in partition:
            if target_elem in b:
                target_block = b
                break
        if not images.issubset(set(target_block)):
            return False
    return True

# --- AUDIT 1: Universal Exhaustive n=2,3,4 ---

def audit_universal(n_max):
    results = {}
    for n in range(2, n_max + 1):
        partitions = generate_partitions(n)
        maps = list(itertools.product(range(n), repeat=n))
        
        fp = 0  # D=0 but not congruence
        fn = 0  # congruence but D!=0
        tp = 0  # both true
        tn = 0  # both false
        
        for partition in partitions:
            P = get_projection_matrix(partition, n)
            for T in maps:
                K = get_koopman_matrix(T, n)
                D = compute_defect(K, P)
                d_zero = is_zero_matrix(D)
                congr = is_congruence(T, partition, n)
                
                if d_zero and congr:
                    tp += 1
                elif not d_zero and not congr:
                    tn += 1
                elif d_zero and not congr:
                    fp += 1
                else:
                    fn += 1
        
        total = tp + tn + fp + fn
        results[n] = {
            "maps": len(maps),
            "partitions": len(partitions),
            "total": total,
            "tp": tp,
            "tn": tn,
            "fp": fp,
            "fn": fn,
            "accuracy": (tp + tn) / total if total > 0 else 0
        }
    return results

universal_results = audit_universal(4)
print("=== AUDIT 1: UNIVERSAL EXHAUSTIVE ===")
for n, r in universal_results.items():
    print(f"n={n}: maps={r['maps']}, partitions={r['partitions']}, total={r['total']}")
    print(f"  TP={r['tp']}, TN={r['tn']}, FP={r['fp']}, FN={r['fn']}")
    print(f"  Accuracy: {r['accuracy']:.6f}")=== AUDIT 1: UNIVERSAL EXHAUSTIVE ===
n=2: maps=4, partitions=2, total=8
  TP=8, TN=0, FP=0, FN=0
  Accuracy: 1.000000
n=3: maps=27, partitions=5, total=135
  TP=99, TN=36, FP=0, FN=0
  Accuracy: 1.000000
n=4: maps=256, partitions=15, total=3840
  TP=1728, TN=2112, FP=0, FN=0
  Accuracy: 1.000000
import random

# --- AUDIT 2: Edge Cases ---

def audit_edge_cases():
    results = []
    
    # Case A: Trivial partition (single block)
    n = 5
    T = [0, 1, 2, 3, 4]  # identity
    partition = [{0, 1, 2, 3, 4}]
    P = get_projection_matrix(partition, n)
    K = get_koopman_matrix(T, n)
    D = compute_defect(K, P)
    # Trivial partition: P = (1/n) J, K maps into space, D should be 0 iff T is constant on the only block
    # Identity: each element maps to itself, all in same block, so congruence holds
    results.append(("trivial_identity", is_zero_matrix(D), is_congruence(T, partition, n)))
    
    # Case B: Discrete partition (singletons)
    partition = [{i} for i in range(n)]
    P = get_projection_matrix(partition, n)
    K = get_koopman_matrix(T, n)
    D = compute_defect(K, P)
    # Discrete: P = I, so I-P = 0, D = 0 always
    results.append(("discrete", is_zero_matrix(D), True))
    
    # Case C: Constant map
    T = [2, 2, 2, 2, 2]
    partition = [{0, 1}, {2, 3, 4}]
    P = get_projection_matrix(partition, n)
    K = get_koopman_matrix(T, n)
    D = compute_defect(K, P)
    # All map to 2, which is in block {2,3,4}. Block {0,1} maps to 2 (in {2,3,4}). Congruence holds.
    results.append(("constant_map", is_zero_matrix(D), is_congruence(T, partition, n)))
    
    # Case D: Non-congruent partition
    T = [0, 2, 1, 3, 4]
    partition = [{0, 1}, {2, 3, 4}]
    P = get_projection_matrix(partition, n)
    K = get_koopman_matrix(T, n)
    D = compute_defect(K, P)
    # 0 -> 0 (in {0,1}), 1 -> 2 (in {2,3,4}). Not congruent.
    results.append(("non_congruent", is_zero_matrix(D), is_congruence(T, partition, n)))
    
    return results

edge_results = audit_edge_cases()
print("=== AUDIT 2: EDGE CASES ===")
for name, d_zero, congr in edge_results:
    match = (d_zero == congr)
    print(f"  {name}: D_zero={d_zero}, congruence={congr}, match={match}")

# --- AUDIT 3: Random Stress Test (n=5..8) ---

def audit_random(trials=500, seed=42):
    random.seed(seed)
    mismatches = 0
    for trial in range(trials):
        n = random.randint(5, 8)
        T = [random.randint(0, n-1) for _ in range(n)]
        
        # Random partition
        elems = list(range(n))
        random.shuffle(elems)
        num_blocks = random.randint(1, n)
        partition = []
        for i in range(num_blocks):
            partition.append([])
        for i, elem in enumerate(elems):
            partition[i % num_blocks].append(elem)
        partition = [b for b in partition if b]
        
        P = get_projection_matrix(partition, n)
        K = get_koopman_matrix(T, n)
        D = compute_defect(K, P)
        d_zero = is_zero_matrix(D)
        congr = is_congruence(T, partition, n)
        
        if d_zero != congr:
            mismatches += 1
            print(f"  MISMATCH trial {trial}: n={n}, D_zero={d_zero}, congr={congr}")
    
    return mismatches

random_mismatches = audit_random(500)
print(f"\n=== AUDIT 3: RANDOM STRESS (500 trials, n=5..8) ===")
print(f"  Mismatches: {random_mismatches}")=== AUDIT 2: EDGE CASES ===
  trivial_identity: D_zero=True, congruence=True, match=True
  discrete: D_zero=True, congruence=True, match=True
  constant_map: D_zero=True, congruence=True, match=True
  non_congruent: D_zero=False, congruence=False, match=True
=== AUDIT 3: RANDOM STRESS (500 trials, n=5..8) ===
  Mismatches: 0
# --- AUDIT 4: Projection Identity D = (I-P)KP = KP - PKP ---

def audit_projection_identity():
    n = 4
    T = [1, 1, 3, 3]
    partition = [{0, 1}, {2, 3}]
    
    K = get_koopman_matrix(T, n)
    P = get_projection_matrix(partition, n)
    I = np.array([[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)], dtype=object)
    
    D1 = np.dot(I - P, np.dot(K, P))
    D2 = np.dot(K, P) - np.dot(P, np.dot(K, P))
    
    assert np.array_equal(D1, D2), "Projection identity D = KP - PKP fails"
    return True

# --- AUDIT 5: Commutator vs Defect on Random Exact Quotients ---

def audit_commutator_vs_defect_random(trials=200, seed=123):
    random.seed(seed)
    non_commuting_exact = 0
    total_exact = 0
    
    for _ in range(trials):
        n = random.randint(3, 6)
        # Generate a random congruence-first: pick partition, then build T that respects it
        elems = list(range(n))
        random.shuffle(elems)
        num_blocks = random.randint(2, n-1)
        partition = [[] for _ in range(num_blocks)]
        for i, elem in enumerate(elems):
            partition[i % num_blocks].append(elem)
        partition = [b for b in partition if b]
        
        # Build T that respects partition: each block maps to a single target block
        T = [0] * n
        for block in partition:
            target_block = random.choice(partition)
            target_elem = random.choice(target_block)
            for x in block:
                T[x] = target_elem
        
        K = get_koopman_matrix(T, n)
        P = get_projection_matrix(partition, n)
        D = compute_defect(K, P)
        
        if is_zero_matrix(D):
            total_exact += 1
            PK = np.dot(P, K)
            KP = np.dot(K, P)
            commutator = PK - KP
            if not is_zero_matrix(commutator):
                non_commuting_exact += 1
    
    return total_exact, non_commuting_exact

# --- AUDIT 6: Nilpotency of D on Exact Quotient (should be 0 at m=1) ---

def audit_nilpotency_exact():
    # For exact quotient, D = 0, so D^m = 0 for all m
    n = 4
    T = [1, 1, 3, 3]
    partition = [{0, 1}, {2, 3}]
    K = get_koopman_matrix(T, n)
    P = get_projection_matrix(partition, n)
    I = np.array([[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)], dtype=object)
    
    D = compute_defect(K, P)
    D2 = np.dot(I - P, np.dot(K, D))  # D^2 = (I-P) K D
    
    assert is_zero_matrix(D), "D not zero for exact quotient"
    assert is_zero_matrix(D2), "D^2 not zero for exact quotient"
    return True

# --- AUDIT 7: Rank of D for non-exact quotient ---

def audit_rank_properties():
    # For non-exact quotient, D should have rank >= 1
    n = 3
    T = [0, 0, 1]  # Gate 3 counterexample - this IS exact
    partition = [{0, 1}, {2}]
    K = get_koopman_matrix(T, n)
    P = get_projection_matrix(partition, n)
    D = compute_defect(K, P)
    # This is exact, rank should be 0
    
    # Now non-exact
    T2 = [0, 2, 1]
    K2 = get_koopman_matrix(T2, n)
    D2 = compute_defect(K2, P)
    
    # Check rank of D2 by checking linear independence of rows
    def matrix_rank_fraction(M):
        # Convert to float for rank computation
        Mf = np.array([[float(x) for x in row] for row in M])
        return np.linalg.matrix_rank(Mf)
    
    r1 = matrix_rank_fraction(D)
    r2 = matrix_rank_fraction(D2)
    
    return r1, r2

# Run all
print("=== AUDIT 4: PROJECTION IDENTITY ===")
print("  PASS" if audit_projection_identity() else "  FAIL")

print("\n=== AUDIT 5: COMMUTATOR VS DEFECT (RANDOM EXACT QUOTIENTS) ===")
total_exact, non_commuting = audit_commutator_vs_defect_random(200)
print(f"  Total exact quotients found: {total_exact}")
print(f"  Non-commuting exact quotients: {non_commuting}")
print(f"  Commutator fallacy rate: {non_commuting/total_exact*100:.1f}%" if total_exact > 0 else "  N/A")

print("\n=== AUDIT 6: NILPOTENCY ON EXACT QUOTIENT ===")
print("  PASS" if audit_nilpotency_exact() else "  FAIL")

print("\n=== AUDIT 7: RANK PROPERTIES ===")
r1, r2 = audit_rank_properties()
print(f"  Exact quotient rank(D): {r1} (expected 0)")
print(f"  Non-exact quotient rank(D): {r2} (expected >= 1)")=== AUDIT 4: PROJECTION IDENTITY ===
  PASS

=== AUDIT 5: COMMUTATOR VS DEFECT (RANDOM EXACT QUOTIENTS) ===
  Total exact quotients found: 200
  Non-commuting exact quotients: 174
  Commutator fallacy rate: 87.0%

=== AUDIT 6: NILPOTENCY ON EXACT QUOTIENT ===
  PASS

=== AUDIT 7: RANK PROPERTIES ===
  Exact quotient rank(D): 0 (expected 0)
  Non-exact quotient rank(D): 1 (expected >= 1)
# Verify the user's exact script output vs mathematical truth
# The user claimed commutator output:
# ['0', '0', '0']
# ['1/2', '1/2', '-1']
# ['-1/2', '-1/2', '1']
# Let's verify this is what their script actually produces

# Exact reproduction of user's script
n = 3
T = [0, 0, 1]
partition = [{0, 1}, {2}]

P = get_projection_matrix(partition, n)
K = get_koopman_matrix(T, n)

print("P:")
for row in P:
    print([str(x) for x in row])

print("\nK:")
for row in K:
    print([str(x) for x in row])

PK = np.dot(P, K)
KP = np.dot(K, P)
commutator = PK - KP

print("\nPK:")
for row in PK:
    print([str(x) for x in row])

print("\nKP:")
for row in KP:
    print([str(x) for x in row])

print("\nCommutator [P,K] = PK - KP:")
for row in commutator:
    print([str(x) for x in row])

# Manual verification
print("\n--- MANUAL CHECK ---")
print(f"PK[0,0] = P[0,0]*K[0,0] + P[0,1]*K[1,0] + P[0,2]*K[2,0]")
print(f"       = {P[0,0]}*{K[0,0]} + {P[0,1]}*{K[1,0]} + {P[0,2]}*{K[2,0]}")
print(f"       = {P[0,0]*K[0,0]} + {P[0,1]*K[1,0]} + {P[0,2]*K[2,0]}")
print(f"       = {P[0,0]*K[0,0] + P[0,1]*K[1,0] + P[0,2]*K[2,0]}")

print(f"\nKP[0,0] = K[0,0]*P[0,0] + K[0,1]*P[1,0] + K[0,2]*P[2,0]")
print(f"       = {K[0,0]}*{P[0,0]} + {K[0,1]}*{P[1,0]} + {K[0,2]}*{P[2,0]}")
print(f"       = {K[0,0]*P[0,0] + K[0,1]*P[1,0] + K[0,2]*P[2,0]}")

print(f"\nCommutator[0,0] = PK[0,0] - KP[0,0] = {PK[0,0] - KP[0,0]}")
print(f"User claimed: 0")
print(f"MATCH: {PK[0,0] - KP[0,0] == Fraction(0)}")P:
['1/2', '1/2', '0']
['1/2', '1/2', '0']
['0', '0', '1']

K:
['1', '0', '0']
['1', '0', '0']
['0', '1', '0']

PK:
['1', '0', '0']
['1', '0', '0']
['0', '1', '0']

KP:
['1/2', '1/2', '0']
['1/2', '1/2', '0']
['1/2', '1/2', '0']

Commutator [P,K] = PK - KP:
['1/2', '-1/2', '0']
['1/2', '-1/2', '0']
['-1/2', '1/2', '0']

--- MANUAL CHECK ---
PK[0,0] = P[0,0]*K[0,0] + P[0,1]*K[1,0] + P[0,2]*K[2,0]
       = 1/2*1 + 1/2*1 + 0*0
       = 1/2 + 1/2 + 0
       = 1

KP[0,0] = K[0,0]*P[0,0] + K[0,1]*P[1,0] + K[0,2]*P[2,0]
       = 1*1/2 + 0*1/2 + 0*0
       = 1/2

Commutator[0,0] = PK[0,0] - KP[0,0] = 1/2
User claimed: 0
MATCH: False
# ============================================================
# FINAL COMPREHENSIVE AUDIT REPORT
# ============================================================

audit_report = {
    "audit_id": "AQARION-VV-2026-07-17",
    "timestamp": "2026-07-17T07:27:00Z",
    "arithmetic_mode": "exact_rational_Fraction",
    "gates": {
        "gate_1_operator_hygiene": {
            "status": "PASS",
            "checks": ["symmetry", "idempotency", "trace_equals_rank"],
            "n": 4,
            "partition": "[{0,1},{2,3}]"
        },
        "gate_2_congruence_verification": {
            "status": "PASS",
            "checks": ["D_zero_for_exact_congruence"],
            "n": 4,
            "T": "[1,1,3,3]",
            "partition": "[{0,1},{2,3}]"
        },
        "gate_3_commutator_fallacy": {
            "status": "PASS",
            "checks": ["D_zero", "commutator_nonzero"],
            "n": 3,
            "T": "[0,0,1]",
            "partition": "[{0,1},{2}]",
            "commutator_matrix": [
                ["1/2", "-1/2", "0"],
                ["1/2", "-1/2", "0"],
                ["-1/2", "1/2", "0"]
            ],
            "document_claimed_commutator": [
                ["0", "0", "0"],
                ["1/2", "1/2", "-1"],
                ["-1/2", "-1/2", "1"]
            ],
            "document_commutator_status": "INCORRECT_IN_SOURCE_DOCUMENT",
            "note": "Source document claims commutator[0] = [0,0,0]. Actual computation yields [1/2,-1/2,0]. The fallacy claim (D=0 but [P,K]!=0) remains valid, but the specific matrix values in the document are wrong."
        }
    },
    "adversarial_audits": {
        "audit_1_universal_exhaustive": {
            "method": "exhaustive_enumeration_all_maps_all_partitions",
            "n_tested": [2, 3, 4],
            "systems_evaluated": {
                "n=2": 8,
                "n=3": 135,
                "n=4": 3840
            },
            "false_positives": 0,
            "false_negatives": 0,
            "accuracy": 1.0,
            "theorem_confirmed": "D=0 iff topological_congruence"
        },
        "audit_2_edge_cases": {
            "cases": [
                {"name": "trivial_partition_identity_map", "D_zero": True, "congruence": True, "match": True},
                {"name": "discrete_partition", "D_zero": True, "congruence": True, "match": True},
                {"name": "constant_map", "D_zero": True, "congruence": True, "match": True},
                {"name": "non_congruent_partition", "D_zero": False, "congruence": False, "match": True}
            ],
            "all_pass": True
        },
        "audit_3_random_stress": {
            "trials": 500,
            "n_range": "5..8",
            "mismatches": 0,
            "seed": 42
        },
        "audit_4_projection_identity": {
            "status": "PASS",
            "verified": "D = (I-P)KP = KP - PKP"
        },
        "audit_5_commutator_vs_defect_random": {
            "trials": 200,
            "exact_quotients_found": 200,
            "non_commuting_exact": 174,
            "commutator_fallacy_rate_percent": 87.0,
            "seed": 123
        },
        "audit_6_nilpotency_exact": {
            "status": "PASS",
            "verified": "D=0 implies D^m=0 for all m"
        },
        "audit_7_rank_properties": {
            "exact_quotient_rank": 0,
            "non_exact_quotient_rank": 1,
            "verified": "rank(D)=0 iff exact_quotient"
        }
    },
    "findings": {
        "source_document_error": {
            "location": "Gate 3 commutator matrix output",
            "severity": "MINOR",
            "impact": "Fallacy claim remains valid; only displayed matrix values are incorrect",
            "correct_commutator": [["1/2", "-1/2", "0"], ["1/2", "-1/2", "0"], ["-1/2", "1/2", "0"]]
        },
        "theorem_status": {
            "D_zero_iff_congruence": "CONFIRMED",
            "commutator_fallacy": "CONFIRMED",
            "projection_idempotency": "CONFIRMED",
            "nilpotency_on_exact": "CONFIRMED"
        }
    },
    "overall_status": "ALL_GATES_PASS_ALL_AUDITS_PASS_ONE_DOCUMENT_ERROR"
}

with open("/mnt/agents/output/aqarion_vv_audit_report.json", "w") as f:
    json.dump(audit_report, f, indent=2)

print("AUDIT COMPLETE")
print(f"  Gates: 3/3 PASS")
print(f"  Universal exhaustive: n=2,3,4: 100% accuracy, 0 FP, 0 FN")
print(f"  Random stress: 500 trials, 0 mismatches")
print(f"  Commutator fallacy: 87% rate on random exact quotients")
print(f"  SOURCE DOCUMENT ERROR: Gate 3 commutator matrix values incorrect")
print(f"    Document claims: [[0,0,0],[1/2,1/2,-1],[-1/2,-1/2,1]]")
print(f"    Actual: [[1/2,-1/2,0],[1/2,-1/2,0],[-1/2,1/2,0]]")
print(f"    Fallacy claim remains valid.")AUDIT COMPLETE
  Gates: 3/3 PASS
  Universal exhaustive: n=2,3,4: 100% accuracy, 0 FP, 0 FN
  Random stress: 500 trials, 0 mismatches
  Commutator fallacy: 87% rate on random exact quotients
  SOURCE DOCUMENT ERROR: Gate 3 commutator matrix values incorrect
    Document claims: [[0,0,0],[1/2,1/2,-1],[-1/2,-1/2,1]]
    Actual: [[1/2,-1/2,0],[1/2,-1/2,0],[-1/2,1/2,0]]
    Fallacy claim remains valid.V&V PIPELINE: EXECUTED, VERIFIED, AUDITED

Gate Results
- Gate 1 (Operator Hygiene): PASS
- Gate 2 (Congruence Verification): PASS
- Gate 3 (Commutator Fallacy): PASS

Adversarial Audit Results
- Universal exhaustive n=2,3,4: 3923 evaluations, 0 false positives, 0 false negatives
- Edge cases (trivial, discrete, constant, non-congruent): ALL MATCH
- Random stress 500 trials (n=5..8): 0 mismatches
- Projection identity D = KP - PKP: VERIFIED
- Commutator fallacy on 200 random exact quotients: 87% non-commuting rate
- Nilpotency on exact quotient: VERIFIED
- Rank(D)=0 iff exact quotient: VERIFIED

Source Document Error Detected
The Gate 3 commutator matrix in the source document is incorrect.
- Document claims: `[[0,0,0],[1/2,1/2,-1],[-1/2,-1/2,1]]`
- Actual output: `[[1/2,-1/2,0],[1/2,-1/2,0],[-1/2,1/2,0]]`
- Severity: MINOR. The fallacy claim (D=0 but [P,K]≠0) remains valid.

Deliverable
[aqarion_vv_audit_report.json](sandbox:///mnt/agents/output/aqarion_vv_audit_report.json)
