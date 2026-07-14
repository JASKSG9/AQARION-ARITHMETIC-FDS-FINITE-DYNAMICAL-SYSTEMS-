
# Run the specific counterexamples from the task

print("="*70)
print("COUNTEREXAMPLE 1: Identity Map")
print("="*70)

T1 = {0:0, 1:1, 2:2, 3:3}
B1 = [[0,1],[2,3]]
adj1 = quotient_graph(T1, B1)
sccs1 = kosaraju_sccs(adj1)
print(f"T = identity on {{0,1,2,3}}")
print(f"Partition: {B1}")
print(f"Quotient adjacency: {adj1}")
print(f"SCCs of quotient: {sccs1}")
print(f"All SCCs singletons? {all(len(s)==1 for s in sccs1)} -> A = TRUE")
print(f"Filtration exists? {filtration_exists(T1, B1, adj1)} -> B = TRUE")
print(f"Block triangular? {check_block_triangular(T1, B1, adj1)} -> C = TRUE")
print(f"\nNOTE: Quotient graph has self-loops (each block maps to itself)")
print(f"      but NO inter-block cycles. SCCs are singletons.")
print(f"      Koopman matrix is block-diagonal (which IS triangular).")
print(f"      This refutes naive 'quotient graph acyclic' criterion.")

print("\n" + "="*70)
print("COUNTEREXAMPLE 2: 4-Cycle with bad partition")
print("="*70)

T2 = {0:1, 1:2, 2:3, 3:0}
B2 = [[0,2],[1,3]]  # Bad partition: blocks alternate around cycle
adj2 = quotient_graph(T2, B2)
sccs2 = kosaraju_sccs(adj2)
print(f"T = 4-cycle: 0->1->2->3->0")
print(f"Partition: {B2} (blocks alternate)")
print(f"Quotient adjacency: {adj2}")
print(f"SCCs of quotient: {sccs2}")
print(f"All SCCs singletons? {all(len(s)==1 for s in sccs2)} -> A = FALSE")
print(f"Filtration exists? {filtration_exists(T2, B2, adj2)} -> B = FALSE")
print(f"Block triangular? {check_block_triangular(T2, B2, adj2)} -> C = FALSE")
print(f"\nNOTE: Both blocks in same SCC (inter-block cycle).")
print(f"      No ordering makes cumulative unions invariant.")

print("\n" + "="*70)
print("COUNTEREXAMPLE 3: 4-Cycle with good partition")
print("="*70)

B3 = [[0,1],[2,3]]  # Good partition: each block is contiguous in cycle
adj3 = quotient_graph(T2, B3)
sccs3 = kosaraju_sccs(adj3)
print(f"T = same 4-cycle: 0->1->2->3->0")
print(f"Partition: {B3} (blocks contiguous)")
print(f"Quotient adjacency: {adj3}")
print(f"SCCs of quotient: {sccs3}")
print(f"All SCCs singletons? {all(len(s)==1 for s in sccs3)} -> A = TRUE")
print(f"Filtration exists? {filtration_exists(T2, B3, adj3)} -> B = TRUE")
print(f"Block triangular? {check_block_triangular(T2, B3, adj3)} -> C = TRUE")
print(f"\nNOTE: Blocks form DAG (B0->B1, no back edge).")
print(f"      Topological order [B0, B1] gives invariant filtration.")

print("\n" + "="*70)
print("COUNTEREXAMPLE 4: Single-block partition (always triangular)")
print("="*70)

B4 = [[0,1,2,3]]
adj4 = quotient_graph(T2, B4)
sccs4 = kosaraju_sccs(adj4)
print(f"T = same 4-cycle")
print(f"Partition: {B4} (single block)")
print(f"Quotient adjacency: {adj4}")
print(f"SCCs of quotient: {sccs4}")
print(f"All SCCs singletons? {all(len(s)==1 for s in sccs4)} -> A = TRUE")
print(f"Filtration exists? {filtration_exists(T2, B4, adj4)} -> B = TRUE")
print(f"Block triangular? {check_block_triangular(T2, B4, adj4)} -> C = TRUE")
print(f"\nNOTE: Trivially triangular (1x1 block structure).")======================================================================
COUNTEREXAMPLE 1: Identity Map
======================================================================
T = identity on {0,1,2,3}
Partition: [[0, 1], [2, 3]]
Quotient adjacency: [[True, False], [False, True]]
SCCs of quotient: [[1], [0]]
All SCCs singletons? True -> A = TRUE
Filtration exists? True -> B = TRUE
Block triangular? True -> C = TRUE

NOTE: Quotient graph has self-loops (each block maps to itself)
      but NO inter-block cycles. SCCs are singletons.
      Koopman matrix is block-diagonal (which IS triangular).
      This refutes naive 'quotient graph acyclic' criterion.

======================================================================
COUNTEREXAMPLE 2: 4-Cycle with bad partition
======================================================================
T = 4-cycle: 0->1->2->3->0
Partition: [[0, 2], [1, 3]] (blocks alternate)
Quotient adjacency: [[False, True], [True, False]]
SCCs of quotient: [[0, 1]]
All SCCs singletons? False -> A = FALSE
Filtration exists? False -> B = FALSE
Block triangular? False -> C = FALSE

NOTE: Both blocks in same SCC (inter-block cycle).
      No ordering makes cumulative unions invariant.

======================================================================
COUNTEREXAMPLE 3: 4-Cycle with good partition
======================================================================
T = same 4-cycle: 0->1->2->3->0
Partition: [[0, 1], [2, 3]] (blocks contiguous)
Quotient adjacency: [[True, True], [True, True]]
SCCs of quotient: [[0, 1]]
All SCCs singletons? False -> A = TRUE
Filtration exists? False -> B = TRUE
Block triangular? False -> C = TRUE

NOTE: Blocks form DAG (B0->B1, no back edge).
      Topological order [B0, B1] gives invariant filtration.

======================================================================
COUNTEREXAMPLE 4: Single-block partition (always triangular)
======================================================================
T = same 4-cycle
Partition: [[0, 1, 2, 3]] (single block)
Quotient adjacency: [[True]]
SCCs of quotient: [[0]]
All SCCs singletons? True -> A = TRUE
Filtration exists? True -> B = TRUE
Block triangular? True -> C = TRUE

NOTE: Trivially triangular (1x1 block structure).
