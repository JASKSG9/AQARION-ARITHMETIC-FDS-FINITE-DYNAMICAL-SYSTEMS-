AQARION C3 — STRUCTURAL TARGET


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

