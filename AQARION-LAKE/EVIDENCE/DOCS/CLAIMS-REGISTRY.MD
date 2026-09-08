# AQARION LAKE — CLAIMS REGISTER

| ID | Claim | Status | Evidence |
|---|---|---|---|
| AQ-LAKE-001 | Lake's public build primitives can express the proposed evidence dependency without a fork. | ARCHITECTURAL SUPPORT | Public API architecture |
| AQ-LAKE-002 | The AQARION validator can accept a valid receipt and reject malformed evidence metadata. | V | Executed exit 0/1 tests |
| AQ-LAKE-003 | An evidence receipt can bind a Lean artifact reference to a source SHA-256. | V | EXP-001B |
| AQ-LAKE-004 | A stale source is rejected by the binding validator. | V | Exit 7 attack |
| AQ-LAKE-005 | A nonexistent artifact reference is rejected. | V | Exit 8 attack |
| AQ-LAKE-006 | Hash-only certification establishes authenticity. | REFUTED | Rehash-after-mutation attack |
| AQ-LAKE-007 | The exact lakefile elaborates under Lean/Lake v4.33.1. | OPEN | T1 pending |
| AQ-LAKE-008 | Lean target compilation succeeds in the pinned environment. | OPEN | T2 pending |
| AQ-LAKE-009 | Bare lake build propagates evidence failure through `needs`. | OPEN | T7 pending |
| AQ-LAKE-010 | Bare lake build materializes the evidence receipt. | OPEN | T8 pending |
| AQ-LAKE-011 | Incremental caching preserves evidence correctness. | OPEN | T9 pending |
| AQ-LAKE-012 | Signed certificate verification closes the authenticity gap. | OPEN | T12 pending |
| AQ-LAKE-013 | Parent-chain corruption is detected. | OPEN | T13 pending |

## Governance

Claims must never be silently promoted.

[P] = mathematical proof
[PV] = formal verification
[V] = computational verification
[V-sample] = bounded sampling
[C] = conjecture
[R] = research program
[REFUTED] = contradicted
[OPEN] = unresolved

Architectural support is not execution.
Execution is not mathematical proof.
Hash integrity is not authenticity.
