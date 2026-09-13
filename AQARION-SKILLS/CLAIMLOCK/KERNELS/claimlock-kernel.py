from __future__ import annotations

import hashlib
from typing import Any


try:
    import rfc8785
except ImportError:
    rfc8785 = None


DECISIONS = {
    "ALLOW",
    "DENY",
    "QUARANTINE",
    "INDETERMINATE",
}

RECEIPT_STATUSES = {
    "VALID",
    "STALE",
    "SUPERSEDED",
    "INVALID",
    "NOT_APPLICABLE",
}


class KernelError(ValueError):
    pass


def canonical_bytes(value: Any) -> bytes:
    """
    Production canonicalization MUST use RFC 8785.

    The kernel deliberately fails closed if the implementation is absent.
    A normal JSON serializer is NOT an acceptable cryptographic substitute.
    """
    if rfc8785 is None:
        raise KernelError(
            "RFC8785 implementation unavailable; "
            "cryptographic canonicalization cannot proceed"
        )

    return rfc8785.dumps(value)


def content_hash(value: Any) -> str:
    return (
        "sha256:"
        + hashlib.sha256(canonical_bytes(value)).hexdigest()
    )


def validate_policy(policy: dict[str, Any]) -> None:
    required = {
        "id",
        "version",
        "rules",
    }

    missing = sorted(required - set(policy))
    if missing:
        raise KernelError(
            "missing policy fields: " + ", ".join(missing)
        )

    if not isinstance(policy["rules"], list):
        raise KernelError("policy.rules must be a list")

    seen = set()

    for rule in policy["rules"]:
        if not isinstance(rule, dict):
            raise KernelError("policy rule must be an object")

        rule_id = rule.get("id")
        outcome = rule.get("outcome")

        if not rule_id:
            raise KernelError("policy rule missing id")

        if rule_id in seen:
            raise KernelError(
                f"duplicate policy rule: {rule_id}"
            )

        seen.add(rule_id)

        if outcome not in DECISIONS:
            raise KernelError(
                f"invalid policy outcome: {outcome}"
            )


def policy_hash(policy: dict[str, Any]) -> str:
    validate_policy(policy)
    return content_hash(policy)


def policy_rule(
    policy: dict[str, Any],
    rule_id: str,
) -> dict[str, Any]:
    validate_policy(policy)

    for rule in policy["rules"]:
        if rule["id"] == rule_id:
            return rule

    raise KernelError(
        f"policy rule not found: {rule_id}"
    )


def require_predicate_vector(
    predicates: dict[str, Any],
) -> None:
    required = {
        "scope",
        "provenance",
        "replay",
        "routes",
        "authority",
    }

    missing = sorted(
        required - set(predicates)
    )

    if missing:
        raise KernelError(
            "missing predicates: "
            + ", ".join(missing)
        )


def validate_predicate_vector(
    predicates: dict[str, Any],
) -> None:
    require_predicate_vector(predicates)

    allowed_results = {
        "PASS",
        "FAIL",
        "INDETERMINATE",
    }

    for name, record in predicates.items():

        if not isinstance(record, dict):
            raise KernelError(
                f"predicate {name} is not an object"
            )

        for field in (
            "predicate",
            "result",
            "input_hash",
            "implementation_hash",
            "result_hash",
        ):
            if field not in record:
                raise KernelError(
                    f"predicate {name} missing {field}"
                )

        if record["result"] not in allowed_results:
            raise KernelError(
                f"predicate {name} has invalid result"
            )


def checked_rule(
    policy: dict[str, Any],
    rule_id: str,
    expected_outcome: str,
) -> str:
    rule = policy_rule(policy, rule_id)

    if rule["outcome"] != expected_outcome:
        raise KernelError(
            f"policy rule {rule_id} outcome mismatch: "
            f"{rule['outcome']} != {expected_outcome}"
        )

    return rule_id


def decide_transition(
    current_state: Any,
    claim: Any,
    evidence: Any,
    predicates: dict[str, Any],
    policy: dict[str, Any],
) -> dict[str, Any]:
    """
    Pure deterministic transition function.

    current_state, claim and evidence are intentionally accepted
    as semantic inputs even where a particular rule does not inspect
    all of them. This fixes the kernel's input contract.

    The function:

        (S, C, E, V, P) -> D

    and performs no network access, LLM inference, repair,
    discovery or implicit evidence generation.
    """

    del current_state
    del claim
    del evidence

    validate_predicate_vector(predicates)
    validate_policy(policy)

    ph = policy_hash(policy)

    # Fail closed on malformed predicate structures.
    for name, record in predicates.items():

        if not isinstance(record["input_hash"], str):
            return {
                "outcome": "INDETERMINATE",
                "rule_id": checked_rule(
                    policy,
                    "TR-MALFORMED-001",
                    "INDETERMINATE",
                ),
                "reason_codes": ["CL000"],
                "policy_hash": ph,
            }

        if not isinstance(
            record["implementation_hash"],
            str,
        ):
            return {
                "outcome": "INDETERMINATE",
                "rule_id": checked_rule(
                    policy,
                    "TR-MALFORMED-001",
                    "INDETERMINATE",
                ),
                "reason_codes": ["CL000"],
                "policy_hash": ph,
            }

        if not isinstance(
            record["result_hash"],
            str,
        ):
            return {
                "outcome": "INDETERMINATE",
                "rule_id": checked_rule(
                    policy,
                    "TR-MALFORMED-001",
                    "INDETERMINATE",
                ),
                "reason_codes": ["CL000"],
                "policy_hash": ph,
            }

    if predicates["scope"]["result"] == "FAIL":
        return {
            "outcome": "DENY",
            "rule_id": checked_rule(
                policy,
                "TR-SCOPE-001",
                "DENY",
            ),
            "reason_codes": ["CL002"],
            "policy_hash": ph,
        }

    if predicates["replay"]["result"] == "FAIL":
        return {
            "outcome": "DENY",
            "rule_id": checked_rule(
                policy,
                "TR-REPLAY-001",
                "DENY",
            ),
            "reason_codes": ["CL101"],
            "policy_hash": ph,
        }

    if predicates["provenance"]["result"] == "FAIL":
        return {
            "outcome": "QUARANTINE",
            "rule_id": checked_rule(
                policy,
                "TR-PROVENANCE-001",
                "QUARANTINE",
            ),
            "reason_codes": ["CL201"],
            "policy_hash": ph,
        }

    if predicates["routes"]["result"] == "FAIL":
        return {
            "outcome": "QUARANTINE",
            "rule_id": checked_rule(
                policy,
                "TR-ROUTES-001",
                "QUARANTINE",
            ),
            "reason_codes": ["CL301"],
            "policy_hash": ph,
        }

    if predicates["authority"]["result"] == "FAIL":
        return {
            "outcome": "QUARANTINE",
            "rule_id": checked_rule(
                policy,
                "TR-AUTHORITY-001",
                "QUARANTINE",
            ),
            "reason_codes": ["CL401"],
            "policy_hash": ph,
        }

    if any(
        record["result"] == "INDETERMINATE"
        for record in predicates.values()
    ):
        return {
            "outcome": "INDETERMINATE",
            "rule_id": checked_rule(
                policy,
                "TR-INDET-001",
                "INDETERMINATE",
            ),
            "reason_codes": ["CL999"],
            "policy_hash": ph,
        }

    return {
        "outcome": "ALLOW",
        "rule_id": checked_rule(
            policy,
            "TR-ALLOW-001",
            "ALLOW",
        ),
        "reason_codes": [],
        "policy_hash": ph,
    }


def build_receipt(
    current_state: Any,
    claim: Any,
    evidence: Any,
    predicates: dict[str, Any],
    policy: dict[str, Any],
    decision: dict[str, Any],
    impact: dict[str, Any],
) -> dict[str, Any]:

    validate_predicate_vector(predicates)
    validate_policy(policy)

    ph = policy_hash(policy)

    if decision.get("policy_hash") != ph:
        raise KernelError(
            "decision policy hash mismatch"
        )

    receipt_body = {
        "schema_version":
            "CLAIMLOCK-RECEIPT-0.2.0",

        "inputs": {
            "state_hash":
                content_hash(current_state),

            "claim_hash":
                content_hash(claim),

            "evidence_hash":
                content_hash(evidence),

            "predicate_hash":
                content_hash(predicates),

            "policy_hash":
                ph,
        },

        "decision": decision,

        "impact": impact,
    }

    receipt = dict(receipt_body)

    receipt["receipt_hash"] = content_hash(
        receipt_body
    )

    return receipt
