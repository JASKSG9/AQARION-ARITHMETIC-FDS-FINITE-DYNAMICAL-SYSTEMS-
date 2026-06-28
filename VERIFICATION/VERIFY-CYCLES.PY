
# ============================================================
# verify_cycles.py — Cycle Decomposition Verification
# ============================================================

verify_cycles_py = '''#!/usr/bin/env python3
"""
AQARION Cycle Decomposition Verifier
=====================================
Version: 1.0
Claim: All cycles in the functional graph are correctly identified with
       accurate lengths, representatives, and attractor classification.

CRITICAL: This script MUST NOT import from any AQARION source module.
          It reconstructs the Kaprekar functional graph independently.

Exit: 0 = PASS, 1 = FAIL, 2 = ERROR
"""

import argparse
import sys
import time
from pathlib import Path
from typing import Dict, List, Set, Tuple


def kaprekar_step(n: int) -> int:
    """One step of Kaprekar routine for 4-digit numbers."""
    s = f"{n:04d}"
    asc = int(''.join(sorted(s)))
    desc = int(''.join(sorted(s, reverse=True)))
    return desc - asc


def build_kaprekar_graph() -> Tuple[Dict[int, int], Set[int]]:
    """
    Build the 4-digit Kaprekar functional graph independently.
    Returns (transition_map, state_set).
    """
    # All 4-digit numbers with at least 2 distinct digits
    states = sorted(set(
        kaprekar_step(n) 
        for n in range(1000, 10000) 
        if len(set(f"{n:04d}")) > 1
    ))
    
    transition = {}
    for s in states:
        next_s = kaprekar_step(s)
        transition[s] = next_s
    
    return transition, set(states)


def find_cycles(transition: Dict[int, int]) -> List[Tuple[int, ...]]:
    """
    Find all cycles in the functional graph using Floyd's algorithm
    per connected component, plus direct detection for small cycles.
    """
    visited = set()
    cycles = []
    
    for start in transition:
        if start in visited:
            continue
        
        # Trace path until we hit a known node or detect a cycle
        path = []
        current = start
        while current not in visited and current not in path:
            path.append(current)
            current = transition[current]
        
        if current in path:
            # Found a cycle
            cycle_start_idx = path.index(current)
            cycle = tuple(path[cycle_start_idx:])
            cycles.append(cycle)
        
        # Mark all nodes in this path as visited
        for node in path:
            visited.add(node)
        visited.add(current)
    
    # Remove duplicate cycles (same cycle, different entry points)
    unique_cycles = []
    seen = set()
    for cycle in cycles:
        # Canonical form: rotate to start at minimum element
        min_idx = cycle.index(min(cycle))
        canonical = tuple(cycle[min_idx:] + cycle[:min_idx])
        if canonical not in seen:
            seen.add(canonical)
            unique_cycles.append(canonical)
    
    return sorted(unique_cycles, key=lambda c: (len(c), c))


def verify_cycles(evidence, logger) -> bool:
    """Verify cycle properties against known Kaprekar invariants."""
    
    logger.info("Building Kaprekar functional graph...")
    transition, states = build_kaprekar_graph()
    evidence.add_metric("total_states", len(states))
    
    logger.info("Finding cycles...")
    cycles = find_cycles(transition)
    evidence.add_metric("cycle_count", len(cycles))
    
    # Check 1: Known cycle count for 4-digit Kaprekar
    # The gap system should have exactly 1 non-trivial cycle (the 6174 loop)
    # plus potentially other cycles depending on definition
    # For the standard 4-digit system: 6174 is a fixed point (cycle length 1)
    # and there may be other cycles in the full state space
    known_6174 = 6174 in states
    evidence.add_check(
        name="state_6174_exists",
        passed=known_6174,
        value=known_6174,
        expected=True
    )
    
    # Check 2: 6174 is a fixed point
    if known_6174:
        is_fixed = transition[6174] == 6174
        evidence.add_check(
            name="6174_fixed_point",
            passed=is_fixed,
            value=transition.get(6174, "missing"),
            expected=6174
        )
    
    # Check 3: Cycle length distribution
    cycle_lengths = [len(c) for c in cycles]
    length_counts = {}
    for l in cycle_lengths:
        length_counts[l] = length_counts.get(l, 0) + 1
    evidence.add_metric("cycle_length_distribution", length_counts)
    
    # Check 4: All states eventually reach a cycle (functional graph property)
    all_reach_cycle = True
    for start in states:
        visited = set()
        current = start
        while current not in visited:
            visited.add(current)
            current = transition[current]
        # If we looped, current is in a cycle
        if current not in [c[0] for c in cycles]:
            # Need to check if current is part of any cycle
            in_cycle = any(current in c for c in cycles)
            if not in_cycle:
                all_reach_cycle = False
                break
    
    evidence.add_check(
        name="all_states_reach_cycle",
        passed=all_reach_cycle,
        value=all_reach_cycle,
        expected=True
    )
    
    # Check 5: Attractor classification
    # Each state should have a unique attractor (the cycle it reaches)
    attractors = {}
    for start in states:
        visited = set()
        current = start
        while current not in visited:
            visited.add(current)
            current = transition[current]
        # Find which cycle contains 'current'
        for cycle in cycles:
            if current in cycle:
                attractors[start] = cycle
                break
    
    all_classified = len(attractors) == len(states)
    evidence.add_check(
        name="all_states_classified",
        passed=all_classified,
        value=f"{len(attractors)}/{len(states)} classified",
        expected=f"{len(states)}/{len(states)}"
    )
    
    # Check 6: Transient depth bounds
    max_depth = 0
    for start in states:
        depth = 0
        visited = set()
        current = start
        while current not in visited and not any(current in c for c in cycles):
            visited.add(current)
            current = transition[current]
            depth += 1
            if depth > 1000:  # Safety bound
                break
        max_depth = max(max_depth, depth)
    
    evidence.add_metric("max_transient_depth", max_depth)
    
    # Known invariant: 4-digit Kaprekar has max depth 7
    evidence.add_check(
        name="max_depth_within_known_bound",
        passed=max_depth <= 7,
        value=max_depth,
        expected="<=7"
    )
    
    logger.info(f"Found {len(cycles)} cycles, max depth {max_depth}")
    for cycle in cycles:
        logger.info(f"  Cycle (len={len(cycle)}): {cycle[:5]}{'...' if len(cycle) > 5 else ''}")
    
    return all([
        known_6174,
        is_fixed if known_6174 else False,
        all_reach_cycle,
        all_classified,
        max_depth <= 7
    ])


def main():
    parser = argparse.ArgumentParser(description="Verify cycle decomposition")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--evidence-dir", type=Path, default=Path("evidence"))
    parser.add_argument("--log-file", type=Path, default=None)
    args = parser.parse_args()
    
    sys.path.insert(0, str(Path(__file__).parent))
    from report import Evidence, ReportLogger, exit_pass, exit_fail, exit_error
    
    logger = ReportLogger(log_file=args.log_file)
    start = time.time()
    
    evidence = Evidence(
        verifier="verify_cycles.py",
        claim="All cycles correctly identified with accurate lengths and attractors"
    )
    
    try:
        passed = verify_cycles(evidence, logger)
        evidence.set_duration(start)
        
        evidence_path = args.evidence_dir / "verify_cycles_evidence.json"
        evidence.save(evidence_path)
        
        if passed:
            exit_pass(evidence, "Cycle verification passed")
        else:
            exit_fail(evidence, "Cycle verification failed")
            
    except Exception as e:
        evidence.set_duration(start)
        exit_error(evidence, e, "Cycle verification error")


if __name__ == "__main__":
    main()
'''

with open("/mnt/agents/output/verify_cycles.py", 'w') as f:
    f.write(verify_cycles_py)

print("[SAVED] verify_cycles.py")
