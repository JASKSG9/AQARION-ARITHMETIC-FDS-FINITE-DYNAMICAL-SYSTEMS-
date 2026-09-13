from __future__ import annotations

import hashlib
from typing import Any, Callable

from claimlock_kernel import canonical_bytes, content_hash


def implementation_hash(fn: Callable[..., Any]) -> str:
    """
    Hash the implementation source.

    Production builds should hash the exact deployed artifact
    rather than relying exclusively on inspect.getsource().
    """
    import inspect

    source = inspect.getsource(fn).encode("utf-8")

    return (
        "sha256:"
        + hashlib.sha256(source).hexdigest()
    )


def predicate_record(
    name: str,
    result: str,
    inputs: Any,
    implementation: Callable[..., Any],
    output: Any,
) -> dict[str, Any]:

    return {
        "predicate": name,
        "result": result,
        "input_hash": content_hash(inputs),
        "implementation_hash":
            implementation_hash(implementation),
        "result_hash": content_hash(output),
    }


def scope_sufficient(
    claim: dict[str, Any],
    evidence: dict[str, Any],
) -> dict[str, Any]:

    required = set(
        claim.get("scope", {}).get("required", [])
    )

    covered = set(
        evidence.get("scope", {}).get("covered", [])
    )

    return {
        "required": sorted(required),
        "covered": sorted(covered),
        "missing": sorted(required - covered),
    }


def compute_scope_predicate(
    claim: dict[str, Any],
    evidence: dict[str, Any],
) -> dict[str, Any]:

    output = scope_sufficient(
        claim,
        evidence,
    )

    result = (
        "PASS"
        if not output["missing"]
        else "FAIL"
    )

    return predicate_record(
        "SCOPE_SUFFICIENT",
        result,
        {
            "claim": claim,
            "evidence": evidence,
        },
        compute_scope_predicate,
        output,
    )


def graph_has_cycle(
    edges: list[list[str]],
) -> bool:

    graph: dict[str, list[str]] = {}

    for src, dst in edges:
        graph.setdefault(src, []).append(dst)
        graph.setdefault(dst, [])

    visiting = set()
    visited = set()

    def visit(node: str) -> bool:

        if node in visiting:
            return True

        if node in visited:
            return False

        visiting.add(node)

        for child in graph[node]:
            if visit(child):
                return True

        visiting.remove(node)
        visited.add(node)

        return False

    return any(
        visit(node)
        for node in graph
    )


def compute_provenance_predicate(
    evidence: dict[str, Any],
) -> dict[str, Any]:

    edges = evidence.get(
        "provenance_edges",
        [],
    )

    output = {
        "cycle": graph_has_cycle(edges),
        "edge_count": len(edges),
    }

    result = (
        "FAIL"
        if output["cycle"]
        else "PASS"
    )

    return predicate_record(
        "PROVENANCE_ACYCLIC",
        result,
        evidence,
        compute_provenance_predicate,
        output,
    )


def compute_replay_predicate(
    evidence: dict[str, Any],
) -> dict[str, Any]:

    expected = evidence.get(
        "expected_result_hash"
    )

    observed = evidence.get(
        "observed_result_hash"
    )

    output = {
        "expected": expected,
        "observed": observed,
        "equal": expected == observed,
    }

    result = (
        "PASS"
        if output["equal"]
        else "FAIL"
    )

    return predicate_record(
        "REPLAY_PASS",
        result,
        evidence,
        compute_replay_predicate,
        output,
    )


def compute_route_predicate(
    evidence: dict[str, Any],
) -> dict[str, Any]:

    routes = evidence.get(
        "routes",
        [],
    )

    result_hashes = {
        route.get("result_hash")
        for route in routes
    }

    implementation_hashes = {
        route.get("implementation_hash")
        for route in routes
    }

    output = {
        "route_count": len(routes),
        "result_agreement":
            len(result_hashes) == 1,
        "implementation_count":
            len(implementation_hashes),
        "implementation_diversity":
            len(implementation_hashes)
            == len(routes),
    }

    # Agreement and independence are intentionally separate.
    result = (
        "PASS"
        if output["result_agreement"]
        else "FAIL"
    )

    return predicate_record(
        "ROUTES_AGREE",
        result,
        evidence,
        compute_route_predicate,
        output,
    )


def compute_authority_predicate(
    evidence: dict[str, Any],
) -> dict[str, Any]:

    edges = evidence.get(
        "authority_edges",
        [],
    )

    output = {
        "cycle":
            graph_has_cycle(edges),
        "edge_count":
            len(edges),
    }

    result = (
        "FAIL"
        if output["cycle"]
        else "PASS"
    )

    return predicate_record(
        "AUTHORITY_ACYCLIC",
        result,
        evidence,
        compute_authority_predicate,
        output,
    )


def compute_all_predicates(
    claim: dict[str, Any],
    evidence: dict[str, Any],
) -> dict[str, Any]:

    return {
        "scope":
            compute_scope_predicate(
                claim,
                evidence,
            ),

        "provenance":
            compute_provenance_predicate(
                evidence,
            ),

        "replay":
            compute_replay_predicate(
                evidence,
            ),

        "routes":
            compute_route_predicate(
                evidence,
            ),

        "authority":
            compute_authority_predicate(
                evidence,
            ),
}
