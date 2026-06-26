#!/usr/bin/env python3
"""
KAPREKAR-KOOPMAN CYOA DEMO — The Obstruction Quest (Terminal Edition)
A tiny interactive narrative that lets you "see" invariant partitions.
"""

import numpy as np

# ---------- The deterministic world ----------
# States: 0=Crossroads, 1=DarkForest, 2=MurkyHollow, 3=WindyRidge, 4=CrystalCave, 5=SacredQuotient
STATE_NAMES = ["Crossroads", "Dark Forest", "Murky Hollow", "Windy Ridge", "Crystal Cave", "Sacred Quotient"]
N = 6

# Transition function T : state -> next state (deterministic chain)
T = np.array([1, 2, 3, 4, 5, 5])  # 0->1, 1->2, 2->3, 3->4, 4->5, 5->5

# Koopman operator (pullback): K_{i,j} = 1 if T(j)=i else 0
K = np.zeros((N, N), dtype=int)
for j in range(N):
    K[T[j], j] = 1

# ---------- Partition & obstruction ----------
def projection_matrix(partition):
    """Build block-constant projection P from a partition (list of lists of state indices)."""
    P = np.zeros((N, N))
    for block in partition:
        block = list(block)
        b = len(block)
        if b == 0:
            continue
        for i in block:
            for j in block:
                P[i, j] = 1.0 / b
    return P

def obstruction_rank(P):
    """Compute rank of obstruction D = (I-P) K P."""
    D = (np.eye(N) - P) @ K @ P
    return np.linalg.matrix_rank(D)

def find_witness(P):
    """Find one state pair that 'leaks': a state x and y in same class with T(x) and T(y) in different classes."""
    partition = partition_from_matrix(P)  # we'll need a function to extract blocks from P
    # Instead of extracting, we can use a simple search: for each state x, find another state y in same class
    # where class of T(x) != class of T(y)
    # We'll build a mapping from state to its class id using the P matrix
    class_of = {}
    for i in range(N):
        # find a representative where P[i,:] has its maximum (the block indicator)
        for j in range(N):
            if np.isclose(P[i, j], 1.0 / len(block_for_state(i, P))):  # not simple
                pass
    # Easier: we'll pass the partition as list of sets
    # We'll redesign: keep the partition as list of sets for witness search
    return None  # will be implemented properly when partition is known

def partition_from_matrix(P):
    # Recover partition blocks from projection matrix (assuming exact block structure)
    blocks = []
    used = set()
    for i in range(N):
        if i in used:
            continue
        block = [i]
        used.add(i)
        for j in range(i+1, N):
            if np.allclose(P[i], P[j]):
                block.append(j)
                used.add(j)
        blocks.append(block)
    return blocks

# ---------- Game narrative ----------
def print_graph():
    print("\n🌐 THE FINITE DETERMINISTIC WILDS 🌐")
    print("Locations and where they lead (the only paths):")
    for s, name in enumerate(STATE_NAMES):
        next_name = STATE_NAMES[T[s]]
        arrow = "→"
        print(f"  [{s}] {name} {arrow} {next_name}")
    print()

def choose_partition():
    print("Before you enter, you must declare how you see the world.")
    print("Group locations that you consider 'the same'.")
    print("\nAvailable quick partitions:")
    print("  1 : All distinct            (every location unique)")
    print("  2 : Merge Hollow & Ridge    (states 2 and 3 together)")
    print("  3 : Merge all               (everything is the same)")
    print("  c : Custom partition        (type your own grouping)")
    choice = input("\nYour choice (1/2/3/c): ").strip().lower()
    if choice == '1':
        partition = [[i] for i in range(N)]
        desc = "All distinct"
    elif choice == '2':
        partition = [[0], [1], [2,3], [4], [5]]
        desc = "Hollow & Ridge merged"
    elif choice == '3':
        partition = [list(range(N))]
        desc = "All merged (coarse world)"
    elif choice == 'c':
        print("Enter groups as space-separated numbers. End each group with a blank line.")
        partition = []
        while True:
            line = input("Group: ").strip()
            if line == "":
                break
            try:
                indices = [int(x) for x in line.split()]
                if all(0 <= x < N for x in indices):
                    partition.append(indices)
                else:
                    print("Invalid state numbers (0-5). Try again.")
            except ValueError:
                print("Invalid input. Use numbers.")
        desc = "custom"
    else:
        print("Invalid choice. Using all distinct.")
        partition = [[i] for i in range(N)]
        desc = "All distinct (default)"
    return partition, desc

def oracle_check(partition):
    P = projection_matrix(partition)
    rankD = obstruction_rank(P)
    if rankD == 0:
        # Check commutator for reducing property (optional)
        C = P @ K - K @ P
        rankC = np.linalg.matrix_rank(C)
        if rankC == 0:
            return "FULL_REDUCTION", rankD, rankC
        else:
            return "INVARIANT_NOT_REDUCING", rankD, rankC
    else:
        return "OBSTRUCTION", rankD, None

def witness(partition):
    """Find a concrete witness: two states x,y in same block with T(x),T(y) in different blocks."""
    # Build a lookup: state -> block index
    block_of = {}
    for idx, blk in enumerate(partition):
        for s in blk:
            block_of[s] = idx
    for blk in partition:
        for i in range(len(blk)):
            for j in range(i+1, len(blk)):
                x = blk[i]
                y = blk[j]
                if block_of[T[x]] != block_of[T[y]]:
                    return (x, y, T[x], T[y], block_of[T[x]], block_of[T[y]])
    return None

# ---------- Main game flow ----------
def main():
    print("="*60)
    print("  KAPREKAR–KOOPMAN CYOA: The Obstruction Quest")
    print("="*60)
    print("Koopman: 'Welcome, Observer. To pass, your observation must survive the dynamics.'")
    print_graph()

    while True:
        partition, desc = choose_partition()
        P = projection_matrix(partition)
        status, rankD, rankC = oracle_check(partition)

        print("\n🔮 Koopman examines your partition...")
        if status == "FULL_REDUCTION":
            print(f"✔ D_Π = 0, C_Π = 0. Fully reducing!")
            print("Koopman: 'Observation and dynamics agree. The path is clear.'")
            print("\n🎉 You have reached the **Sacred Quotient**.")
            break
        elif status == "INVARIANT_NOT_REDUCING":
            print(f"⚠ D_Π = 0 (invariant), but commutator rank {rankC}.")
            print("Koopman: 'A stable quotient exists, yet a shadow remains. Not fully reduced.'")
            print("\n🔚 Ending: **Invariant Limbo**. You may pass, but the world is not fully understood.")
            # In a full game, could allow retry, but for demo, end.
            break
        else:  # obstruction
            print(f"❌ Obstruction detected! D_Π rank = {rankD}.")
            w = witness(partition)
            if w:
                x, y, tx, ty, blk_x, blk_y = w
                print(f"Koopman: 'You merged {STATE_NAMES[x]} and {STATE_NAMES[y]} (states {x},{y}).")
                print(f"         Yet {STATE_NAMES[x]} → {STATE_NAMES[tx]} and {STATE_NAMES[y]} → {STATE_NAMES[ty]}.")
                print(f"         Those futures are in different classes. Your observation leaks.'")
            print("\nKoopman: 'Adjust your partition and try again.'\n")
            # Loop back to retry partition choice

if __name__ == "__main__":
    main()
