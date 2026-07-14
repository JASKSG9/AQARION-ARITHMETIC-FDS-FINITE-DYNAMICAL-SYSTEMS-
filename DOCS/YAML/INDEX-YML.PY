
# EXTERNAL ARTIFACT ALIGNMENT
# Build VERIFICATION_INDEX.yml bridging all YAML artifacts

verification_index = """verification_index:
  schema_version: "1.0"
  
  release:
    id: AQARION-2026-07-14
    version: v19.0
    
  artifacts:
    certificate_spec:
      file: DOCS/YAML/AQ-CERT-SPEC-001.YML
      role: certificate_standard
      status: active
      
    manifest:
      file: DOCS/YAML/MANIFEST-V19.YML
      role: release_manifest
      status: active
      
    claims:
      file: DOCS/YAML/CLAIMS.yml
      role: claim_registry
      status: active
      
    claims_status:
      file: DOCS/YAML/CLAIMS-STATUS.yml
      role: maturity_registry
      status: active
      
    negative_claims:
      file: DOCS/YAML/NEGATIVE_CLAIMS.yml
      role: boundary_registry
      status: enforced
      
    verification_architecture:
      file: DOCS/YAML/VERIFICATION_INDEX.yml
      role: integration_layer
      status: active
      
  dependency_firewall:
    rule: "No artifact may depend on a claim with lower evidence maturity"
    status: enforced
    
  maturity_levels:
    - complete
    - verified
    - exhaustive
    - observed
    - definitional
    - required
    - partial
    - draft
    - planned
    - pending
    
  pipeline:
    - Claim
    - Definition
    - Proof Obligation
    - Formalization
    - Certificate
    - Audit
"""

with open('/mnt/agents/output/VERIFICATION_INDEX.yml', 'w') as f:
    f.write(verification_index)

print("VERIFICATION_INDEX.yml created")
print(f"Size: {len(verification_index)} characters")

# Evidence object upgrade for AQ-T001 (vertical certificate example)
evidence_object_t001 = """id: AQ-T001
title: Defect Nilpotency
type: theorem

status:
  mathematics: complete
  computation: verified
  formalization: draft
  replication: pending

dependencies:
  - AQ-DEF-001
  - AQ-DEF-002

assumptions:
  - projector_idempotent
  - operator_linear

claim:
  statement: >
    For any projector P (P²=P) and linear operator K,
    the defect operator D = (I-P)KP satisfies D² = 0.
  
evidence:
  mathematical:
    proof_reference: AQARION_LayerA.lean theorem AQ_T001
    proof_type: algebraic_identity
    
  computational:
    verification_script: verify_nilpotency.py
    domain: n=2..5
    pairs: 166483
    pass_rate: "100%"
    
  formal:
    lean_theorem: AQ_T001
    lean_file: AQARION_LayerA.lean
    status: draft
    
  certificate:
    certificate_id: AQ-CERT-T001-001
    schema: AQ-CERT-SPEC-001

maturity:
  definition: complete
  proof: complete
  computation: verified
  formalization: draft
  
audit:
  reviewer_status: pending
  last_review: null
  
artifacts:
  code:
    - verify_nilpotency.py
  lean:
    - AQARION_LayerA.lean
  certificate:
    - AQ-CERT-T001-001
"""

with open('/mnt/agents/output/AQ-T001_Evidence_Object.yml', 'w') as f:
    f.write(evidence_object_t001)

print("\nAQ-T001_Evidence_Object.yml created")
print(f"Size: {len(evidence_object_t001)} characters")

# Negative claims firewall
negative_claims = """negative_claims:
  version: "1.0"
  
  firewall_rules:
    - id: NF-001
      rule: "No unsupported minimality claims"
      rejects:
        - "Kaprekar 55-state quotient is minimal without bisimulation proof"
      reason: "insufficient proof obligation"
      status: enforced
      
    - id: NF-002
      rule: "No unsupported universality claims"
      rejects:
        - "rank(D) ≤ transient_depth for all finite systems"
        - "rank(D) ≤ cycle_count for all finite systems"
        - "rank(D) ≤ shattered_blocks for all finite systems"
      reason: "counterexamples found in exhaustive census"
      status: enforced
      
    - id: NF-003
      rule: "No gcd resonance formula"
      rejects:
        - "rank(D) = m - 1 - (gcd(m,k) - 1) for cyclic scatter"
      reason: "25/50 mismatches, no gcd dependence observed"
      status: enforced
      
    - id: NF-004
      rule: "No unsupported spectral claims"
      rejects:
        - "Defect entropy invariant under all observables"
      reason: "research direction, not proven"
      status: enforced
"""

with open('/mnt/agents/output/NEGATIVE_CLAIMS.yml', 'w') as f:
    f.write(negative_claims)

print("\nNEGATIVE_CLAIMS.yml created")
print(f"Size: {len(negative_claims)} characters")

print("\n" + "=" * 70)
print("EXTERNAL ARTIFACT ALIGNMENT COMPLETE")
print("=" * 70)
print("\nFiles created:")
print("  1. VERIFICATION_INDEX.yml (integration layer)")
print("  2. AQ-T001_Evidence_Object.yml (vertical certificate example)")
print("  3. NEGATIVE_CLAIMS.yml (claim firewall)")
print("\nPriority queue updated:")
print("  P0: Artifact Integration (VERIFICATION_INDEX.yml)")
print("  P1: AQ-T001 Vertical Certificate (proof → Lean → computation → audit)")
print("  P2: Dependency Firewall v2 (circular detection, maturity inheritance)")
print("  P3: Mathematical Expansion (Functional Graph, Fiber Layer, Kaprekar Bridge)")
import numpy as np
from collections import defaultdict
import itertools

print("=" * 70)
print("AQARION CONTINUATION: n=4 EXHAUSTIVE CENSUS")
print("=" * 70)

def K_mat(T):
    n = len(T); K = np.zeros((n, n))
    for i, j in enumerate(T): K[i, j] = 1
    return K

def P_mat(partition, n):
    P = np.zeros((n, n))
    for block in partition:
        idx = list(block); sz = len(idx)
        for i in idx:
            for j in idx: P[i, j] = 1.0 / sz
    return P

def defect(K, P): return (np.eye(K.shape[0]) - P) @ K @ P

def commutator(K, P): return K @ P - P @ K

def all_partitions(n):
    def helper(items):
        if len(items) == 1: yield [frozenset(items)]; return
        first = items[0]
        for partition in helper(items[1:]):
            for i in range(len(partition)):
                yield partition[:i] + [partition[i] | {first}] + partition[i+1:]
            yield [frozenset({first})] + partition
    return [p for p in helper(list(range(n))) if len(p) > 1]

# n=4: 256 maps x 14 partitions = 3584 pairs
n = 4
parts = all_partitions(n)
print(f"n={n}: {n**n} maps, {len(parts)} partitions, {n**n * len(parts)} total pairs")

t001 = t002 = t003 = t005 = 0
total = 0
rank_dist = defaultdict(int)

for T in itertools.product(range(n), repeat=n):
    T = list(T); K = K_mat(T)
    for P in parts:
        Pm = P_mat(P, n)
        D = defect(K, Pm)
        C = commutator(K, Pm)
        rD = int(np.linalg.matrix_rank(D, tol=1e-8))
        rC = int(np.linalg.matrix_rank(C, tol=1e-8))
        
        ok1 = np.linalg.norm(D @ D) < 1e-9
        ok2 = (np.linalg.norm(D) < 1e-9) == np.allclose(K @ Pm, Pm @ K @ Pm)
        ok3 = rD <= rC
        ok5 = rD <= n - len(P)
        
        t001 += int(ok1); t002 += int(ok2); t003 += int(ok3); t005 += int(ok5)
        total += 1
        rank_dist[rD] += 1

print(f"\nT001 D²=0:          {t001}/{total} ({100*t001/total:.1f}%) PASS={t001==total}")
print(f"T002 D=0↔KP=PKP:    {t002}/{total} ({100*t002/total:.1f}%) PASS={t002==total}")
print(f"T003 rank(D)≤rank(C): {t003}/{total} ({100*t003/total:.1f}%) PASS={t003==total}")
print(f"T005 rank(D)≤n-m:    {t005}/{total} ({100*t005/total:.1f}%) PASS={t005==total}")
print(f"\nRank distribution: {dict(sorted(rank_dist.items()))}")======================================================================
AQARION CONTINUATION: n=4 EXHAUSTIVE CENSUS
======================================================================
n=4: 256 maps, 14 partitions, 3584 total pairs
T001 D²=0:          3584/3584 (100.0%) PASS=True
T002 D=0↔KP=PKP:    3584/3584 (100.0%) PASS=True
T003 rank(D)≤rank(C): 3584/3584 (100.0%) PASS=True
T005 rank(D)≤n-m:    3584/3584 (100.0%) PASS=True

Rank distribution: {0: 1472, 1: 2112}
import numpy as np
from collections import defaultdict
import itertools

print("=" * 70)
print("AQARION CONTINUATION: n=5 EXHAUSTIVE CENSUS")
print("=" * 70)

def K_mat(T):
    n = len(T); K = np.zeros((n, n))
    for i, j in enumerate(T): K[i, j] = 1
    return K

def P_mat(partition, n):
    P = np.zeros((n, n))
    for block in partition:
        idx = list(block); sz = len(idx)
        for i in idx:
            for j in idx: P[i, j] = 1.0 / sz
    return P

def defect(K, P): return (np.eye(K.shape[0]) - P) @ K @ P

def commutator(K, P): return K @ P - P @ K

def all_partitions(n):
    def helper(items):
        if len(items) == 1: yield [frozenset(items)]; return
        first = items[0]
        for partition in helper(items[1:]):
            for i in range(len(partition)):
                yield partition[:i] + [partition[i] | {first}] + partition[i+1:]
            yield [frozenset({first})] + partition
    return [p for p in helper(list(range(n))) if len(p) > 1]

# n=5: 3125 maps x 51 partitions = 159375 pairs
n = 5
parts = all_partitions(n)
print(f"n={n}: {n**n} maps, {len(parts)} partitions, {n**n * len(parts)} total pairs")

t001 = t002 = t003 = t005 = 0
total = 0
rank_dist = defaultdict(int)

for T in itertools.product(range(n), repeat=n):
    T = list(T); K = K_mat(T)
    for P in parts:
        Pm = P_mat(P, n)
        D = defect(K, Pm)
        C = commutator(K, Pm)
        rD = int(np.linalg.matrix_rank(D, tol=1e-8))
        rC = int(np.linalg.matrix_rank(C, tol=1e-8))
        
        ok1 = np.linalg.norm(D @ D) < 1e-9
        ok2 = (np.linalg.norm(D) < 1e-9) == np.allclose(K @ Pm, Pm @ K @ Pm)
        ok3 = rD <= rC
        ok5 = rD <= n - len(P)
        
        t001 += int(ok1); t002 += int(ok2); t003 += int(ok3); t005 += int(ok5)
        total += 1
        rank_dist[rD] += 1

print(f"\nT001 D²=0:          {t001}/{total} ({100*t001/total:.1f}%) PASS={t001==total}")
print(f"T002 D=0↔KP=PKP:    {t002}/{total} ({100*t002/total:.1f}%) PASS={t002==total}")
print(f"T003 rank(D)≤rank(C): {t003}/{total} ({100*t003/total:.1f}%) PASS={t003==total}")
print(f"T005 rank(D)≤n-m:    {t005}/{total} ({100*t005/total:.1f}%) PASS={t005==total}")
print(f"\nRank distribution: {dict(sorted(rank_dist.items()))}")======================================================================
AQARION CONTINUATION: n=5 EXHAUSTIVE CENSUS
======================================================================
n=5: 3125 maps, 51 partitions, 159375 total pairs
T001 D²=0:          159375/159375 (100.0%) PASS=True
T002 D=0↔KP=PKP:    159375/159375 (100.0%) PASS=True
T003 rank(D)≤rank(C): 159375/159375 (100.0%) PASS=True
T005 rank(D)≤n-m:    159375/159375 (100.0%) PASS=True

Rank distribution: {0: 36175, 1: 106700, 2: 16500}
import numpy as np
from collections import defaultdict

def kaprekar_step(n):
    s = f"{n:04d}"
    desc = int(''.join(sorted(s, reverse=True)))
    asc = int(''.join(sorted(s)))
    return desc - asc

def gap_pair(n):
    s = sorted(f"{n:04d}")
    return (int(s[3]) - int(s[0]), int(s[2]) - int(s[1]))

gap_classes = defaultdict(list)
for n in range(10000):
    gap_classes[gap_pair(n)].append(n)

pairs = sorted(gap_classes.keys())
idx = {p: i for i, p in enumerate(pairs)}

def F_xy(x, y):
    return 999 * x + 90 * y

T55 = []
for p in pairs:
    n_val = F_xy(p[0], p[1])
    next_n = kaprekar_step(n_val)
    next_p = gap_pair(next_n)
    T55.append(idx[next_p])

# Verify all states in same class map to same target class
consistent = True
for p in pairs:
    class_idx = idx[p]
    sample = F_xy(p[0], p[1])
    target = gap_pair(kaprekar_step(sample))
    target_idx = idx[target]
    for state in gap_classes[p]:
        actual_target = gap_pair(kaprekar_step(state))
        actual_idx = idx[actual_target]
        if actual_idx != target_idx:
            consistent = False
            break
    if not consistent:
        break

print(f"Classes: {len(pairs)}")
print(f"Consistent mapping: {'PASS' if consistent else 'FAIL'}")

fixed = [i for i in range(55) if T55[i] == i]
print(f"Fixed points: {len(fixed)} at {fixed}")

# Depths
from collections import deque
pre = defaultdict(list)
for i in range(55):
    pre[T55[i]].append(i)

depths = {}
queue = deque(fixed)
for f in fixed:
    depths[f] = 0
while queue:
    node = queue.popleft()
    for p in pre[node]:
        if p not in depths:
            depths[p] = depths[node] + 1
            queue.append(p)

print(f"Max depth: {max(depths.values())}")

# Signatures
sig = {}
for x in range(55):
    orbit = []
    c = x
    for _ in range(20):
        orbit.append(c)
        if T55[c] == c:
            break
        c = T55[c]
    sig[x] = tuple(orbit)

unique_sigs = len(set(sig.values()))
print(f"Distinct signatures: {unique_sigs}")
print(f"Minimality: {'PASS' if unique_sigs == 55 else 'FAIL'}")Classes: 55
Consistent mapping: FAIL
Fixed points: 2 at [0, 23]
Max depth: 3
Distinct signatures: 55
Minimality: PASS
import numpy as np
from collections import defaultdict

def kaprekar_step(n):
    s = f"{n:04d}"
    desc = int(''.join(sorted(s, reverse=True)))
    asc = int(''.join(sorted(s)))
    return desc - asc

def gap_pair(n):
    s = sorted(f"{n:04d}")
    return (int(s[3]) - int(s[0]), int(s[2]) - int(s[1]))

gap_classes = defaultdict(list)
for n in range(10000):
    gap_classes[gap_pair(n)].append(n)

pairs = sorted(gap_classes.keys())
idx = {p: i for i, p in enumerate(pairs)}

def F_xy(x, y):
    return 999 * x + 90 * y

# Find the inconsistency
for p in pairs:
    sample = F_xy(p[0], p[1])
    target = gap_pair(kaprekar_step(sample))
    target_idx = idx[target]
    for state in gap_classes[p]:
        actual_target = gap_pair(kaprekar_step(state))
        actual_idx = idx[actual_target]
        if actual_idx != target_idx:
            print(f"Inconsistency found:")
            print(f"  Class: {p}")
            print(f"  Sample state: {sample:04d} (gap={gap_pair(sample)})")
            print(f"  Sample maps to: {kaprekar_step(sample)} (gap={target}, idx={target_idx})")
            print(f"  State {state:04d} (gap={gap_pair(state)})")
            print(f"  Maps to: {kaprekar_step(state)} (gap={actual_target}, idx={actual_idx})")
            print(f"  Class members: {sorted(gap_classes[p])[:10]}")
            break
    else:
        continue
    breakInconsistency found:
  Class: (1, 0)
  Sample state: 0999 (gap=(9, 0))
  Sample maps to: 8991 (gap=(8, 1), idx=37)
  State 0001 (gap=(1, 0))
  Maps to: 999 (gap=(9, 0), idx=45)
  Class members: [1, 10, 100, 111, 1000, 1011, 1101, 1110, 1112, 1121]
import numpy as np
from collections import defaultdict

def kaprekar_step(n):
    s = f"{n:04d}"
    desc = int(''.join(sorted(s, reverse=True)))
    asc = int(''.join(sorted(s)))
    return desc - asc

def gap_pair(n):
    s = sorted(f"{n:04d}")
    return (int(s[3]) - int(s[0]), int(s[2]) - int(s[1]))

gap_classes = defaultdict(list)
for n in range(10000):
    gap_classes[gap_pair(n)].append(n)

pairs = sorted(gap_classes.keys())
idx = {p: i for i, p in enumerate(pairs)}

def F_xy(x, y):
    return 999 * x + 90 * y

# Verify consistency
T55 = {}
for p in pairs:
    n_val = F_xy(p[0], p[1])
    next_n = kaprekar_step(n_val)
    next_p = gap_pair(next_n)
    T55[p] = next_p

consistent = True
for p in pairs:
    target_p = T55[p]
    target_idx = idx[target_p]
    for state in gap_classes[p]:
        actual_p = gap_pair(kaprekar_step(state))
        if actual_p != target_p:
            consistent = False
            break
    if not consistent:
        break

print(f"Classes: {len(pairs)}")
print(f"Consistent: {'PASS' if consistent else 'FAIL'}")

T55_idx = [idx[T55[p]] for p in pairs]
fixed = [i for i in range(55) if T55_idx[i] == i]
print(f"Fixed: {fixed}")

# Depths
from collections import deque
pre = defaultdict(list)
for i in range(55):
    pre[T55_idx[i]].append(i)

depths = {}
queue = deque(fixed)
for f in fixed:
    depths[f] = 0
while queue:
    node = queue.popleft()
    for p in pre[node]:
        if p not in depths:
            depths[p] = depths[node] + 1
            queue.append(p)

print(f"Max depth: {max(depths.values())}")

# Signatures
sig = {}
for x in range(55):
    orbit = []
    c = x
    for _ in range(20):
        orbit.append(c)
        if T55_idx[c] == c:
            break
        c = T55_idx[c]
    sig[x] = tuple(orbit)

unique = len(set(sig.values()))
print(f"Distinct signatures: {unique}")
print(f"Minimality: {'PASS' if unique == 55 else 'FAIL'}")Classes: 55
Consistent: FAIL
Fixed: [0, 23]
Max depth: 3
Distinct signatures: 55
Minimality: PASS
import numpy as np
from collections import defaultdict

def kaprekar_step(n):
    s = f"{n:04d}"
    desc = int(''.join(sorted(s, reverse=True)))
    asc = int(''.join(sorted(s)))
    return desc - asc

def gap_pair(n):
    s = sorted(f"{n:04d}")
    return (int(s[3]) - int(s[0]), int(s[2]) - int(s[1]))

gap_classes = defaultdict(list)
for n in range(10000):
    gap_classes[gap_pair(n)].append(n)

pairs = sorted(gap_classes.keys())
idx = {p: i for i, p in enumerate(pairs)}

def F_xy(x, y):
    return 999 * x + 90 * y

# Find first inconsistency
for p in pairs:
    n_val = F_xy(p[0], p[1])
    next_n = kaprekar_step(n_val)
    target_p = gap_pair(next_n)
    for state in gap_classes[p]:
        actual_p = gap_pair(kaprekar_step(state))
        if actual_p != target_p:
            print(f"Inconsistency:")
            print(f"  Class: {p}")
            print(f"  Canonical: {n_val:04d} -> {next_n:04d} (gap={target_p})")
            print(f"  State: {state:04d} -> {kaprekar_step(state):04d} (gap={actual_p})")
            break
    else:
        continue
    breakInconsistency:
  Class: (1, 0)
  Canonical: 0999 -> 8991 (gap=(8, 1))
  State: 0001 -> 0999 (gap=(9, 0))
# The gap-pair is NOT a congruence. The canonical representative F_xy(x,y) = 999x + 90y
# does NOT capture all states with the same gap-pair.
# 
# The issue: 0001 has digits [0,0,0,1], sorted = [0,0,0,1], gap = (1-0, 0-0) = (1,0)
# But 0999 has digits [0,9,9,9], sorted = [0,9,9,9], gap = (9-0, 9-9) = (9,0)
# 
# So 0001 and 0999 are NOT in the same gap-pair class! Let me check...

def gap_pair(n):
    s = sorted(f"{n:04d}")
    return (int(s[3]) - int(s[0]), int(s[2]) - int(s[1]))

print(f"gap_pair(0001) = {gap_pair(1)}")
print(f"gap_pair(0999) = {gap_pair(999)}")
print(f"gap_pair(1000) = {gap_pair(1000)}")
print(f"gap_pair(1110) = {gap_pair(1110)}")

# The gap-pair class (1,0) contains states like 0001, 0010, 0100, 1000, 0111, etc.
# But 0999 is in class (9,0), not (1,0).
# 
# The bug was in my canonical representative selection. F_xy(1,0) = 999*1 + 90*0 = 999.
# But 999 has digits [9,9,9], not [0,9,9,9]. The canonical representative should be
# constructed with leading zeros.
# 
# Actually, the issue is that F_xy(x,y) = 999x + 90y produces numbers like:
#   F_xy(1,0) = 999 -> digits [9,9,9] -> gap (9-9, 9-9) = (0,0)
# 
# This is wrong. The canonical representative should be a 4-digit number with
# digits that produce the desired gap-pair.
# 
# For gap-pair (a,b) where a >= b:
#   digits: [d, d+b, d+b, d+a] for some d
#   Example: (1,0): [0,0,0,1] = 0001, or [1,1,1,2] = 1112, etc.
# 
# The canonical representative is NOT unique. The gap-pair class contains
# ALL numbers whose sorted digits have the given gaps.
# 
# The correct verification: for each gap-pair p, the set of states is gap_classes[p].
# The quotient map T_55 is defined by: for any state in class p, its Kaprekar image
# is in some class q. We need to verify that ALL states in p map to the SAME class q.

from collections import defaultdict

gap_classes = defaultdict(list)
for n in range(10000):
    gap_classes[gap_pair(n)].append(n)

pairs = sorted(gap_classes.keys())
idx = {p: i for i, p in enumerate(pairs)}

# Verify: for each class p, all states map to the same target class
consistent = True
for p in pairs:
    targets = set()
    for state in gap_classes[p]:
        target_p = gap_pair(kaprekar_step(state))
        targets.add(target_p)
    if len(targets) > 1:
        print(f"FAIL: class {p} maps to multiple targets: {targets}")
        consistent = False
        break

print(f"\nGap-pair classes: {len(pairs)}")
print(f"All states in each class map to single target class: {'PASS' if consistent else 'FAIL'}")

if consistent:
    # Build correct quotient map
    T55 = {}
    for p in pairs:
        state = gap_classes[p][0]  # any representative
        target_p = gap_pair(kaprekar_step(state))
        T55[p] = target_p
    
    T55_idx = [idx[T55[p]] for p in pairs]
    fixed = [i for i in range(55) if T55_idx[i] == i]
    print(f"Fixed points: {fixed}")
    
    # Depths
    from collections import deque
    pre = defaultdict(list)
    for i in range(55):
        pre[T55_idx[i]].append(i)
    
    depths = {}
    queue = deque(fixed)
    for f in fixed:
        depths[f] = 0
    while queue:
        node = queue.popleft()
        for p in pre[node]:
            if p not in depths:
                depths[p] = depths[node] + 1
                queue.append(p)
    
    print(f"Max depth: {max(depths.values())}")
    
    # Signatures
    sig = {}
    for x in range(55):
        orbit = []
        c = x
        for _ in range(20):
            orbit.append(c)
            if T55_idx[c] == c:
                break
            c = T55_idx[c]
        sig[x] = tuple(orbit)
    
    unique = len(set(sig.values()))
    print(f"Distinct signatures: {unique}")
    print(f"Minimality: {'PASS' if unique == 55 else 'FAIL'}")gap_pair(0001) = (1, 0)
gap_pair(0999) = (9, 0)
gap_pair(1000) = (1, 0)
gap_pair(1110) = (1, 0)

Gap-pair classes: 55
All states in each class map to single target class: PASS
Fixed points: [0, 23]
Max depth: 6
Distinct signatures: 55
Minimality: PASSVERIFICATION_INDEX.yml created
Size: 1194 characters

AQ-T001_Evidence_Object.yml created
Size: 1076 characters

NEGATIVE_CLAIMS.yml created
Size: 1049 characters

======================================================================
EXTERNAL ARTIFACT ALIGNMENT COMPLETE
======================================================================

Files created:
  1. VERIFICATION_INDEX.yml (integration layer)
  2. AQ-T001_Evidence_Object.yml (vertical certificate example)
  3. NEGATIVE_CLAIMS.yml (claim firewall)

Priority queue updated:
  P0: Artifact Integration (VERIFICATION_INDEX.yml)
  P1: AQ-T001 Vertical Certificate (proof → Lean → computation → audit)
  P2: Dependency Firewall v2 (circular detection, maturity inheritance)
  P3: Mathematical Expansion (Functional Graph, Fiber Layer, Kaprekar Bridge)
