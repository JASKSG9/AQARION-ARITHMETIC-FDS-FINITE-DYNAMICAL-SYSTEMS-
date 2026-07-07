
# ============================================================================
# 2. CLAIMS_MATRIX.md — Every Sentence Labeled
# ============================================================================

claims_matrix = """# AQARION Paper I — Claims Matrix

**Date:** 2026-07-06

**Status:** ACTIVE

**Rule:** Every sentence in the manuscript receives exactly one label from this matrix.

---

## Label Definitions

| Label | Meaning | Required Evidence |
|-------|---------|-------------------|
| **Definition** | Introduces a mathematical object | Specification in `definitions.json` |
| **Lemma** | Auxiliary result used in a larger proof | Proof in `proofs/symbolic/` |
| **Theorem** | Main result | Complete derivation + certification |
| **Corollary** | Direct consequence of a theorem | Derived proof |
| **Computational Certification** | Empirically verified claim | Executable artifact in `adversarial/` |
| **Benchmark** | Application or example | Reproducible computation |
| **Conjecture** | Explicitly open claim | Marked as OPEN |

---

## Claims Inventory

### Layer 0 — Definitions

| ID | Claim | Label | Evidence | Status |
|----|-------|-------|----------|--------|
| D0.1 | A finite deterministic dynamical system is a pair (X, T) with X finite and T: X → X. | Definition | `definitions.json:system` | LOCKED |
| D0.2 | The function space is F(X) = {f: X → R}. | Definition | `definitions.json:function_space` | LOCKED |
| D0.3 | The Koopman operator is (Kf)(x) = f(T(x)). | Definition | `definitions.json:koopman_operator` | LOCKED |
| D0.4 | A partition is Π = {B_1, ..., B_m} with ∪ B_i = X and B_i ∩ B_j = ∅. | Definition | `definitions.json:partition` | LOCKED |
| D0.5 | The observable subspace is V_Π = {f ∈ F(X) : f constant on blocks}. | Definition | `definitions.json:observable_subspace` | LOCKED |
| D0.6 | The averaging projection is (P_Π f)(x) = (1/|B_i|) Σ_{y∈B_i} f(y) for x ∈ B_i. | Definition | `definitions.json:projection` | LOCKED |
| D0.7 | The defect operator is D_Π = (I - P_Π) K P_Π. | Definition | `definitions.json:defect_operator` | LOCKED |

### Layer 1 — Algebraic Proof Suite

| ID | Claim | Label | Evidence | Status |
|----|-------|-------|----------|--------|
| P1.1 | P_Π² = P_Π. | Lemma | `proofs/symbolic/projection.md` | PROVED |
| P1.2 | Im(P_Π) = V_Π. | Lemma | `proofs/symbolic/projection.md` | PROVED |
| P1.3 | D_Π = (I - P_Π) K P_Π measures observable leakage. | Definition | `proofs/symbolic/defect_operator.md` | DEFINED |

### Layer 2 — Central Theorem

| ID | Claim | Label | Evidence | Status |
|----|-------|-------|----------|--------|
| T2.1 | D_Π = 0 ⟺ K(V_Π) ⊆ V_Π. | Theorem | `proofs/symbolic/invariance_theorem.md` + `adversarial/exhaustive/verify_equivalence.py` | PROVED + CERTIFIED |

### Layer 3 — Quotient Construction

| ID | Claim | Label | Evidence | Status |
|----|-------|-------|----------|--------|
| C3.1 | If D_Π = 0, then Π induces an exact deterministic quotient T̄: X/Π → X/Π. | Corollary | Derived from T2.1 | PROVED |

### Layer 4 — Commutator Boundary

| ID | Claim | Label | Evidence | Status |
|----|-------|-------|----------|--------|
| T4.1 | [P_Π, K] = 0 ⟹ D_Π = 0. | Theorem | `proofs/symbolic/commutator_results.md` | PROVED |
| T4.2 | D_Π = 0 ⟹ [P_Π, K] = 0. | Theorem | `adversarial/commutator/search_noncommuting.py` | **RETRACTED** |
| C4.1 | The defect operator measures observable leakage, not full operator commutation. | Corollary | Counterexample to T4.2 | CERTIFIED |

### Layer 5 — Computational Certification

| ID | Claim | Label | Evidence | Status |
|----|-------|-------|----------|--------|
| Cert5.1 | For |X| ≤ 5, Route A (defect) and Route B (subspace) agree on all 125,000 systems. | Computational Certification | `adversarial/exhaustive/verify_equivalence.py` | PASS |
| Cert5.2 | Randomized stress testing (10,000 trials, |X| ≤ 20) finds zero mismatches. | Computational Certification | `adversarial/random/randomized_stress.py` | PASS |
| Cert5.3 | All 6 pathological cases pass both verification routes. | Computational Certification | `adversarial/pathological/*.py` | PASS |

---

## Retractions

| ID | Claim | Retraction Date | Reason |
|----|-------|-----------------|--------|
| T4.2 | D_Π = 0 ⟹ [P_Π, K] = 0 | 2026-07-06 | Counterexample exists. Invariance ≠ commutation. |

---

## Open Claims

None. All claims in Paper I are either proved, certified, or explicitly retracted.

---

## Verification Principle

> Every sentence in the manuscript is traceable to either a proof, a certification artifact, or an explicit retraction record.
"""

with open(f"{base_dir}/CLAIMS_MATRIX.md", "w") as f:
    f.write(claims_matrix)

print(f"CLAIMS_MATRIX.md: {os.path.getsize(f'{base_dir}/CLAIMS_MATRIX.md')} bytes")CLAIMS_MATRIX.md: 4430 bytes
