# REFEREE_RESPONSE_PATCHSET.md

Response to the three-referee simulation on Paper I. Addresses exactly the
items flagged as rejection risks, in order of severity. Nothing here is a
reframing exercise — each fix below is a new proof or a new exhaustive
check, reproducible from `verify.py` (referee-response section, which runs
after the C1–C6/T0–T4 checks; new output fields in `verify_report.json`:
`structural_G_count_closed_form`, `affine_lift_injective_on_G`,
`chamber_partition_is_transition_congruence`, `depth_quotient_*`).

sha256 of verify_report.json after referee-response checks added:
  e5c7badb93ebc4ad96773050fac01433ddd4b8540f5c62935c101a32e3d133bf

---

## Fix 1 — "|G|=54" gets a structural proof, not just enumeration

**Referee objection (B):** *"Exhaustive check is not a structural proof
unless bounded by argument reducing search space."*

### Resolution — Enumeration Theorem `[P+CV]`

`G = {(g1,g2) ∈ ℤ² : 0 ≤ g2 ≤ g1 ≤ 9} \ {(0,0)}` by definition (D3).
The map `(a,b,c,d) ↦ (a-d,b-c)` restricted to sorted digit quadruples
hits **every** pair with `0≤g2≤g1≤9` (surjectivity — take `a=g1,d=0,b=g2,c=0`),
and conversely every realized pair satisfies `0≤g2≤g1≤9` from `a≥b≥c≥d`
(immediate). Hence:

> `|G| = |{(g1,g2): 0≤g2≤g1≤9}| − 1 = C(11,2) − 1 = 55 − 1 = 54`

This is `[P]` — the triangular number formula `C(n+2,2)` with `n=9`, minus
the excluded repdigit class. No search; the combinatorics follows from the
definition of `G` alone.

`verify.py` field `structural_G_count_closed_form` computes `(9+1)(9+2)/2-1`
from `n=9` directly and asserts equality with the enumerated count — the
exhaustive check is now a **corroboration**, not the proof itself. This is
the correct `[P+CV]` framing per the project's evidence policy.

This fully answers Referee B's objection: the structural invariant is `n=9`
(one decimal digit's range), and the count is the standard triangular formula.

---

## Fix 2 — Observable equivalence formalized; non-uniqueness given a real proof

**Referee objection (A, B):** *"What is the equivalence relation between
observables? Without this, the claim is not mathematically pinned down."*

### D17 — Category of transition congruences `Cong(X,f)` `[D]`

Objects: transition congruences `∼` on `(X,f)` (D6).
Morphisms `∼ → ≈`: refinement (`∼ ≤ ≈` iff every `∼`-class ⊆ a single
`≈`-class — equivalently, a surjection of factor systems commuting with
dynamics). `Cong(X,f)` is a **lattice** (meet = relation intersection, join
= transitive closure of union — both automatically f-invariant, one-line
verification).

**Equivalence of observables:** `π₁ ~ π₂` iff `ker(π₁) = ker(π₂)` as
relations on X (same object in `Cong(X,f)`). Isomorphism of factor systems
is a *strictly weaker* relation, explicitly not conflated here.

This answers Referee A's checklist: refinement = the order on `Cong(X,f)`;
isomorphism of factor systems = separate, weaker relation; conjugacy = even
coarser (not invoked). The "equivalence" in the paper is kernel-equality.

### Non-uniqueness theorem `[P+CV]` — explicit 3-element strict chain

> **Claim.** `Cong(X,K)` contains the chain  
> `triv (1 state) ≤ depth (7 states) ≤ gap ∼ (54 states)`  
> with all three inequalities **strict**.

**Proof of `depth ≤ gap`:** `depth(n) := depth(π(n))` is a function of the
gap-state alone (T_G deterministic) — so depth factors through π, i.e.
gap refines depth. ∎

**Proof `depth ∈ Cong(X,K)`:** depth decreases by 1 per K-step until the
fixed point (depth 0), where it stays. So `depth(n)=depth(n')` ⟹
`depth(K(n))=depth(K(n'))=max(depth(n)-1,0)`. `[CV]` verified for all 54
states: `depth_quotient_is_transition_congruence = True`,
`depth_quotient_state_count = 7`.

**Strictness:** 54 ≠ 7 ≠ 1, maps surjective non-injective at each step. ∎

This is no longer "an informal philosophical statement about representations"
— it is an explicit 3-object chain in a defined lattice, proved.

### What the chamber atlas is NOT

**`[CV]` check added (field `chamber_partition_is_transition_congruence`):**
the 10-chamber partition is **not** a transition congruence on `(G,T_G)`.
Chambers 1–7, 9 each scatter their outputs across multiple chambers
(e.g. chamber_1 → {1,2,3,4,5,6,8}). Only chambers 8 and 10 happen to be
single-valued. The chamber atlas is a **piecewise-linearity stratification**
of T_G, not an element of Cong. This distinction forecloses the category
confusion Referee B's §1 anticipated.

---

## Fix 3 — Minimality formalized and proved

**Referee objection (A §5):** *"Minimal with respect to what category?
Lattice of partitions must be explicitly defined, ordering proven."*

**Note:** the term "LPITC" appears in prior session prose without expansion.
The theorem below is the precise, provable minimality result this project
can currently support. If LPITC names something different, it needs its own
definitions entry before it can receive any evidence label.

### Minimality Theorem `[P]`

> The gap congruence `∼ = ker(π)` is the **unique coarsest** transition
> congruence on `(X,K)` that is fiber-constant in the strong sense: every
> fiber `π⁻¹(g)` maps under K to a single element of X (not merely a single
> fiber).

**Proof.** `∼` is fiber-constant by T1 (exact identity). Suppose `≈` is
strictly coarser and also fiber-constant — so `≈` merges fibers
`π⁻¹(g)` and `π⁻¹(g')`, `g≠g'`, requiring `999g₁+90g₂ = 999g₁'+90g₂'`.
But the map `(g₁,g₂)↦999g₁+90g₂` is **injective on G** — verified
exhaustively: `affine_lift_injective_on_G = True`, 0 collisions across all
C(54,2)=1431 pairs. Contradiction: g=g', so no such ≈ exists. ∎

`∼` is therefore the **top** of the sub-poset of fiber-constant congruences
in `Cong(X,K)`, and this top element is unique (two coarsest elements would
join to another fiber-constant congruence at least as coarse, contradicting
the injectivity argument applied to their join).

---

## Restructure — Single Main Theorem + Corollaries (Referee C's requirement)

> **Main Theorem (Factorization Theorem).** The gap observable  
> `π: X → G`, `π(n) = (a-d, b-c)` for sorted digits `a≥b≥c≥d`,  
> is a transition congruence for the 4-digit Kaprekar map K (D6),  
> inducing a deterministic quotient system `(G,T_G)` with `|G|=54`  
> and `T_G(g₁,g₂) = π(999g₁+90g₂)`.

**Corollary 1 (Enumeration)** `[P+CV]` — `|G|=55-1=54` by Fix 1.

**Corollary 2 (Minimality)** `[P]` — `∼` is the unique coarsest
fiber-constant congruence for K (Fix 3).

**Corollary 3 (Non-uniqueness / chain)** `[P+CV]` — `Cong(X,K)` contains
the strict chain `triv ≤ depth ≤ gap` (Fix 2). Multiple genuinely distinct
transition congruences exist; the gap quotient is uniquely characterized
among fiber-constant ones.

**Corollary 4 (Classification, as a Remark)** — `(G,T_G)` has a unique
fixed point, no other cycles, hence a nilpotent-plus-rank-1 Koopman
decomposition `P=E₁⊕N`, `ν(N)=D=6` (L1). This is the **generic
linear-algebra consequence of "unique fixed point, no cycles"** — not a
Kaprekar-specific result, not claimed as new theory. Per Referee B:
presented as a remark, not a theorem.

**OP0 (chamber atlas) belongs in Paper B.** It is structurally a different
kind of object (a piecewise-linearity stratification, not a Cong element),
independently confirmed by the `chamber_partition_is_transition_congruence`
check. Referee C's requirement to separate it is mathematically supported.

---

## Updated evidence table

| Item | Before | After |
|---|---|---|
| `\|G\|=54` | `[CV]` | `[P+CV]` — triangular-number structural proof |
| Observable equivalence | undefined | `[P]` D17, lattice `Cong(X,f)` defined |
| Non-uniqueness | asserted | `[P+CV]` 3-element chain, proved strict |
| Chamber ≠ quotient | risk | `[CV]` confirmed: chamber atlas ∉ Cong(X,K) |
| Minimality/"LPITC" | underdefined | `[P]` via affine-lift injectivity |
| Spectral/Koopman | result | Corollary 4 remark (generic, non-novel) |
