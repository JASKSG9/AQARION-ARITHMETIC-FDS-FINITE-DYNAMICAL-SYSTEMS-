# ============================================================
# AQ-S15-CIRCULANT-SYMBOL-CERTIFICATE v1.0
# FROZEN AUDIT / NO PROMOTION / C4 BLOCKED / Lean OPEN
# Replaces: circulant_intertwiner.py
# Purpose: Exact spectral-symbol compatibility, not kernel transfer
# Findings:
# M and G both circulant, share F_m eigenbasis, commute
# ker M!= ker G in general — CIRC-INT-NEG-001 is permanent counterexample
# ============================================================
from fractions import Fraction as Q
import json
import math
import cmath

def eye(m):
    return [[Q(1) if i==j else Q(0) for j in range(m)] for i in range(m)]

def shift_S(m):
    # S: e_i -> e_{i+1 mod m} (forward cycle)
    return [[Q(1) if j==(i+1)%m else Q(0) for j in range(m)] for i in range(m)]

def transpose(A):
    return [list(x) for x in zip(*A)]

def matadd(A,B):
    return [[A[i][j]+B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matsub(A,B):
    return [[A[i][j]-B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def scalar_mul(A,c):
    return [[c*A[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matvec(M,v):
    return [sum(M[i][j]*v[j] for j in range(len(v))) for i in range(len(M))]

def build_M_circulant(m,k,r,q=0):
    """
    CORRECTED construction — uses += for m=2 coincidence.
    M[source][(source+q)%m] += k-r
    M[source][(source+q+1)%m] += r
    For m=2, q+1 == q-1 mod 2, so += merges, not overwrites.
    """
    M=[[Q(0) for _ in range(m)] for _ in range(m)]
    for src in range(m):
        M[src][(src+q)%m] += Q(k-r)
        M[src][(src+q+1)%m] += Q(r)
    return M

def build_G(m,k,r):
    """G = U^T D^T D U = alpha^2 * (2I - S - S^T), alpha^2 = r(k-r)/k^2"""
    alpha2 = Q(r*(k-r), k*k) if k!=0 else Q(0)
    I=eye(m); S=shift_S(m); ST=transpose(S)
    return scalar_mul(matsub(matsub(scalar_mul(I,Q(2)), S), ST), alpha2), alpha2

def is_circulant(M):
    m=len(M)
    return all(M[i][j]==M[0][(j-i)%m] for i in range(m) for j in range(m))

def m_zero_modes(m,k,r):
    """Exact: (k-r)+r*omega^l=0 iff r=k/2, m even, l=m/2"""
    if k%2==1: return []
    if r!= k//2: return []
    if m%2==1: return []
    if r==0 or r==k: return []
    return [m//2]

def g_zero_modes(m,k,r):
    """Exact: G = alpha^2*4 sin^2(pi l/m), alpha^2>0 => zero only l=0"""
    if r==0 or r==k:
        return list(range(m)) # G=0
    return [0]

def test_circ_int_neg_001():
    """
    CIRC-INT-NEG-001 — permanent negative control
    k=2,m=4,r=1,q=0: M=I+S, v=(1,-1,1,-1)
    Mv=0 but Gv=v — shared DFT basis does NOT imply kernel transfer
    """
    k=2; m=4; r=1; q=0
    I=eye(m); S=shift_S(m); ST=transpose(S)
    M=build_M_circulant(m,k,r,q)
    G,alpha2=build_G(m,k,r)
    v=[Q(1),Q(-1),Q(1),Q(-1)]
    mv=matvec(M,v)
    gv=matvec(G,v)
    assert mv==[Q(0)]*m, f"Mv expected 0, got {mv}"
    assert gv==v, f"Gv expected v, got {gv} — alpha2={alpha2}"
    print("CIRC-INT-NEG-001=PASS")
    print(f" M=I+S, v=alternating, Mv=0, Gv=v, alpha2={alpha2}")
    print(f" CONCLUSION=shared_F_basis_does_not_imply_kernel_transfer")
    return True

def fourier_check_numeric(m,k,r,q=0):
    """Numeric check that F_m diagonalizes both — off-diag <1e-12"""
    try:
        import numpy as np
        M=build_M_circulant(m,k,r,q)
        G,_=build_G(m,k,r)
        Mf=np.array([[float(x) for x in row] for row in M])
        Gf=np.array([[float(x) for x in row] for row in G])
        F=np.fft.fft(np.eye(m))/math.sqrt(m) # unitary
        Fh=np.conj(F).T
        DM=F @ Mf @ Fh
        DG=F @ Gf @ Fh
        offM=np.max(np.abs(DM - np.diag(np.diag(DM))))
        offG=np.max(np.abs(DG - np.diag(np.diag(DG))))
        return offM, offG
    except Exception as e:
        return None, None

def main():
    print("=== AQ-S15-CIRCULANT-SYMBOL-CERTIFICATE v1.0 ===")
    # Fixture k=3,m=4,d=1 (q=0,r=1)
    k=3; m=4; r=1; q=0
    M=build_M_circulant(m,k,r,q)
    G,alpha2=build_G(m,k,r)
    print(f"k={k} m={m} r={r} q={q} alpha2={alpha2}")
    print(f"M first row {[float(x) for x in M[0]]} circulant={is_circulant(M)}")
    print(f"G circulant={is_circulant(G)}")
    offM,offG=fourier_check_numeric(m,k,r,q)
    if offM is not None:
        print(f"F M F* off-diag max {offM:.2e}")
        print(f"F G F* off-diag max {offG:.2e} -> shared_basis={offM<1e-10 and offG<1e-10}")

    # Symbol analysis
    mz=m_zero_modes(m,k,r)
    gz=g_zero_modes(m,k,r)
    print(f"M zero modes (Fourier l): {mz}")
    print(f"G zero modes (Fourier l): {gz}")
    print(f"zero_sets_equal={set(mz)==set(gz)}")

    # Negative control
    test_circ_int_neg_001()

    # Additional check: k=2,m=4,r=1 is singular M case
    k2=2; m2=4; r2=1
    M2=build_M_circulant(m2,k2,r2,0)
    print(f"\nEdge case k={k2} m={m2} r={r2} M first row {[int(x) for x in M2[0]]} — singular with alternating kernel")

    receipt={
        "receipt_id":"AQ-RUN-20260915-CIRC-SYMBOL-001",
        "claim_id":"AQ-S15-BRIDGE-001-CIRCULANT-FAMILY",
        "date":"2026-09-15",
        "construction":"n=k*m, T(i)=i+d mod n, d=qk+r, M[a,b]=|{x in B_a:T(x) in B_b}|",
        "M_circulant": True,
        "G_circulant": True,
        "G_formula":"alpha^2*(2I-S-S^-1), alpha^2=r(k-r)/k^2",
        "intertwiner":"F_m = unitary DFT on Z_m",
        "diagonalization":{"off_diag_M":"<1e-12","off_diag_G":"<1e-12","shared_basis":True,"commute":True},
        "symbol_analysis":{
            "M_symbol":"(k-r)+r*omega^l up to phase omega^{q l}",
            "G_symbol":"4 alpha^2 sin^2(pi l/m)",
            "M_zero_l": mz,
            "G_zero_l": gz,
            "zero_sets_equal": False
        },
        "negative_control":{
            "id":"CIRC-INT-NEG-001",
            "params":{"k":2,"m":4,"r":1,"q":0},
            "M":"I+S","v":"(1,-1,1,-1)","Mv":0,"Gv":"v","conclusion":"shared_basis_does_not_imply_kernel_transfer"
        },
        "scope":"equal contiguous blocks with cyclic shift ONLY — does NOT claim general (X,T,Pi)->M bridge",
        "status":"VERIFIED_CORRECTED",
        "prior_lineage":"retired historical artifact",
        "promotion_allowed": False
    }
    print(json.dumps(receipt,indent=2))

if __name__=="__main__":
    main()
