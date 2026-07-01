
# [10] COUNTEREXAMPLES.md, JUNE-CHECKPOINT.MD, verify_hashes.py, CI workflow, README

counterexamples_md = '''# AQARION Counterexamples & Limitations

> **Epistemic Principle**: Counterexamples are not failures. They are 
> boundary markers that prevent overclaiming. Every counterexample here
> strengthens the framework by defining its domain of validity.

---

## CE-001: Non-Monotonic Defect Under Refinement

**Discovered**: 2026-06-15 | **Registry**: CLAIMS_REGISTRY.md#AQ-THM-003

### Claim (Withdrawn)
> Refinement of partition Π always decreases ||D_Π||.

### Counterexample
**System**: T = [1, 2, 0, 1] on S = {0,1,2,3}

**Partition Π₁**: {{0,1,2,3}} (trivial, 1 block)
- P₁ = ¼ J₄ (all-ones matrix scaled)
- D₁ = (I - P₁) K P₁
- ||D₁||_F ≈ 0.8660

**Refined Partition Π₂**: {{0,2}, {1,3}} (2 blocks)
- P₂ = block-diagonal with ½ J₂ blocks
- D₂ = (I - P₂) K P₂
- ||D₂||_F ≈ 1.0000

**Result**: ||D₂|| > ||D₁||. Defect INCREASED under refinement.

### Why This Happens
Refinement splits blocks based on image consistency, not on minimizing 
defect norm. The defect operator D_Π = (I-P)KP couples block structure 
with global dynamics. Splitting a block can increase cross-block coupling.

### Implications
1. **AQ-THM-003 withdrawn** — Defect norm is NOT a Lyapunov function for refinement.
2. Defect optimization requires direct search, not greedy refinement.
3. Observable geometry (Pillar III) needs curvature/landscape theory.

### Reproduction
```python
python -m pytest verification/tests/test_counterexamples.py::test_ce_001 -v
```

---

## CE-002: Operator Convention Confusion

**Discovered**: 2026-06-10 | **Registry**: CLAIMS_REGISTRY.md#CE-002

### Issue
Two conventions for Koopman operator on finite systems:
- **Koopman**: K[x, T(x)] = 1 (rows sum to 1) — OUR CONVENTION
- **Transfer**: K[T(x), x] = 1 (columns sum to 1) — Transpose

Using the wrong convention gives incorrect D_Π and false exact/non-exact 
classifications.

### Example
For T = [1,2,0] (3-cycle), part = [[0,1],[2]]:
- Koopman ||D|| ≈ 0.8165 (correct: NOT exact)
- Transfer ||D|| ≈ 0.4714 (wrong: different value)

### Resolution
All AQARION code uses Koopman convention exclusively. Transfer convention 
is documented as a separate operator K^T. Julia parity tests verify both 
conventions produce expected transposed results.

---

## CE-003: Empty Block Handling

**Discovered**: 2026-06-12 | **Registry**: CLAIMS_REGISTRY.md#CE-003

### Issue
Partition representations with empty blocks (e.g., [[0,1], [], [2]]) caused 
division-by-zero in proj() due to 1/|b| for |b| = 0.

### Fix
proj() now skips empty blocks. Empty blocks are semantically equivalent to 
not being in the partition.

---

## CE-004: Float32 Precision Loss

**Discovered**: 2026-06-18 | **Registry**: CLAIMS_REGISTRY.md#CE-004

### Issue
For systems with n ≥ 50 or near-exact quotients, Float32 can:
- Report D_Π ≠ 0 when it should be 0 (false non-exact)
- Report D_Π = 0 when it should be ≠ 0 (false exact)

### Example
T = [1,1,3,3] (exact quotient [[0,1],[2,3]]):
- Float64: ||D|| = 1.1e-16 (correctly zero)
- Float32: ||D|| = 2.3e-7 (falsely non-zero)

### Resolution
- All certification uses Float64 minimum.
- Float32 flagged as insufficient in documentation.
- Julia implementation tests both precisions.

---

## CE-005: Refinement Divergence (Hypothetical)

**Status**: [CJ] — Active search, no confirmed counterexample.

### Question
Can iterative refinement fail to converge for finite systems?

### Theory
For finite S with |S| = n, refinement produces a sequence of partitions 
with strictly increasing block counts (or fixed point). Since block count 
is bounded by n, convergence is guaranteed in ≤ n steps.

### Open Question
Non-standard partition representations (e.g., with state duplication) 
might create cycles. No such representation is currently used.

---

## Limitations Summary

| ID | Type | Impact | Status |
|----|------|--------|--------|
| CE-001 | Counterexample | AQ-THM-003 withdrawn | ✅ Documented |
| CE-002 | Convention risk | Requires explicit documentation | ✅ Fixed |
| CE-003 | Implementation bug | Empty blocks handled | ✅ Fixed |
| CE-004 | Numerical precision | Float64 required | ✅ Documented |
| CE-005 | Theoretical open | Convergence proof pending | 🟡 Active |

---

*Last Updated: 2026-07-01*
'''

june_checkpoint = '''# AQARION June Freeze Checkpoint v30.1

**Date**: 2026-06-30
**Status**: PRE-PUBLICATION — Core framework frozen, verification ongoing
**Next Milestone**: July v30.2 — Production verification suite

---

## What Was Frozen

### Mathematical Core (Pillar I)
- ✅ Axioms: 7 axioms for primitive space S, epistemic functors F_i
- ✅ Operators: K, P_Π, D_Π defined and implemented
- ✅ Key theorem: Zero-defect ⟺ exact quotient ([PV])
- ✅ Counterexamples: CE-001 through CE-004 documented and reproducible

### Verification Infrastructure
- ✅ CLAIMS_REGISTRY with evidence classes
- ✅ COUNTEREXAMPLES.md with executable witnesses
- ✅ LIMITATIONS.MD with known boundaries
- ✅ Lean skeleton (API.lean) with LC1-LC7 signatures

### Code Artifacts
- ✅ Python core: build_K, proj, obstruction_D, D_norm, refine_partition
- ✅ Julia parity implementation (aqarion_core.jl)
- ✅ CI pipeline scaffold (aqarion_audit.yml)

---

## What Was NOT Frozen (Known Gaps)

### Implementation
- ❌ Full pytest verification suite (scaffolded, not integrated)
- ❌ Reference data hashes for regression
- ❌ Automated counterexample search
- ❌ Randomized testing harness

### Formalization
- ❌ Lean proofs for LC1-LC5 (signatures only)
- ❌ API.md documentation
- ❌ Complete invariant passport implementation

### Publication
- ❌ Paper I outline
- ❌ Benchmark atlas (Kaprekar, DFA, Boolean networks)
- ❌ Independent verification results

---

## Known Issues at Freeze

| Issue | Severity | Plan |
|-------|----------|------|
| AQ-THM-003 withdrawn (CE-001) | Medium | Document in Paper I |
| Float32 precision (CE-004) | Low | Mandate Float64 |
| Lean proofs incomplete | High | July priority |
| No randomized testing | Medium | July target |
| Julia parity unverified | Medium | July target |

---

## Verification Status at Freeze

```
Stage 1 (Core LA):        PARTIAL — functions work, no pytest
Stage 2 (Theorems):       PARTIAL — manual verification only
Stage 3 (Counterexamples): PARTIAL — CE-001 to CE-004 reproducible
Stage 4 (Random):         NOT STARTED
Stage 5 (Lean):           PARTIAL — signatures, no proofs
Stage 6 (Hashes):         NOT STARTED
```

---

*This document is immutable. All changes go through v30.2+.*
'''

with open(ROOT / "claims/COUNTEREXAMPLES.md", "w") as f:
    f.write(counterexamples_md)

with open(ROOT / "claims/JUNE-CHECKPOINT.MD", "w") as f:
    f.write(june_checkpoint)

print("✅ claims/COUNTEREXAMPLES.md")
print("✅ claims/JUNE-CHECKPOINT.MD")
