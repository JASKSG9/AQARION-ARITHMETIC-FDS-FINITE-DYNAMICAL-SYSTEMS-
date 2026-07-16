
from pathlib import Path
import json
import hashlib
import subprocess
import sys

ROOT = Path("/mnt/agents/output/AQARION-TOOL-CHAIN")

# ============================================================
# Option C: Graph Analysis Engine
# ============================================================

graph_analyzer = '''#!/usr/bin/env python3
"""aq_analyze — Graph Analysis Engine for AQARION Dependency Graphs

Computes structural metrics from PDG/CDG/EDG/RDG:
  - Centrality (degree, betweenness approx)
  - Cycle detection
  - Depth / longest path
  - Connected components
  - Topological order (if DAG)

Usage:
    aq_analyze <graph_name>
    aq_analyze all
"""

import json
import sys
from pathlib import Path
from collections import defaultdict, deque

ROOT = Path(__file__).parent.resolve()
GRAPHS_DIR = ROOT / "graphs"
REPORTS_DIR = ROOT / "reports"


def load_graph(name):
    with open(GRAPHS_DIR / (name + ".json"), "r") as f:
        return json.load(f)


def build_adjacency(graph):
    """Build adjacency list from edges."""
    adj = defaultdict(list)
    for edge in graph["edges"]:
        adj[edge["from"]].append(edge["to"])
    return adj


def compute_degree_centrality(graph):
    """In-degree and out-degree for each node."""
    in_deg = defaultdict(int)
    out_deg = defaultdict(int)
    for edge in graph["edges"]:
        out_deg[edge["from"]] += 1
        in_deg[edge["to"]] += 1
    return dict(in_deg), dict(out_deg)


def detect_cycles(graph):
    """Detect cycles using DFS. Returns list of cycles (as node lists)."""
    adj = build_adjacency(graph)
    nodes = set(graph["nodes"])
    visited = set()
    rec_stack = []
    cycles = []
    
    def dfs(node, path):
        visited.add(node)
        rec_stack.append(node)
        path_set = set(path)
        
        for neighbor in adj.get(node, []):
            if neighbor in path_set:
                # Found cycle
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles.append(cycle)
            elif neighbor not in visited:
                dfs(neighbor, path + [neighbor])
        
        rec_stack.pop()
    
    for node in nodes:
        if node not in visited:
            dfs(node, [node])
    
    # Deduplicate cycles
    unique = []
    seen = set()
    for c in cycles:
        key = tuple(sorted(c))
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique


def longest_path(graph):
    """Longest path in DAG (or approximate for cyclic). Returns length and path."""
    adj = build_adjacency(graph)
    nodes = list(graph["nodes"])
    
    # Topological sort attempt
    in_deg = defaultdict(int)
    for edge in graph["edges"]:
        in_deg[edge["to"]] += 1
    
    queue = deque([n for n in nodes if in_deg[n] == 0])
    topo_order = []
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        for neighbor in adj.get(node, []):
            in_deg[neighbor] -= 1
            if in_deg[neighbor] == 0:
                queue.append(neighbor)
    
    if len(topo_order) != len(nodes):
        # Graph has cycles — fall back to BFS from each node
        max_len = 0
        max_path = []
        for start in nodes:
            dist = {start: 0}
            parent = {start: None}
            q = deque([start])
            while q:
                node = q.popleft()
                for neighbor in adj.get(node, []):
                    if neighbor not in dist:
                        dist[neighbor] = dist[node] + 1
                        parent[neighbor] = node
                        q.append(neighbor)
            for node, d in dist.items():
                if d > max_len:
                    max_len = d
                    # Reconstruct path
                    path = []
                    cur = node
                    while cur is not None:
                        path.append(cur)
                        cur = parent[cur]
                    max_path = list(reversed(path))
        return max_len, max_path
    
    # DAG: dynamic programming
    dist = {n: 0 for n in nodes}
    parent = {n: None for n in nodes}
    for node in topo_order:
        for neighbor in adj.get(node, []):
            if dist[neighbor] < dist[node] + 1:
                dist[neighbor] = dist[node] + 1
                parent[neighbor] = node
    
    max_node = max(nodes, key=lambda n: dist[n])
    path = []
    cur = max_node
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return dist[max_node], list(reversed(path))


def connected_components(graph):
    """Find weakly connected components."""
    adj = defaultdict(set)
    for edge in graph["edges"]:
        adj[edge["from"]].add(edge["to"])
        adj[edge["to"]].add(edge["from"])
    
    visited = set()
    components = []
    for node in graph["nodes"]:
        if node not in visited:
            comp = []
            stack = [node]
            while stack:
                n = stack.pop()
                if n not in visited:
                    visited.add(n)
                    comp.append(n)
                    for neighbor in adj.get(n, set()):
                        if neighbor not in visited:
                            stack.append(neighbor)
            components.append(sorted(comp))
    return components


def analyze_graph(name):
    graph = load_graph(name)
    adj = build_adjacency(graph)
    in_deg, out_deg = compute_degree_centrality(graph)
    cycles = detect_cycles(graph)
    max_depth, critical_path = longest_path(graph)
    components = connected_components(graph)
    
    report = {
        "graph_name": name,
        "graph_type": graph.get("graph_type"),
        "nodes": len(graph["nodes"]),
        "edges": len(graph["edges"]),
        "density": len(graph["edges"]) / (len(graph["nodes"]) * (len(graph["nodes"]) - 1)) if len(graph["nodes"]) > 1 else 0,
        "cycles_detected": len(cycles),
        "cycles": cycles,
        "max_depth": max_depth,
        "critical_path": critical_path,
        "connected_components": len(components),
        "component_sizes": [len(c) for c in components],
        "degree_centrality": {
            "in_degree": dict(in_deg),
            "out_degree": dict(out_deg)
        },
        "is_dag": len(cycles) == 0
    }
    return report


def main():
    if len(sys.argv) < 2:
        print("Usage: aq_analyze <graph_name>|all")
        sys.exit(1)
    
    target = sys.argv[1]
    graphs = ["pdg", "cdg", "edg", "rdg"] if target == "all" else [target]
    
    all_reports = {}
    for name in graphs:
        if not (GRAPHS_DIR / (name + ".json")).exists():
            print(f"SKIP: {name} not found")
            continue
        report = analyze_graph(name)
        all_reports[name] = report
        print(f"\\n=== {name.upper()} ===")
        print(f"  Nodes: {report['nodes']}, Edges: {report['edges']}")
        print(f"  Density: {report['density']:.4f}")
        print(f"  Cycles: {report['cycles_detected']}")
        print(f"  Max Depth: {report['max_depth']}")
        print(f"  Critical Path: {' -> '.join(report['critical_path'])}")
        print(f"  Components: {report['connected_components']}")
        print(f"  Is DAG: {report['is_dag']}")
    
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(REPORTS_DIR / "graph_analysis_report.json", "w") as f:
        json.dump(all_reports, f, indent=2, sort_keys=True)
    print(f"\\nReport saved: {REPORTS_DIR / 'graph_analysis_report.json'}")


if __name__ == "__main__":
    main()
'''

with open(ROOT / "aq_analyze.py", "w") as f:
    f.write(graph_analyzer)

print("aq_analyze.py created.")

# Run analysis
result = subprocess.run(
    [sys.executable, str(ROOT / "aq_analyze.py"), "all"],
    capture_output=True, text=True, cwd=str(ROOT)
)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)aq_analyze.py created.
=== PDG ===
  Nodes: 4, Edges: 3
  Density: 0.2500
  Cycles: 0
  Max Depth: 2
  Critical Path: PHI377 -> AQ001 -> TEST-001
  Components: 1
  Is DAG: True

=== CDG ===
  Nodes: 4, Edges: 3
  Density: 0.2500
  Cycles: 0
  Max Depth: 2
  Critical Path: PHI377 -> AQ001 -> TEST-001
  Components: 1
  Is DAG: True

=== EDG ===
  Nodes: 6, Edges: 2
  Density: 0.0667
  Cycles: 0
  Max Depth: 1
  Critical Path: AQ001 -> DefectVanishing.lean
  Components: 4
  Is DAG: True

=== RDG ===
  Nodes: 4, Edges: 0
  Density: 0.0000
  Cycles: 0
  Max Depth: 0
  Critical Path: ALG-TEST
  Components: 4
  Is DAG: True

Report saved: /mnt/agents/output/AQARION-TOOL-CHAIN/reports/graph_analysis_report.json
