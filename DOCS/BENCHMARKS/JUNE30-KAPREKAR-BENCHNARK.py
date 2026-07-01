"""
Kaprekar Benchmark for AQARION

Canonical finite dynamical system:
- State space: 0000–9999 excluding repdigits
- Dynamics: descending digits - ascending digits
- True attractor: 6174
"""

import numpy as np
from collections import defaultdict


# ============================================================
# 1. Kaprekar step (core dynamics)
# ============================================================
def kaprekar_step(n: int, digits: int = 4) -> int:
    s = f"{n:0{digits}d}"
    desc = int("".join(sorted(s, reverse=True)))
    asc = int("".join(sorted(s)))
    return desc - asc


# ============================================================
# 2. Build Kaprekar system (faithful FDDS)
# ============================================================
def build_kaprekar_system(digits: int = 4):
    max_n = 10 ** digits

    # include all states (including repdigits as valid nodes)
    states = list(range(max_n))

    state_map = {n: i for i, n in enumerate(states)}
    n_states = len(states)

    T = [0] * n_states

    for n in states:
        i = state_map[n]
        nxt = kaprekar_step(n, digits)
        T[i] = state_map[nxt]

    return T, state_map


# ============================================================
# 3. True cycle detection (SCC-style for functional graph)
# ============================================================
def kaprekar_cycles(T):
    n = len(T)
    visited = [False] * n
    stack = []
    in_stack = [False] * n
    cycles = []

    def dfs(v):
        visited[v] = True
        stack.append(v)
        in_stack[v] = True

        nxt = T[v]

        if not visited[nxt]:
            dfs(nxt)
        elif in_stack[nxt]:
            # extract cycle
            cycle = []
            for x in reversed(stack):
                cycle.append(x)
                if x == nxt:
                    break
            cycles.append(set(cycle))

        stack.pop()
        in_stack[v] = False

    for i in range(n):
        if not visited[i]:
            dfs(i)

    return cycles


# ============================================================
# 4. Basin partition (true dynamical equivalence)
# ============================================================
def kaprekar_basin_partition(T, cycles):
    n = len(T)

    # map node → cycle id
    cycle_id = {}
    for i, c in enumerate(cycles):
        for x in c:
            cycle_id[x] = i

    basins = defaultdict(list)

    for i in range(n):
        seen = set()
        cur = i

        # follow trajectory until cycle reached
        while cur not in seen:
            seen.add(cur)
            cur = T[cur]

        # assign to cycle basin
        for c in cycles:
            if cur in c:
                basins[frozenset(c)].append(i)
                break

    return list(basins.values())


# ============================================================
# 5. Attractor identification (Kaprekar constant emerges here)
# ============================================================
def identify_attractors(T):
    return [i for i in range(len(T)) if T[i] == i]


# ============================================================
# 6. Benchmark runner (AQARION-compatible)
# ============================================================
def run_kaprekar_benchmark(digits: int = 4):
    print(f"=== Kaprekar Benchmark ({digits}-digit) ===")

    T, state_map = build_kaprekar_system(digits)

    cycles = kaprekar_cycles(T)
    basins = kaprekar_basin_partition(T, cycles)
    fixed_points = identify_attractors(T)

    print(f"States: {len(T)}")
    print(f"Cycles detected: {len(cycles)}")
    print(f"Basin blocks: {len(basins)}")
    print(f"Fixed points: {len(fixed_points)}")

    # verify Kaprekar constant presence
    inv = {v: k for k, v in state_map.items()}
    fixed_values = [inv[i] for i in fixed_points]

    print("Fixed points (values):", fixed_values)

    # check if 6174 exists
    if 6174 in fixed_values:
        print("✔ Kaprekar constant (6174) confirmed as fixed point")
    else:
        print("⚠ 6174 not a fixed point in current representation")

    return {
        "states": len(T),
        "cycles": cycles,
        "basins": basins,
        "fixed_points": fixed_points
    }


# ============================================================
# 7. CLI entry
# ============================================================
if __name__ == "__main__":
    results = run_kaprekar_benchmark(4)
    print("\n=== Benchmark Complete ===")
