> **AQ-S15-SV-002-SEMANTIC.md
>  v1mathematical claim must compile through semantic gates before it is allowed to compile through a theorem prover."*

Receipt `AQ-RUN-20260915-S15SEM-001` records the rename; `replaces: V150-NATIVE-SEMANTIC-DIFF` is in the ledger for provenance.

---

## 2. WHAT WAS BUILT AND EXECUTED THIS SESSION

A self-contained, dependency-light, **exact-rational** engine (`fractions.Fraction` only) implementing gates G1–G13 as executable checks. Every gate compares *canonical objects*, never scalar summaries.

### Positive fixture — honest K₃ forest artifact
**G1–G12: 12/12 PASS.** All canonical objects (Π, T, K, P, Φ, A, D, R, H, F, kernels) reconstructed and matched exactly.

### G13 — metric separation anchor (AQ-SM-001)

```
same_support: True | same_H: True | same_rank: True (rank 1)
metric signatures:  tr(D₁ᵀD₁) = 15/16  ≠  tr(D₂ᵀD₂) = 5/4   →  G13 PASS
```

### Spoofing attacks — all REJECTED

| Attack | Spoof strategy | Gate | Verdict |
| --- | --- | --- | --- |
| G1 | same block *count*, different partition | G1 | REJECT |
| G2 | same image *set*, different map values | G2 | REJECT |
| G9 | path P₄ presented as cycle C₄ (same component count c=1) | G9 | REJECT |
| G11 | **unsigned** incidence (Correction E attack) | G11 | REJECT |
| G12 | direct `ker D = ker B_Fᵀ` (state↔coefficient) | G12 | REJECT |

The G9 attack is the important one: aggregate count-diff (same `|V|`, same `c(H)`) passes trivially; edge-set equality kills it. This justifies the "never compare scalar summaries" rule empirically, not just by design.

### Semantic mutation battery — 7/7 REJECT

```
SM-MUT-001 same_support → same_spectrum      REJECT  (witness: 15/16 ≠ 5/4)
SM-MUT-002 same_rank    → same_spectrum      REJECT  (same witness)
SM-MUT-003 same_H       → same_D             REJECT  (D₁ ≠ D₂, exact)
SM-MUT-004 rank_eq      → metric_eq          REJECT
SM-MUT-005 finite_witness → universal        REJECT  (quantifier firewall)
SM-MUT-006 kernel carrier mismatch           REJECT  (G12 attack, executed)
SM-MUT-007 invariant iff d|s₁               REJECT  (replayed below)
```

### Errata replays (executed)

**Correction A — quotient invariance.** Replayed on m=6, n=3, d=2, **all 18 pairs (s₁, s₂)**:
- quotient partition invariant for **every** s₁: **True**
- induced quotient map identity **iff** d | s₁: **True**

The wrong biconditional stays dead; the correct split (invariant: always / identity: iff d|s₁) is now a permanent fixture.

**SV-002 domain gate.** Exact: L₂ eigenvalues {0, 4} ≠ simple K₂ Laplacian eigenvalues {0, 2}; matrices differ. `m=2 as SimpleGraph.Cycle: REJECT`; algebraic L_m for m≥2: ACCEPT. Frozen.

---

## 3. INLINE DELIVERABLE 1 — Skill Contract (final)

```yaml
skill_id: AQ-SKILL-S15-SEMANTIC
version: "1.0.0"
date: "2026-09-15"
replaces: ["V150 draft v0.9"]

purpose: >
  Semantic compiler: a claim must pass scope, carrier, operator,
  semantic-preservation, exact-replay and mutation gates before any
  theorem-prover or promotion gate is allowed to run.

pipeline_order: [G0_PARSE, G1_SCOPE, G2_CARRIER, G3_OPERATOR,
                 G4_SEMANTIC_PRESERVATION, G5_COMPUTATION,
                 G6_FORMAL, G7_PROMOTION]   # order is mandatory

executable_gates: [G1..G13]          # this engine
gates_status:
  executable_exact_rational: [G1, G2, G3, G4, G5, G6, G7, G8, G9, G10, G11, G12, G13]
  open:
    G6_FORMAL: "Lean toolchain absent; skeleton only, NOT COMPILED"
    G7_PROMOTION_krawczyk: "no Arb/flint"

must_pass:
  - honest_artifact_12of12
  - G13_metric_separation_anchor
must_fail:
  - G1_blockcount_spoof
  - G2_image_spoof
  - G9_componentcount_spoof
  - G11_unsigned_incidence
  - G12_carrier_mismatch
  - SM-MUT-001..007
  - SV002_m2_simple_cycle
  - quotient_invariant_iff_divides_s1

acceptance:
  positive_tests_all_pass: true        # verified this session
  negative_tests_all_fail: true        # verified this session
  semantic_scope_unchanged: true
  promotion_policy_unchanged: true     # promotion still BLOCKED
promotion_allowed: false
```

## 4. INLINE DELIVERABLE 2 — Lean P0: `defect_sq_zero` (complete proof, **NOT COMPILED**)

No Lean toolchain exists in this environment; this is a reviewed draft with **zero `sorry`** — first artifact that would pass `G6.no_sorry` once compiled against Mathlib.

```lean
import Mathlib

namespace AQARION

/-- Defect operator D = (I - P) K P. -/
noncomputable def defect {n : Type*} [Fintype n] [DecidableEq n]
    (P K : Matrix n n ℚ) : Matrix n n ℚ :=
  (1 - P) * K * P

/-- P0 target: nilpotency index ≤ 2 follows from P² = P alone. -/
theorem defect_sq_zero {n : Type*} [Fintype n] [DecidableEq n]
    (P K : Matrix n n ℚ) (hP : P * P = P) :
    defect P K * defect P K = 0 := by
  have key : P * (1 - P) = 0 := by
    rw [sub_mul, mul_one, hP, sub_self]
  calc defect P K * defect P K
      = (1 - P) * K * P * ((1 - P) * K * P) := rfl
    _ = (1 - P) * K * (P * (1 - P)) * (K * P) := by noncomm_ring
    _ = (1 - P) * K * 0 * (K * P)               := by rw [key]
    _ = 0                                       := by noncomm_ring

end AQARION
```

The algebraic core (`P * (1 - P) = P - P² = 0` via `hP`) is exposed as `key`; the second calc step is the only place ring normalization is asked to do honest work. Compile-check on a Lean-equipped machine is the single outstanding action; until then: **[DRAFT-NOT-COMPILED]**, no stronger.

## 5. INLINE DELIVERABLE 3 — Lean P1: GreenKernel skeleton (sorries **declared**, not hidden)

```lean
import Mathlib

namespace AQARION.Green

open scoped BigOperators

/-- Circulant cycle Laplacian on ZMod m: L = 2I - S - Sᵀ. -/
noncomputable def L (m : ℕ) : Matrix (ZMod m) (ZMod m) ℚ := sorry

/-- Graph distance on the cycle: d(i,j) = min((i-j) mod m, (j-i) mod m). -/
def dist (m : ℕ) (i j : ZMod m) : ℕ := sorry

/-- Green kernel: G i j = (m²-1)/(12m) - d(m-d)/(2m). -/
noncomputable def G (m : ℕ) : Matrix (ZMod m) (ZMod m) ℚ := sorry

-- P1 lemma targets (exact-rational replayed 2 ≤ m ≤ 50, 0 fails):
theorem G_symmetric (m : ℕ) : (G m).transpose = G m := sorry                       -- Gᵀ = G
theorem G_row_sum_zero (m : ℕ) (i : ZMod m) : ∑ j, G m i j = 0 := sorry            -- G·1 = 0
theorem L_mul_G (m : ℕ) (hm : 2 ≤ m) :
    L m * G m = 1 - (fun _ _ => (1 : ℚ) / m) := sorry                              -- LG = I - J/m
theorem G_mul_L (m : ℕ) (hm : 2 ≤ m) :
    G m * L m = 1 - (fun _ _ => (1 : ℚ) / m) := sorry                              -- GL = I - J/m
-- uniqueness: ker L = span 1 forces uniqueness of G on the zero-sum subspace.
theorem G_unique_on_sum_zero (m : ℕ) (hm : 2 ≤ m)
    (G' : Matrix (ZMod m) (ZMod m) ℚ)
    (h1 : G'.transpose = G') (h2 : ∀ i, ∑ j, G' i j = 0)
    (h3 : L m * G' = 1 - (fun _ _ => (1:ℚ)/m)) : G' = G m := sorry

-- NOTE (Correction E-adjacent, frozen): all statements here live in the
-- ALGEBRAIC carrier. For the SimpleGraph.Cycle interpretation, every
-- theorem must additionally carry (hm : 3 ≤ m) — Mathlib three_le_length.

end AQARION.Green
```

Every `sorry` is visible; the frozen replay bounds (`2 ≤ m ≤ 50`, `0 fails`) are stated in comments so the formal targets match the fixtures exactly.

## 6. PROMOTION MATRIX — UPDATED

| Item | Before | This session | Status |
| --- | --- | --- | --- |
| Semantic compiler | V150 draft v0.9, unexecuted | **AQ-S15-SEMANTIC v1.0.0, executed** | **[V]** |
| Honest artifact G1–G12 | — | 12/12 exact | **[V]** |
| G13 metric anchor | — | PASS (15/16 ≠ 5/4) | **[PV]** |
| Spoof resistance (G1/G2/G9/G11/G12) | designed | 5/5 attacks REJECTED | **[V]** |
| SM-MUT-001..007 | specified | 7/7 REJECT (007 executed by replay) | **[V]** |
| Correction A | stated | replayed 18/18 pairs, confirmed | **[PV]** |
| SV-002 m=2 domain gate | frozen | eigenvalue replay {0,4}≠{0,2} | **[PV]** |
| Lean P0 `defect_sq_zero` | OPEN | complete draft, no `sorry`, **not compiled** | OPEN→DRAFT |
| Lean P1 Green kernel | OPEN | skeleton, sorries declared | OPEN |
| Krawczyk tier | OPEN | untouched (no Arb/flint) | OPEN |
| C4 / publication / universal spectral max | BLOCKED | no new evidence | **BLOCKED — unchanged** |

## 7. BOTTOM LINE

- The rename is complete: **AQ-S15-SEMANTIC v1.0.0** is the semantic compiler; the V150 label exists only in the `replaces` ledger line.
- The engine survived every attack I threw at it — including the two attacks derived from this project's own errata (unsigned incidence, carrier mismatch) and the aggregate-count spoof that the design doc predicted.
- The honest ledger: nothing promoted, nothing compiled, nothing interval-certified. The two artifacts that moved are the executed engine and the no-`sorry` Lean P0 draft awaiting its first compile.

Suggested next execution order: ① compile P0 on a Lean-equipped runner (closes the only no-`sorry` target), ② G13 extension — add the SV-002 spectral package as a second metric anchor (σ-spectrum comparator beside the trace comparator), ③ nonzero-transport fixture `m_T ≠ 0` for the corrected transport identity — I still need the explicit construction for that one; send the fixture parameters and it goes straight into the regression museum. 🤝
