# ============================================================
# AQ-S15-SV-002-BRIDGE
# PURPOSE: Reconstruct actual finite-state Koopman/block bridge
# A_actual = U^T K U vs A_model = q S^b + p S^(b+1)
# GOVERNANCE: FROZEN AUDIT / NO PROMOTION / C4 BLOCKED
# Exact Fraction only
# ============================================================
from fractions import Fraction as Q

def eye(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]

def matmul(A, B):
    nr = len(A); nk = len(B); nc = len(B[0])
    assert len(A[0]) == nk
    return [[sum(A[i][t] * B[t][j] for t in range(nk)) for j in range(nc)] for i in range(nr)]

def transpose(A):
    return [list(row) for row in zip(*A)]

def shift_S(m):
    return [[Q(j == (i + 1) % m) for j in range(m)] for i in range(m)]

def matpow(A, n):
    if n == 0:
        return eye(len(A))
    R = eye(len(A)); B = A
    while n:
        if n & 1:
            R = matmul(R, B)
        B = matmul(B, B)
        n >>= 1
    return R

def scalar(A, c):
    return [[c * x for x in row] for row in A]

def add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def permutation_K(n, T):
    K = [[Q(0) for _ in range(n)] for _ in range(n)]
    for x in range(n):
        y = T[x]
        K[x][y] = Q(1)
    return K

def block_indicator_U(m, k):
    n = m * k
    U = [[Q(0) for _ in range(m)] for _ in range(n)]
    norm = Q(1, k)
    for j in range(m):
        for a in range(k):
            x = j * k + a
            U[x][j] = norm
    return U

def translation_T(m, k, d):
    n = m * k
    return [(x + d) % n for x in range(n)]

def model_A(m, k, r, b):
    p = Q(r, k); q = Q(k - r, k)
    S = shift_S(m)
    return add(scalar(matpow(S, b), q), scalar(matpow(S, b + 1), p))

def actual_A(m, k, r, b):
    d = b * k + r
    T = translation_T(m, k, d)
    K = permutation_K(m * k, T)
    U = block_indicator_U(m, k)
    return matmul(matmul(transpose(U), K), U)

def first_difference(A, B):
    for i in range(len(A)):
        for j in range(len(A[0])):
            if A[i][j]!= B[i][j]:
                return i, j, A[i][j], B[i][j]
    return None

def bridge_check(m, k, r, b):
    A_actual = actual_A(m, k, r, b)
    A_model = model_A(m, k, r, b)
    diff = first_difference(A_actual, A_model)
    return diff is None, diff

failures = []
for m in range(2, 21):
    for k in range(3, 9):
        for r in range(1, k):
            for b in range(m):
                ok, diff = bridge_check(m, k, r, b)
                if not ok:
                    failures.append((m, k, r, b, diff))

print("AQ-S15-SV-002-BRIDGE")
print("parameter range: m=2..20, k=3..8, 1<=r<k, 0<=b<m")
print("failures:", len(failures))
if failures:
    print("FIRST FAILURE:")
    print(failures[0])
else:
    print("BRIDGE: ALL PASS")
