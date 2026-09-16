def forest_acyclic(Fset, m):
    """Exact DSU test: F contains no undirected cycle. m = num vertices."""
    parent = list(range(m))
    def find(x):
        while parent[x]!= x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in Fset:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[ra] = rb
    return True
