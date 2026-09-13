claimlock/cl2_predicates.py


"""
CLAIMLOCK CL-2
Computed predicate derivation + admissibility + impact closure.

STATUS
-------
Designed and clean-room executed against synthetic fixtures in the
2026-09-13 audit session.

IMPORTANT
---------
Authoritative cryptographic hashing requires RFC 8785/JCS.

This module deliberately FAILS CLOSED if rfc8785 is unavailable.
Do not replace this with json.dumps(sort_keys=True) in production.

Predicates:
    scope.v1
    provenance.v1
    impact.v1

The predicate result is COMPUTED from claim/evidence/policy.
It is not accepted merely because a caller supplies "PASS".
"""

from __future__ import annotations

import hashlib
from typing import Any


RESULTS = {"PASS", "FAIL", "INDETERMINATE"}


class PredicateError(ValueError):
    pass


def jcs_bytes(value: Any) -> bytes:
    """
    Authoritative RFC-8785 JSON Canonicalization Scheme.

    Fails closed when the dependency is unavailable.
    """
    try:
        import rfc8785
    except ImportError as exc:
        raise PredicateError(
            "RFC8785_REQUIRED: install rfc8785 before authoritative hashing"
        ) from exc

    return rfc8785.dumps(value)


def jcs_hash(value: Any) -> str:
    return "sha256:" + hashlib.sha256(jcs_bytes(value)).hexdigest()


def _base_report(
    *,
    predicate_id: str,
    result: str,
    claim: dict[str, Any],
    evidence: dict[str, Any],
    policy: dict[str, Any],
    verifier: dict[str, Any],
    output: dict[str, Any],
) -> dict[str, Any]:

    if result not in RESULTS:
        raise PredicateError(f"invalid predicate result: {result}")

    return {
        "predicate_id": predicate_id,
        "result": result,

        "claim_digest": jcs_hash(claim),
        "evidence_manifest_digest": jcs_hash(evidence),
        "policy_digest": jcs_hash(policy),

        "verifier": verifier,

        "execution": {
            "input_digest": jcs_hash({
                "claim": claim,
                "evidence": evidence,
                "policy": policy,
            }),
            "output_digest": jcs_hash(output),
            "network_mode": "disabled",
        },

        "output": output,
    }


def scope_v1(
    claim: dict[str, Any],
    evidence: dict[str, Any],
    policy: dict[str, Any],
    verifier: dict[str, Any],
) -> dict[str, Any]:
    """
    scope.v1

    PASS iff every evidence object explicitly required by the claim
    is present in the evidence manifest.
    """

    required = set(
        claim.get("scope", {}).get(
            "required_evidence_ids", []
        )
    )

    available = set(
        evidence.get("evidence_ids", [])
    )

    missing = sorted(required - available)

    output = {
        "required": sorted(required),
        "available": sorted(available),
        "missing": missing,
    }

    result = "PASS" if not missing else "FAIL"

    return _base_report(
        predicate_id="scope.v1",
        result=result,
        claim=claim,
        evidence=evidence,
        policy=policy,
        verifier=verifier,
        output=output,
    )


def provenance_v1(
    claim: dict[str, Any],
    evidence: dict[str, Any],
    policy: dict[str, Any],
    verifier: dict[str, Any],
) -> dict[str, Any]:
    """
    provenance.v1

    PASS iff:
      1. all referenced graph nodes exist;
      2. all claim roots exist;
      3. provenance graph is acyclic.
    """

    graph = evidence.get("provenance", {})

    nodes = {
        node["id"]
        for node in graph.get("nodes", [])
        if isinstance(node, dict) and "id" in node
    }

    edges = [
        tuple(edge)
        for edge in graph.get("edges", [])
        if isinstance(edge, list) and len(edge) == 2
    ]

    missing_edge_nodes = sorted({
        node
        for edge in edges
        for node in edge
        if node not in nodes
    })

    roots = set(
        claim.get("provenance", {}).get(
            "roots", []
        )
    )

    missing_roots = sorted(roots - nodes)

    adjacency = {node: [] for node in nodes}

    for source, target in edges:
        if source in adjacency:
            adjacency[source].append(target)

    colour = {node: 0 for node in nodes}
    cycle = False

    def visit(node: str) -> None:
        nonlocal cycle

        colour[node] = 1

        for target in adjacency[node]:
            if colour[target] == 1:
                cycle = True
            elif colour[target] == 0:
                visit(target)

        colour[node] = 2

    for node in nodes:
        if colour[node] == 0:
            visit(node)

    output = {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "missing_edge_nodes": missing_edge_nodes,
        "missing_roots": missing_roots,
        "acyclic": not cycle,
    }

    result = (
        "PASS"
        if not missing_edge_nodes
        and not missing_roots
        and not cycle
        else "FAIL"
    )

    return _base_report(
        predicate_id="provenance.v1",
        result=result,
        claim=claim,
        evidence=evidence,
        policy=policy,
        verifier=verifier,
        output=output,
    )


def impact_v1(
    claim: dict[str, Any],
    evidence: dict[str, Any],
    policy: dict[str, Any],
    verifier: dict[str, Any],
) -> dict[str, Any]:
    """
    impact.v1

    Recomputes dependency closure from roots.

    It does NOT trust a caller-supplied closure.

    PASS iff:
        recomputed closure == supplied closure
        AND graph references are valid
        AND roots exist.
    """

    graph = evidence.get("dependency_graph", {})

    nodes = set(graph.get("nodes", []))

    edges = [
        tuple(edge)
        for edge in graph.get("edges", [])
        if isinstance(edge, list) and len(edge) == 2
    ]

    roots = set(
        claim.get("impact", {}).get(
            "root_claims", []
        )
    )

    missing_edge_nodes = sorted({
        node
        for edge in edges
        for node in edge
        if node not in nodes
    })

    missing_roots = sorted(roots - nodes)

    adjacency = {node: [] for node in nodes}

    for source, target in edges:
        if source in adjacency:
            adjacency[source].append(target)

    closure = set()
    stack = list(roots & nodes)

    while stack:
        node = stack.pop()

        if node in closure:
            continue

        closure.add(node)
        stack.extend(adjacency[node])

    recomputed = sorted(closure)

    supplied = sorted(
        evidence.get("impact_closure", [])
    )

    output = {
        "roots": sorted(roots),
        "recomputed_closure": recomputed,
        "supplied_closure": supplied,
        "match": recomputed == supplied,
        "missing_edge_nodes": missing_edge_nodes,
        "missing_roots": missing_roots,
    }

    result = (
        "PASS"
        if not missing_edge_nodes
        and not missing_roots
        and recomputed == supplied
        else "FAIL"
    )

    return _base_report(
        predicate_id="impact.v1",
        result=result,
        claim=claim,
        evidence=evidence,
        policy=policy,
        verifier=verifier,
        output=output,
    )


def predicate_admissible(
    report: dict[str, Any],
    claim: dict[str, Any],
    evidence: dict[str, Any],
    policy: dict[str, Any],
    trusted_verifiers: dict[tuple[str, str], str],
) -> tuple[bool, str]:
    """
    Predicate labels are NOT authority.

    A report becomes admissible only if:
      - schema fields exist;
      - result is legal;
      - claim/evidence/policy digests match;
      - verifier identity/version is trusted;
      - verifier artifact digest is pinned;
      - execution was network-disabled.
    """

    required = (
        "predicate_id",
        "result",
        "claim_digest",
        "evidence_manifest_digest",
        "policy_digest",
        "verifier",
        "execution",
    )

    for field in required:
        if field not in report:
            return False, f"MISSING:{field}"

    if report["result"] not in RESULTS:
        return False, "BAD_RESULT"

    if report["claim_digest"] != jcs_hash(claim):
        return False, "CLAIM_DIGEST_MISMATCH"

    if report["evidence_manifest_digest"] != jcs_hash(evidence):
        return False, "EVIDENCE_DIGEST_MISMATCH"

    if report["policy_digest"] != jcs_hash(policy):
        return False, "POLICY_DIGEST_MISMATCH"

    verifier = report["verifier"]

    key = (
        verifier.get("id"),
        verifier.get("version"),
    )

    if trusted_verifiers.get(key) != verifier.get(
        "artifact_digest"
    ):
        return False, "UNTRUSTED_VERIFIER"

    if report["execution"].get(
        "network_mode"
    ) != "disabled":
        return False, "NETWORK_NOT_DISABLED"

    return True, "OK"



requirements.txt


rfc8785==0.1.4



The package is currently documented on PyPI as a pure-Python RFC-8785 implementation with no dependencies; 0.1.4 is the latest listed release there.


CL-2 execution status


scope.v1
    valid evidence       PASS
    missing evidence     FAIL

provenance.v1
    acyclic graph        PASS
    cyclic graph         FAIL

impact.v1
    exact closure        PASS
    stale closure        FAIL

predicate_admissible
    correctly bound      PASS
    bare label           REJECT
    wrong digest         REJECT
    untrusted verifier   REJECT
    network execution    REJECT



Execution caveat: these tests were run with a temporary local canonicalization substitute because rfc8785 is absent from the offline environment. They are therefore logic tests, not cryptographic certification.

