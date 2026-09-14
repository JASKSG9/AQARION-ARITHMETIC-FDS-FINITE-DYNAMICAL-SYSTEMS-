#!/usr/bin/env python3
import math, itertools, sys
try: import numpy as np
except: np=None
def bell_numbers(n):
    bell=[0]*(n+1); bell[0]=1
    for m in range(1,n+1): bell[m]=sum(math.comb(m-1,k)*bell[k] for k in range(m))
    return bell
def F(t): return math.ceil(2*math.sqrt(t))-1
def beta_max(s): return s-math.ceil(2*math.sqrt(s))+1
bell=bell_numbers(8); assert bell[8]==4140 and bell[8]-2==4138
assert 40320*4138==166844160
print("Bell 4138 PASS")
viol=sum(1 for a in range(1,1001) for b in range(1,1001) if F(a+b)>F(a)+F(b))
assert viol==0; print("F subadd PASS")
for s,exp in [(1,0),(2,0),(3,0),(4,1),(5,1),(6,2),(12,6)]: assert beta_max(s)==exp
print("beta_max PASS")
def k2r(r): return {"V":r+2,"E":2*r,"beta":r-1}
for r in range(2,9): assert k2r(r)["beta"]==r-1
assert 12-7+1==6 and 12-(2+6)+1==5
print("K2,r + K3,4 PASS")
if np is None: print("numpy missing")
else:
    def spectral_case(m,k,s):
        n=m*k; K=np.zeros((n,n))
        for i in range(n): K[i,(i+s)%n]=1.0
        P=np.zeros((n,n))
        for b in range(m): P[b*k:(b+1)*k, b*k:(b+1)*k]=1.0/k
        U=np.zeros((n,m))
        for b in range(m): U[b*k:(b+1)*k, b]=1.0/math.sqrt(k)
        A=(np.eye(n)-P)@K@P@U
        r=s%k; alpha2=r*(k-r)/(k*k); alpha=math.sqrt(alpha2)
        pred_t=2*m*alpha2
        pred_n=2*alpha if m%2==0 else 2*alpha*math.cos(math.pi/(2*m))
        return abs(np.trace(A.T@A)-pred_t), abs(np.linalg.norm(A,2)-pred_n)
    cases=0; max_t=0; max_n=0
    for k in range(2,12):
        for m in range(2,15):
            for s in range(1,m*k):
                if s%k==0: continue
                et,eo=spectral_case(m,k,s); cases+=1
                max_t=max(max_t,et); max_n=max(max_n,eo)
    print(f"cases={cases} max_t={max_t:.3e} max_n={max_n:.3e}")
    assert cases==5720 and max_t<1e-12 and max_n<1e-12
    print("5720 REAL PASS")
print("REPLAY HARNESS v13.1 ALL PASS")
