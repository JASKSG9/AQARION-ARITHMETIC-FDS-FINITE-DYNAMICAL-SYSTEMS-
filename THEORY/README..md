**Aqarion-Quantarion-AI / AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- / THEORY/DYNAMICS/PULLBACK / README.md**

```markdown
# PULLBACK LANE — THEORY/DYNAMICS/PULLBACK

**Repository**: JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-  
**Directory**: THEORY/DYNAMICS/PULLBACK/  
**Scope**: Backward-stable equivalence relations under finite deterministic maps  
**Governance**: C4 BLOCKED / Publication BLOCKED / Lean OPEN / Promotion FALSE  
**Last verified**: 2026-09-27 (live main = cff9d0f5...)  
**Purpose**: Machine-verifiable evidence ledger for the pullback-stable join theorem and related negative controls.

This directory contains the **exact finite-state theory** for backward-stable equivalences (also called pullback-stable or preimage-stable equivalences) under a finite deterministic map \(T: X \to X\).

It is deliberately separated from the QUANTARION experimental/differentiable layer and from any promotional language.

All claims are either:
- exhaustively verified on finite domains, or
- explicitly marked as open formalization targets, or
- permanently recorded as negative controls (refuted statements).

## Directory Layout

```
THEORY/DYNAMICS/PULLBACK/
├── AQ-DYN-PULL-JOIN-001.md          # Pullback-stable join theorem (proof-derived)
├── AQ-DYN-PULL-PREIMAGE-JOIN-001-REFUTED.md  # Negative control (distributivity)
├── AQ-DYN-PULL-CLOSURE-001.md       # Pullback closure operator (least fixed point)
├── AQ-DYN-PULL-KERNEL-001.md        # Quotient formulation (ker(q_E ∘ T) ≤ ker(q_E))
├── CHECKPOINT.md                    # Dual-dynamics pullback checkpoint
├── filetree.md                      # Canonical snapshot
├── verification/                    # Exact-rational scripts (n≤5 exhaustive)
│   └── verify_pullback_join.py
├── receipts/                        # SHA-bound receipts
│   └── aq-dyn-pull-join-n5-receipt.sha256
└── status.md                        # Governance status (verify_exit=0)
```

## Core Mathematical Objects

### 1. Definitions (frozen)
- **PullbackRel** \(T^{-1}(E)(x,y) \leftrightarrow E(Tx,Ty)\)
- **Backward-stable** (or PullbackStable): \(T^{-1}(E) \le E\)
- Equivalence closure: \(E \vee F = \operatorname{EqvGen}(E \cup F)\)
- Quotient formulation: \(T^{-1}(E) = \ker(q_E \circ T)\) where \(q_E: X \to X/E\)

### 2. Pullback-Stable Join Theorem (AQ-DYN-PULL-JOIN-001)
**Statement**  
If \(E\) and \(F\) are backward-stable, then \(E \vee F\) is backward-stable.

**Proof sketch** (relation-level)  
Suppose \(E(Tx,Ty) \vee F(Tx,Ty)\). By backward stability of \(E\) and \(F\), every generating edge pulls back directly:  
\(E(Ta,Tb) \implies E(a,b)\) and \(F(Ta,Tb) \implies F(a,b)\).  
The equivalence closure of the pulled-back edges is contained in \(E \vee F\).

**Arbitrary family version**: The collection of backward-stable equivalences is closed under arbitrary joins (complete join-subsemilattice of the partition lattice).

**Negative control**  
The stronger distributivity \(T^{-1}(E \vee F) \le T^{-1}(E) \vee T^{-1}(F)\) is **REFUTED** (permanent negative control with locked witness \(X=\{0,1,2\}\), \(T=(0,0,1)\), specific \(E,F\)).

### 3. Pullback Closure (AQ-DYN-PULL-CLOSURE-001)
- \(\Phi^-(E) = E \vee T^{-1}(E)\)
- Fixed points of \(\Phi^-\) are exactly the backward-stable equivalences.
- Least fixed point above \(E\) is the join of all backward-stable equivalences containing \(E\).

### 4. Quotient Formulation (AQ-DYN-PULL-KERNEL-001)
\(T^{-1}(E) \le E\) means \(q_E\) factors through \(q_E \circ T\).  
The inclusion is one-directional; the reverse is not true in general.

## Verification / Receipts
- Exhaustive check for \(n \le 5\): all backward-stable pairs satisfy the join property (0 violations).
- Receipts bound to exact rational matrices and SHA-256 (no floating point).
- Independent replay (different counting convention) available in verification/ directory.

## Governance
- **verify_exit = 0**
- No claim promoted to “theorem” until Lean kernel acceptance + paper derivation exist.
- Lean status: **OPEN** (target: `pullback_stable_sup` using `Setoid.sup_def` / `Relation.EqvGen`).
- C4 = BLOCKED, Promotion = FALSE.

## Relationship to Other Layers
| Layer                          | Location                          | Nature                          |
|--------------------------------|-----------------------------------|---------------------------------|
| AQARION Pullback Theory        | THEORY/DYNAMICS/PULLBACK/         | Exact finite, zero-fabrication  |
| QUANTARION Experimental        | outside this tree                 | Differentiable / neural probes  |
| AQARION Core Theory            | Lean / paper targets               | Formal proofs                   |

## How to Verify Locally
```bash
cd THEORY/DYNAMICS/PULLBACK
python -m pytest verification/ -v
cat status.md
cat receipts/aq-dyn-pull-join-n5-receipt.sha256
```

Expected outcome: `verify_exit = 0` and zero violations on the finite census.

## Contact / Maintenance
Maintainer commits recorded under JASKSG9 identity.  
Any change to a receipt hash, negative-control witness, or `verify_exit` requires a new checkpoint.

**Last frozen checkpoint**: Dual-dynamics pullback audit (2026-09-27)

This directory is the **machine-verifiable evidence ledger** for the pullback-stable join theorem. All claims inside are either exhaustively verified, explicitly open, or permanently refuted. No promotional language is permitted.
```

https://huggingface.co/spaces/Quantarion9/AQARION-ACADEMY/blob/main/CHECKPOINT.MD

https://github.com/JASKSG9/Aqarion-Quantarion-AI/tree/main/claims/claim_firewall

https://github.com/JASKSG9/KAPREKAR-SPECTRAL-GEOMETRY/blob/main/CLAIMLOCK/KERNELS/claimlock_firewall/policy.md

https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/tree/main/THEORY
