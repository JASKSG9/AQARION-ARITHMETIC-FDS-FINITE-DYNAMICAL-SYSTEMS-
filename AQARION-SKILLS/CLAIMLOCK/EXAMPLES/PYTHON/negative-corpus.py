"""
CLAIMLOCK-KERNEL-001 adversarial corpus.

The corpus intentionally distinguishes:

    decision
    receipt status
    predicate result
    semantic applicability

A receipt can be cryptographically valid while semantically stale.
"""

CASES = [

    {
        "id": "CLN-001",
        "attack": "valid exact witness",
        "expected_decision": "ALLOW",
        "expected_status": "VALID",
    },

    {
        "id": "CLN-002",
        "attack": "insufficient scope",
        "expected_decision": "DENY",
        "expected_status": "VALID",
    },

    {
        "id": "CLN-003",
        "attack": "replay failure",
        "expected_decision": "DENY",
        "expected_status": "VALID",
    },

    {
        "id": "CLN-004",
        "attack": "route disagreement",
        "expected_decision": "QUARANTINE",
        "expected_status": "VALID",
    },

    {
        "id": "CLN-005",
        "attack": "missing verifier metadata",
        "expected_decision": "INDETERMINATE",
        "expected_status": "VALID",
    },

    {
        "id": "CLN-006",
        "attack": "evidence hash substitution",
        "expected_decision": "QUARANTINE",
        "expected_status": "INVALID",
    },

    {
        "id": "CLN-007",
        "attack": "policy hash substitution",
        "expected_decision": "QUARANTINE",
        "expected_status": "INVALID",
    },

    {
        "id": "CLN-008",
        "attack": "forged output state",
        "expected_decision": "QUARANTINE",
        "expected_status": "INVALID",
    },

    {
        "id": "CLN-009",
        "attack": "provenance cycle",
        "expected_decision": "QUARANTINE",
        "expected_status": "VALID",
    },

    {
        "id": "CLN-010",
        "attack": "mutual authority cycle",
        "expected_decision": "QUARANTINE",
        "expected_status": "VALID",
    },

    {
        "id": "CLN-011",
        "attack": "same implementation under two route names",
        "expected_decision": "INDETERMINATE",
        "expected_status": "VALID",
    },

    {
        "id": "CLN-012",
        "attack": "canonical scope mutation",
        "expected_decision": "DENY",
        "expected_status": "STALE",
    },
]
