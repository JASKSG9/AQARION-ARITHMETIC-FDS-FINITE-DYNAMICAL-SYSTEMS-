
# ============================================================
# FIXED verify_scc.py — Genuine Independent Algorithm Cross-Check
# ============================================================

verify_scc_py = '''#!/usr/bin/env python3
"""
AQARION SCC Verifier (FIXED v2.0)
==================================
Claim: Strongly connected components computed by Tarjan's algorithm
       and Kosaraju's algorithm produce identical results.

CRITICAL FIX (v2.0): Previous version had both functions calling
       nx.strongly_connected_components — a tautology, not a verification.
       
       This version implements BOTH algorithms from scratch using
       only Python standard library. No NetworkX dependency for the
       core algorithms. NetworkX is used only as a third reference
       if available.

Exit: 0 = PASS, 1 = FAIL, 2 = ERROR
"""

import argparse
import sys
import time
from pathlib import Path
from typing import Dict, List, Set, Tuple

# ============================================================
# ALGORITHM 1: Tarjan's SCC (Single-pass DFS with lowlink)
# ============================================================

def tarjan_scc(adj: Dict[int, List[int]]) -> List[List[int]]:
    """
    Tarjan's algorithm for strongly connected components.
    
    adj: dict mapping node -> list of successors
    Returns: list of SCCs, each sorted internally, SCCs sorted by min element
    """
    n_nodes = len(adj)
    index = 0
    stack = []
    on_stack = set()
    indices = {}
    lowlinks = {}
    sccs = []
    
    def strongconnect(v: int):
        nonlocal index
        indices[v] = index
        lowlinks[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)
        
        for w in adj.get(v, []):
            if w not in indices:
                strongconnect(w)
                lowlinks[v] = min(lowlinks[v], lowlinks[w])
            elif w in on_stack:
                lowlinks[v] = min(lowlinks[v], indices[w])
        
        # If v is a root node, pop the stack and generate an SCC
        if lowlinks[v] == indices[v]:
            scc = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                scc.append(w)
                if w == v:
                    break
            sccs.append(sorted(scc))
    
    for v in range(n_nodes):
        if v not in indices:
            strongconnect(v)
    
    # Canonical ordering: sort SCCs by their minimum element
    return sorted(sccs, key=lambda c: c[0])


# ============================================================
# ALGORITHM 2: Kosaraju's SCC (Two-pass DFS on G and G^T)
# ============================================================

def kosaraju_scc(adj: Dict[int, List[int]]) -> List[List[int]]:
    """
    Kosaraju's algorithm for strongly connected components.
    
    Phase 1: DFS on original graph, record finishing order
    Phase 2: DFS on transposed graph in reverse finishing order
    
    adj: dict mapping node -> list of successors
    Returns: list of SCCs, each sorted internally, SCCs sorted by min element
    """
    n_nodes = len(adj)
    visited = [False] * n_nodes
    order = []
    
    # Phase 1: Forward DFS to compute finishing order
    def dfs_forward(v: int):
        visited[v] = True
        for w in adj.get(v, []):
            if not visited[w]:
                dfs_forward(w)
        order.append(v)
    
    for v in range(n_nodes):
        if not visited[v]:
            dfs_forward(v)
    
    # Phase 2: Build transpose graph
    rev_adj = {v: [] for v in range(n_nodes)}
    for v in range(n_nodes):
        for w in adj.get(v, []):
            rev_adj[w].append(v)
    
    # Phase 3: DFS on transpose in reverse finishing order
    visited = [False] * n_nodes
    sccs = []
    
    def dfs_reverse(v: int, component: List[int]):
        visited[v] = True
        component.append(v)
        for w in rev_adj.get(v, []):
            if not visited[w]:
                dfs_reverse(w, component)
    
    for v in reversed(order):
        if not visited[v]:
            comp = []
            dfs_reverse(v, comp)
            sccs.append(sorted(comp))
    
    # Canonical ordering
    return sorted(sccs, key=lambda c: c[0])


# ============================================================
# ALGORITHM 3: Reference check (NetworkX if available)
# ============================================================

def networkx_scc(adj: Dict[int, List[int]]) -> List[List[int]]:
    """NetworkX reference implementation (optional third check)."""
    try:
        import networkx as nx
        G = nx.DiGraph()
        for v, successors in adj.items():
            for w in successors:
                G.add_edge(v, w)
        sccs = [sorted(list(c)) for c in nx.strongly_connected_components(G)]
        return sorted(sccs, key=lambda c: c[0])
    except ImportError:
        return None


# ============================================================
# VERIFICATION LOGIC
# ============================================================

def build_kaprekar_adjacency() -> Dict[int, List[int]]:
    """
    Build adjacency for the 4-digit Kaprekar map (54-state gap system).
    This is an independent reconstruction — does not read from source files.
    """
    def kaprekar_step(n: int) -> int:
        """One step of Kaprekar routine for 4-digit numbers."""
        s = f"{n:04d}"
        asc = int(''.join(sorted(s)))
        desc = int(''.join(sorted(s, reverse=True)))
        return desc - asc
    
    # Build state space (all 4-digit numbers except 6174 fixed point treated separately)
    # The gap system has 54 states (excluding the 6174 fixed point or including it)
    states = sorted(set(kaprekar_step(n) for n in range(1000, 10000) if len(set(f"{n:04d}")) > 1))
    
    # Map to indices
    state_to_idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    
    adj = {i: [] for i in range(n)}
    for s in states:
        next_s = kaprekar_step(s)
        if next_s in state_to_idx:
            adj[state_to_idx[s]].append(state_to_idx[next_s])
    
    return adj


def verify_scc_agreement(adj: Dict[int, List[int]], evidence, logger) -> bool:
    """Run all three algorithms and verify agreement."""
    
    # Run Tarjan
    logger.info("Running Tarjan's algorithm...")
    start_t = time.time()
    tarjan_result = tarjan_scc(adj)
    tarjan_time = time.time() - start_t
    evidence.add_metric("tarjan_time", round(tarjan_time, 6))
    evidence.add_metric("tarjan_scc_count", len(tarjan_result))
    
    # Run Kosaraju
    logger.info("Running Kosaraju's algorithm...")
    start_k = time.time()
    kosaraju_result = kosaraju_scc(adj)
    kosaraju_time = time.time() - start_k
    evidence.add_metric("kosaraju_time", round(kosaraju_time, 6))
    evidence.add_metric("kosaraju_scc_count", len(kosaraju_result))
    
    # Compare Tarjan vs Kosaraju
    tarjan_eq_kosaraju = tarjan_result == kosaraju_result
    evidence.add_check(
        name="tarjan_vs_kosaraju",
        passed=tarjan_eq_kosaraju,
        value=f"Tarjan: {len(tarjan_result)} SCCs, Kosaraju: {len(kosaraju_result)} SCCs",
        expected="identical"
    )
    
    if not tarjan_eq_kosaraju:
        evidence.add_note("TARJAN vs KOSARAJU MISMATCH — algorithms disagree!")
        evidence.add_note(f"Tarjan: {tarjan_result[:3]}...")
        evidence.add_note(f"Kosaraju: {kosaraju_result[:3]}...")
    
    # Optional: NetworkX reference
    logger.info("Running NetworkX reference (if available)...")
    nx_result = networkx_scc(adj)
    if nx_result is not None:
        evidence.add_metric("networkx_scc_count", len(nx_result))
        tarjan_eq_nx = tarjan_result == nx_result
        kosaraju_eq_nx = kosaraju_result == nx_result
        
        evidence.add_check(
            name="tarjan_vs_networkx",
            passed=tarjan_eq_nx,
            value=f"Match: {tarjan_eq_nx}",
            expected=True
        )
        evidence.add_check(
            name="kosaraju_vs_networkx",
            passed=kosaraju_eq_nx,
            value=f"Match: {kosaraju_eq_nx}",
            expected=True
        )
        
        if not (tarjan_eq_nx and kosaraju_eq_nx):
            evidence.add_note("NetworkX reference disagrees with hand-rolled algorithms")
    else:
        evidence.add_note("NetworkX not available — skipped third reference")
    
    # Verify SCC properties
    all_nodes = set(range(len(adj)))
    covered = set()
    for scc in tarjan_result:
        covered.update(scc)
    
    complete_coverage = covered == all_nodes
    evidence.add_check(
        name="scc_complete_coverage",
        passed=complete_coverage,
        value=f"Covered: {len(covered)}/{len(all_nodes)}",
        expected=f"{len(all_nodes)}/{len(all_nodes)}"
    )
    
    # Check for singletons (fixed points) and cycles
    singletons = [scc for scc in tarjan_result if len(scc) == 1]
    cycles = [scc for scc in tarjan_result if len(scc) > 1]
    evidence.add_metric("singleton_sccs", len(singletons))
    evidence.add_metric("cycle_sccs", len(cycles))
    evidence.add_metric("largest_scc_size", max(len(scc) for scc in tarjan_result) if tarjan_result else 0)
    
    return tarjan_eq_kosaraju and complete_coverage


def main():
    parser = argparse.ArgumentParser(description="Verify SCC algorithm agreement")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--evidence-dir", type=Path, default=Path("evidence"))
    parser.add_argument("--log-file", type=Path, default=None)
    args = parser.parse_args()
    
    sys.path.insert(0, str(Path(__file__).parent))
    from report import Evidence, ReportLogger, exit_pass, exit_fail, exit_error
    
    logger = ReportLogger(log_file=args.log_file)
    start = time.time()
    
    evidence = Evidence(
        verifier="verify_scc.py",
        claim="Tarjan and Kosaraju algorithms produce identical SCC decompositions"
    )
    
    logger.info("SCC verification — independent algorithm cross-check")
    
    try:
        # Build Kaprekar adjacency independently
        logger.info("Building Kaprekar gap system adjacency...")
        adj = build_kaprekar_adjacency()
        evidence.add_metric("graph_nodes", len(adj))
        edge_count = sum(len(v) for v in adj.values())
        evidence.add_metric("graph_edges", edge_count)
        logger.info(f"Graph: {len(adj)} nodes, {edge_count} edges")
        
        # Verify SCC agreement
        passed = verify_scc_agreement(adj, evidence, logger)
        evidence.set_duration(start)
        
        evidence_path = args.evidence_dir / "verify_scc_evidence.json"
        evidence.save(evidence_path)
        logger.info(f"Evidence saved: {evidence_path}")
        
        if passed:
            logger.success("SCC algorithms agree — independent cross-check verified")
            exit_pass(evidence, "SCC verification passed")
        else:
            logger.fail("SCC algorithms DISAGREE — critical inconsistency detected")
            exit_fail(evidence, "SCC verification FAILED")
            
    except Exception as e:
        evidence.set_duration(start)
        exit_error(evidence, e, "SCC verification error")


if __name__ == "__main__":
    main()
'''

with open("/mnt/agents/output/verify_scc.py", 'w') as f:
    f.write(verify_scc_py)

print("[SAVED] verify_scc.py (FIXED v2.0 — genuine independent algorithms)")
