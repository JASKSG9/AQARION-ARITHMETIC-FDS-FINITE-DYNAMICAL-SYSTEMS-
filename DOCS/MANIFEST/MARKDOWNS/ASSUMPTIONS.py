
# ============================================================================
# 3. ASSUMPTIONS.md — Explicit Assumption Registry
# ============================================================================

assumptions_md = """# AQARION Paper I — Explicit Assumptions

**Date:** 2026-07-06

**Status:** LOCKED

**Rule:** No proof may depend on an unstated assumption. Every assumption is listed here with justification.

---

## A1 — Finiteness

**Statement:** X is a finite nonempty set.

**Justification:** The theory is developed for finite deterministic systems. All combinatorial arguments (partition enumeration, exhaustive search) depend on finiteness.

**Impact:** If X is infinite, the Koopman operator acts on an infinite-dimensional space, the projection P_Π may not be well-defined without additional measure-theoretic structure, and the quotient construction fails.

---

## A2 — Determinism

**Statement:** T: X → X is a well-defined total function (single-valued, defined for all x ∈ X).

**Justification:** Determinism requires exactly one successor per state. The Koopman operator definition (Kf)(x) = f(T(x)) requires T(x) to be uniquely defined.

**Impact:** If T is multi-valued or partial, K is not a linear operator and the entire algebraic framework collapses.

---

## A3 — Real-Valued Functions

**Statement:** The function space is F(X) = {f: X → R}.

**Justification:** Real-valued observables are sufficient for the quotient criterion. The projection P_Π is defined via averaging, which requires no complex structure.

**Note:** The Koopman operator literature often uses ℂ^X for spectral completeness. For Paper I, R is sufficient because the quotient criterion is purely algebraic (subspace inclusion, not spectral decomposition).

**Impact:** If complex-valued functions are required later (e.g., for eigenfunction analysis), A3 must be revised and all proofs rechecked.

---

## A4 — Standard Inner Product

**Statement:** The standard inner product on F(X) is ⟨f, g⟩ = Σ_{x∈X} f(x) g(x).

**Justification:** The averaging projection P_Π is the orthogonal projection with respect to this inner product. Without this choice, P_Π is not uniquely defined.

**Impact:** A different inner product (e.g., weighted by a measure μ) would change P_Π and therefore change D_Π. The quotient criterion would need re-derivation.

---

## A5 — Partition Blocks Are Nonempty

**Statement:** Every block B_i ∈ Π is nonempty.

**Justification:** Empty blocks would make the averaging projection undefined (division by |B_i| = 0). This is standard in partition theory.

**Impact:** None under standard definitions. Included for completeness.

---

## A6 — Partition Covers X

**Statement:** ∪_{i=1}^m B_i = X.

**Justification:** If some state is not in any block, the projection P_Π is not defined on that state and the observable subspace V_Π is not a subspace of F(X).

**Impact:** None under standard definitions. Included for completeness.

---

## Assumption Dependency Graph

```
A1 (Finiteness)
    ├── Enables: exhaustive enumeration
    ├── Enables: Bell number partition counting
    └── Required by: all proofs

A2 (Determinism)
    ├── Enables: Koopman operator linearity
    └── Required by: T2.1, T3.1, T4.1

A3 (Real-valued)
    ├── Enables: averaging projection
    └── Required by: P1.1, P1.2, T2.1

A4 (Standard inner product)
    ├── Defines: P_Π uniquely
    └── Required by: P1.1, P1.2, all theorems

A5 (Nonempty blocks)
    └── Required by: P_Π definition

A6 (Covers X)
    └── Required by: V_Π = subspace of F(X)
```

---

## Assumption Change Protocol

If any assumption is modified:

1. Update this document.
2. Re-verify all proofs that depend on the modified assumption.
3. Re-run the adversarial harness.
4. Update the theorem ledger.
5. Increment the schema version.

**Current version:** `aqarion:paper-i:assumptions:v1.0.0`
"""

with open(f"{base_dir}/ASSUMPTIONS.md", "w") as f:
    f.write(assumptions_md)

print(f"ASSUMPTIONS.md: {os.path.getsize(f'{base_dir}/ASSUMPTIONS.md')} bytes")ASSUMPTIONS.md: 3757 bytes
