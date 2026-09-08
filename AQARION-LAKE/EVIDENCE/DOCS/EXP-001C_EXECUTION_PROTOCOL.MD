# EXP-001C — T1–T13 EXECUTION PROTOCOL

## Toolchain

leanprover/lean4:v4.33.1

## T1 — Lakefile elaboration

Run the exact repository with the pinned toolchain.

Record:

- lean version
- lake version
- OS
- architecture
- source revision
- timestamp
- stdout
- stderr
- exit code

PASS requires successful Lake elaboration.

## T2 — Lean build

Build the Lean library and executable.

PASS requires actual compilation in the pinned environment.

## T3 — Valid receipt

Run:

python3 scripts/validate_registry.py

Expected:

exit 0

Already executed.

## T4 — Invalid schema

Remove `source_scope`.

Expected:

non-zero validator exit.

Already executed:

exit 1.

Restore the canonical receipt afterward.

## T5 — Stale source

Modify `AqarionLake/Core.lean` without modifying the receipt.

Expected:

SOURCE HASH MISMATCH
exit 7

Already executed.

Restore the exact canonical source afterward.

## T6 — Invalid artifact

Reference a declaration that does not exist.

Expected:

ARTIFACT REFERENCE INVALID
exit 8

Already executed.

Restore the canonical receipt afterward.

## T7 — Bare Lake build

Run:

lake build

The validation target must execute through:

needs := #[validateEvidence]

A validation failure must prevent the dependent Lean target from
being considered successfully built.

This is the critical real Lake execution gate.

## T8 — Receipt materialization

After a successful build verify:

.lake/build/evidence/registry.receipt.json

Verify:

- file exists
- content equals the validated receipt
- resulting artifact hash is recorded
- build run identifier is recorded if implemented

## T9 — Incremental caching

Perform:

1. clean build
2. second identical build
3. mutate relevant input
4. rebuild
5. restore source
6. rebuild

Record Lake's actual rebuild behavior.

The system must not accept stale evidence merely because an
unrelated cached artifact exists.

## T10 — Claim mutation without rehash

Mutate claim content while preserving the recorded hash.

Expected:

integrity failure.

Already demonstrated.

## T11 — Claim mutation with rehash

Mutate claim content and recompute its hash.

Expected:

hash-only integrity may pass.

This is an intentional security finding.

It must NOT be classified as a successful authenticity test.

## T12 — Signed receipt

Implement:

signature = SIGN_K(H_cert)

Verify:

1. valid signature
2. wrong public key
3. modified certificate
4. modified signed digest
5. malformed signature
6. missing signature

Every invalid case must fail closed.

## T13 — Parent-chain break

Create a valid parent certificate.

Then corrupt:

- parent hash
- dependency identifier
- parent signature
- parent certificate

Expected:

certificate validation failure.

## Promotion

Only after T1–T13 have actual recorded evidence may the experiment
be promoted.

A partial execution must remain partial.

No overclaim.
