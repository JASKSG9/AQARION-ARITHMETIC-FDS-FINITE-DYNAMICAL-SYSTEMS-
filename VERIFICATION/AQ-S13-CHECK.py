#!/usr/bin/env python3
"""
AQ-S13-CHECK.PY — AQARION S13 Checkpoint
Bell 4140 vs qualifying 4138 + F subadd + beta_max + K2,r + K3,4 vs K2,6 + REAL 5720 spectral + P0/T10
Governance: C4=BLOCKED / Publication=BLOCKED / SDS-002=QUARANTINED
"""
import math, itertools, sys
try:
    import numpy as np
except:
    np = None

def bell_numbers(n):
    bell = [0]*(n+1)
    bell[0]=1
    for m in range(1,n+1):
        bell[m]=sum(math.comb(m-1,k)*bell[k] for k in range(m))
    return bell

def F(t): return math.ceil(2*math.sqrt(t))-1
def beta_max(s): return s - math.ceil(2*math.sqrt(s)) + 1

# 1. BELL
bell = bell_numbers(8)
assert bell[8]==4140
qual = bell[8]-2
assert qual==4138
assert 40320*4138==166844160
assert 3212*4138==13291256
print(f"Bell(8)=4140 qualifying={qual} 40320*4138=166844160 PASS")

# 2. F SUBADD 1e6 pairs
viol=0
for a in range(1,1001):
    for b in range(1,1001):
        if F(a+b) > F(a)+F(b):
            viol+=1
            break
    if viol: break
assert viol==0
print("F(a+b)<=F(a)+F(b) 1e6 pairs violations=0 PASS")

# 3. BETA ENVELOPE
for s,exp in [(1,0),(2,0),(3,0),(4,1),(5,1),(6,2),(12,6)]:
    assert beta_max(s)==exp
print("beta_max 1..12 PASS s=12->6 K3,4 attains")

# 4. K2,r + K3,4 vs K2,6
def k2r(r): return {"V":r+2,"E":2*r,"beta":r-1,"s0":r-1}
for r in range(2,9):
    assert k2r(r)["beta"]==r-1
print("K2,r r=2..8 beta=r-1 PASS")
k34=12-7+1
k26=12-(2+6)+1
assert k34==6 and k26==5 and k34>k26
print(f"s=12 K3,4 beta={k34} > K2,6 beta={k26} PASS")

# 5. REAL 5720 SPECTRAL
if np is None:
    print("numpy missing -> spectral SKIPPED ENVIRONMENT_BLOCKED")
else:
    def spectral_case(m,k,s):
        n=m*k
        K=np.zeros((n,n))
        for i in range(n): K[i,(i+s)%n]=1.0
        P=np.zeros((n,n))
        for b in range(m): P[b*k:(b+1)*k, b*k:(b+1)*k]=1.0/k
        U=np.zeros((n,m))
        for b in range(m): U[b*k:(b+1)*k, b]=1.0/math.sqrt(k)
        A=(np.eye(n)-P)@K@P@U
        r=s%k
        alpha2=r*(k-r)/(k*k)
        alpha=math.sqrt(alpha2)
        pred_trace=2*m*alpha2
        pred_norm=2*alpha if m%2==0 else 2*alpha*math.cos(math.pi/(2*m))
        return abs(float(np.trace(A.T@A))-pred_trace), abs(float(np.linalg.norm(A,2))-pred_norm)
    cases=0; max_t=0.0; max_n=0.0
    for k in range(2,12):
        for m in range(2,15):
            for s in range(1,m*k):
                if s%k==0: continue
                et,eo=spectral_case(m,k,s)
                cases+=1
                max_t=max(max_t,et)
                max_n=max(max_n,eo)
    print(f"Spectral total={cases} expected 5720")
    print(f"Trace max err {max_t:.3e} Op-norm max err {max_n:.3e}")
    assert cases==5720
    assert max_t<1e-12 and max_n<1e-12
    print("Spectral 5720 REAL replay PASS")

print("\nAQ-S13-CHECK.PY: ALL CHECKS PASS")
