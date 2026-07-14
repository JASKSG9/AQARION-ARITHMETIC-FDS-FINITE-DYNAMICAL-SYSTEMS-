
# ============================================================
# 5. AQARION-OVERVIEW.md — Architecture & Design Philosophy
# ============================================================

overview = """# AQARION v0.4.1-final — Architecture Overview

## Design Philosophy

AQARION treats mathematical claims about finite systems like cryptographic protocols: every claim produces a certificate that can be independently verified without trusting the original computation.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        HUMAN LAYER                               │
│  Mathematician: States conjecture, interprets results          │
│  AI: Generates candidate claims, searches patterns             │
│  Community: Reviews certificates, builds on results              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     AQARION KERNEL LAYER                         │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   FDDS      │  │   Exact     │  │   Claim     │             │
│  │   Engine    │  │   Arithmetic│  │   Registry  │             │
│  │             │  │             │  │             │             │
│  │  States     │  │  Fractions  │  │  Definitions│             │
│  │  Transition │  │  No float   │  │  Theorems   │             │
│  │  Orbit      │  │  Exact = =  │  │  Claims     │             │
│  │  Cycle      │  │             │  │  Versioned  │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Koopman    │  │   Defect    │  │  Certificate│             │
│  │  Operator   │  │   Operator  │  │  Generator  │             │
│  │             │  │             │  │             │             │
│  │  K_ij = 1   │  │  D = (I-P)KP│  │  Hash chain │             │
│  │  if f(xj)=xi│  │  D=0 ⟺ inv  │  │  Immutable  │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     VERIFICATION LAYER                           │
│                                                                  │
│  Independent Verifier: Recomputes everything from scratch       │
│  - Checks hash integrity                                        │
│  - Validates registry version                                   │
│  - Verifies dependency existence                                │
│  - Reconstructs system                                          │
│  - Recomputes evidence (claimed vs recomputed separation)       │
│  - Grants VALID or INVALID (never from certificate file)        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MACHINE LAYER                               │
│  Docker: Reproducible environment                              │
│  CI/CD: Automated verification on commit                       │
│  GitHub: Distributed collaboration, PR review                  │
│  arXiv: Certificate-attached preprints                          │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
Mathematical Claim
       │
       ▼
┌──────────────┐
│ Claim Registry│  ← Definitions, Theorems, Dependencies (versioned)
└──────────────┘
       │
       ▼
┌──────────────┐
│   FDDS       │  ← Finite system definition
│   System     │
└──────────────┘
       │
       ▼
┌──────────────┐
│  Evidence    │  ← Exact computation (Fractions)
│  Computation │
└──────────────┘
       │
       ▼
┌──────────────┐
│  Certificate │  ← JSON with hash chain, status: UNVERIFIED
│  (AEO)       │
└──────────────┘
       │
       ▼
┌──────────────┐
│  Independent │  ← Recomputes, compares, grants VALID/INVALID
│  Verifier    │
└──────────────┘
       │
       ▼
┌──────────────┐
│  Community   │  ← Distributed trust through verification
│  Consensus   │
└──────────────┘
```

## Key Design Decisions

### 1. Exact Arithmetic
**Decision:** Use Python `fractions.Fraction` exclusively. No floating point in verification logic.
**Rationale:** Floating point introduces disputable rounding errors. Exact arithmetic makes verification binary: pass or fail, no "close enough".

### 2. Certificate Immutability
**Decision:** Certificates are generated once, never modified. Hash covers all mathematical content.
**Rationale:** Prevents tampering. Any modification breaks the hash chain.

### 3. Status Separation
**Decision:** Certificate files contain "UNVERIFIED". Only verifier output contains "VALID" or "INVALID".
**Rationale:** Prevents self-validation. The generating system cannot certify its own output.

### 4. Registry Versioning
**Decision:** Every claim pins `registry_version`. Certificates from old registries fail verification.
**Rationale:** Mathematical definitions evolve. Claims must be evaluated against the definitions they reference.

### 5. Sparse Optimization
**Decision:** Defect check has both dense (O(|X|³)) and sparse (O(|X|)) implementations.
**Rationale:** Dense is reference. Sparse is practical for large systems (10,000+ states).

### 6. Canonical Labels
**Decision:** Cycles labeled by lexicographically minimal rotation.
**Rationale:** Eliminates ordering dependence. [1,2,3] and [2,3,1] are the same cycle.

## The "Missing Middle"

```
FULL FORMALIZATION                    HEURISTIC/NUMERICAL
Lean/mathlib, Coq                     MATLAB, Python, R
│                                         │
│    ←—— AQARION lives here ——→          │
│                                         │
Exact arithmetic certificates           Floating-point approximations
Machine-auditable                       Trust-me results
Reproducible offline                    Cloud-dependent
Claim-structured                        Ad-hoc analysis
Months to formalize                     Minutes to write
Same-day verification                   No verification
```

## Trust Model

| Layer | Component | Trust Basis | Failure Mode |
|-------|-----------|-------------|--------------|
| 0 | Human statement | Mathematical rigor | Human error |
| 1 | Exact computation | Python Fractions | Implementation bug |
| 2 | Independent reproduction | Docker, open source | Environment drift |
| 3 | Formal bridge | Future: Lean export | Translation error |
| 4 | Community | Distributed verification | Coordinated attack |

**Defense in depth:** Each layer catches errors the previous layer missed.

## Version Roadmap

```
v0.4.0-final  →  Kernel foundation, exact arithmetic
     │
v0.4.1-final  →  Mathematical registry, hardened certificates, canonical cycles
     │              ← YOU ARE HERE
v0.4.2        →  Certificate schema locked, reference artifact frozen
     │
v0.5.0        →  4-digit Kaprekar (10,000 states), sparse exact verification
     │
v0.5.1        →  Sparse Koopman, block-structured defect check
     │
v0.6.0        →  KSD spectral certificates
     │
v1.0.0        →  AQARION Formal Verification Platform
```

## Session Principles (Frozen)

1. Mathematics defines claims. Algorithms compute them. Certificates record them. Verifiers check them.
2. Claim IDs never change meaning. New versions get new IDs.
3. Dependencies are explicit and versioned.
4. Hash covers mathematical content only. Audit metadata is not part of the cryptographic guarantee.
5. The verifier checks dependencies first. Unknown registry version = invalid certificate.
6. Canonical labels eliminate ordering dependence.
7. Claimed ≠ recomputed. Verifier outputs both, never overwrites.
8. Status from verifier only. Certificate files claim nothing about their own validity.
9. Exact arithmetic eliminates dispute. No floating point in verification logic.
10. One command reproduction. `docker build → docker run → CERTIFICATE VALID`.
"""

with open(os.path.join(output_dir, "AQARION-OVERVIEW.md"), 'w') as f:
    f.write(overview)

print("✅ AQARION-OVERVIEW.md")
