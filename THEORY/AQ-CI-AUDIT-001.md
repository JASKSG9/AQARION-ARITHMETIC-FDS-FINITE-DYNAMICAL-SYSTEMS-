# AQ-CI-AUDIT-001

**2026-09-27**

## Status

CI CERTIFICATION BLOCKED.

## Findings

### Repository identity drift

Live main:

    cff9d0f5...

Audited tree:

    6bc45c13...

These are different commits.

Therefore artifacts audited against 6bc45c13 must not be represented as
certification of cff9d0f5.

### Missing paths

A24-A27 paths referenced by the audited material are not present in the
current tree.

### Wrapper-verifier defect

Five wrapper verifiers:

    OBSTRUCTION
    PROJECTION
    COMMUTATOR
    REPRESENTATIVE
    SCC

write embedded source into /mnt/agents/output/ without executing it.

Therefore a wrapper exit-success signal can be a false positive.

### Lean workflow defect

The workflow masks failures with constructions equivalent to:

    || true
    || echo

The root AQARION_LEAN.YML is not under .github/workflows/.

Sorries are present.

Therefore Lean certification is NOT established.

## Required policy

A verifier must:

1. materialize the claimed artifact;
2. execute the verifier;
3. capture exit status;
4. reject masked failures;
5. bind result to source commit/tree;
6. bind receipt to artifact hashes.

## Governance

CI certification: BLOCKED.
Lean certification: BLOCKED.
Publication promotion: BLOCKED.
