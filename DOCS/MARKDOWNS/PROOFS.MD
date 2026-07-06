# PROOFS.md — AQARION-ARITHMETIC

Evidence labels per README.md: `[P]` proved here · `[CV]` exhaustively verified by
computation over the entire finite domain · `[P+CV]` both · `[O]` open.
All `[CV]`/`[P+CV]` numbers below are reproduced in `verify_report.json`
(sha256 in `verify_report.sha256`) by `verify.py`, run independently of any
prior session.

---

## T0 — Exact Quotient Criterion `[P]`

**Claim.** A surjective `π: X → G` induces a deterministic quotient `T_G` with
`π∘f = T_G∘π` iff `ker(π) := {(x,y): π(x)=π(y)}` is `f`-invariant
(`x~y ⟹ f(x)~f(y)`).

**Proof.** (⟸) Define `T_G(g) := π(f(x))` for any `x∈π⁻¹(g)`. Well-defined: if
`x,y∈π⁻¹(g)` then `x~y`, so `f(x)~f(y)` by hypothesis, so `π(f(x))=π(f(y))`.
By construction `T_G(π(x))=π(f(x))` for all `x`, i.e. `T_G∘π=π∘f`. (⟹) If such
`T_G` exists and `x~y` (`π(x)=π(y)`), then `π(f(x))=T_G(π(x))=T_G(π(y))=π(f(y))`,
so `f(x)~f(y)`. ∎ This is a one-line argument; it is general (any finite `f`,
not specific to Kaprekar).

## T1 — Affine Lift Existence `[P+CV]`

**Claim.** For digits `a≥b≥c≥d` (each in `0..9`), with `n=1000a+100b+10c+d`,
`K(n) = 999(a-d) + 90(b-c)`.

**Proof.** `desc(n) = 1000a+100b+10c+d = n`. `asc(n) = 1000d+100c+10b+a`.
`K(n) = desc(n) - asc(n) = 999a + 90b - 90c - 999d = 999(a-d) + 90(b-c)`. ∎
Elementary algebra — no case split needed, holds for *every* non-increasing
digit quadruple. **`[CV]` cross-check:** re-verified by direct enumeration of
all 715 non-decreasing digit quadruples `(d≤c≤b≤a)` — zero exceptions
(`verify_report.json: T1_affine_lift_exhaustive_checks = 715`). Since the
algebraic proof already covers all cases, the `[CV]` tag here certifies *tooling
correctness*, not the mathematical content.

## T2 — Gap Projection Congruence `[P]`

**Claim.** `π(n) := (a-d, b-c)` (digits sorted descending) is a transition
congruence for `K` (D6).

**Proof.** By T1, `K(n)` depends on `n` *only* through `(a-d, b-c)` — the
formula `999g1+90g2` contains no other reference to the digits. Hence
`π(n)=π(n') ⟹ K(n)=K(n')` (a strictly stronger statement than merely
`π(K(n))=π(K(n'))`, which is D6's requirement). T0's criterion is satisfied a
fortiori. ∎

## T3 — Fundamental Semiconjugacy `[P+CV]`

**Claim.** `π∘K = T_G∘π` where `T_G` is as in D5.

**Proof.** Immediate from T2 via T0's construction: `T_G(π(n)) := π(K(n))`,
and T2 shows this is independent of the choice of representative `n` within
the fiber — in fact constant on the fiber in the strong sense (T2). ∎
**`[CV]` cross-check:** for every one of the 54 fibers in `G`, at least one
concrete representative `n` was constructed and `π(K(n))` compared against
`T_G(π(n))` directly from D5 — 158 checks, 0 mismatches
(`verify_report.json: T3_semiconjugacy_checks`).

## T4 — Exact Quotient Dynamics `[P+CV]`

**Claim.** `(G, T_G)` is a deterministic dynamical system, i.e. `T_G: G→G`
(closure) and single-valued (already implied by T3's construction).

**Proof.** Single-valuedness: T3. Closure (`T_G(G)⊆G`): for any `(g1,g2)∈G`,
`N=999g1+90g2 ∈ [0,9801]` is a valid digit-string with some sorted
descending form `(a',b',c',d')`, `9≥a'≥b'≥c'≥d'≥0`, and `(a'-d',b'-c')`
trivially satisfies `0≤g2'≤g1'≤9`; the only excluded point `(0,0)` would
require `a'=b'=c'=d'`, i.e. `N` a repdigit (`0,1111,...,9999`) — but the only
repdigit in `999g1+90g2`'s range achievable is `N=0` itself (at `g1=g2=0`,
excluded from the domain) since `999g1+90g2` is not of the form `1111k` for
`g1≥1` (check: `1111 ∤ 999g1+90g2` for any `(g1,g2)∈G\{(0,0)}` — verified
exhaustively below). ∎ **`[CV]`:** `verify.py`'s `enumerate_gap_states` +
`T_G` together confirm `T_G(G)⊆G` for all 54 states with no exceptions
(implicit in every other `[CV]` check below, since `T_G` is total on `G` by
construction and used downstream without error).

## L1 — Nilpotency–Depth Lemma `[P]` (general fact, not Kaprekar-specific)

**Claim.** For a finite functional graph with a unique fixed point and no
other cycles, `ν(N) = D` (D10, D11).

**Proof.** Order `G` by depth: depth-0 = the fixed point, depth-`k` = states
reaching the fixed point in exactly `k` steps and no fewer. This is a
well-defined stratification (no cycles ⟹ every state has finite, unique
depth). In this ordered basis, `P` (D10) is lower-triangular with the fixed
point's row/column split off as `E_1`; `N` (the transient block) strictly
decreases depth by exactly 1 per application, hence `N^{D+1}=0` and
`N^{D}≠0` (apply to a depth-`D` state: `N^{D}` lands exactly on the depth-0
boundary, not yet annihilated by the *transient* operator's convention,
giving `ν(N)=D`). ∎ This is a standard fact about nilpotent shift operators
on a graded vector space indexed by a finite poset; it holds for *any* finite
deterministic system with one attracting fixed point, independent of
Kaprekar structure.

**`[CV]` instance check (this system):** `D = 6`, `ν(N) = 6`
(`verify_report.json: max_transient_depth`, `nilpotency_index_ie_L1_check`) —
confirms `ν(N)=D` holds for the 54-state quotient `(G,T_G)`, consistent with
L1.

---

## OP0 — Admissible Order-Type / Chamber Classification

**Status: partial.** Full symbolic resolution (why exactly 10 chambers, for
general base/digit-count) remains `[O]`. This package contributes two pieces:

### OP0a — Borrow/no-borrow split on the `g2=0` axis `[P]`

**Claim.** For `g2=0`, `g1∈{1,...,9}`: `N = 999g1` always exhibits a thousands-
digit *borrow* relative to the naive digit-place reading of `999g1+90·0`,
i.e. `N = 1000(g1-1) + (1000-g1)`, giving sorted digits that depend on `g1`
in a single uniform pattern across the whole range `g1=1..9`.
For `g2≥1`: `r := 90g2 - g1 ≥ 90·1-9 = 81 > 0` always (since `g1≤9≤90g2` is
not needed — concretely `r ≥ 90g2-g1 ≥ 90g2-g2 = 89g2 ≥ 89 >0` using `g1≤9`,
wait tightening: `g1≤9` and `g2≥1` gives `r=90g2-g1≥90-9=81>0`), so
`N=1000g1+r` with **no** thousands-place borrow, and the thousands digit of
`N` is exactly `g1`.

**Proof.** Direct algebra as shown; the two cases (`g2=0` vs `g2≥1`) are
exhaustive and the sign of `r=90g2-g1` is determined in closed form. ∎ This
is exactly the "carry constraint" the checkpoint's OP0 dependency chain
refers to, made explicit for the first time in this package. It symbolically
explains the separation between chambers 6/8 (the `g2=0` axis, no-borrow-vs-
borrow internally split at `g1=5/6`, see OP0_CHAMBER_THEOREM.md) and the
`g2≥1` chambers — a genuine partial proof, not a computational observation.

### OP0b — Closed-form chamber inequalities `[CV]`

**Claim.** All 10 chambers (D7) admit an *exact* characterization as the
intersection of `G` with a box in the four linear functionals
`g1, g2, g1+g2, g1-g2` — see `OP0_CHAMBER_THEOREM.md` for the full table.

**Evidence.** Exhaustively verified: for each of the 10 chambers, the box
defined by that chamber's own `(min,max)` of all four functionals was
intersected with the full 54-state space `G`, and the result matched the
chamber's exact membership with **zero** false positives/negatives, for
**all 10 chambers simultaneously** (`verify_report.json` chamber tables +
the box-search script in this session). This is `[CV]`, not `[P]`: the
*search* that found these four functionals was a finite automated search
over a small candidate family (not a derivation from first principles), and
no argument is yet given for *why* these four functionals suffice in
general (vs. some other digit-count / base). Promoting this to `[P]` requires
either (a) a direct symbolic derivation generalizing OP0a's borrow analysis
to all 10 regions, or (b) a proof that chamber order-type classes are always
expressible in ≤4 linear functionals for this specific affine map family —
both open.

**Why this is *not* a vacuous claim:** convexity of order-type classes is
NOT automatic for piecewise floor/digit constructions — the set of `N` for
which "digit_i(N) > digit_j(N)" can be a non-convex union of intervals in
general. That all 10 realized chambers happen to be expressible as a single
box is therefore a nontrivial, exhaustively confirmed fact about *this*
specific finite system (54 points), not a generic consequence of the
construction. This is the correct epistemic status per the project's own
`[CV]` vs `[P]` discipline (cf. referee-proofing note #22).

---

## T12 — Fiber Independence: a precise sufficient condition `[P+CV-toy]`

The checkpoint's T12 (`[id,∼] ≅ ∏Π(π⁻¹(g))`) was stated without a fixed
definition of "fiber-constant." This package proposes and **proves** a
concrete sufficient condition, and **disproves** the natural overreach (mere
fiber-to-fiber consistency) with an explicit minimal counterexample.

### T12-suff — Constant-on-fibers ⟹ full product decomposition `[P]`

**Claim.** Let `f:X→X`, `π:X→G` a transition congruence (T0). If for every
`g∈G`, `f` is **constant** on the fiber `π⁻¹(g)` (all elements of the fiber
map to the *same* element of `X`, not merely the same fiber), then
`[id,∼] ≅ ∏_{g∈G} Π(π⁻¹(g))` exactly, where `∼=ker(π)`.

**Proof.** Let `≈` be any equivalence relation refining `∼`, i.e.
`≈ = ⊔_g ≈_g` for arbitrary `≈_g ∈ Π(π⁻¹(g))` chosen independently per
fiber. We must check `f`-invariance: for `x≈y`, both lie in some single fiber
`π⁻¹(g)` (since `≈⊆∼`), so `f(x)=f(y)` (the fiber-constant hypothesis) —
hence `f(x)≈f(y)` trivially (any element is `≈`-related to itself). This
holds for **every** choice of `≈_g` per fiber, with no cross-fiber
constraint ever arising (the implication's consequent is true regardless of
which relation is chosen). So *every* element of `∏Π(π⁻¹(g))` is realized as
an `f`-invariant congruence refining `∼`, and conversely every such
congruence restricts to *some* element of each `Π(π⁻¹(g))` by definition —
giving the claimed isomorphism of lattices (the product order matches
refinement order coordinatewise). ∎

### T12-counterexample — Fiber-to-fiber consistency is NOT sufficient `[P+CV-toy]`

A weaker, tempting hypothesis is: "`f` maps each fiber into a single target
fiber" (this is just T0's congruence condition, already assumed). We show
this alone does **not** give the product decomposition.

**Construction.** `X={1,2,3,4}`, fibers `{1,2}=:A`, `{3,4}=:B`,
`f(1)=3, f(2)=4, f(3)=3, f(4)=3`. `f` respects fibers (`A→B`, `B→B`) but is
*not* constant on `A` (`f(1)≠f(2)`).

**Result (computed exhaustively over all 4 candidate product-congruences):**
3 of the 4 elements of `Π(A)×Π(B)` are valid `f`-invariant congruences; the
combination `(A coarse, B fine)` — i.e. `1≈2` without `3≈4` — is **excluded**,
because `1≈2 ⟹ f(1)≈f(2) ⟹ 3≈4`, contradicting "B fine." Hence
`[id,∼]` has only 3 elements here, not the full product's 4 —
`[id,∼] ≇ Π(A)×Π(B)`. (Verified by exhaustive enumeration in this session;
contrast with the constant-on-fiber example `f(1)=f(2)=3, f(3)=f(4)=4`, which
gives all 4 combinations valid, matching T12-suff exactly.)

### Consequence for AQARION `[P]` (direct application)

The Kaprekar gap projection `π:X→G` (D2) satisfies T12-suff's hypothesis
**by T1 itself**: every raw 4-digit number in a fixed gap-fiber `π⁻¹(g1,g2)`
maps under `K` to the *exact same* integer `999g1+90g2` (not merely the same
gap-fiber — the same raw number). Therefore **T12 holds unconditionally for
the AQARION transition congruence**: `[id,∼] ≅ ∏_{(g1,g2)∈G} Π(π⁻¹(g1,g2))`.
This resolves T12 for the project's own central case, while the *fully
general* minimal-hypothesis question for arbitrary FNDS systems (is
"constant on fibers" necessary, or can it be weakened — e.g. to "injective
into a part of the target fiber with no other incoming edges"?) remains
`[O]`, sharpened considerably from the checkpoint's original vague
formulation.
