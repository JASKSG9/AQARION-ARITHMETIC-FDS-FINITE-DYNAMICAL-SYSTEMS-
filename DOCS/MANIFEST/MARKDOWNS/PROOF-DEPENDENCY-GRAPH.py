
# ============================================================================
# 4. PROOF_DEPENDENCY_GRAPH.md — Logical Dependency Chain
# ============================================================================

proof_dep_graph = """# AQARION Paper I — Proof Dependency Graph

**Date:** 2026-07-06

**Status:** ACTIVE

---

## Graph Structure

```
Layer 0: Definitions (no dependencies)
========================================
D0.1  System (X, T)
D0.2  Function space F(X)
D0.3  Koopman operator K
D0.4  Partition Π
D0.5  Observable subspace V_Π
D0.6  Projection P_Π
D0.7  Defect operator D_Π


Layer 1: Propositions (depend on Layer 0)
==========================================
P1.1  Projection Idempotence
        └── depends on: D0.6

P1.2  Image Characterization
        └── depends on: D0.5, D0.6

P1.3  Defect Operator Definition
        └── depends on: D0.3, D0.6, D0.7


Layer 2: Central Theorem (depends on Layer 1)
===============================================
T2.1  Exact Observable Quotient Criterion
        └── depends on: P1.1, P1.2, P1.3
        └── evidence: symbolic proof + computational certification


Layer 3: Quotient Construction (depends on Layer 2)
====================================================
C3.1  Exact Deterministic Quotient
        └── depends on: T2.1, D0.4


Layer 4: Commutator Boundary (depends on Layer 2)
==================================================
T4.1  Commutation Implies Invariance
        └── depends on: T2.1

T4.2  [RETRACTED] Converse Commutation
        └── depends on: T2.1
        └── status: FALSE (counterexample found)

C4.1  Defect measures observable leakage, not commutation
        └── depends on: T4.2 retraction


Layer 5: Computational Certification (independent verification)
===============================================================
Cert5.1  Exhaustive verification (|X| ≤ 5)
        └── verifies: T2.1
        └── method: Two independent routes

Cert5.2  Randomized stress testing
        └── verifies: T2.1
        └── method: 10,000 random trials

Cert5.3  Pathological case verification
        └── verifies: T2.1 boundary behavior
```

---

## Dependency Table

| Node | Type | Depends On | Used By |
|------|------|------------|---------|
| D0.1 | Definition | — | D0.3, Cert5.1 |
| D0.2 | Definition | — | D0.5, D0.6 |
| D0.3 | Definition | D0.1, D0.2 | P1.3, T4.1 |
| D0.4 | Definition | — | C3.1, Cert5.1 |
| D0.5 | Definition | D0.2, D0.4 | P1.2, T2.1 |
| D0.6 | Definition | D0.2, D0.4, A4 | P1.1, P1.2, P1.3, T2.1, T4.1 |
| D0.7 | Definition | D0.3, D0.6 | P1.3, T2.1, T4.1, T4.2 |
| P1.1 | Proposition | D0.6 | T2.1 |
| P1.2 | Proposition | D0.5, D0.6 | T2.1 |
| P1.3 | Proposition | D0.3, D0.6, D0.7 | T2.1 |
| T2.1 | Theorem | P1.1, P1.2, P1.3 | C3.1, T4.1, T4.2, Cert5.1, Cert5.2, Cert5.3 |
| C3.1 | Corollary | T2.1, D0.4 | — |
| T4.1 | Theorem | T2.1, D0.3, D0.6, D0.7 | — |
| T4.2 | Theorem | T2.1, D0.7 | C4.1 |
| C4.1 | Corollary | T4.2 retraction | — |
| Cert5.1 | Certification | T2.1, D0.1, D0.4 | — |
| Cert5.2 | Certification | T2.1 | — |
| Cert5.3 | Certification | T2.1 | — |

---

## Critical Path

The longest dependency chain from definitions to a certified theorem:

```
D0.1 → D0.3 → P1.3 → T2.1 → Cert5.1
D0.2 → D0.5 → P1.2 → T2.1 → Cert5.1
D0.4 → Cert5.1
```

T2.1 is the **bottleneck node**. All downstream results (C3.1, T4.1, T4.2, all certifications) depend on it. T2.1 itself depends on all Layer 1 propositions, which depend on all Layer 0 definitions.

---

## Retraction Impact

T4.2 retraction affects:

- **C4.1** (directly: C4.1 is the interpretation of the retraction)
- **No other theorems** (T4.2 was never used as a dependency for any proved result)
- **The manuscript** (must explicitly state that the converse fails)

This is a **safe retraction**: it does not invalidate any downstream proved results.

---

## Verification Coverage

Every edge in this graph is covered by either:
- A symbolic proof (Layer 1–4)
- A computational certification (Layer 5)
- An explicit retraction record (T4.2)

No edge is unverified.
"""

with open(f"{base_dir}/PROOF_DEPENDENCY_GRAPH.md", "w") as f:
    f.write(proof_dep_graph)

print(f"PROOF_DEPENDENCY_GRAPH.md: {os.path.getsize(f'{base_dir}/PROOF_DEPENDENCY_GRAPH.md')} bytes")PROOF_DEPENDENCY_GRAPH.md: 3958 bytes
