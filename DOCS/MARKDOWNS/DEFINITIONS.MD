# DEFINITIONS.md — AQARION-ARITHMETIC

All later documents (`PROOFS.md`, `CLAIMS_REGISTER.md`) refer back to this file by
symbol. Nothing here is novel terminology — it is the minimal precise vocabulary
needed to state T0–T4, L1, and OP0 without ambiguity.

---

## D1 — The four-digit Kaprekar map K

For an integer `0 ≤ n ≤ 9999`, write `n` as a 4-digit string with leading zeros.
Let `desc(n)` be the number formed by sorting the digits of `n` in non-increasing
order, and `asc(n)` the number formed by sorting them in non-decreasing order
(also read with leading zeros, e.g. digits `(9,8,0,0) → asc = 0089 = 89`).

`K(n) := desc(n) − asc(n)`

`K` is defined on the full space `X = {0,...,9999}` (9999 raw states; the
4-fold repdigits `{0,1111,...,9999}` map to 0 and are conventionally excluded
from the *nontrivial* domain, `|X \ repdigits| = 9990`).

## D2 — Sorted digit representation and the gap vector

For `n ∈ X`, write its digits sorted in non-increasing order as `(a,b,c,d)`,
`9 ≥ a ≥ b ≥ c ≥ d ≥ 0`. Define the **gap vector**

`π(n) := (g1, g2) := (a − d, b − c)`

## D3 — The gap state space G

`G := { (g1,g2) ∈ ℤ² : 0 ≤ g2 ≤ g1 ≤ 9 } \ {(0,0)}`

`(0,0)` is excluded because `g1=g2=0` forces `a=b=c=d`, i.e. exactly the
repdigit class, which `K` sends to `0` trivially and which carries no gap
information. `|G| = 54` (verified [CV], not merely claimed — see
`verify_report.json: C1_state_count`).

## D4 — The affine lift (statement, proof in PROOFS.md §T1)

For any `(a,b,c,d)` with `a≥b≥c≥d`, `999 g1 ≥ 0` and

`K(1000a+100b+10c+d) = 999·g1 + 90·g2`

i.e. `K` factors through `π` via a single *globally exact* affine formula —
no piecewise correction is needed at this stage. (The piecewise structure in
T_G below comes entirely from re-sorting the digits of the **output**.)

## D5 — The quotient map T_G

`T_G : G → G`, `T_G(g1,g2) := π( 999·g1 + 90·g2 )`

i.e. apply D4's formula to get a raw number `N`, then re-extract its gap
vector by D2. `T_G` is well-defined on all of `G` (closure is part of T4).

## D6 — Transition congruence / semiconjugacy

`π` is a **transition congruence** for `K` if `π(x)=π(y) ⟹ π(K(x))=π(K(y))`
for all `x,y` in the domain. Equivalently, there exists `T_G` with

`π ∘ K = T_G ∘ π`   (the **semiconjugacy equation**, T3)

## D7 — Chamber / order-type class

For `(g1,g2) ∈ G`, let `N = 999g1+90g2` (a 4-digit zero-padded string) and let
`ord(g1,g2) ∈ S_4` be the permutation of digit-positions that sorts the digits
of `N` into non-increasing order (ties broken by position index, lowest index
first). Two states are in the same **chamber** iff they share the same
`ord(·,·)`. This is the precise, checkable meaning of "chamber" used in
C1–C3 and OP0; it is *not* a definition by convex region — convexity of each
chamber in `(g1,g2)` is a *theorem* (OP0_CHAMBER_THEOREM.md), not a definition.

## D8 — Branch matrix

A chamber's **branch matrix** `(M_k, t_k)` is the (unique, when full rank;
minimum-norm when rank-deficient) integer pair such that
`T_G(g1,g2) = M_k·(g1,g2)ᵗ + t_k` for every `(g1,g2)` in that chamber.

## D9 — Image filtration

`Im⁰ := G`, `Im^{i+1} := T_G(Im^i)`. The filtration **stabilizes** at the first
`i` with `Im^{i+1} = Im^i`; that fixed set is the eventual image (here, the
single fixed point `{(6,2)}`).

## D10 — Nilpotent transient operator / nilpotency index ν(N)

Let `P` be the 0/1 functional-graph matrix of `T_G` on `G` (`P_{s,T_G(s)}=1`).
`P` has a unique eigenvalue-1 eigenvector (the fixed point indicator); write
`P = E_1 ⊕ N` where `N` acts on the complementary (transient) subspace. `ν(N)`
is the smallest `k` with `N^k = 0`.

## D11 — Maximum transient depth D

For `s ∈ G`, `depth(s) :=` number of applications of `T_G` needed to first
reach a fixed point of `T_G`. `D := max_{s∈G} depth(s)`.

## D12 (L1) — Nilpotency–Depth identity

`ν(N) = D`. (True for *any* finite functional graph with a unique sink and no
nontrivial cycles — a general fact about nilpotent shift operators on a
rooted forest, not specific to Kaprekar; restated here because L1 invokes it.)

---

## FNDS objects (Pillar III) — proposed formalizations, NOT yet author-locked

The checkpoint's FNDS section uses `[id,∼]`, `Π(π⁻¹(g))`, "fiber-constant
transition congruence" without a definitions file. The candidates below are
the most natural reading consistent with D6–D8 above; they are flagged
`[PROPOSED]` and must be confirmed or replaced before T12/T13/T14 can carry a
`[P]` or `[O]` label rather than `[undefined]`.

**[PROPOSED] D13 — Congruence lattice interval `[id, ∼]`**
For a finite `f: X→X` and a congruence `∼` (an `f`-invariant equivalence
relation), `[id, ∼]` denotes the interval of the congruence lattice of `(X,f)`
between the identity relation and `∼`: all congruences `≈` with `id ⊆ ≈ ⊆ ∼`.

**[PROPOSED] D14 — Fiber partition lattice `Π(S)`**
For a set `S`, `Π(S)` is the full partition lattice of `S` (all equivalence
relations on `S`, ordered by refinement).

**[PROPOSED] D15 — Fiber-constant transition congruence**
`∼` is *fiber-constant* (relative to an observation map `π: X→G` with
`∼ = ker(π)`) if for every `g,g' ∈ G` the induced local dynamics
`f|_{π⁻¹(g)} → π⁻¹(f̄(g))` are related by a fixed combinatorial pattern
independent of `g` — concretely, there is an isomorphism of `f`-restricted
structures across all fibers of the same "type." **This is the weakest point
in the current formalization**: "fixed combinatorial pattern" is exactly what
needs to be pinned down before T12 is a real theorem statement. See
`PROOFS.md §T12-status`.

**[PROPOSED] D16 — Candidate T12 statement**
Under D15, `[id,∼] ≅ ∏_{g∈G} Π(π⁻¹(g))` — i.e., congruences refining `∼` from
below decompose as an independent product over fibers, exactly when no
*cross-fiber* coupling is forced by `f`. The precise necessary-and-sufficient
condition on `f` for this product decomposition to hold is the open content
of T12 (see PROOFS.md and the toy counterexample in AUDIT_REPORT.md §T12).
