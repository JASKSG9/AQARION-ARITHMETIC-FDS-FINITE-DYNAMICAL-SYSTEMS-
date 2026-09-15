from fractions import Fraction as Q
import numpy as np
from math import sqrt

def build_M_circulant(m,k,r,q=0):
    M=[[Q(0) for _ in range(m)] for _ in range(m)]
    for j in range(m):
        M[j][(j+q)%m]=Q(k-r)
        M[j][(j+q+1)%m]+=Q(r) # += not = — handles m=2
    return M

def cycle_laplacian_circulant(m):
    L=[[Q(0) for _ in range(m)] for _ in range(m)]
    for i in range(m):
        L[i][i]+=Q(2)
        L[i][(i-1)%m]-=Q(1)
        L[i][(i+1)%m]-=Q(1)
    return L

def check_fourier(m,k,r):
    M=build_M_circulant(m,k,r)
    L=cycle_laplacian_circulant(m)
    Mf=np.array([[float(v) for v in row] for row in M])
    Lf=np.array([[float(v) for v in row] for row in L])
    # Fourier matrix
    w=np.exp(2j*np.pi/m)
    F=np.array([[w**(i*j) for j in range(m)] for i in range(m)])/sqrt(m)
    FMF=np.round(F @ Mf @ np.linalg.inv(F),10)
    FLF=np.round(F @ Lf @ np.linalg.inv(F),10)
    off_M=np.max(np.abs(FMF-np.diag(np.diag(FMF))))
    off_L=np.max(np.abs(FLF-np.diag(np.diag(FLF))))
    return off_M, off_L, np.diag(FMF), np.diag(FLF)

for m,k,r in [(4,3,1),(3,3,1),(2,3,1),(5,4,2)]:
    offM,offL,diagM,diagL=check_fourier(m,k,r)
    print(f"m={m} k={k} r={r} off-diag M:{offM:.2e} L:{offL:.2e} PASS={offM<1e-8 and offL<1e-8}")
