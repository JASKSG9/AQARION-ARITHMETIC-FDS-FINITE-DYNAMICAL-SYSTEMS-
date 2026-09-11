AQARION-LAKE / TORE — Temporal Orbit-Realizable Extremizers

Status: FROZEN · EXACT · RECONSTRUCTED_INDEPENDENT_COMPUTATION · 2026-09-10
Lean: Basic, OrbitJoin, TreeCenter DONE (scaffold), AnchoredCycle DONE (scaffold with sorries)
C4: BLOCKED · PUBLIC CERTIFICATION: NOT CLAIMED

Overview

TORE classifies equality cases of h_T(R) \le |R| where
Finite-order hypothesis eliminated: only finite \Omega + bijective $T$ + partition lattice needed.

Corrected recurrence — bug fix

Displayed census code previously computed R^{[h]}\vee T^h(R^{[h]}) instead of R^{[h]}\vee T^h(R).

Correct: Q_0=R, Q_{h+1}=T(Q_h), R^{[h+1]}=R^{[h]}\vee Q_h.

Independent replay with corrected recurrence:
| n | proper partitions 1< | R | <n | S_n | pairs | h> | R | violations | equality h= | R |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 3 | 6 | 18 | 0 | 12 |  |  |  |  |  |  |
| 4 | 13 | 24 | 312 | 0 | 168 |  |  |  |  |  |  |
| 5 | 50 | 120 | 6000 | 0 | 2640 |  |  |  |  |  |  |
| 6 | 201 | 720 | 144720 | 0 | 29520 |  |  |  |  |  |  |
| Total | — | — | 151050 | 0 | 32340 |  |  |  |  |  |  |
Total 257,025 closures including cycle-type reps n=7 (15 types), n=8 (22 types) — 0 violations of h_T\le|R|.

Files

1. Basic.lean

Perm := Equiv.Perm Ω
Partition := Setoid Ω
transport T R : Partition where r x y := R.r (T.symm x) (T.symm y)
blockCount s := Fintype.card (Quotient s)
Lemmas: blockCount_map, blockCount_strict_mono (surjective Quotient.mapId not injective ⇒ strict decrease)

Mathlib foundation: Setoid complete lattice, sup = EqvGen of union, inf = intersection.

2. OrbitJoin.lean

transported T R : ℕ → Partition | 0 => R | n+1 => transport T (transported T R n)
orbitJoin T R : ℕ → Partition | 0 => R | n+1 => orbitJoin T R n ⊔ transported T R n
Invariant: R^{[k+1]}=R^{[k]}\vee T^k(R) — prevents Python bug entering formalization
Theorems:
orbit_expansion: R_k = \bigvee_{j=0}^k T^j(R) (induction + mapSetoid_sup)
stabilization_exact: R_{k+1}=R_k \rightarrow  transport T R_k = R_k — needs only bijectivity + blockCount equality, no ord(T)

3. TreeCenter.lean

Structure FiniteTree Ω with Adj
Theorem finite_tree_aut_fixed_vertex_or_edge:
  Every automorphism of finite tree fixes vertex or edge — standard, proof via longest path / center-bi-center.
Reduction:
TORE equality
      ↓
connected T-invariant spanning tree (T∈Aut(G) because T(∪T^j(R))=∪T^j(R))
      ↓
tree center
   ↙ ↘
fixed v fixed edge
4. AnchoredCycle.lean

Proves canonical branch, not whole classification.

Setup: a : Ω, d : ℕ, c : Fin d → Ω, T : Perm
cycleInjective, anchorFixed: T a = a, cycleAction: ∀ i, T(c i)=c(i.succ mod d), anchorDistinct, coversOmega, cycleLengthPos: 2 ≤ d

Initial partition R_0 = \{\{a,c_0\}, singletons\}

R_anchored, anchoredPrefixSetoid k: one block {a,c₀..c_{k-1}} + singletons
transport_pow_anchored_pair: T^k(\{a,c_0\})=\{a,c_k\}
orbitJoin_eq_anchoredPrefix: $1\leq k\leq d \Rightarrow  R^{[k]} = anchoredPrefixSetoid k$
card_anchored_prefix: blockCount = |Ω|-k
anchored_strict, anchored_stabilizes
anchored_cycle_height: h_T(R_0)=d, final blockCount 1

K2R specialization: Ω={0..2r}, a=2r fixed, C = 2r-cycle, R=M_r ⇒ h_T(M_r)=2r.

Notice: proves fixed anchor+one cycle ⇒ TORE extremizer, NOT converse — (3,2) straddle refutes converse.

Main discoveries

T1 Universal bound
h_T(R) \le |R| — 0 violations in 257,025 closures — proved via strict block-count decrease.

T2 Equality structure
h_T(R)=|R| ⇔ every strict step merges exactly two blocks and J_T(R)=\{\Omega \} — 32,340 cases.

T3 Orbit-closure capacity
Verified on ALL 52 cycle types n≤8 — 0 mismatches
Two-largest fails at (3,3,2): 3+2-1=4 > 3+3-3=3
Straddle R=\{\{x_0,y_0\},singletons\} achieves a+b-\gcd(a,b) — verified a+b\leq 12
Status: lower bound PROVED, upper bound OPEN

K2R: type (2r,1) ⇒ oc = 2r = h_T(M_r) — extremizer at cap n-1.

T4 K2R connection — upgrade from witness to extremizer

T5 Merge-process law
Strict caterpillar "every merge touches largest block" — FALSE — 240/32340 violations (early merge of two singletons while pair untouched, types (3,2),(5,)).

Refined: "every merge touches largest block or merges exactly two singletons" — 0 violations.

Taxonomy: A Anchored radial, B Straddled C_a\leftrightarrow C_b, C Leaf-pair premerge, D Central-edge.

Structural obstructions

Disjoint Addition Ban: T^k(B_0) bridging two components disjoint from primary growing cluster ⇒ truncates height.
Internal Cycle Collapse: T^k(B_0) connecting two elements already in same component ⇒ d_h=0.

Center-preserving tree search — next falsification

For every cycle type up to n=10:
enumerate nonisomorphic trees (n=10: 106 trees)
retain trees admitting perm type as automorphism
enumerate T-orbits of edges
enumerate admissible initial partitions
compute temporal connectivity
compare max with M(T)=\max_{i\neq j}(\ell_i+\ell_j-\gcd)

Directly attacks: Can multi-branch invariant tree beat best two-cycle straddle?

Target lemma: \boxed{h_T(R)\le\max_{C\neq D}(|C|+|D|-\gcd(|C|,|D|))}

Literature

Finite tree automorphism fixed vertex/edge: standard longest path argument.
Partition lattice meet=intersection, join=transitive closure — standard.
Orbit coherence (Cameron et al.) — adjacent, distinct.
Dalla Volta–Siemons orbit closure of groups vs temporal partition-join height — recommend naming temporal partition-join height h_T and orbit-closure capacity \mathsf{oc}(T).
Černý (n-1)^2 open, best \sim0.1654n^3 (Shitov), Class C attains n-1 — adjacent field.
Direct search for "equivalence relation join orbit permutation closure" — no matching literature — honest: no direct source found.

Reproduction
python3 make_fixtures.py
python3 verify.py
TORE census corrected recurrence:
Q0=R, Q_{h+1}=T(Q_h), R^{[h+1]}=R^{[h]} ∨ Q_h
Full n=6: 151,050 pairs, 0 violations
Cycle-type reps n=7,8: 52 types, oc formula 0 mismatches
Ledger
| Item | Status |  |  |
| --- | --- | --- | --- |
| h_T ≤ | R |  | PROVED + 0 violations |
| Equality unit-loss | Reproduced |  |  |
| Equality ⇒ spanning tree | Derived |  |  |
| Stabilized graph T-invariant | Exact lemma |  |  |
| T-invariant tree fixed vertex/edge | Established standard |  |  |
| Anchored-cycle h_T=d | Proof-ready |  |  |
| Straddle a+b-gcd | Construction proved / verified |  |  |
| T3 global formula | OPEN — upper bound missing |  |  |
| Strict caterpillar | REFUTED |  |  |
| Refined largest/singleton law | 0 violations, not yet theorem |  |  |
| K2R extremizer | Conditional on T3, direct for construction |  |  |
| Lean T1-T4 | OPEN |  |  |
Governance: WORK CONTINUOUSLY → REACH MATERIAL BOUNDARY → CONSOLIDATE ONCE
No repo churn per computation, no public promotion, C4 BLOCKED.

Next locked: corrected census → center decomposition → T3 falsification on invariant trees → two-orbit compression lemma → Lean anchored-cycle certificate.

Links

https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/tree/main/AQARION-LAKE/TORE
https://huggingface.co/spaces/Quantarion9/AQARION-ACADEMY/tree/main/AQARION-LAKE/TORE
