
# [8] CLAIMS_REGISTRY.md, COUNTEREXAMPLES.md, JUNE-CHECKPOINT.MD
# [9] CI/CD workflow, verify_hashes.py, README.md

claims_registry = '''# AQARION Claims Registry v30.2

> **Governance Rule**: Every mathematical claim in AQARION MUST have an entry here.
> Claims without registry entries are [L] (unverified) by default.
> Format: `[ID] Claim | Evidence Class | Status | Test ID | Notes`

---

## Evidence Class Legend

| Class | Meaning | Color |
|-------|---------|-------|
| [PV] | Proven Verifiable — Formal proof exists or follows from definitions | 🟢 |
| [CV] | Computationally Verified — Extensive numerical evidence, no proof | 🔵 |
| [CE] | Counterexample Exists — Claim is false, limitation documented | 🔴 |
| [CJ] | Conjecture — Plausible but unproven, active research | 🟡 |
| [L] | Limitation — Known boundary, not a bug but a constraint | 🟠 |
| [W] | Withdrawn — Previously claimed, now retracted | ⚪ |

---

## Core Claims (Pillar I)

### AQ-THM-001: Projection Idempotence
**Claim**: For any partition Π of finite set S, the averaging projection P_Π satisfies P_Π² = P_Π.
- **Evidence Class**: [PV]
- **Status**: ✅ VERIFIED
- **Test ID**: `test_core.py::test_projection_idempotence`, `test_theorems.py::test_thm_001`
- **Proof**: Follows directly from averaging property. Each block contributes rank-1 projector.
- **Lean**: `lc1_projection_idempotent.lean` — COMPLETE
- **Maturity**: 80%

### AQ-THM-002: Zero-Defect Characterization
**Claim**: D_Π = 0 ⟺ Π is an exact dynamical quotient of (S, f).
- **Evidence Class**: [PV]
- **Status**: ✅ VERIFIED
- **Test ID**: `test_core.py::test_zero_defect_exact_quotient`, `test_theorems.py::test_thm_002`
- **Proof**: Forward: D_Π = (I-P)KP = 0 ⟹ KP = PKP ⟹ f respects block structure. Backward: exact quotient ⟹ K maps blocks consistently ⟹ KP = PKP ⟹ D_Π = 0.
- **Lean**: `lc2_zero_defect.lean` — IN PROGRESS
- **Maturity**: 70%

### AQ-THM-003: Refinement Monotonicity (WITHDRAWN)
**Claim**: ||D_Π|| decreases monotonically under refinement.
- **Evidence Class**: [CE] — Counterexample exists
- **Status**: ❌ FALSE (documented in COUNTEREXAMPLES.md#CE-001)
- **Test ID**: `test_theorems.py::test_thm_003_refinement_monotonic` (XFAIL)
- **Counterexample**: T = [1,2,0,1], Π₁ = {{0,1,2,3}}, Π₂ = {{0,2},{1,3}}. ||D_{Π₂}|| > ||D_{Π₁}||.
- **Maturity**: 100% (as counterexample)

### AQ-THM-004: Rank Bound
**Claim**: rank(D_Π) ≤ min(n - k, k) where k = |Π|.
- **Evidence Class**: [PV]
- **Status**: ✅ VERIFIED
- **Test ID**: `test_core.py::test_defect_rank_bound`, `test_theorems.py::test_thm_004`
- **Proof**: D_Π = (I-P)KP. rank(I-P) = n-k, rank(P) = k. Submultiplicativity gives bound.
- **Lean**: PENDING
- **Maturity**: 60%

### AQ-THM-005: Canonical Quotient Existence
**Claim**: Every finite dynamical system admits a maximal exact quotient.
- **Evidence Class**: [CJ]
- **Status**: 🟡 CONJECTURE
- **Test ID**: `test_theorems.py::test_thm_005_canonical_quotient_existence`
- **Evidence**: Computational search up to n=20, 1000 random systems per n — all admit canonical quotient.
- **Open Problem**: General proof for arbitrary finite dynamical systems.
- **Maturity**: 40%

### AQ-THM-006: Spectral Radius
**Claim**: For Koopman operator K of finite deterministic system, ρ(K) = 1.
- **Evidence Class**: [PV]
- **Status**: ✅ VERIFIED
- **Test ID**: `test_theorems.py::test_thm_006_spectral_radius_bound`
- **Proof**: K is row-stochastic with entries 0 or 1. By Perron-Frobenius, ρ(K) = 1.
- **Maturity**: 70%

---

## Counterexample Claims

### CE-001: Non-Monotonic Defect
- **Registry**: COUNTEREXAMPLES.md#CE-001
- **Evidence Class**: [CE]
- **Status**: ✅ REPRODUCIBLE
- **Test ID**: `test_counterexamples.py::test_ce_001_non_monotonic_defect`
- **Impact**: AQ-THM-003 withdrawn. Defect optimization is non-convex.

### CE-002: Operator Convention Confusion
- **Registry**: COUNTEREXAMPLES.md#CE-002
- **Evidence Class**: [L]
- **Status**: ✅ DOCUMENTED
- **Test ID**: `test_counterexamples.py::test_ce_002_operator_convention`
- **Impact**: All implementations must explicitly declare Koopman vs. transfer convention.

### CE-003: Empty Block Handling
- **Registry**: COUNTEREXAMPLES.md#CE-003
- **Evidence Class**: [L]
- **Status**: ✅ FIXED
- **Test ID**: `test_counterexamples.py::test_ce_003_empty_block_handling`
- **Impact**: proj() now skips empty blocks.

### CE-004: Float32 Precision Loss
- **Registry**: COUNTEREXAMPLES.md#CE-004
- **Evidence Class**: [L]
- **Status**: ✅ DOCUMENTED
- **Test ID**: `test_counterexamples.py::test_ce_004_float_precision`
- **Impact**: All certification uses Float64 minimum. Float32 flagged as insufficient.

---

## Pillar II Claims (Defect Geometry)

### AQ-THM-101: Defect Fingerprint Uniqueness
**Claim**: The 15-invariant Defect Fingerprint uniquely characterizes D_Π up to unitary equivalence.
- **Evidence Class**: [CJ]
- **Status**: 🟡 CONJECTURE
- **Test ID**: PENDING
- **Maturity**: 10%

---

## Pillar III Claims (Observable Geometry)

### AQ-THM-201: Observable Curvature
**Claim**: The observable curvature κ(Π) = lim_{Π'→Π} ||D_{Π'} - D_Π|| / d(Π',Π)² exists.
- **Evidence Class**: [CJ]
- **Status**: 🟡 CONJECTURE
- **Maturity**: 0%

---

## Pillar IV Claims (Canonical Filtration)

### AQ-THM-301: τ-Filtration Existence
**Claim**: Every finite dynamical system admits a canonical hitting-time filtration.
- **Evidence Class**: [CJ]
- **Status**: 🟡 CONJECTURE
- **Maturity**: 10%

---

## Pillar V Claims (Exact Quotients)

### AQ-THM-401: Quotient Lattice Modularity
**Claim**: The lattice of exact quotients is modular.
- **Evidence Class**: [CJ]
- **Status**: 🟡 CONJECTURE
- **Maturity**: 0%

---

## Maturity Scale

| Claim | Maturity | Target for Paper I |
|-------|----------|-------------------|
| AQ-THM-001 | 80% | 100% |
| AQ-THM-002 | 70% | 100% |
| AQ-THM-003 | 100% (as CE) | N/A |
| AQ-THM-004 | 60% | 80% |
| AQ-THM-005 | 40% | 60% |
| AQ-THM-006 | 70% | 80% |

---

*Last Updated: 2026-07-01*
*Registry Version: 30.2.0*
'''

with open(ROOT / "claims/CLAIMS_REGISTRY.md", "w") as f:
    f.write(claims_registry)

print("✅ claims/CLAIMS_REGISTRY.md")
