from fractions import Fraction as Q

def build_M(m, k, r, q=0):
    M = [[Q(0) for _ in range(m)] for _ in range(m)]
    for j in range(m):
        M[j][(j+q) % m] = Q(k-r)
        M[j][(j+q+1) % m] += Q(r) # += handles m=2 where q and q+1 coincide
    return M

def cycle_laplacian(m):
    L = [[Q(0) for _ in range(m)] for _ in range(m)]
    for i in range(m):
        L[i][i] += Q(2)
        L[i][(i-1) % m] -= Q(1)
        L[i][(i+1) % m] -= Q(1) # +=/-= pattern valid for all m>=1, multigraph at m=2
    return L
