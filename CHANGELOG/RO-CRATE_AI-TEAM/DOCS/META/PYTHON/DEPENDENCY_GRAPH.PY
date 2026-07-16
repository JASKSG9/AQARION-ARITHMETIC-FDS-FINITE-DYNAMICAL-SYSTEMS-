import json, hashlib, pathlib
from collections import deque
FIXED_TIMESTAMP = "2026-07-16T00:00:00+00:00"
BASE = pathlib.Path(__file__).parent.parent
def load_registry():
    report_path = BASE / "reports/claim-registry-report.json"
    if not report_path.exists():
        from src.registry_loader import load_claims
        return load_claims()
    with open(report_path) as f:
        data = json.load(f)
    return data["claims"]
def build_graph(claims):
    nodes = sorted([c["id"] for c in claims])
    node_set = set(nodes)
    adj = {n: [] for n in nodes}
    rev_adj = {n: [] for n in nodes}
    edges = []
    missing = []
    for claim in claims:
        cid = claim["id"]
        for dep in claim.get("dependencies", []):
            if dep not in node_set:
                missing.append({"claim": cid, "missing_dependency": dep})
            else:
                adj[dep].append(cid)
                rev_adj[cid].append(dep)
                dep_type = "formal" if cid == "AQ001" and dep == "TEST-001" else "conceptual" if cid == "PHI377" else "formal"
                edges.append({
                    "from": cid,
                    "to": dep,
                    "relation": "requires",
                    "dependency_type": dep_type,
                    "internal_convention": "internal claim -> prerequisite for requires",
                    "support_convention": "prerequisite -> claim for build order"
                })
    indegree = {n: len(rev_adj[n]) for n in nodes}
    q = deque(sorted([n for n in nodes if indegree[n]==0]))
    topo = []
    while q:
        n = q.popleft()
        topo.append(n)
        for m in sorted(adj[n]):
            indegree[m] -= 1
            if indegree[m]==0:
                q.append(m)
        q = deque(sorted(q))
    has_cycle = len(topo) != len(nodes)
    cycles = []
    if has_cycle:
        visited = set()
        stack = []
        def dfs(u, path_set):
            visited.add(u)
            stack.append(u)
            path_set.add(u)
            for v in adj.get(u, []):
                if v not in visited:
                    dfs(v, path_set)
                elif v in path_set:
                    idx = stack.index(v)
                    cycles.append(stack[idx:] + [v])
            stack.pop()
            path_set.remove(u)
        for n in nodes:
            if n not in visited:
                dfs(n, set())
    support_order = list(reversed(topo)) if not has_cycle else []
    return {
        "nodes": nodes,
        "edges": sorted(edges, key=lambda e: (e["from"], e["to"])),
        "adjacency": {k: sorted(v) for k,v in adj.items()},
        "reverse_adjacency": {k: sorted(v) for k,v in rev_adj.items()},
        "missing_dependencies": missing,
        "cycles": cycles,
        "cycle_count": len(cycles),
        "topological_build_order": topo,
        "support_order": support_order,
        "has_cycle": has_cycle
    }
def canonical_graph_hash(graph_struct):
    scope = {
        "nodes": graph_struct["nodes"],
        "edges": graph_struct["edges"],
        "adjacency": graph_struct["adjacency"]
    }
    canonical = json.dumps(scope, sort_keys=True, separators=(',',':'))
    return hashlib.sha256(canonical.encode()).hexdigest(), canonical
def adversarial_tests():
    results = {}
    test_claims_missing = [{"id": "A", "dependencies": ["NONEXISTENT"]}]
    g_missing = build_graph(test_claims_missing)
    results["missing_dependency_test"] = {
        "expected": "fail with 1 unresolved",
        "actual_missing": len(g_missing["missing_dependencies"]),
        "status": "pass" if len(g_missing["missing_dependencies"])==1 else "fail"
    }
    test_claims_cycle = [
        {"id": "A", "dependencies": ["B"]},
        {"id": "B", "dependencies": ["C"]},
        {"id": "C", "dependencies": ["A"]},
    ]
    g_cycle = build_graph(test_claims_cycle)
    results["cycle_detection_test"] = {
        "expected": "1 cycle and fail status",
        "cycle_count": g_cycle["cycle_count"],
        "has_cycle": g_cycle["has_cycle"],
        "status": "pass" if g_cycle["has_cycle"] and g_cycle["cycle_count"]>=1 else "fail"
    }
    from src.registry_loader import load_claims
    claims = load_claims()
    g1 = build_graph(claims)
    g2 = build_graph(claims)
    g3 = build_graph(claims)
    results["stable_ordering_test"] = {
        "topo_run1": g1["topological_build_order"],
        "topo_run2": g2["topological_build_order"],
        "topo_run3": g3["topological_build_order"],
        "identical": g1["topological_build_order"]==g2["topological_build_order"]==g3["topological_build_order"],
        "status": "pass" if g1["topological_build_order"]==g2["topological_build_order"]
