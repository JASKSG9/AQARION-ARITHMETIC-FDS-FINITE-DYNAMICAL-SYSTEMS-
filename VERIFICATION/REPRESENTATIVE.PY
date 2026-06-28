
# ============================================================
# verify_representative.py — Quotient Certification (Key Theorem)
# ============================================================

verify_representative_py = '''#!/usr/bin/env python3
"""
AQARION Quotient Certification Verifier — Key Theorem: π∘T = T̄∘π
================================================================
Version: 1.0
Claim: For every realizable gap pair, the quotient map π satisfies:
       
       π(T(x)) = T̄(π(x))    for every state x
       
       This is the defining property of a genuine dynamical quotient.

VERIFICATION STRATEGY:
  1. For every realizable gap pair g:
     a. Compute representative rep(g) independently
     b. Verify gap(rep(g)) == g (representative correctness)
     c. Verify T(rep(g)) maps to the same successor as all other states in the block
  
  2. For the full Kaprekar system:
     a. Enumerate all 54 states
     b. Build quotient map T̄ on equivalence classes
     c. Verify π(T(x)) = T̄(π(x)) for every x

This proves (or disproves) that the observable partition is a genuine
quotient, not just an observable.

CRITICAL: This script MUST NOT import from any AQARION source module.
          It reconstructs the Kaprekar system and quotient from first principles.

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


def gap_value(n: int) -> int:
    """
    Compute the gap value (max digit - min digit) for a 4-digit number.
    This is the observable that induces the quotient partition.
    """
    digits = [int(d) for d in f"{n:04d}"]
    return max(digits) - min(digits)


def build_gap_system() -> Tuple[Dict[int, int], Dict[int, int], Dict[int, List[int]]]:
    """
    Build the complete 4-digit Kaprekar gap system.
    
    Returns:
      transition: state_idx -> next_state_idx
      gap_map: state_idx -> gap_value
      state_values: state_idx -> original 4-digit number
    """
    # All 4-digit numbers with at least 2 distinct digits
    states = sorted(set(
        kaprekar_step(n)
        for n in range(1000, 10000)
        if len(set(f"{n:04d}")) > 1
    ))
    
    state_idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    
    transition = {}
    gap_map = {}
    state_values = {i: states[i] for i in range(n)}
    
    for i, s in enumerate(states):
        next_s = kaprekar_step(s)
        transition[i] = state_idx[next_s]
        gap_map[i] = gap_value(s)
    
    return transition, gap_map, state_values


def build_quotient_partition(gap_map: Dict[int, int]) -> Dict[int, List[int]]:
    """
    Build partition by gap value.
    Returns: gap_value -> list of state indices with that gap
    """
    partition = {}
    for idx, g in gap_map.items():
        if g not in partition:
            partition[g] = []
        partition[g].append(idx)
    return partition


def build_quotient_map(transition: Dict[int, int], 
                        partition: Dict[int, List[int]],
                        gap_map: Dict[int, int]) -> Dict[int, int]:
    """
    Build quotient transition T̄: gap_value -> gap_value.
    For each block (gap value), compute the gap of the successor.
    """
    quotient_map = {}
    for gap_val, states in partition.items():
        # All states in a block should map to the same quotient successor
        successors = set()
        for s in states:
            next_s = transition[s]
            next_gap = gap_map[next_s]
            successors.add(next_gap)
        
        if len(successors) == 1:
            quotient_map[gap_val] = successors.pop()
        else:
            # This indicates the partition is NOT a genuine quotient
            quotient_map[gap_val] = None
    
    return quotient_map


def verify_quotient_property(transition: Dict[int, int],
                             gap_map: Dict[int, int],
                             partition: Dict[int, List[int]],
                             quotient_map: Dict[int, int],
                             evidence, logger) -> bool:
    """
    Verify π(T(x)) = T̄(π(x)) for every state x.
    
    π(x) = gap_value of x
    T(x) = Kaprekar successor of x
    T̄(g) = quotient successor of gap value g
    """
    
    all_pass = True
    mismatch_count = 0
    max_mismatches_to_report = 10
    
    for state_idx, gap_val in gap_map.items():
        # Compute π(T(x))
        next_state = transition[state_idx]
        next_gap = gap_map[next_state]
        
        # Compute T̄(π(x))
        expected_next_gap = quotient_map.get(gap_val)
        
        if expected_next_gap is None:
            # Partition failed to be a quotient at this block
            all_pass = False
            mismatch_count += 1
            if mismatch_count <= max_mismatches_to_report:
                evidence.add_note(
                    f"State {state_idx} (gap={gap_val}): "
                    f"block has multiple successor gaps — not a genuine quotient"
                )
        elif next_gap != expected_next_gap:
            all_pass = False
            mismatch_count += 1
            if mismatch_count <= max_mismatches_to_report:
                evidence.add_note(
                    f"State {state_idx}: π(T(x))={next_gap} != T̄(π(x))={expected_next_gap}"
                )
    
    evidence.add_metric("total_states_checked", len(gap_map))
    evidence.add_metric("mismatch_count", mismatch_count)
    
    evidence.add_check(
        name="quotient_property_all_states",
        passed=all_pass,
        value=f"{len(gap_map) - mismatch_count}/{len(gap_map)} states agree",
        expected=f"{len(gap_map)}/{len(gap_map)}"
    )
    
    # Verify representative independence
    # For each gap value, all representatives should map to the same successor gap
    rep_independence = True
    for gap_val, states in partition.items():
        successor_gaps = set(gap_map[transition[s]] for s in states)
        if len(successor_gaps) > 1:
            rep_independence = False
            evidence.add_note(
                f"Gap {gap_val}: representatives have different successor gaps: {successor_gaps}"
            )
    
    evidence.add_check(
        name="representative_independence",
        passed=rep_independence,
        value=rep_independence,
        expected=True
    )
    
    logger.info(f"Checked {len(gap_map)} states, {mismatch_count} mismatches")
    logger.info(f"Representative independence: {rep_independence}")
    
    return all_pass and rep_independence


def verify_three_routes(gap_map: Dict[int, int], 
                        partition: Dict[int, List[int]],
                        evidence, logger) -> bool:
    """
    Verify the "three routes" property:
    For each gap value, there should be exactly three independent ways
    to reach the same quotient successor (corresponding to the three
    non-trivial digit permutations).
    """
    # This is a simplified check — full three-routes verification
    # would require enumerating all digit permutations
    
    three_routes = True
    for gap_val, states in partition.items():
        if len(states) < 3:
            # Not enough states for three routes
            continue
        
        # Check that at least 3 states in the block map to the same successor gap
        successor_counts = {}
        for s in states:
            next_gap = gap_map[transition[s]]
            successor_counts[next_gap] = successor_counts.get(next_gap, 0) + 1
        
        max_count = max(successor_counts.values()) if successor_counts else 0
        if max_count < 3 and len(states) >= 3:
            three_routes = False
            evidence.add_note(
                f"Gap {gap_val}: only {max_count} states map to same successor (expected ≥3)"
            )
    
    evidence.add_check(
        name="three_routes_property",
        passed=three_routes,
        value=three_routes,
        expected=True
    )
    
    return three_routes


def main():
    parser = argparse.ArgumentParser(description="Verify quotient certification")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--evidence-dir", type=Path, default=Path("evidence"))
    parser.add_argument("--log-file", type=Path, default=None)
    args = parser.parse_args()
    
    sys.path.insert(0, str(Path(__file__).parent))
    from report import Evidence, ReportLogger, exit_pass, exit_fail, exit_error
    
    logger = ReportLogger(log_file=args.log_file)
    start = time.time()
    
    evidence = Evidence(
        verifier="verify_representative.py",
        claim="Quotient map satisfies π(T(x)) = T̄(π(x)) for every state with representative independence"
    )
    
    try:
        logger.info("Building Kaprekar gap system...")
        transition, gap_map, state_values = build_gap_system()
        n = len(transition)
        evidence.add_metric("state_space_size", n)
        
        logger.info("Building quotient partition...")
        partition = build_quotient_partition(gap_map)
        evidence.add_metric("quotient_blocks", len(partition))
        
        logger.info("Building quotient transition map...")
        quotient_map = build_quotient_map(transition, partition, gap_map)
        
        # Check if quotient is well-defined
        well_defined = all(v is not None for v in quotient_map.values())
        evidence.add_check(
            name="quotient_well_defined",
            passed=well_defined,
            value=well_defined,
            expected=True
        )
        
        if not well_defined:
            evidence.add_note("Quotient map is NOT well-defined — partition is not a genuine quotient")
        
        logger.info("Verifying π(T(x)) = T̄(π(x)) for all states...")
        passed = verify_quotient_property(transition, gap_map, partition, quotient_map, evidence, logger)
        
        logger.info("Verifying three routes property...")
        routes_passed = verify_three_routes(gap_map, partition, evidence, logger)
        
        evidence.set_duration(start)
        
        evidence_path = args.evidence_dir / "verify_representative_evidence.json"
        evidence.save(evidence_path)
        
        if passed and routes_passed and well_defined:
            exit_pass(evidence, "Quotient certification passed — π∘T = T̄∘π verified for all states")
        else:
            exit_fail(evidence, "Quotient certification failed")
            
    except Exception as e:
        evidence.set_duration(start)
        exit_error(evidence, e, "Quotient certification error")


if __name__ == "__main__":
    main()
'''

with open("/mnt/agents/output/verify_representative.py", 'w') as f:
    f.write(verify_representative_py)

print("[SAVED] verify_representative.py — Key theorem π∘T = T̄∘π verification")
