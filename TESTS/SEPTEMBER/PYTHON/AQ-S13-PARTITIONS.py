"""
ksg_defect.partitions — restricted growth strings and the TORE closure recurrence.

KNOWN PITFALL (regression-tested): the natural-looking RGS generator
`for v in range(mx+1)` can NEVER open a new block (v can never exceed the
current max), so it silently enumerates only the single all-in-one-block
partition instead of all Bell(n) partitions. The fix is `range(mx+2)`
(Knuth, "The Art of Computer Programming" Vol 4A, Algorithm 7.2.1.5H /
restricted growth strings: a_1=0, a_{j+1} <= 1 + max(a_1..a_j)).
This is checked against exact Bell numbers in tests/.
"""
from collections import defaultdict
from typing import Dict, Iterator, List, Optional, Tuple

Partition = Tuple[Tuple[int, ...], ...]


def all_rgs(n: int) -> Iterator[List[int]]:
    """Yield every restricted growth string of length n (one per set partition)."""
    def gen(pos: int, mx: int, rgs: List[int]):
        if pos == n:
            yield rgs[:]
            return
        for v in range(mx + 2):  # correct: allows opening a new block (mx+1)
            if v >= n:
                continue
            rgs[pos] = v
            yield from gen(pos + 1, max(mx, v), rgs)

    rgs = [0] * n
    yield from gen(1, 0, rgs)


def rgs_to_partition(rgs: List[int], n: int) -> Partition:
    g: Dict[int, List[int]] = defaultdict(list)
    for i, v in enumerate(rgs):
        g[v].append(i)
    return tuple(tuple(sorted(v)) for v in sorted(g.values()))


def all_partitions(n: int) -> List[Partition]:
    """All set partitions of {0,...,n-1}. len(result) == Bell(n)."""
    return list({rgs_to_partition(rgs, n) for rgs in all_rgs(n)})


def apply_perm(partition: Partition, T: List[int]) -> Partition:
    return tuple(tuple(sorted(T[x] for x in B)) for B in partition)


def join_partitions(P: Partition, Q: Partition, n: int) -> Partition:
    """Coarsest common refinement's dual: the join in the partition lattice."""
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def unite(a: int, b: int) -> None:
        pa, pb = find(a), find(b)
        if pa != pb:
            parent[pa] = pb

    for B in P:
        for x in B:
            unite(B[0], x)
    for C in Q:
        for x in C:
            unite(C[0], x)
    all_x = {x for part in (P, Q) for B in part for x in B}
    groups: Dict[int, List[int]] = defaultdict(list)
    for x in all_x:
        groups[find(x)].append(x)
    return tuple(tuple(sorted(set(v))) for v in groups.values())


def tore_closure(R: Partition, T: List[int], n: int, max_h: Optional[int] = None
                  ) -> Tuple[Optional[int], Partition]:
    """
    Dynamical closure recurrence: O_{h+1} = O_h v T^h(R), starting O_0 = R.
    Returns (h_T, closure) where h_T is the first h at which the sequence
    stabilizes, or (None, last_O) if it hasn't stabilized within max_h steps
    -- callers MUST check for None, not silently treat it as a bound violation
    or as success. Default max_h = n+2 gives headroom over the conjectured
    h_T <= |R| bound (exhaustively verified for n <= 8, see THEOREMS.md;
    NOT proven for general n).
    """
    if max_h is None:
        max_h = n + 2
    O = R
    T_power = list(range(n))
    for h in range(1, max_h + 1):
        T_power = [T[T_power[i]] for i in range(n)]
        Th_R = apply_perm(R, T_power)
        O_new = join_partitions(O, Th_R, n)
        if set(O_new) == set(O):
            return h, O
        O = O_new
    return None, O
