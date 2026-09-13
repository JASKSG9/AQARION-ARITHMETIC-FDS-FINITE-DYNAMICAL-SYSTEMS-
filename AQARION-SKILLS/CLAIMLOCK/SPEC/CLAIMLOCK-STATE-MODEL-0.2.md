# CLAIMLOCK State Model 0.2

## Epistemic axis

OPEN
PROVED
REFUTED
EMPIRICAL
UNKNOWN

## Verification axis

UNVERIFIED
REPLAY_PASS
MULTI_ROUTE_PASS
FORMAL_KERNEL_PASS
INDEPENDENT_CHECK_PASS

## Governance axis

CHECKING
LOCKED
BLOCKED
QUARANTINED
PROMOTABLE
PUBLISHED

## Receipt axis

VALID
STALE
SUPERSEDED
INVALID
NOT_APPLICABLE

## Decision algebra

ALLOW
DENY
QUARANTINE
INDETERMINATE

These axes MUST NOT be collapsed.

Example:

epistemic:
    REFUTED

verification:
    MULTI_ROUTE_PASS

governance:
    LOCKED

receipt:
    VALID

decision:
    DENY

This is coherent.

A refuted claim can have a perfectly valid receipt documenting
its refutation.

The receipt authenticates the transition.

It does not resurrect the claim.

---

## Core distinction

AUTHENTIC
    means the receipt and its inputs have not been altered.

CORRECT
    means the relevant computation recomputes successfully.

APPLICABLE
    means the receipt still applies to the current claim state.

AUTHORIZED
    means the current policy permits the transition.

INDEPENDENT
    means the evidence routes satisfy the declared
    independence criterion.

These are independent predicates.

No single boolean named "verified" may substitute for them.
