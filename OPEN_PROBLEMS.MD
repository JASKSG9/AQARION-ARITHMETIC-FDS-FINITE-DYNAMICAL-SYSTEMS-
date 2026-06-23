# AQARION-ARITHMETIC — OPEN PROBLEMS

**Version:** v16.0-freeze  
**Date:** 2026-06-22  
**Scope:** Deterministic quotient theory, induced spectral observables, and extension boundaries  
**Status:** Research roadmap, not theorem claims

---

## 0. Purpose

This file collects the genuinely open questions left by the current AQARION-ARITHMETIC framework. The deterministic finite case is treated as structurally mature, but several extension problems remain unresolved, especially when branching, probabilistic, or uncertain semantics are introduced [web:210][web:213][web:215].

The guiding principle is simple:

> Deterministic quotient semantics are closed enough to certify; branching and uncertainty are not yet closed enough to compress into a single universal theorem.

---

## 1. Core Open Gap

### OP-0: Fixed-point quotient vs behavioral kernel beyond determinism

**Question.** When does the fixed-point quotient construction (
u Phi) coincide with the kernel of the behavioral map in nondeterministic, probabilistic, or uncertainty-bearing systems?

**Why it matters.** In deterministic finite systems, the quotient construction and behavioral equivalence align cleanly. In branching or uncertain systems, the canonical quotient may fail to be unique, and trace semantics may diverge from bisimulation semantics [web:210][web:211][web:213][web:215].

**Current status.** Open.

**Suggested target statement.**
[

u Phi stackrel{?}{=} ker(mathrm{beh})
]
in a suitably enriched coalgebraic setting.

---

## 2. Deterministic-to-Branching Lift

### OP-1: Canonical quotient uniqueness for branching systems

**Question.** Is there a canonical quotient semantics operator for branching systems that behaves like FOQDS in the deterministic case?

**Obstacle.** For nondeterministic systems, bisimulation and trace equivalence are distinct, and no single partition-refinement fixed point is known to serve as a universal quotient in all semantics [web:210][web:211].

**What would count as progress.**
- A functorial quotient operator for branching coalgebras.
- A precise condition under which the fixed point recovers bisimulation.
- A counterexample showing that no such operator exists in full generality.

**Current status.** Open.

---

### OP-2: Trace vs bisimulation collapse conditions

**Question.** Under what functorial or structural hypotheses do trace equivalence and bisimulation coincide?

**Why it matters.** AQARION currently relies on the deterministic collapse where forward bisimulation, trace equivalence, and fixed-point quotienting agree. That collapse is not automatic once branching enters the system [web:211][web:213].

**What would count as progress.**
- A theorem identifying the exact class of functors where collapse holds.
- A semantics-preserving determinization procedure compatible with quotient refinement.
- A counterexample demonstrating unavoidable divergence.

**Current status.** Open.

---

## 3. Uncertainty and Quantitative Semantics

### OP-3: Unified uncertainty coalgebra

**Question.** Can nondeterminism, probability, plausibility, and possibility be embedded into one common coalgebraic quotient semantics?

**Why it matters.** Existing coalgebraic modal frameworks treat uncertainty via different functor classes, but there is no fully unified quotient theory that preserves a deterministic-style fixed point and a canonical behavioral kernel across all uncertainty types [web:213][web:215].

**What would count as progress.**
- A single categorical construction covering powerset, probabilistic, and belief-style semantics.
- A corresponding modal logic with a complete quotient theorem.
- A proof that the construction cannot exist without weakening uniqueness or exactness.

**Current status.** Open.

---

### OP-4: Final semantics under uncertainty

**Question.** When does a final coalgebra exist for the relevant uncertainty functors?

**Why it matters.** The identification of quotient classes with behavioral kernels depends on having a final semantic target. Without final semantics, the “kernel of behavior” interpretation may fail or become non-canonical [web:210][web:213][web:215].

**What would count as progress.**
- Existence theorem for a specific uncertainty functor class.
- A weakened finality notion adequate for quotient semantics.
- A proof of nonexistence for important hybrid functors.

**Current status.** Open.

---

### OP-5: Metric equivalence vs exact equivalence

**Question.** Can the exact quotient theory be lifted to a metric or approximate version in which spectral objects become stability witnesses rather than invariants?

**Why it matters.** Paper II uses induced Koopman, Laplacian, and resistance objects as canonical images of quotienting. In uncertain systems, those objects may only behave approximately, so the relevant notion may become stability rather than equality [web:137][web:212].

**What would count as progress.**
- A robust metric version of FOQDS.
- Stability bounds for quotient-induced operators under perturbation.
- A theorem relating approximate kernels to approximate behavioral equivalence.

**Current status.** Open.

---

## 4. Kaprekar-Specific Open Problems

### OP-6: Cross-base universality

**Question.** Which structural features of the four-digit Kaprekar quotient persist across bases?

**Why it matters.** Recent work in odd bases shows a strong projective-doubling structure after a short transient, suggesting that some quotient geometry may be base-universal while others are not [web:191][web:200][web:208].

**What would count as progress.**
- A theorem classifying quotient sizes across bases.
- A generalization of the 54-state gap quotient to arbitrary odd bases.
- A proof of universality or a family of counterexamples.

**Current status.** Open.

---

### OP-7: Quotient rigidity vs quotient collapse

**Question.** When does an observable quotient preserve enough structure to be rigid, and when does it collapse distinct behaviors?

**Why it matters.** The AQARION benchmark shows both phenomena: a 54-state observable quotient and a 55-state behavioral refinement quotient. The split of one gap class is a concrete rigidity signal, but no general theory yet explains when such splits must occur.

**What would count as progress.**
- A rigidity criterion for quotient splitting.
- A classification of singleton splits in fixed-point refinements.
- A proof that certain observables cannot distinguish fixed points from transients without refinement.

**Current status.** Open.

---

### OP-8: Kaprekar automorphism groups

**Question.** What is the automorphism group of the Kaprekar quotient system, and how does it vary with base?

**Why it matters.** Quotient automorphism groups encode symmetry, rigidity, and possible hidden equivalences. Even in finite deterministic systems, these groups can be subtle.

**What would count as progress.**
- Explicit group computation for the base-10 quotient.
- A family theorem across bases.
- Relations to Green’s relations or semigroup structure.

**Current status.** Open.

---

## 5. Spectral and Operator Questions

### OP-9: Exact meaning of induced spectral observables

**Question.** Can the induced Koopman, Laplacian, and resistance objects be characterized by a single universal quotient-semantics theorem?

**Why it matters.** The stable formulation is that spectral objects are functorial images of the quotient, not invariants of the original system. This is plausible and useful, but it still needs a clean theorem statement and proof architecture.

**What would count as progress.**
- A theorem with precise functoriality hypotheses.
- A commutative diagram showing restriction, projection, and coarse-graining.
- A general proof that all three operators arise as induced images.

**Current status.** Open.

---

### OP-10: Spectral phase transition theorem

**Question.** Under what conditions does observable granularity produce a sharp spectral phase transition in the quotient Laplacian or Koopman restriction?

**Why it matters.** The current framework suggests that refinement can create threshold behavior, but the general theorem has not been written.

**What would count as progress.**
- A monotonicity theorem for the first nonzero Laplacian eigenvalue under refinement.
- A critical-value theorem for observable families.
- A proof that the Kaprekar benchmark is or is not a representative phase-transition model.

**Current status.** Open.

---

### OP-11: Spectral minimal polynomial structure

**Question.** Is there a structural explanation for the observed nilpotent index and minimal polynomial of the quotient Koopman operator?

**Why it matters.** In the base-10 Kaprekar benchmark, the operator data are fully certified computationally, but the algebraic explanation of the nilpotent structure remains incomplete.

**What would count as progress.**
- A proof-level derivation of the nilpotent index.
- A general theorem relating transient depth to minimal polynomial degree.
- A classification of possible Jordan patterns for quotient Koopman operators.

**Current status.** Open.

---

## 6. Approximation and Algorithmic Questions

### OP-12: Exact quotient vs approximation schemes

**Question.** How close are multilevel coarsening schemes such as SHyPar or related graph/hypergraph methods to the exact quotient refinement produced by AQARION?

**Why it matters.** Approximation methods can validate the exact quotient but may also merge non-equivalent states. The limiting relationship should be made precise [web:212].

**What would count as progress.**
- Convergence theorem for approximation-to-exact quotienting.
- Error bounds in partition lattice distance.
- Explicit examples where approximation provably deviates from exact quotient structure.

**Current status.** Open.

---

### OP-13: Complexity of quotient refinement

**Question.** What is the sharp complexity bound for computing the exact quotient on general finite deterministic systems?

**Why it matters.** The current implementation is finite and practical, but a full complexity analysis would clarify the algorithmic cost of exact quotienting versus approximation.

**What would count as progress.**
- Worst-case time and space complexity.
- Average-case bounds under random system models.
- Lower bounds showing inherent difficulty.

**Current status.** Open.

---

## 7. Minimal Compression Targets

The following compression goals are explicitly open because they would unify the current framework into a smaller theorem schema:

### OP-14: AQARION Collapse Principle

**Question.** Can the entire deterministic theory be compressed into one theorem that states:

- FOQDS is a quotient-semantics fixed point,
- the quotient induces canonical operator images,
- and exact descent is equivalent to obstruction vanishing?

**Why it matters.** This would be the cleanest possible publication-level formulation of the project.

**Current status.** Open.

---

### OP-15: Minimal axiom system

**Question.** Is there a 5-axiom basis from which Papers I and II can be derived?

**Why it matters.** A minimal axiom set would make the theory easier to teach, review, and extend.

**What would count as progress.**
- Five axioms that generate the quotient construction.
- Derived theorems matching the current paper structure.
- Proof that the axioms are independent, or identification of redundancy.

**Current status.** Open.

---

## 8. Research Priorities

### High priority
- OP-0: Fixed-point quotient vs behavioral kernel beyond determinism.
- OP-1: Canonical quotient uniqueness for branching systems.
- OP-3: Unified uncertainty coalgebra.
- OP-9: Induced spectral observables as a single theorem.
- OP-14: AQARION Collapse Principle.

### Medium priority
- OP-2: Trace vs bisimulation collapse conditions.
- OP-4: Final semantics under uncertainty.
- OP-5: Metric equivalence vs exact equivalence.
- OP-10: Spectral phase transition theorem.
- OP-12: Exact quotient vs approximation schemes.

### Lower priority, but structurally important
- OP-6: Cross-base universality.
- OP-7: Quotient rigidity vs quotient collapse.
- OP-8: Kaprekar automorphism groups.
- OP-11: Spectral minimal polynomial structure.
- OP-13: Complexity of quotient refinement.
- OP-15: Minimal axiom system.

---

## 9. Working Principle

The current AQARION program should not expand by adding more layers. It should compress by proving that the existing layers are manifestations of one quotient-semantics principle.

The deterministic case is the certified core.  
The branching case is the first open extension.  
The uncertainty case is the broader frontier.  
The compression problem is the unifying question.

---

## 10. Shortest Honest Summary

AQARION is currently strongest in the deterministic finite setting, where exact quotienting, refinement, and induced spectral observables are all coherent. The main open questions begin where determinism ends: branching, uncertainty, approximate semantics, and universal categorical completion [web:210][web:213][web:215].

---

## 11. Next Files to Write

- `AQARION_COLLAPSE_THEOREM.md`
- `TIKZ_QUOTIENT_SEMANTICS_DIAGRAM.tex`
- `MINIMAL_AXIOMS.md`
- `PAPER_II_CORRECTION_NOTES.md`

---

**Status:** Open problems identified and separated from certified claims.
