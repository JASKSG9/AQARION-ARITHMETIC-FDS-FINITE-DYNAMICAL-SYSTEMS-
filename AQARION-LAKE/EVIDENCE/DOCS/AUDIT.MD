# AQARION LAKE — EXP-001 FINAL AUDIT

Root:
020a9110088010116075e1812c98bcd2bcc4905367fa8943a68c8cd224cf284e

Mode:
FROZEN · EXACT · NO FORK · NO OVERCLAIM

## Current disposition

ARCHITECTURAL SUPPORT VERIFIED
EXECUTION PENDING REAL LAKE COMPILATION

## Established

The experiment establishes architectural support for an AQARION
evidence gate implemented using Lake's public build-system surface.

The relevant pattern is:

input_file
    ↓
custom target
    ↓
validation
    ↓
needs
    ↓
Lean target
    ↓
default lake build

No Lake fork is required by this architecture.

## Executed evidence

### Validator

A valid receipt produced exit code 0.

Removing `source_scope` produced exit code 1.

### Source binding

EXP-001B binds:

AqarionLake.Core.transport_identity_skeleton

to:

AqarionLake/Core.lean

through SHA-256:

2173b29dd48710b09d683a922801ecfed385df6e1cf058d00741d3281aa9bc27

Changing the source without updating the receipt produced a
source-hash mismatch and exit code 7.

### Artifact binding

Referencing a nonexistent Lean artifact produced exit code 8.

### Hash limitation

Changing the claim and recomputing its hash causes a hash-only
integrity check to pass.

Therefore:

HASH INTEGRITY != AUTHENTICITY

The certificate path must eventually include:

SIGN_K(H_cert)

and independent signature verification.

## Not yet established

The following require real Lake/Lean execution:

1. lakefile elaboration
2. Lean compilation
3. bare `lake build` dependency propagation
4. real receipt materialization
5. incremental caching behavior
6. signed certificate verification
7. parent-chain verification

## Correct claim

AQ-LAKE-EXP-001:

ARCHITECTURAL SUPPORT VERIFIED,
EXECUTION PENDING REAL LAKE COMPILATION.

Do not call this:

- formally verified Lake integration
- empirically verified Lake integration
- production-certified evidence infrastructure

until the corresponding evidence exists.

## Architectural interpretation

Lake provenance answers:

"What inputs produced this artifact?"

AQARION evidence answers:

"What claim may this artifact support?"

The receipt is the binding layer.

The resulting model is:

TASK_PROPOSAL
→ EXECUTION
→ H_src
→ H_run
→ H_result
→ RESULT_RECEIPT
→ ADVERSARIAL_VALIDATOR
→ CERTIFICATE
→ SIGN_K(H_cert)
→ PROMOTION

Agent autonomy does not imply epistemic autonomy.
