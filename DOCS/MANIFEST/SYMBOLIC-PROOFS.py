
# ============================================================================
# 5. SYMBOLIC PROOFS (Markdown)
# ============================================================================

projection_md = """# Theorem T1.1: Projection Idempotence

## Statement

$$P_\\Pi^2 = P_\\Pi$$

## Proof

**Given:** $P_\\Pi$ is the orthogonal projection onto $V_\\Pi = \\text{span}\\{1_{B_1}, \\ldots, 1_{B_m}\\}$.

**Step 1:** By definition of orthogonal projection, for any $f \\in \\mathbb{C}^X$:
$$P_\\Pi f = \\sum_{i=1}^m \\frac{\\langle f, 1_{B_i} \\rangle}{\\langle 1_{B_i}, 1_{B_i} \\rangle} 1_{B_i}$$

**Step 2:** For any $v \\in V_\\Pi$, we have $v = P_\\Pi v$ (since $P_\\Pi$ acts as identity on its range).

**Step 3:** Apply $P_\\Pi$ to both sides:
$$P_\\Pi v = P_\\Pi (P_\\Pi v) = P_\\Pi^2 v$$

Since this holds for all $v \\in V_\\Pi$, and $P_\\Pi f \\in V_\\Pi$ for all $f \\in \\mathbb{C}^X$:
$$P_\\Pi (P_\\Pi f) = P_\\Pi f \\quad \\forall f \\in \\mathbb{C}^X$$

Therefore $P_\\Pi^2 = P_\\Pi$. **QED.**

## Dependencies

- Definition: `projection_operator`
- Assumption: `A3` (standard inner product)

## Certification

- Status: PROVED
- Lean file: `Projection.lean`
"""

with open(f"{base_dir}/proofs/symbolic/projection.md", "w") as f:
    f.write(projection_md)


defect_md = """# Theorem T1.2: Defect Annihilation on Range

## Statement

$$D_\\Pi P_\\Pi = D_\\Pi$$

## Proof

**Given:** $D_\\Pi = (I - P_\\Pi) K P_\\Pi$.

**Step 1:** Compute $D_\\Pi P_\\Pi$:
$$D_\\Pi P_\\Pi = (I - P_\\Pi) K P_\\Pi \\cdot P_\\Pi$$

**Step 2:** By Theorem T1.1, $P_\\Pi^2 = P_\\Pi$:
$$D_\\Pi P_\\Pi = (I - P_\\Pi) K P_\\Pi^2 = (I - P_\\Pi) K P_\\Pi = D_\\Pi$$

**QED.**

## Dependencies

- Theorem: `T1.1` (Projection Idempotence)
- Definition: `defect_operator`

## Certification

- Status: PROVED
- Lean file: `DefectOperator.lean`
"""

with open(f"{base_dir}/proofs/symbolic/defect_operator.md", "w") as f:
    f.write(defect_md)


invariance_md = """# Theorem T2.1: Defect Invariance Criterion

## Statement

$$D_\\Pi = 0 \\iff K(V_\\Pi) \\subseteq V_\\Pi$$

## Proof

### Direction $(\\Rightarrow)$: $D_\\Pi = 0$ implies $K(V_\\Pi) \\subseteq V_\\Pi$

**Step 1:** Let $v \\in V_\\Pi$. Since $P_\\Pi$ is the projection onto $V_\\Pi$:
$$P_\\Pi v = v$$

**Step 2:** Apply the defect operator:
$$D_\\Pi v = (I - P_\\Pi) K P_\\Pi v = (I - P_\\Pi) K v$$

**Step 3:** If $D_\\Pi = 0$, then $D_\\Pi v = 0$ for all $v$:
$$(I - P_\\Pi) K v = 0$$

**Step 4:** Therefore:
$$K v = P_\\Pi K v$$

Since $P_\\Pi K v \\in V_\\Pi$, we have $K v \\in V_\\Pi$ for all $v \\in V_\\Pi$.

**Step 5:** Hence $K(V_\\Pi) \\subseteq V_\\Pi$.

### Direction $(\\Leftarrow)$: $K(V_\\Pi) \\subseteq V_\\Pi$ implies $D_\\Pi = 0$

**Step 1:** Assume $K(V_\\Pi) \\subseteq V_\\Pi$.

**Step 2:** For any $v \\in V_\\Pi$, we have $K v \\in V_\\Pi$.

**Step 3:** Since $P_\\Pi$ acts as identity on $V_\\Pi$:
$$P_\\Pi K v = K v$$

**Step 4:** Therefore:
$$(I - P_\\Pi) K v = K v - K v = 0$$

**Step 5:** For any $v \\in V_\\Pi$:
$$D_\\Pi v = (I - P_\\Pi) K P_\\Pi v = (I - P_\\Pi) K v = 0$$

**Step 6:** Since $D_\\Pi$ maps $V_\\Pi \\to V_\\Pi^\\perp$ and vanishes on all of $V_\\Pi$:
$$D_\\Pi = 0$$

**QED.**

## Interpretation

This is the **central theorem** of Paper I. The defect operator $D_\\Pi$ measures exactly the failure of the Koopman operator to preserve the partition subspace. When $D_\\Pi = 0$, the partition is dynamically meaningful.

## Dependencies

- Theorem: `T1.1`, `T1.2`
- Definition: `koopman_operator`, `projection_operator`, `defect_operator`
- Assumption: `A3`

## Certification

- Status: PROVED
- Lean file: `QuotientCriterion.lean`
- Computational verification: `adversarial/exhaustive/verify_equivalence.py`
"""

with open(f"{base_dir}/proofs/symbolic/invariance_theorem.md", "w") as f:
    f.write(invariance_md)


quotient_md = """# Theorem T3.1: Exact Quotient Descent

## Statement

If $D_\\Pi = 0$, then $\\Pi$ induces a deterministic quotient system $T_\\Pi$ on the partition blocks.

## Proof

**Step 1:** By Theorem T2.1, $D_\\Pi = 0$ implies $K(V_\\Pi) \\subseteq V_\\Pi$.

**Step 2:** The subspace $V_\\Pi$ consists of functions constant on each block $B_i$.

**Step 3:** $K(V_\\Pi) \\subseteq V_\\Pi$ means that for any $f$ constant on blocks, $Kf = f \\circ T$ is also constant on blocks.

**Step 4:** Therefore, if $x, y \\in B_i$, then $T(x)$ and $T(y)$ must lie in the same block $B_j$.

**Step 5:** Define $T_\\Pi(B_i) = B_j$ where $T(B_i) \\subseteq B_j$. This is well-defined by Step 4.

**Step 6:** $T_\\Pi$ is deterministic: each block maps to exactly one block.

**QED.**

## Dependencies

- Theorem: `T2.1`
- Definition: `partition`, `quotient_system`

## Certification

- Status: PROVED
- Lean file: `QuotientCriterion.lean`
"""

with open(f"{base_dir}/proofs/symbolic/quotient_theorem.md", "w") as f:
    f.write(quotient_md)


commutator_md = """# Theorem T4.1: Commutation Implies Invariance

## Statement

$$[P_\\Pi, K] = 0 \\implies D_\\Pi = 0$$

## Proof

**Step 1:** The commutator is $[P_\\Pi, K] = P_\\Pi K - K P_\\Pi$.

**Step 2:** If $[P_\\Pi, K] = 0$, then $P_\\Pi K = K P_\\Pi$.

**Step 3:** For any $v \\in V_\\Pi$, we have $P_\\Pi v = v$, so:
$$P_\\Pi K v = K P_\\Pi v = K v$$

**Step 4:** Therefore $K v = P_\\Pi K v$, which means $K v \\in V_\\Pi$.

**Step 5:** Hence $K(V_\\Pi) \\subseteq V_\\Pi$.

**Step 6:** By Theorem T2.1, $K(V_\\Pi) \\subseteq V_\\Pi$ implies $D_\\Pi = 0$.

**QED.**

## Retraction: T4.2 (Converse)

The converse statement $D_\\Pi = 0 \\implies [P_\\Pi, K] = 0$ is **FALSE**.

**Counterexample intuition:** Invariance only requires $K$ to preserve $V_\\Pi$. Commutation requires $K$ to preserve both $V_\\Pi$ and $V_\\Pi^\\perp$. These are not equivalent.

See `adversarial/commutator/search_noncommuting.py` for explicit computational search.

## Dependencies

- Theorem: `T2.1`
- Definition: `defect_operator`, `koopman_operator`, `projection_operator`

## Certification

- Status: PROVED (T4.1), RETRACTED (T4.2)
- Lean file: `DefectOperator.lean` (T4.1 only)
"""

with open(f"{base_dir}/proofs/symbolic/commutator_results.md", "w") as f:
    f.write(commutator_md)

print("Symbolic proofs created.")Symbolic proofs created.
