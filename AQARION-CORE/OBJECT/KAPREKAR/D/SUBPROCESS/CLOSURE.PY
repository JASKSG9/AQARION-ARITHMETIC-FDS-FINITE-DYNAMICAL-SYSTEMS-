"""
aq_closure.py — Reference implementation for Defect Closure Filtration
AQARION-CLOSURE-SUITE v1.0 minimal checkpoint

Computes canonical invariants:
- V_0 = Im(P), V_{n+1} = V_n + K(V_n)
- V_n = sum_{i=0}^n K^i(V_0)
- delta = min{m: V_m = V_{m+1}} stabilization depth
- c = dim V_infty closure dimension
- g_i = dim(V_i)-dim(V_{i-1}) growth
- eta_i = c - dim(V_i) defect index
- E_k = rank((I-P_k) K P_k) = g_{k+1}

Exact arithmetic over Q using Fraction. Numeric fallback via numpy.

Input: K, P as matrices
Output: closure.json + verification
"""
from fractions import Fraction
import json
import hashlib
from pathlib import Path

def to_fraction_matrix(M):
    """Convert list of lists / numpy array to Fraction matrix"""
    n = len(M)
    m = len(M[0]) if n>0 else 0
    F = [[Fraction(0) for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            v = M[i][j]
            if isinstance(v, Fraction):
                F[i][j]=v
            else:
                # handle float 0.5 etc
                if isinstance(v, float):
                    F[i][j]=Fraction(v).limit_denominator(1000000)
                else:
                    F[i][j]=Fraction(v)
    return F

def mat_mul(A,B):
    """A: n x p, B: p x q -> n x q Fractions"""
    n = len(A)
    p = len(A[0]) if n else 0
    q = len(B[0]) if len(B)>0 else 0
    C = [[Fraction(0) for _ in range(q)] for _ in range(n)]
    for i in range(n):
        for k in range(p):
            if A[i][k]==0: continue
            aik = A[i][k]
            for j in range(q):
                if B[k][j]!=0:
                    C[i][j]+= aik * B[k][j]
    return C

def mat_concat(A,B):
    """Concat columns: [A | B]"""
    if not A:
        return B
    if not B:
        return A
    n = len(A)
    return [ A[i] + B[i] for i in range(n) ]

def col_basis(M):
    """
    Return (basis matrix, pivot_cols, rank) where basis matrix columns are
    a subset of columns of M forming basis of column space.
    Gaussian elimination on rows to find pivot columns.
    M: n x m Fraction
    """
    if not M or not M[0]:
        return [], [], 0
    n = len(M)
    m = len(M[0])
    # Copy for elimination
    A = [row[:] for row in M]
    pivot_cols = []
    row = 0
    for col in range(m):
        # find pivot row
        piv = None
        for r in range(row, n):
            if A[r][col] != 0:
                piv = r
                break
        if piv is None:
            continue
        # swap
        A[row], A[piv] = A[piv], A[row]
        # normalize row (optional)
        # eliminate below and above for rank detection (full)
        piv_val = A[row][col]
        for r in range(n):
            if r==row: continue
            if A[r][col]!=0:
                factor = A[r][col]/piv_val
                for c in range(col, m):
                    A[r][c] -= factor * A[row][c]
        pivot_cols.append(col)
        row+=1
        if row==n:
            break
    rank = len(pivot_cols)
    # basis = columns of original M at pivot_cols
    basis = [[M[i][c] for c in pivot_cols] for i in range(n)]
    return basis, pivot_cols, rank

def basis_union(B1, B2):
    """Basis of span(B1)+span(B2) where B1,B2 are n x r matrices"""
    if not B1:
        return col_basis(B2)
    if not B2:
        return col_basis(B1)
    concat = mat_concat(B1,B2)
    return col_basis(concat)

def closure_filtration(K, P, max_steps=100):
    """
    K,P: n x n Fraction matrices
    Returns dict with filtration data
    """
    n = len(K)
    # V0 = Im(P)
    V_basis, _, dim0 = col_basis(P)
    dims = [dim0]
    bases = [V_basis]
    
    for step in range(1, max_steps+1):
        if not bases[-1] or len(bases[-1][0])==0:
            KV = []
        else:
            KV = mat_mul(K, bases[-1])
        V_next_basis, _, dim_next = basis_union(bases[-1], KV)
        if dim_next == dims[-1]:
            break
        dims.append(dim_next)
        bases.append(V_next_basis)
    else:
        raise RuntimeError("Did not stabilize within max_steps")
    
    delta = len(dims)-1
    c = dims[-1]
    growth = [dims[0]] + [dims[i]-dims[i-1] for i in range(1,len(dims))]
    # defect index eta_i = c - dim_i
    eta = [c - d for d 
