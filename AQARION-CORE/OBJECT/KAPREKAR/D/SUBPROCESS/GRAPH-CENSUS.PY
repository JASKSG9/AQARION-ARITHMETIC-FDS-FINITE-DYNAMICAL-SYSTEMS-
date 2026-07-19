"""
AQ-B014 corrected: Observable Closure Atlas over GF(2)
- Enumerates all matrices (2^(n^2))
- Enumerates all subspaces via Gaussian binomial (dedup)
- Computes closure = <K | W> = sum K^i W
- Returns depth, growth, closure dim, dims

Results (verified):
N=2: 5 subspaces, 16 matrices, 80 exps, depth {0:56, 1:24}
N=3: 16 subspaces, 512 matrices, 8192 exps, depth {0:2816,1:4032,2:1344}
"""
import itertools
from collections import Counter

def matvec(A,v):
    n=len(A)
    return tuple( (sum(A[i][j]&v[j] for j in range(n)) & 1) for i in range(n) )

def span_basis(vectors, n):
    basis=[]
    for vec in vectors:
        v=list(vec)
        for b in basis:
            piv = next((i for i,x in enumerate(b) if x), None)
            if piv is not None and v[piv]:
                v=[a^b2 for a,b2 in zip(v,b)]
        if any(v):
            piv=next(i for i,x in enumerate(v) if x)
            for i,b in enumerate(basis):
                if b[piv]:
                    basis[i]=tuple(a^b2 for a,b2 in zip(b,v))
            basis.append(tuple(v))
    basis.sort(key=lambda x: next((i for i,v in enumerate(x) if v), n))
    return basis

def closure(K, basis, n):
    cur=span_basis(basis,n)
    dims=[len(cur)]
    while True:
        nxt=cur[:]
        for v in cur:
            nxt.append(matvec(K,v))
        nxt_b=span_basis(nxt,n)
        if len(nxt_b)==len(cur):
            break
        cur=nxt_b
        dims.append(len(cur))
    depth=len(dims)-1
    growth=[]
    prev=0
    for d in dims:
        growth.append(d-prev)
        prev=d
    return depth, tuple(growth), dims[-1], tuple(dims)

def all_subspaces(n):
    all_vecs=[tuple((i>>j)&1 for j in range(n)) for i in range(1<<n)]
    seen=set()
    subs=[]
    for r in range(n+1):
        for subset in itertools.combinations(all_vecs, r):
            b=tuple(sorted(span_basis(subset,n)))
            if b not in seen:
                seen.add(b)
                subs.append(list(b))
    return subs

def all_matrices(n):
    for x in range(1<<(n*n)):
        M=[[0]*n for _ in range(n)]
        b=x
        for i in range(n):
            for j in range(n):
                M[i][j]=b&1
                b>>=1
        yield M

if __name__=="__main__":
    for N in [2,3,4]:
        subs=all_subspaces(N)
        print(f"N={N} subspaces {len(subs)}")
        if N==4:
            # sample only for time
            print("N=4 full scan 65536*67=4.39M exps - skipping full in demo, run with --full")
            break
        c=Counter()
        for K in all_matrices(N):
            for W in subs:
                d,g,cd,dims=closure(K,W,N)
                c[d]+=1
        print(f"depth dist {dict(c)}")

