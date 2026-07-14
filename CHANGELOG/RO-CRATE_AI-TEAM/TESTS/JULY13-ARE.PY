
import random, numpy as np
from collections import deque

random.seed(0)

def quotient_graph(T, blocks):
    block_of = {x:i for i,blk in enumerate(blocks) for x in blk}
    m = len(blocks)
    adj = [[False]*m for _ in range(m)]
    for x in T: adj[block_of[x]][block_of[T[x]]] = True
    return adj

def kosaraju_sccs(adj):
    m = len(adj)
    vis=[False]*m; order=[]
    def dfs1(u):
        stk=[(u,False)]
        while stk:
            v,d=stk.pop()
            if d: order.append(v); continue
            if vis[v]: continue
            vis[v]=True; stk.append((v,True))
            for w in range(m):
                if adj[v][w] and not vis[w]: stk.append((w,False))
    for u in range(m):
        if not vis[u]: dfs1(u)
    radj=[[adj[j][i] for j in range(m)] for i in range(m)]
    vis2=[False]*m; sccs=[]
    for u in reversed(order):
        if vis2[u]: continue
        scc=[]; stk=[u]
        while stk:
            v=stk.pop()
            if vis2[v]: continue
            vis2[v]=True; scc.append(v)
            for w in range(m):
                if radj[v][w] and not vis2[w]: stk.append(w)
        sccs.append(scc)
    return sccs

def condensation_and_topo(adj, sccs):
    m=len(adj); scc_of=[0]*m
    for i,s in enumerate(sccs):
        for n in s: scc_of[n]=i
    S=len(sccs)
    cadj=[[False]*S for _ in range(S)]
    for u in range(m):
        for v in range(m):
            if adj[u][v] and scc_of[u]!=scc_of[v]:
                cadj[scc_of[u]][scc_of[v]]=True
    indeg=[sum(cadj[j][i] for j in range(S)) for i in range(S)]
    q=deque(i for i in range(S) if indeg[i]==0); topo=[]
    while q:
        u=q.popleft(); topo.append(u)
        for v in range(S):
            if cadj[u][v]:
                indeg[v]-=1
                if indeg[v]==0: q.append(v)
    return topo, scc_of, cadj

def is_triangularizable(adj):
    """A: all SCCs in quotient graph are singletons (no inter-block cycles)."""
    return all(len(s)==1 for s in kosaraju_sccs(adj))

def filtration_exists(T, blocks, adj):
    """B: cumulative union filtration S_k is T-forward-closed."""
    sccs = kosaraju_sccs(adj)
    if not all(len(s)==1 for s in sccs): return False
    topo, scc_of, _ = condensation_and_topo(adj, sccs)
    rev_topo = list(reversed(topo))
    cumulative = set()
    for scc_idx in rev_topo:
        for blk_idx in sccs[scc_idx]:
            cumulative.update(blocks[blk_idx])
        for x in cumulative:
            if T[x] not in cumulative:
                return False
    return True

def check_block_triangular(T, blocks, adj):
    """C: Koopman matrix is block-lower-triangular under some ordering."""
    sccs = kosaraju_sccs(adj)
    if not all(len(s)==1 for s in sccs): return False
    topo, _, _ = condensation_and_topo(adj, sccs)
    rev_topo = list(reversed(topo))
    block_order = [sccs[i][0] for i in rev_topo]
    ordered = [blocks[b] for b in block_order]
    all_states = [x for blk in ordered for x in blk]
    n = len(all_states); pos = {x:i for i,x in enumerate(all_states)}
    K = np.zeros((n,n))
    for x in T: K[pos[x], pos[T[x]]] = 1.0
    sizes=[len(b) for b in ordered]
    offsets=[0]
    for s in sizes: offsets.append(offsets[-1]+s)
    upper_norm=0.0
    for bi in range(len(ordered)):
        for bj in range(bi+1, len(ordered)):
            block=K[offsets[bi]:offsets[bi+1], offsets[bj]:offsets[bj+1]]
            upper_norm+=np.sum(np.abs(block))
    return upper_norm < 1e-10

# Run tests
fails=0; tested=0
for _ in range(5000):
    n=random.randint(3,12)
    T={i:random.randint(0,n-1) for i in range(n)}
    m=random.randint(2,min(n,5))
    perm=list(range(n)); random.shuffle(perm)
    cuts=sorted(random.sample(range(1,n),m-1))
    cuts=[0]+cuts+[n]
    blocks=[perm[cuts[i]:cuts[i+1]] for i in range(m)]
    blocks=[b for b in blocks if b]
    if len(blocks)<2: continue
    adj=quotient_graph(T,blocks)
    A=is_triangularizable(adj)
    B=filtration_exists(T,blocks,adj)
    C=check_block_triangular(T,blocks,adj)
    tested+=1
    if not(A==B==C):
        fails+=1
        print(f"MISMATCH: T={T} blocks={blocks} A={A} B={B} C={C}")
        if fails>=3: break

print(f"\n=== 5000 RANDOM TESTS ===")
print(f"Tested: {tested}")
print(f"Failures: {fails}")
print(f"Result: {'ALL PASS (A==B==C)' if fails==0 else f'{fails} FAILURES'}")=== 5000 RANDOM TESTS ===
Tested: 5000
Failures: 0
Result: ALL PASS (A==B==C)
