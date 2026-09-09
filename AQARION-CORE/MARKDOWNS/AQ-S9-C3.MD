8AQARION C3 — STRUCTURAL TARGET


Version: S9-C3-STRUCTURAL-TARGET

Date: 2026-09-09

Status: OPEN · NO PROMOTION · C4 BLOCKED · PUBLICATION BLOCKED


1. Primitive target


Let P,Q be the two partitions and let


[
M=P\wedge Q,\qquad U=P\vee Q.
]


For the order-three orbit closure,


[
J_T(P)=P\vee T(P)\vee T^2(P).
]


Assume


[
s(P,Q)=1
]


and


[
m_T


|J_T(M)|


|J_T(P)\wedge J_T(Q)|
=0.
]


The target theorem is


[
\boxed{
s(J_T(P),J_T(Q))\ge1.
}
]


Equivalently, in the incidence interpretation,


[
\boxed{
\beta(G_0)=1,\quad
m_T=0
\Longrightarrow
\beta(G_T)\ge1.
}
]


2. Equivalent contradiction form


The sharp contrapositive target is


[
\boxed{
\beta(G_0)=1,\quad
\beta(G_T)=0
\Longrightarrow
m_T>0.
}
]


This is the preferred structural formulation.


3. Rank-defect formulation


Define


[
r(P)=n-|P|,
\qquad
d_T(P)=r(J_T(P))-r(P).
]


For the current AQARION identities,


[
\Delta_d


d_T(P)+d_T(Q)-d_T(M)-d_T(U)


\Gamma_T-s_0.
]


When m_T=0,


[
\Gamma_T=s_T.
]


Therefore, on the C3 critical locus s_0=1,m_T=0,


[
\boxed{
\Delta_d=s_T-1.
}
]


Hence C3 is equivalent to


[
\boxed{\Delta_d\ge0.}
]


This is a useful computational and mathematical primitive, but global submodularity of d_T is NOT asserted.


4. Join/meet asymmetry


For finite-order T,


[
J_T(P\vee Q)=J_T(P)\vee J_T(Q)
]


holds automatically.


The only relevant closure defect is the meet side:


[
J_T(P\wedge Q)
\le
J_T(P)\wedge J_T(Q).
]


Moreover,


[
m_T=0
\iff
J_T(P\wedge Q)


J_T(P)\wedge J_T(Q).
]


Thus the C3 problem is:




Can a unique incidence cycle be destroyed by the order-three orbit closure while the meet square remains exact?




The conjectured answer is no.


5. Three-sheet representation


The three relevant incidence structures are


[
G(P,Q),
]


[
G(J_T(P),Q),
]


[
G(J_T(P),J_T(Q)).
]


The principal obstruction hypothesis is:


[
\boxed{
\text{cycle destruction}
\Longrightarrow
\text{strict meet defect}
}
]


in the unique-cycle/order-three setting.


This implication is NOT yet proved and must remain a research conjecture.


6. Computational evidence


Independent n=8 replay:




s_0=1: 2,405,613


s_0=1,m_T=0: 198,630


s_T=1: 197,550


s_T=2: 1,080


violations: 0




Independent n=9 replay:




s_0=1: 75,193,461


s_0=1,m_T=0: 7,657,635


\Delta_d<0: 0


\Delta_d=0: 7,454,595


\Delta_d=1: 203,040


direct transport failures: 0




These are computational audits, not a universal theorem.


7. Adversarial boundary


The following claims are NOT currently established:




C3 for arbitrary n


the cycle-destruction \Rightarrow m_T>0 lemma


global submodularity of d_T


a general closure theorem implying C3


Lean formalization of C3


compiler certification


publication readiness




8. Required proof architecture


Preferred sequence:




characterize the unique cycle of G_0;


characterize how J_T identifies incidence classes;


assume \beta(G_T)=0;


identify the first necessary cycle-destroying identification;


prove that identification forces
[
J_T(P\wedge Q)
\subsetneq
J_T(P)\wedge J_T(Q);
]


conclude m_T>0;


contradict m_T=0.




9. Governance


Status:


C3 = OPEN


Lean = OPEN


Compiler receipt = OPEN


C4 = BLOCKED


Publication = BLOCKED


No theorem promotion is authorized by this document.

AQARION C3 — STRUCTURAL THEOREM


Version: S9-C3-PROVED-MATH

Date: 2026-09-09

Status: MATHEMATICALLY PROVED · LEAN OPEN · NO PROMOTION · C4 BLOCKED · PUBLICATION BLOCKED


1. Frozen definitions


Let T=(012) act on a finite ground set X, fixing every point outside


[
S={0,1,2}.
]


For a partition P, define


[
J_T(P)=P\vee T(P)\vee T^2(P).
]


Let


[
M=P\wedge Q,\qquad U=P\vee Q.
]


Define


[
r(P)=n-|P|,
]


[
d_T(P)=r(J_T(P))-r(P)=|P|-|J_T(P)|.
]


Define


[
s_0


|M|-|P|-|Q|+|U|,
]


and


[
\Delta_d


d_T(P)+d_T(Q)-d_T(M)-d_T(U).
]


Define


[
m_T


|J_T(M)|


|J_T(P)\wedge J_T(Q)|.
]


Under the frozen definitions,


[
m_T\ge0.
]


Moreover, m_T=0 iff


[
J_T(M)=J_T(P)\wedge J_T(Q).
]


2. Support-local defect theorem


Let


[
q(P)=#{B\in P:B\cap S\ne\varnothing}.
]


Let


[
\varepsilon(P)=1
]


iff all three points 0,1,2 are singleton blocks of P, and otherwise let


[
\varepsilon(P)=0.
]


Then


[
\boxed{
d_T(P)=q(P)-1-2\varepsilon(P).
}
]


Proof:


Only blocks meeting S can change under J_T.


If q(P)=1, no new merger occurs.


If q(P)=2, the order-three orbit connects the two support-meeting blocks.


If q(P)=3 but at least one support point is attached to a point outside S, the fixed outside point transports that attachment through the order-three orbit and connects all three support blocks.


If all three support points are singleton blocks, the orbit only permutes those singleton blocks and J_T(P)=P.


Thus the stated formula holds in all cases.


3. Epsilon-correction lemma


Define


[
E_S


\varepsilon(P)+\varepsilon(Q)
-\varepsilon(M)-\varepsilon(U).
]


Then


[
\boxed{
m_T=0\Longrightarrow E_S=0.
}
]


Proof:


If both P,Q have singleton support, then both M and U have singleton support.


If exactly one has singleton support, then M retains singleton support while U does not.


If neither has singleton support but M has singleton support, then P and Q each separate the support points while each has at least one external attachment. Their order-three closures therefore merge all three support points. Hence J_T(P)\wedge J_T(Q) merges the support, while J_T(M)=M leaves the three support points singleton. Thus


[
J_T(M)
\subsetneq
J_T(P)\wedge J_T(Q),
]


so m_T>0, contradiction.


Therefore E_S=0 whenever m_T=0.


4. Marked-incidence lemma


Construct the bipartite incidence graph H(P,Q):




left vertices = blocks of P;


right vertices = blocks of Q;


an edge = a nonempty meet cell.




Mark every edge whose meet cell contains a point of S.


There are at most three marked edges, so the marked subgraph is a forest.


Let V_S,E_S,C_{\mathrm{ind}} denote respectively its incident vertices, edges, and connected components.


Then


[
V_S-E_S=C_{\mathrm{ind}}.
]


Furthermore,


[
q(P)+q(Q)=V_S,
]


[
q(M)=E_S,
]


and if C_{\mathrm{full}} denotes the number of connected components of the full incidence graph meeting the marked subgraph, then


[
q(U)=C_{\mathrm{full}}.
]


Therefore


[
\kappa_S


q(P)+q(Q)-q(M)-q(U)


C_{\mathrm{ind}}-C_{\mathrm{full}}
\ge0,
]


because adding unmarked edges can only merge components.


Hence


[
\boxed{\kappa_S\ge0}.
]


5. Rank-defect identity


Using the support-local formula,


[
\Delta_d


\kappa_S-2E_S.
]


Consequently,


[
m_T=0
\Longrightarrow
E_S=0
\Longrightarrow
\boxed{\Delta_d=\kappa_S\ge0}.
]


This is the primitive C3 theorem.


6. C3 corollary


The transport identity gives


[
\Delta_d=\Gamma_T-s_0.
]


When m_T=0,


[
\Gamma_T=s_T.
]


Therefore, on the critical locus


[
s_0=1,\qquad m_T=0,
]


we obtain


[
\Gamma_T


1+\Delta_d
\ge1,
]


and hence


[
\boxed{
s_T=\Gamma_T\ge1.
}
]


Equivalently,


[
\boxed{
s_0=1,\quad m_T=0
\Longrightarrow
\Gamma_T\ge1.
}
]


In incidence-graph language,


[
\boxed{
\beta(G_0)=1,\quad m_T=0
\Longrightarrow
\beta(G_T)\ge1.
}
]


The contrapositive


[
\beta(G_0)=1,\quad\beta(G_T)=0
\Longrightarrow m_T>0
]


is therefore a corollary, not the primitive proof target.


7. Computational validation


Independent exact validation confirms:




local d_T formula: zero failures through n=7;


epsilon correction under m_T=0: zero failures through n=7;


\kappa_S\ge0: zero failures through n=7;


exact marked-forest identity: zero failures through n=7;


n=8 independent replay: zero C3 violations;


n=9 independent replay: zero \Delta_d<0 cases on the critical m_T=0 locus.




These computations are validation of the proof architecture, not substitutes for Lean certification.


8. Formalization boundary


The following are mathematically established:




support-local defect formula;


epsilon correction lemma under m_T=0;


marked-incidence forest inequality;


\Delta_d\ge0 under m_T=0;


C3.




The following remain open:




Lean formalization of the C3 lemma stack;


compilation in the pinned AQARION Lean/Mathlib environment;


#print axioms receipt;


independent formal replay;


C4.




No theorem promotion is authorized until formal certification is complete.

