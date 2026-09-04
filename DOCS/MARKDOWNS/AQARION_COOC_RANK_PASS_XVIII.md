AQARION — THM-COOC


Defect Rank via Target-Cooccurrence Components


Pass: XVIII

Root: 020a9110088010116075e1812c98bcd2bcc4905367fa8943a68c8cd224cf284e

Governance: FROZEN AUDIT · NO PROMOTION · C4 BLOCKED · PUBLICATION BLOCKED



1. Theorem Status


THM-COOC — Defect Rank via Target-Cooccurrence Components


Let


[
T:X\to X
]


be a finite deterministic dynamical system and let


[
\Pi={B_1,\ldots,B_m}
]


be a finite partition of X.


Let P_\Pi be the block-averaging projection onto the block-constant observable space


[
V_\Pi=\operatorname{Im}(P_\Pi),
]


and let the Koopman operator be


[
(Kf)(x)=f(Tx).
]


Define the defect operator


[
D_\Pi=(I-P_\Pi)KP_\Pi.
]


For every source block B_s, define its target set


[
S_s=
{t\in{1,\ldots,m}:
T(B_s)\cap B_t\neq\varnothing}.
]


Define the one-copy target-cooccurrence graph


[
H_\Pi
]


on the m target-block indices by


[
{t,u}\in E(H_\Pi)
]


iff


[
t\neq u
]


and there exists a source block B_s such that


[
t,u\in S_s.
]


Equivalently,


[
H_\Pi=\bigcup_s K[S_s].
]


Then


[
\boxed{
\operatorname{rank}(D_\Pi)


m-c(H_\Pi)
}
]


where c(H_\Pi) denotes the number of connected components of H_\Pi.



2. Proof Structure


Since


[
D_\Pi P_\Pi=D_\Pi,
]


the rank may be computed on V_\Pi:


[
\operatorname{rank}D_\Pi


\operatorname{rank}(D_\Pi|{V\Pi}).
]


Every f\in V_\Pi has a unique representation


[
f=\sum_{t=1}^m\alpha_t\chi_{B_t}.
]


For x\in B_s,


[
(Kf)(x)=\alpha_{b(Tx)}.
]


Therefore


[
D_\Pi f=0
]


iff Kf is constant on every source block B_s.


This is equivalent to


[
\alpha_t=\alpha_u
]


for every pair t,u\in S_s.


But these are exactly the edge-equality constraints of H_\Pi:


[
D_\Pi f=0
\iff
\forall{t,u}\in E(H_\Pi),
\quad
\alpha_t=\alpha_u.
]


Equality propagates along graph paths. Hence the coefficient vector \alpha is constant on every connected component of H_\Pi.


Thus


[
\dim\ker(D_\Pi|{V\Pi})


c(H_\Pi).
]


Since


[
\dim V_\Pi=m,
]


rank-nullity gives


[
\boxed{
\operatorname{rank}(D_\Pi)=m-c(H_\Pi).
}
]



3. Laplacian Form


Let L_{H_\Pi} be the ordinary graph Laplacian of H_\Pi.


The coefficient-space kernel is exactly the Laplacian kernel:


[
\ker(D_\Pi|{V\Pi})
\cong
\ker L_{H_\Pi}.
]


The connected-component kernel theorem therefore gives


[
\dim\ker L_{H_\Pi}=c(H_\Pi),
]


and rank-nullity yields the theorem.


This is the preferred formalization route because the connected-component basis need not be constructed manually.



4. Formalization Architecture


The Lean development is organized into the following layers:


TargetSet
    ↓
HAdj
    ↓
H : SimpleGraph ι
    ↓
Defect-zero coefficient condition
    ↓
H-edge equality
    ↓
Laplacian kernel
    ↓
Connected-component dimension
    ↓
Coefficient/block-function equivalence
    ↓
Rank-nullity
    ↓
THM-COOC



The intended definitions are:


def TargetSet
    (T : X → X) (block : ι → Set X)
    (s t : ι) : Prop :=
  ∃ x, x ∈ block s ∧ T x ∈ block t



def HAdj
    (T : X → X) (block : ι → Set X)
    (t u : ι) : Prop :=
  t ≠ u ∧ ∃ s,
    TargetSet T block s t ∧
    TargetSet T block s u



and


def H
    (T : X → X) (block : ι → Set X) : SimpleGraph ι where
  Adj := HAdj T block
  symm := by
    intro t u h
    rcases h with ⟨hne, s, ht, hu⟩
    exact ⟨hne.symm, s, hu, ht⟩
  loopless := by
    intro t h
    exact h.1 rfl




5. Required AQARION Lean Lemmas


The formal development targets:


theorem defect_blockFun_eq_zero_iff
    (α : ι → ℝ) :
    Defect T Π (blockFun Π α) = 0 ↔
      ∀ s t u,
        TargetSet T Π s t →
        TargetSet T Π s u →
        α t = α u



followed by


theorem defect_blockFun_eq_zero_iff_H
    (α : ι → ℝ) :
    Defect T Π (blockFun Π α) = 0 ↔
      ∀ t u, H T Π t u → α t = α u



and the Laplacian bridge


theorem H_edge_const_iff_lap_kernel
    (α : ι → ℝ) :
    (∀ t u, H T Π t u → α t = α u) ↔
      α ∈ LinearMap.ker
        (Matrix.toLin'
          (SimpleGraph.lapMatrix ℝ (H T Π)))



The final dimension argument uses Mathlib's rank-nullity and connected-component Laplacian results.



6. Computational Evidence


The corrected target-cooccurrence identity has been reported as exhaustively tested over the finite corpus through n=5, with additional exact-rational random testing at n=6,7,8.


These computations are evidence for THM-COOC.


They are not a substitute for the Lean certificate.


The computational certificate must remain separate from the formal certificate.



7. Regression Witness


Use the minimal isolation-sensitive example


[
X={0,1,2,3},
]


[
\Pi={{0,3},{1},{2}},
]


with


[
T=(2,3,2,3).
]


The source block {0,3} reaches both target blocks {0,3} and {2}, producing one edge in H_\Pi.


The block {1} is isolated.


Therefore


[
c(H_\Pi)=2,
\qquad
m=3,
]


and


[
\operatorname{rank}(D_\Pi)=3-2=1.
]


This regression specifically protects against incorrectly collapsing isolated target vertices.



8. WITHDRAWN THEOREM — DO NOT CERTIFY


THM-BIP — WITHDRAWN


The previous bipartite-component formulation is not part of the AQARION theorem stack.


It must not be used as a proof of THM-COOC.


Repository references to the old theorem should be marked:


WITHDRAWN
LEGACY
NOT CERTIFICATION EVIDENCE



Historical computational results associated with the old formulation may remain in the repository only when explicitly labeled historical/legacy evidence.



9. Formal Certificate Gate


THM-COOC is classified:


MATHEMATICS: PROVEN
COMPUTATION: VERIFIED
LEAN ARCHITECTURE: READY
LEAN BUILD: OPEN
ZERO-SORRY RECEIPT: OPEN
AXIOM AUDIT: OPEN



No promotion to C4 occurs until an observed pinned Lean build establishes:


exit code = 0
sorry count = 0
admit count = 0
required theorem present
#print axioms reviewed
source SHA recorded
lakefile SHA recorded
lockfile SHA recorded
Lean version recorded
Mathlib revision recorded
stdout SHA recorded
stderr SHA recorded



Therefore:


C4: BLOCKED
PUBLICATION: BLOCKED



This document records the theorem and its formalization target. It does not falsely represent an unobserved Lean build as completed.



10. Final Authority


The authoritative defect-rank theorem is:


[
\boxed{
\operatorname{rank}(D_\Pi)


|\Pi|-c(H_\Pi)
}
]


where H_\Pi is the one-copy target-cooccurrence graph.


The bipartite theorem is withdrawn.


No numerical tolerance enters the theorem.


No spectral approximation enters the theorem.


No heuristic rank calculation enters the theorem.


The final certification path is:


[
\boxed{
\text{AQARION defect}
\rightarrow
\text{co-occurrence constraints}
\rightarrow
\text{graph Laplacian kernel}
\rightarrow
\text{connected components}
\rightarrow
\text{rank-nullity}.
}
]


Status: FROZEN AUDIT · NO PROMOTION · C4 BLOCKED · PUBLICATION BLOCKED
