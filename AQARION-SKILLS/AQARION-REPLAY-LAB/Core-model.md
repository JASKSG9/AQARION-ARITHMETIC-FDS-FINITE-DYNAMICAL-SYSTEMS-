# AQARION Replay Lab — Core Model
> Can you replay this claim—and can its evidence survive nearby wrong versions?

Records: 1. What was claimed 2. domain/carrier 3. fixture 4. verifier 5. observed facts 6. verdict allowed 7. nearby invalid rejected

Frozen invariants:
- No promotion without exact env pin Lean 4.33.1 2026-08-21 + Mathlib commit
- Zero-sorry + #print axioms zero + forbid unsafe/extern/native_decide
- docref!= proof_dependency
- observed null allowed while expected complete
- Promote <=> ∧_cone ReceiptValid
- Public LeanGraph 388105 nodes 11.3M edges Mathlib v4.27–v4.29 NOT 4.33.1
- KILLED!= DELETED

State vector S(C)=(T,D,M,E,R,I,A,F,P,G)
Anti-silent: wrong_root, wrong_case_count, altered_expected, missing_fixture, broken_path, stale_receipt, self_comparison, synthetic_pass, unexercised_claim, forged_observed, formal_target_true → all REJECTED
Live demo: WEB/index.html — A15 AqarionAgent.kt
