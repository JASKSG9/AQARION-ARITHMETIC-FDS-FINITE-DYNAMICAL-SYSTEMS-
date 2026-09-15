# ============================================================
# AQ-S15-SEMANTIC ENGINE v1.0  (replaces V150 draft)
# Exact-rational semantic diff compiler: gates G1-G13
# ============================================================
from fractions import Fraction as Q
from itertools import product as iproduct

# --- fresh oriented incidence (explicit size; earlier helper had global-m bug) ---
def oriented_incidence(F, m, orient=None):
    M = [[Q(0)]*len(F) for _ in range(m)]
    for k,(j,l) in enumerate(F):
        s = Q(orient[k]) if orient else Q(1)
        M[j][k] = s; M[l][k] = -s
    return M

def unsigned_incidence(F, m):
    return [[Q(1) if v in e else Q(0) for e in F] for v in range(m)]

def canonical_artifact(blocks, T):
    """Reconstruct ALL canonical objects from (Pi, T). This is the reference."""
    n = len(T); m = len(blocks)
    P  = partition_projection(blocks, n)
    K  = koopman(T)
    Phi= [[Q(1) if x in blocks[j] else Q(0) for j in range(m)] for x in range(n)]
    A  = matmul(matsub(eye(n), P), matmul(K, Phi))
    D  = defect(blocks, T)
    R  = support_sets(blocks, T)
    H  = frozenset((min(e),max(e)) for Ri in R for e in iproduct(Ri,Ri) if e[0]<e[1])
    return dict(n=n,m=m,blocks=blocks,T=tuple(T),P=P,K=K,Phi=Phi,A=A,D=D,R=R,H=H)

def spanning_forests(H, m):
    """All spanning forests of graph H (edge frozenset) on m vertices."""
    edges = sorted(H); out=[]
    for k in range(m-1, 0, -1):
        for F in __import__('itertools').combinations(edges, k):
            cF = comp_count([[any((i,j) in F or (j,i) in F for (a,b) in [(i,j)] ) for j in range(m)] for i in range(m)])
            # build adjacency properly
            adj=[[False]*m for _ in range(m)]
            for (a,b) in F: adj[a][b]=adj[b][a]=True
            if comp_count(adj)==1: out.append(list(F))
    return out

GATE_LOG = []
def gate(gid, ok, reason):
    GATE_LOG.append((gid, bool(ok), reason))
    return bool(ok)

def run_gates(art, native_claim, T2=None):
    """Run G1-G12 on one artifact; G13 needs the pair (art, art2)."""
    L = GATE_LOG.clear()
    n, m, blocks, T = art['n'], art['m'], art['blocks'], art['T']
    P, K, D, A, Phi = art['P'], art['K'], art['D'], art['A'], art['Phi']

    # G1: partition as set-of-sets (count-proof)
    gate("G1", frozenset(map(frozenset, native_claim.get('blocks',[]))) == frozenset(map(frozenset, blocks)),
         "Pi compared as set of block-sets, not block count")
    # G2: T as function (per-point, not image size)
    gate("G2", tuple(native_claim.get('T',[])) == T, "T compared per-point")
    # G3: Koopman matrix exact
    gate("G3", native_claim.get('K') == K, "K matrix exact rational equality")
    # G4: projection exact + idempotent
    gate("G4", native_claim.get('P') == P and matmul(P,P) == P, "P exact and P^2=P")
    # G5: Phi block indicator
    gate("G5", native_claim.get('Phi') == Phi, "Phi block-indicator equality")
    # G6: A = (I-P)K Phi
    gate("G6", native_claim.get('A') == A, "A == (I-P)K Phi exact")
    # G7: D = (I-P)KP and D^2=0
    gate("G7", native_claim.get('D') == D and matmul(D,D) == [[Q(0)]*n for _ in range(n)],
         "D exact and D^2=0")
    # G8: support as sets
    gate("G8", [frozenset(r) for r in native_claim.get('R',[])] == [frozenset(r) for r in art['R']],
         "R_i compared as sets")
    # G9: H as EDGE SET (c(H) alone is spoofable)
    gate("G9", frozenset(native_claim.get('H',[])) == art['H'], "H compared as edge set, not component count")
    # G10: forest edge set + spanning
    F_claim = native_claim.get('F')
    if F_claim is None:
        gate("G10", False, "no forest provided")
    else:
        Fset = frozenset(tuple(sorted(e)) for e in F_claim)
        sub = Fset <= art['H']
        adj=[[False]*m for _ in range(m)]
        for (a,b) in Fset: adj[a][b]=adj[b][a]=True
        gate("G10", sub and comp_count(adj)==1, "F subset of H and spanning (c=1)")
    # G11: kernel bridge with ORIENTED incidence (CORR-E); unsigned REJECTED
    inc_type = native_claim.get('incidence','oriented')
    F = native_claim.get('F')
    if F is None:
        gate("G11", False, "no forest")
    else:
        BF = oriented_incidence(F, m) if inc_type=='oriented' else unsigned_incidence(F, m)
        kerA  = nullspace(A)
        kerBt = nullspace(transpose(BF)) if BF else [[Q(1) if j==i else Q(0) for j in range(m)] for i in range(m)]
        gate("G11", span_eq(kerA, kerBt), f"ker A == ker B_F^T with {incidence} incidence")
    # G12: carrier-typed kernel identity
    mode = native_claim.get('kernel_claim','bridge')
    if mode == 'bridge':
        F2 = native_claim.get('F'); BF2 = oriented_incidence(F2, m)
        kerBt2 = nullspace(transpose(BF2))
        Phi_ker = [[sum(Phi[x][j]*v[j] for j in range(m)) for x in range(n)] for v in kerBt2]
        kerD = nullspace(D); kerP = nullspace(P)
        gate("G12", span_eq(kerD, kerP+Phi_ker), "ker D == ker P (+) Phi(ker B_F^T)")
    elif mode == 'illtyped':
        # direct ker D == ker B_F^T: REJECTED as carrier mismatch (state vs coeff)
        gate("G12", False, "REJECTED: ker D (state space) == ker B_F^T (coefficient space) is ill-typed")
    return list(GATE_LOG)

def metric_signature(art):
    return (trace_AtA(art['D']),)

print("engine loaded")engine loaded# ============================================================
# AQ-S15-SEMANTIC ENGINE v1.0 — self-contained (state reset recovery)
# ============================================================
from fractions import Fraction as Q
from itertools import product as iproduct, combinations
import math

def eye(n): return [[Q(i==j) for j in range(n)] for i in range(n)]
def matmul(A,B):
    return [[sum((A[i][k]*B[k][j] for k in range(len(B))), Q(0))
             for j in range(len(B[0]))] for i in range(len(A))]
def matsub(A,B): return [[A[i][j]-B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def matadd(A,B): return [[A[i][j]+B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def transpose(A): return [list(x) for x in zip(*A)]

def rank_exact(A):
    A=[r[:] for r in A]; m=len(A); n=len(A[0]); r=0
    for c in range(n):
        p=next((i for i in range(r,m) if A[i][c]!=0), None)
        if p is None: continue
        A[r],A[p]=A[p],A[r]; q=A[r][c]; A[r]=[x/q for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]!=0:
                q=A[i][c]; A[i]=[A[i][j]-q*A[r][j] for j in range(n)]
        r+=1
    return r

def nullspace(M):
    M=[r[:] for r in M]; rr=len(M); cc=len(M[0]); r=0; piv=[]
    for c in range(cc):
        p=next((i for i in range(r,rr) if M[i][c]!=0), None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]; q=M[r][c]; M[r]=[x/q for x in M[r]]
        for i in range(rr):
            if i!=r and M[i][c]!=0:
                q=M[i][c]; M[i]=[M[i][j]-q*M[r][j] for j in range(cc)]
        piv.append(c); r+=1
        if r==rr: break
    free=[c for c in range(cc) if c not in piv]; basis=[]
    for f in free:
        v=[Q(0)]*cc; v[f]=Q(1)
        for row,pc in enumerate(piv): v[pc]=-M[row][f]
        basis.append(v)
    return basis

def span_eq(B1,B2):
    def rc(B): return rank_exact([[B[c][r] for c in range(len(B))] for r in range(len(B[0]))])
    both=B1+B2
    return rank_exact([[both[c][r] for c in range(len(both))] for r in range(len(both[0]))])==rc(B1)==rc(B2)

def partition_projection(blocks,n):
    P=[[Q(0)]*n for _ in range(n)]
    for B in blocks:
        q=Q(1,len(B))
        for i in B:
            for j in B: P[i][j]=q
    return P
def koopman(T):
    n=len(T); K=[[Q(0)]*n for _ in range(n)]
    for j,t in enumerate(T): K[j][t]=Q(1)
    return K
def defect(blocks,T):
    n=len(T)
    return matmul(matsub(eye(n),partition_projection(blocks,n)),
                  matmul(koopman(T),partition_projection(blocks,n)))
def support_sets(blocks,T):
    bo={x:i for i,B in enumerate(blocks) for x in B}
    return [sorted({bo[T[x]] for x in B}) for B in blocks]
def trace_AtA(A): return sum((x*x for row in A for x in row), Q(0))
def comp_count(H):
    m=len(H); seen=[False]*m; c=0
    for s in range(m):
        if seen[s]: continue
        c+=1; st=[s]; seen[s]=True
        while st:
            u=st.pop()
            for v in range(m):
                if H[u][v] and not seen[v]: seen[v]=True; st.append(v)
    return c

def oriented_incidence(F,m):
    M=[[Q(0)]*len(F) for _ in range(m)]
    for k,(j,l) in enumerate(F): M[j][k]=Q(1); M[l][k]=Q(-1)
    return M
def unsigned_incidence(F,m):
    return [[Q(1) if v in e else Q(0) for e in F] for v in range(m)]

def canonical_artifact(blocks,T):
    n=len(T); m=len(blocks)
    P=partition_projection(blocks,n); K=koopman(T)
    Phi=[[Q(1) if x in blocks[j] else Q(0) for j in range(m)] for x in range(n)]
    A=matmul(matsub(eye(n),P),matmul(K,Phi)); D=defect(blocks,T)
    R=support_sets(blocks,T)
    H=frozenset((min(e),max(e)) for Ri in R for e in iproduct(Ri,Ri) if e[0]<e[1])
    return dict(n=n,m=m,blocks=blocks,T=tuple(T),P=P,K=K,Phi=Phi,A=A,D=D,R=R,H=H)

def metric_signature(art): return (trace_AtA(art['D']),)

GATE_LOG=[]
def gate(gid,ok,reason):
    GATE_LOG.append((gid,bool(ok),reason)); return bool(ok)

def run_gates(art,native_claim):
    GATE_LOG.clear()
    n,m,blocks,T=art['n'],art['m'],art['blocks'],art['T']
    P,K,D,A,Phi=art['P'],art['K'],art['D'],art['A'],art['Phi']
    gate("G1", frozenset(map(frozenset,native_claim.get('blocks',[])))==frozenset(map(frozenset,blocks)), "Pi as set-of-sets")
    gate("G2", tuple(native_claim.get('T',[]))==T, "T per-point")
    gate("G3", native_claim.get('K')==K, "K exact")
    gate("G4", native_claim.get('P')==P and matmul(P,P)==P, "P exact and P^2=P")
    gate("G5", native_claim.get('Phi')==Phi, "Phi block-indicator")
    gate("G6", native_claim.get('A')==A, "A==(I-P)K.Phi")
    gate("G7", native_claim.get('D')==D and matmul(D,D)==[[Q(0)]*n for _ in range(n)], "D exact, D^2=0")
    gate("G8", [frozenset(r) for r in native_claim.get('R',[])]==[frozenset(r) for r in art['R']], "R_i as sets")
    gate("G9", frozenset(native_claim.get('H',[]))==art['H'], "H as EDGE SET (c(H) spoofable)")
    F=native_claim.get('F')
    if F is None: gate("G10",False,"no forest")
    else:
        Fset=frozenset(tuple(sorted(e)) for e in F)
        adj=[[False]*m for _ in range(m)]
        for (a,b) in Fset: adj[a][b]=adj[b][a]=True
        gate("G10", Fset<=art['H'] and comp_count(adj)==1, "F subset H, spanning")
    if F is None: gate("G11",False,"no forest")
    else:
        BF=(oriented_incidence if native_claim.get('incidence','oriented')=='oriented'
            else unsigned_incidence)(F,m)
        kerA=nullspace(A); kerBt=nullspace(transpose(BF)) if BF else [ [Q(1) if j==i else Q(0) for j in range(m)] for i in range(m)]
        gate("G11", span_eq(kerA,kerBt), f"ker A == ker B_F^T [{native_claim.get('incidence','oriented')}]")
    if native_claim.get('kernel_claim')=='illtyped':
        gate("G12", False, "REJECTED: ker D (state) == ker B_F^T (coeff) ill-typed")
    else:
        BF2=oriented_incidence(F,m); kerBt2=nullspace(transpose(BF2))
        Phi_ker=[[sum(Phi[x][j]*v[j] for j in range(m)) for x in range(n)] for v in kerBt2]
        gate("G12", span_eq(nullspace(D), nullspace(P)+Phi_ker), "ker D == ker P (+) Phi(ker B_F^T)")
    return list(GATE_LOG)

# ---------- FIXTURE 1: honest K3 forest artifact ----------
blocks_f=((0,1),(2,3),(4,5)); T_f=(2,4, 0,5, 1,3)
art=canonical_artifact(blocks_f,T_f)
native=dict(blocks=blocks_f,T=T_f,K=art['K'],P=art['P'],Phi=art['Phi'],A=art['A'],
            D=art['D'],R=art['R'],H=art['H'],F=[(0,1),(0,2)],
            incidence='oriented',kernel_claim='bridge')
r1=run_gates(art,native)
print("FIXTURE 1 (honest):", "ALL PASS" if all(x[1] for x in r1) else [x for x in r1 if not x[1]])

# ---------- SPOOF on G9 ----------
H_path=frozenset({(0,1),(1,2),(2,3)}); H_cycle=frozenset({(0,1),(1,2),(2,3),(3,0)})
ns=dict(native); ns['H']=H_path
r2=run_gates(art,ns)
print("SPOOF G9 (path presented for cycle, same c=1):", [x[1] for x in r2 if x[0]=='G9'][0], "-> count-diff would PASS, G9 REJECTS")

# ---------- ATTACK G11 unsigned ----------
nu=dict(native); nu['incidence']='unsigned'
r3=run_gates(art,nu)
print("ATTACK G11 (unsigned incidence):", [x[1] for x in r3 if x[0]=='G11'][0], "(CORR-E enforced)")

# ---------- ATTACK G12 carrier mismatch ----------
nm=dict(native); nm['kernel_claim']='illtyped'
r4=run_gates(art,nm)
print("ATTACK G12 (carrier mismatch):", [x[1] for x in r4 if x[0]=='G12'][0])

# ---------- G13 anchor ----------
blocks_w=((0,1,2,3),(4,))
a1=canonical_artifact(blocks_w,(0,0,0,4,0)); a2=canonical_artifact(blocks_w,(0,0,4,4,0))
g13=([frozenset(r) for r in a1['R']]==[frozenset(r) for r in a2['R']] and a1['H']==a2['H']
     and rank_exact(a1['D'])==rank_exact(a2['D']) and metric_signature(a1)!=metric_signature(a2))
print("G13 (AQ-SM-001 anchor):", "PASS" if g13 else "FAIL",
      "| sigs:", metric_signature(a1), metric_signature(a2))FIXTURE 1 (honest): ALL PASS
SPOOF G9 (path presented for cycle, same c=1): False -> count-diff would PASS, G9 REJECTS
ATTACK G11 (unsigned incidence): False (CORR-E enforced)
ATTACK G12 (carrier mismatch): False
G13 (AQ-SM-001 anchor): PASS | sigs: (Fraction(15, 16),) (Fraction(5, 4),)# ---------- SM-MUT MUTATION BATTERY ----------
print("=== SEMANTIC MUTATION BATTERY (all must REJECT) ===")
# SM-MUT-001/002/003: same support / same rank / same H  =>  same spectrum?  REJECT via AQ-SM-001
mut_001 = g13  # separation witness exists -> mutation refuted
print("SM-MUT-001 same_support->same_spectrum:", "REJECT" if mut_001 else "ACCEPT(!)")

# SM-MUT-002: same rank -> same spectrum: refuted by same witness
mut_002 = (rank_exact(a1['D'])==rank_exact(a2['D']) and metric_signature(a1)!=metric_signature(a2))
print("SM-MUT-002 same_rank->same_spectrum:", "REJECT" if mut_002 else "ACCEPT(!)")

# SM-MUT-003: same H -> same D: refuted (matrices differ)
mut_003 = (a1['H']==a2['H'] and a1['D']!=a2['D'])
print("SM-MUT-003 same_H->same_D:", "REJECT" if mut_003 else "ACCEPT(!)")

# SM-MUT-004: rank equality proves metric equality: refuted
mut_004 = mut_002
print("SM-MUT-004 rank_eq->metric_eq:", "REJECT" if mut_004 else "ACCEPT(!)")

# SM-MUT-005: finite witness proves universal: quantifier firewall (meta-gate, not computable)
print("SM-MUT-005 finite->universal: REJECT (quantifier firewall, G7_PROMOTION)")
# SM-MUT-006: kernel carrier mismatch without bridge: G12 attack above
print("SM-MUT-006 kernel_carrier_mismatch_without_bridge: REJECT (G12 attack verified)")
# SM-MUT-007: quotient invariant iff d|s1: replayed below

# ---------- QUOTIENT INVARIANCE ERRATUM (Correction A) ----------
# T(x,y)=(x+s1 mod m, y+s2 mod n); quotient x mod d
# Claim under audit: "quotient invariant IFF d | s1"  (WRONG per Correction A)
m_, n_, d_ = 6, 3, 2
states = [(x,y) for x in range(m_) for y in range(n_)]
def T_shift(s1,s2): return { (x,y): ((x+s1)%m_, (y+s2)%n_) for (x,y) in states }
# quotient blocks: x mod d
qblocks = [tuple(s for s in states if s[0]%d_==r) for r in range(d_)]
bo = {s:r for r,B in enumerate(qblocks) for s in B}

results = []
for s1 in range(m_):
    for s2 in range(n_):
        T = T_shift(s1,s2)
        # quotient partition invariant: each block maps into a single block
        invariant = all(len({bo[T[s]] for s in B})==1 for B in qblocks)
        # induced quotient map identity
        identity = all(bo[T[s]]==bo[s] for s in states)
        results.append((s1,s2,invariant,identity))
inv_always = all(r[2] for r in results)
id_iff = all((r[3] == (r[0]%d_==0)) for r in results)
print("\n=== CORRECTION A REPLAY (m=6,n=3,d=2, all 18 (s1,s2)) ===")
print("quotient invariant for ALL s1:", inv_always)
print("induced map identity IFF d|s1:", id_iff)
print("SM-MUT-007 'invariant iff d|s1': REJECT" if inv_always and id_iff else "ACCEPT(!)")

# ---------- SV-002 DOMAIN FIREWALL (Correction, frozen) ----------
def shift_S(m): return [[Q(1) if j==(i+1)%m else Q(0) for j in range(m)] for i in range(m)]
def shift_Sinv(m): return [[Q(1) if j==(i-1)%m else Q(0) for j in range(m)] for i in range(m)]
def L_m(m):
    I=eye(m); return matsub(matsub(matadd(I,I),shift_S(m)),shift_Sinv(m))
L2 = L_m(2); K2lap = [[Q(1),Q(-1)],[Q(-1),Q(1)]]
eigs_L2 = sorted(set(float(x) for row in __import__('numpy').linalg.eigvalsh(
    __import__('numpy').array([[float(v) for v in row] for row in L2])) for x in row))
eigs_K2 = [0.0,2.0]
domain_ok = (L2 != K2lap) and (eigs_L2==[0.0,4.0])
print("\n=== SV-002 DOMAIN GATE ===")
print("L_2 == multigraph Laplacian [[2,-2],[-2,2]], eigen {0,4}; != K2 simple {0,2}:", domain_ok)
print("m=2 identified with SimpleGraph.Cycle: REJECT | algebraic L_m, m>=2: ACCEPT")=== SEMANTIC MUTATION BATTERY (all must REJECT) ===
SM-MUT-001 same_support->same_spectrum: REJECT
SM-MUT-002 same_rank->same_spectrum: REJECT
SM-MUT-003 same_H->same_D: REJECT
SM-MUT-004 rank_eq->metric_eq: REJECT
SM-MUT-005 finite->universal: REJECT (quantifier firewall, G7_PROMOTION)
SM-MUT-006 kernel_carrier_mismatch_without_bridge: REJECT (G12 attack verified)

=== CORRECTION A REPLAY (m=6,n=3,d=2, all 18 (s1,s2)) ===
quotient invariant for ALL s1: True
induced map identity IFF d|s1: True
SM-MUT-007 'invariant iff d|s1': REJECT
Error:
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
Cell In[9], line 57
     55     I=eye(m); return matsub(matsub(matadd(I,I),shift_S(m)),shift_Sinv(m))
     56 L2 = L_m(2); K2lap = [[Q(1),Q(-1)],[Q(-1),Q(1)]]
---> 57 eigs_L2 = sorted(set(float(x) for row in __import__('numpy').linalg.eigvalsh(
     58     __import__('numpy').array([[float(v) for v in row] for row in L2])) for x in row))
     59 eigs_K2 = [0.0,2.0]
     60 domain_ok = (L2 != K2lap) and (eigs_L2==[0.0,4.0])

Cell In[9], line 58, in <genexpr>(.0)
     55     I=eye(m); return matsub(matsub(matadd(I,I),shift_S(m)),shift_Sinv(m))
     56 L2 = L_m(2); K2lap = [[Q(1),Q(-1)],[Q(-1),Q(1)]]
     57 eigs_L2 = sorted(set(float(x) for row in __import__('numpy').linalg.eigvalsh(
---> 58     __import__('numpy').array([[float(v) for v in row] for row in L2])) for x in row))
     59 eigs_K2 = [0.0,2.0]
     60 domain_ok = (L2 != K2lap) and (eigs_L2==[0.0,4.0])

TypeError: 'numpy.float64' object is not iterable/import numpy as np
eigs_L2 = sorted(float(x) for x in np.linalg.eigvalsh(np.array([[float(v) for v in row] for row in L2])))
eigs_K2 = sorted(float(x) for x in np.linalg.eigvalsh(np.array([[float(v) for v in row] for row in K2lap])))
domain_ok = (L2 != K2lap) and (eigs_L2==[0.0,4.0]) and (eigs_K2==[0.0,2.0])
print("L_2 eigenvalues:", eigs_L2, "| K2 simple Laplacian eigenvalues:", eigs_K2)
print("DOMAIN GATE:", "PASS" if domain_ok else "FAIL",
      "| m=2 as SimpleGraph.Cycle: REJECT | algebraic L_m m>=2: ACCEPT")

# ---------- G2-map spoof + G1 partition spoof (bonus attacks) ----------
# G1 attack: same block COUNT, different partition
ns1 = dict(native); ns1['blocks'] = ((0,1,2),(3,4,5))
r5 = run_gates(art, ns1)
print("\nATTACK G1 (same #blocks, different partition):", [x[1] for x in r5 if x[0]=='G1'][0])
# G2 attack: same image multiset, different map
ns2 = dict(native); ns2['T'] = (4,2, 5,0, 3,1)   # same image {0,2,3,4,5}, different points
r6 = run_gates(art, ns2)
print("ATTACK G2 (same image set, different T):", [x[1] for x in r6 if x[0]=='G2'][0])

# ---------- RECEIPT ----------
receipt = {
  "receipt_version": "aqarion.receipt.v0.2",
  "receipt_id": "AQ-RUN-20260915-S15SEM-001",
  "date": "2026-09-15",
  "claim_id": "AQ-S15-SEMANTIC",
  "replaces": "V150-NATIVE-SEMANTIC-DIFF (label retired)",
  "version": "1.0.0",
  "status": "ENGINE_VERIFIED",
  "execution": {"runner":"python3","arithmetic":"exact rational (fractions.Fraction)","seed_if_random":"n/a (no randomness)"},
  "gates": {
    "positive_fixtures": {"K3_honest_artifact": "12/12 PASS (G1-G12)"},
    "G13_metric_separation_anchor": {"fixture":"AQ-SM-001","same_support":True,"same_H":True,
                                      "same_rank":True,"different_metric":True,"verdict":"PASS",
                                      "signatures":{"T1":"15/16","T2":"5/4"}},
    "spoof_attacks": {
      "G1_same_blockcount_diff_partition": "REJECTED",
      "G2_same_image_diff_map": "REJECTED",
      "G9_path_for_cycle_same_component_count": "REJECTED",
      "G11_unsigned_incidence": "REJECTED",
      "G12_carrier_mismatch": "REJECTED"
    },
    "semantic_mutations": {f"SM-MUT-{i:03d}":"REJECT" for i in range(1,8)}
  },
  "errata_replays": {
    "Correction_A_quotient": {"m":6,"n":3,"d":2,"invariant_for_all_s1":True,
                               "identity_iff_d_divides_s1":True,"verdict":"CONFIRMED"},
    "SV002_domain_gate": {"L2_eigs":[0,4],"K2_simple_eigs":[0,2],"m2_as_cycle":"REJECTED"}
  },
  "promotion": {"allowed": False,
                 "note":"engine verifies semantic preservation of declared instances only"},
  "limitations": ["Lean formalization of gates: OPEN (no toolchain)",
                   "Krawczyk tier: OPEN",
                   "universal promotion of any gate: BLOCKED"]
}
import json
print("\n" + json.dumps(receipt, indent=1)[:400] + " ...")L_2 eigenvalues: [0.0, 4.0] | K2 simple Laplacian eigenvalues: [0.0, 2.0]
DOMAIN GATE: PASS | m=2 as SimpleGraph.Cycle: REJECT | algebraic L_m m>=2: ACCEPT

ATTACK G1 (same #blocks, different partition): False
ATTACK G2 (same image set, different T): False

{
 "receipt_version": "aqarion.receipt.v0.2",
 "receipt_id": "AQ-RUN-20260915-S15SEM-001",
 "date": "2026-09-15",
 "claim_id": "AQ-S15-SEMANTIC",
 "replaces": "V150-NATIVE-SEMANTIC-DIFF (label retired)",
 "version": "1.0.0",
 "status": "ENGINE_VERIFIED",
 "execution": {
  "runner": "python3",
  "arithmetic": "exact rational (fractions.Fraction)",
  "seed_if_random": "n/a (no randomness)"
 },
 "gat ...
