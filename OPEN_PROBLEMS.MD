AQARION-ARITHMETIC — OPEN PROBLEMS


Version: v18.0-CURRENT-RESEARCH-BOUNDARY

Date: 2026-09-09

Status: FROZEN RESEARCH LEDGER · C4 BLOCKED · PUBLICATION BLOCKED · NO PROMOTION

Repository: JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-



0. PURPOSE AND GOVERNANCE


This document is the current authoritative open-problems ledger for AQARION-ARITHMETIC.


It replaces obsolete June-2026 roadmap language. Historical versions remain preserved by Git history and should not be copied forward merely for continuity.


The governing rule is:




A mathematical derivation, numerical agreement, repository artifact, or Lean source file is not promoted to a certified theorem merely because it is plausible or because a related computation passes.




Every item must be classified by its actual evidence state.


Evidence states




State
Meaning




OPEN
Unresolved mathematical or structural question


CONJECTURE
Precisely stated but not proved


COMPUTED
Exact finite computation or numerical evidence exists


DERIVED
Mathematical derivation exists but an explicit certificate/remainder/formal closure remains


PROVED
Mathematical proof is complete at the stated scope


FORMAL-OPEN
Mathematical result is established, but the public Lean theorem/proof is incomplete or under-specified


REPRO-OPEN
Artifact exists but independent reproduction/compilation has not been established


QUARANTINED
Claim is plausible or partially supported but deliberately not promoted


REFUTED
Earlier formulation has been disproved or superseded


BLOCKED
Governance gate prevents promotion regardless of local mathematical progress




Non-promotion rule


No item marked DERIVED, FORMAL-OPEN, REPRO-OPEN, or QUARANTINED may be described elsewhere in the repository as a fully certified result.



1. CURRENT EXECUTIVE STATUS


1.1 Overall state


[
\boxed{
\text{MATHEMATICS ADVANCED}
\quad
\text{FORMAL CERTIFICATION OPEN}
\quad
\text{C4 BLOCKED}
\quad
\text{PUBLICATION BLOCKED}
}
]


The strongest current advances are:




exact structural understanding of the Koopman defect;


mathematical proof architecture for THM-BIP;


independent exact finite census through n=5;


correction of the historical census metadata;


exact two-block defect identities;


analytic resolution of the former WU1 \lambda=2 residual;


exact cancellation of the \delta^{3/2} coefficient;


explicit derivation of the new \delta^2 coefficient;


identification of the remaining WU1 task as an explicit uniform remainder certificate;


identification of the actual Lean specification hole;


identification of the public Lean-toolchain baseline as unresolved;


separation of RO-Crate schema existence from actual theorem certification.




None of these changes, individually or collectively, closes C4.



2. P0 — COMPILER AND FORMAL BASELINE


OP-P0: Establish the actual public Lean compiler baseline


Question


What exact Lean compiler, Mathlib revision, Lake configuration, and build command constitute the reproducible AQARION formalization baseline?


Current issue


The repository has referred to Lean 4.33.1 as the intended formal environment, but the public Mathlib/AQARION artifacts do not currently provide an observed compiler certificate establishing that baseline.


A public fork also contains instructions referring to a later release-candidate environment.


Therefore:


[
\boxed{\text{Lean 4.33.1 is an intended baseline, not yet a public compiler receipt.}}
]


Required closure


A reproducible certificate must record:




exact lean-toolchain;


exact Lean version;


exact Mathlib commit;


exact Lake configuration;


successful dependency resolution;


successful build;


successful theorem compilation;


#print axioms or equivalent axiom audit where required;


reproducible command sequence.




Status


[
\boxed{\text{BLOCKED / OPEN}}
]


Priority


P0



3. P1 — THM-BIP FORMAL SPECIFICATION


OP-P1: Repair the concrete Lean statement for THM-BIP


Mathematical theorem


For a finite deterministic dynamical system (X,T), observable partition \Pi with m blocks, Koopman operator K_T, and block projection P_\Pi, define


[
D_\Pi=(I-P_\Pi)K_TP_\Pi.
]


The intended structural theorem is


[
\boxed{
\operatorname{rank}D_\Pi


m-c(G_{\Pi,T}),
}
]


where G_{\Pi,T} is the bipartite block-transition graph.


Current formalization problem


The public Lean theorem currently permits an arbitrary defect operator D while asserting a kernel characterization that depends on the concrete definition


[
D=(I-P_\Pi)K_TP_\Pi.
]


A comment describing the missing hypothesis does not substitute for the hypothesis in the theorem signature.


This is a genuine specification defect.


Required repair


The primary formal object should be the concrete restriction


[
L_\Pi


(I-P_\Pi)\circ K_T\circ\iota_\Pi,
]


where


[
\iota_\Pi:\mathbb R^m\hookrightarrow\mathbb R^X
]


is the block-constant embedding.


Then prove:


[
\boxed{
\ker L_\Pi


\operatorname{ConstRightComp}(\Pi,T).
}
]


Only afterward derive the rank theorem.


Status


[
\boxed{\text{MATHEMATICS PROVED / LEAN FORMALIZATION OPEN}}
]


Priority


P1



4. P2 — THM-BIP KERNEL/COMPONENT THEOREM


OP-P2: Formalize the component-indicator kernel basis


Let the bipartite graph have left vertices corresponding to source blocks and right vertices corresponding to target blocks.


For each source block B_i, let


[
R_i


{j:\exists x\in B_i,\ T(x)\in B_j}.
]


For a block-coordinate vector


[
v=(v_1,\ldots,v_m),
]


the concrete defect vanishes precisely when


[
v_j=v_k
\qquad
\forall i,\quad j,k\in R_i.
]


These equality constraints generate the equivalence relation represented by connected components of G_{\Pi,T}.


For every connected component C, define


[
u_C=\mathbf 1_C.
]


The intended theorem is


[
\boxed{
\ker L_\Pi


\operatorname{span}{u_C:C\in\pi_0(G_{\Pi,T})}.
}
]


Hence


[
\boxed{
\dim\ker L_\Pi=c(G_{\Pi,T}).
}
]


Preferred Lean architecture


Do not begin with Matrix.rank.


Formalize, in order:




concrete block embedding;


concrete defect restriction;


pointwise kernel criterion;


generated equality relation;


equivalence with graph connected components;


component-indicator basis;


kernel dimension;


rank-nullity.




Status


[
\boxed{\text{MATHEMATICS PROVED / LEAN OPEN}}
]


Priority


P2



5. P3 — THM-BIP RANK THEOREM


OP-P3: Derive rank from kernel dimension


After OP-P2 is formalized, derive


[
\dim\ker L_\Pi=c(G_{\Pi,T})
]


and


[
\dim V_\Pi=m.
]


Rank-nullity then gives


[
\boxed{
\operatorname{rank}D_\Pi


m-c(G_{\Pi,T}).
}
]


The theorem should be stated for the concrete defect, not for an arbitrary matrix satisfying only


[
D=(I-P)KP.
]


Status


[
\boxed{\text{MATHEMATICS PROVED / LEAN OPEN}}
]


Priority


P3



6. P4 — CYCLE-RANK REFORMULATION


OP-P4: Formalize the cycle-rank corollary


For a bipartite graph with 2m vertices, e edges, and c connected components,


[
\beta(G)=e-2m+c.
]


Combining this with


[
\operatorname{rank}D=m-c
]


gives


[
\boxed{
\operatorname{rank}D=e-m-\beta(G).
}
]


This is a derived graph-theoretic reformulation, not an independent foundational theorem.


Further deterministic consequence


Under the pinned deterministic/nonempty-block setting,


[
D=0
\iff
c(G)=m
\iff
e=m
\iff
\beta(G)=0.
]


Thus the graph has no cycles and exactly one outgoing target block per source block.


Equivalently, the graph is a forest of m source-centered stars.


Status


[
\boxed{\text{MATHEMATICS DERIVED / FORMALIZATION OPEN}}
]


Priority


P4



7. P5 — UNIVERSAL DEFECT IDENTITIES


The following identities remain part of the mathematical core:


[
\boxed{D^2=0}
]


[
\boxed{PD=0}
]


[
\boxed{D(I-P)=0}
]


[
\boxed{DP=D}.
]


These are distinct from the false identity described below.


Refuted identity


The statement


[
\boxed{D(KP)=D}
]


is refuted.


Direct computation shows that it does not hold in general.


The correct depth-cut behavior is geometric decay of appropriate iterates of D(KP), with the two-block forward-invariant case governed by p_{BB}.


Governance rule


The refuted identity must not be reintroduced into future proofs, summaries, benchmarks, or theorem statements.


Status


[
\boxed{\text{CLOSED: FALSE IDENTITY KILLED}}
]



8. P6 — EXACT FINITE CENSUS


OP-P6: Preserve the corrected all-map/all-partition census


An independent exact enumeration of deterministic maps and set partitions for


[
n=2,3,4,5
]


gives:


[
B_2=2,\quad
B_3=5,\quad
B_4=15,\quad
B_5=52.
]


The total number of map/partition pairs is


[
2^2B_2+
3^3B_3+
4^4B_4+
5^5B_5


8+135+3840+162500


\boxed{166479}.
]


Independent exact rational construction of P,K,D, exact rank computation, and independent graph-component computation gives:




n
Cases
Passed




2
8
8


3
135
135


4
3,840
3,840


5
162,500
162,500


Total
166,479
166,479




No failures occurred in this independent replay.


Governance correction


The historical number


[
166483
]


must no longer be presented as the exact all-map/all-partition census.


The corrected independently reproduced count is


[
\boxed{166479}.
]


Status


[
\boxed{\text{COMPUTED / REPRODUCED}}
]


This is a computational certificate for the tested finite scope, not a Lean theorem.



9. P7 — TWO-BLOCK DEFECT FORMULA


For a two-block partition


[
\Pi=A|B,
]


with


[
a=|A|,\qquad b=|B|,\qquad n=a+b,
]


and A forward invariant, let


[
q=p_{BA}.
]


Then


[
\boxed{
|D|_F^2


\frac{nq(1-q)}a.
}
]


The associated second eigenvalue is


[
\boxed{
\lambda_2=p_{BB}=1-q.
}
]


For the depth-cut example with a=1, b=53, q=3/53,


[
|D|_F


\frac{90}{53}
\approx1.6981132075.
]


These formulas should be retained as derived structural results.


Status


[
\boxed{\text{MATHEMATICS DERIVED/PROVED}}
]



10. P8 — WU1 CORE ASYMPTOTICS


OP-P8: Preserve the locked c_k and optimal-term scale


The WU1 coefficient ladder


[
c_k


\frac{\zeta(1-2k)^2}{(2k-2)!}
]


and equivalent exact fast form remain mathematically locked at their established scope.


The optimal-term scale is likewise treated as established within the current WU1 derivation.


Status


[
\boxed{\text{MATHEMATICALLY LOCKED}}
]



11. P9 — WU1-B ORIGINAL TRANSPORT LAW


The original WU1-B transport/power-law formulation is refuted.


It must not be revived merely because later asymptotics resemble part of its heuristic structure.


Status


[
\boxed{\text{REFUTED}}
]



12. P10 — WU1-B.REVISED ABEL DECOMPOSITION


The revised route begins from


[
f(x)=\frac{x^2}{4\sinh^2(x/2)}


\frac{x^2e^{-x}}{(1-e^{-x})^2},
]


and


[
S(\delta,\alpha)


\sum_{r\ge1}\frac{e^{-\alpha r}}r f(\delta r).
]


Then


[
D(\delta,\alpha)


S(\delta,\alpha)-S(\delta,0)


-\int_0^\alpha
\sum_{r\ge1}f(\delta r)e^{-tr},dt.
]


The decomposition


[
g(x)=f(x)-e^{-x}
]


removes the divergent harmonic subtraction and produces the exact reference term


[
D_{\exp}


\log
\frac{1-e^{-\delta}}
{1-e^{-(\alpha+\delta)}}.
]


The remaining g-term is controlled by Euler–Maclaurin and a Laplace-tail expansion.


Status


[
\boxed{\text{DERIVED}}
]


The proof architecture is considered substantially preferable to the previous contour-shift route.



13. P11 — EXACT REGULARIZED CONSTANT


The regularized integral


[
I_g


\int_0^\infty\frac{g(x)}x,dx
]


evaluates to


[
\boxed{I_g=1+\gamma}.
]


Therefore the constant contribution is


[
\boxed{-(1+\gamma)}.
]


This removes the former numerical mystery surrounding the finite constant.


Status


[
\boxed{\text{DERIVED}}
]



14. P12 — WU1-B.REVISED JOINT-SCALING EXPANSION


Under


[
\alpha=\lambda\sqrt{\delta},
]


the current derived expansion is


[
\boxed{
\begin{aligned}
S(\delta,\lambda\sqrt\delta)-S(\delta,0)
={}&
-\frac12\log\frac1\delta
-\log\lambda
-(1+\gamma)\
&+\frac{\lambda}{2}\sqrt\delta\
&-\left(
\frac{\lambda^2}{24}
+\frac1{12\lambda^2}
\right)\delta\
&+
\left(
\frac{\lambda^4}{2880}
+\frac1{40\lambda^4}
\right)\delta^2\
&+O(\delta^{5/2}).
\end{aligned}
}
]


The displayed coefficient of \delta^{3/2} cancels identically.


Important qualification


The asymptotic structure is analytically derived, but the final uniform theorem requires an explicit, independently checkable remainder constant.


Therefore the expansion must not yet be labelled as a fully certified uniform theorem.


Status


[
\boxed{\text{DERIVED / REMAINDER OPEN}}
]



15. P13 — EXACT \delta^{3/2} CANCELLATION


The \delta^{3/2} coefficient is


[
-\frac{\lambda^4+4}{12\lambda^3}
+
\frac1{3\lambda^3}
+
\frac{\lambda}{12}.
]


It simplifies identically to


[
\boxed{0}.
]


This is a structural coefficient identity, not a numerical fit.


Status


[
\boxed{\text{PROVED AT THE FORMAL ASYMPTOTIC-DERIVATION LEVEL}}
]


The remaining issue is inclusion of this cancellation inside a fully bounded uniform remainder theorem.



16. P14 — NEW \delta^2 COEFFICIENT


The next nonzero coefficient is


[
\boxed{
C_4(\lambda)


\frac{\lambda^4}{2880}
+
\frac1{40\lambda^4}.
}
]


For example,


[
C_4(2)


\frac{16}{2880}+\frac1{640}


0.007118055555\ldots
]


The previous \lambda=2 residual is therefore explained by the omitted \delta^2 term.


The old governance statement




“\lambda=2 indicates unresolved higher-order fine structure”




should be retired.


The stronger current statement is:




The former \lambda=2 residual is consistent with the explicitly derived \delta^2 coefficient, while the \delta^{3/2} coefficient cancels identically.




Status


[
\boxed{\text{DERIVED + NUMERICALLY CONSISTENT}}
]


Not yet promoted to a complete uniform theorem.



17. P15 — WU1 EXPLICIT UNIFORM REMAINDER


Primary remaining WU1 analytic problem


Construct an explicit constant


[
C(\lambda_0,\lambda_1)
]


such that, uniformly for


[
\lambda\in[\lambda_0,\lambda_1]
\subset(0,\infty),
]


the remainder satisfies


[
\left|
R(\delta,\lambda)
\right|
\le
C(\lambda_0,\lambda_1)\delta^{5/2}
]


for all sufficiently small \delta.


The preferred proof route is:


[
\boxed{
\text{exact Abel identity}
\rightarrow
\text{exponential reference}
\rightarrow
\text{Euler--Maclaurin}
\rightarrow
\text{Laplace tail}
\rightarrow
\text{explicit uniform bound}.
}
]


Required ingredients




uniform control of the Euler–Maclaurin remainder;


explicit bounds on derivatives of g;


explicit Laplace-tail remainder;


explicit dependence on [\lambda_0,\lambda_1];


independent numerical adversarial testing;


preferably an exact or interval-arithmetic certificate.




Status


[
\boxed{\text{OPEN}}
]


Priority


P5



18. P16 — GENERAL ABEL-TRANSPORT COEFFICIENT THEOREM


The WU1 cancellation suggests a general theorem.


Suppose


[
g(x)=\sum_{j\ge1}b_jx^j.
]


Then


[
\int_0^\infty
\frac{g(x)}x e^{-Ux},dx


\sum_{j\ge1}
b_j\frac{(j-1)!}{U^j}.
]


Thus the local Taylor jet of g, combined with Euler–Maclaurin corrections, generates the joint-scaling transport ladder.


The desired abstract result is schematically


[
\boxed{
\text{Taylor jet of }g
+
\text{Euler--Maclaurin data}
\Longrightarrow
\text{joint-scaling asymptotic ladder}.
}
]


The \delta^{3/2} cancellation in WU1 would then become an instance of a general coefficient theorem rather than an isolated calculation.


Status


[
\boxed{\text{OPEN / CONJECTURAL GENERALIZATION}}
]


Priority


P6



19. P17 — WU1 NUMERICAL ADVERSARIAL CHECKS


The current independent checks at


[
\lambda\in{1/2,1,2,3}
]


are consistent with


[
C_4(\lambda)


\frac{\lambda^4}{2880}
+
\frac1{40\lambda^4}.
]


This is evidence, not proof.


Future checks should:




increase precision;


vary \delta over multiple scales;


test values close to both ends of compact \lambda-intervals;


explicitly test the predicted O(\delta^{5/2}) remainder;


use exact or interval arithmetic where feasible.




Status


[
\boxed{\text{COMPUTED / REPRODUCTION OPEN}}
]



20. P18 — 55-STATE MINIMALITY


The claim that the 55-state representation is a minimal observable quotient remains quarantined.


The safe statement is:




55 is the exact number of states in the chosen 55-state representation.




This is not equivalent to proving:




55 is the minimal observable quotient.




A valid minimality theorem requires an explicit distinguishability argument or an equivalent observable-separation theorem.


Status


[
\boxed{\text{QUARANTINED}}
]


Priority


P7



21. P19 — KAPREKAR DEPTH TERMINOLOGY


Depth, quotient size, semigroup size, nilpotent index, and lattice height must not be conflated.


The repository previously mixed several quantities under “height” or “depth.”


The current governance rule is:




state-space depth must be defined from the actual transition graph;


quotient refinement depth must be defined separately;


nilpotent index must be defined from the operator;


congruence-lattice height must be defined from the lattice;


none may be substituted for another without proof.




Status


[
\boxed{\text{GOVERNANCE CONSTRAINT}}
]



22. P20 — CONGRUENCE LATTICE


An exhibited congruence chain of length six is evidence of a chain.


It is not a classification of the entire congruence lattice.


Open questions:




Is the exhibited chain maximal?


What is the exact lattice height?


How many congruences exist?


Is the lattice distributive/modular?


Can the lattice be computed recursively from the rooted functional graph?




Preferred route


Exploit the functional-graph structure recursively rather than enumerate all partitions of 54 states.


Status


[
\boxed{\text{QUARANTINED / OPEN}}
]


Priority


P8



23. P21 — SLACK HISTOGRAM


Historical repository artifacts contain conflicting tight/slack counts.


Examples include different reported totals for tight cases.


Therefore no historical histogram is promoted until a fresh exact replay is generated from a single pinned implementation.


Required certificate


The replay must specify:




state space;


partition;


exact inequality;


all parameter ranges;


arithmetic type;


total cases;


tight cases;


non-tight cases;


SHA-256 of the generating source;


SHA-256 of the output artifact.




Status


[
\boxed{\text{OPEN / REPLAY REQUIRED}}
]


Priority


P9



24. P22 — C3: GLOBAL \Gamma_T INEQUALITY


Target:


[
s_0=1,\qquad m_T=0
\quad\Longrightarrow\quad
\Gamma_T\ge1.
]


The global statement remains open.


The preferred route is structural rather than another blind large-n census.


Proposed proof architecture


[
\text{unique incidence cycle}
\Longrightarrow
\text{linear dependence}
\Longrightarrow
\text{closure-compatible dependence}
\Longrightarrow
\text{nontrivial cycle image}
\Longrightarrow
\Gamma_T\ge1.
]


Status


[
\boxed{\text{OPEN}}
]


Priority


P10



25. P23 — THM-BIP EXHAUSTIVE REPLAY


The independent n\le5 census establishes the identity over the enumerated finite scope.


The remaining formalization question is not whether the small census passes, but whether the exact general theorem is correctly specified and formally proved.


Therefore:


[
\boxed{
\text{finite exhaustive evidence}
\neq
\text{general Lean theorem}.
}
]


Status


[
\boxed{\text{COMPUTED / FORMAL-OPEN}}
]



26. P24 — RO-CRATE CERTIFICATION


An AQARION RO-Crate extension/profile exists as an experimental research-object architecture.


Its intended fields include:




claims;


evidence;


provenance;


certificates;


revisions;


machine-readable status.




However, schema existence does not itself establish theorem certification.


Illustrative hashes or example claims must never be interpreted as cryptographic certificates for mathematical results.


Required closure


A certified RO-Crate pipeline must demonstrate:




generation from actual theorem artifacts;


deterministic serialization;


cryptographic hashing;


independent validation;


claim-to-artifact provenance;


tamper detection;


successful end-to-end replay.




Status


[
\boxed{\text{EXPERIMENTAL / REPRO-OPEN}}
]


Priority


P11



27. P25 — AQARION EVIDENCE TUPLE


The recommended claim object is


[
\boxed{
E=(S,H,P,V,R)
}
]


where:




S = precise statement;


H = hypotheses;


P = symbolic/mathematical proof;


V = independent verification;


R = reproduction recipe.




A claim should advance through


[
\boxed{
\text{CONJECTURE}
\rightarrow
\text{COMPUTED}
\rightarrow
\text{DERIVED}
\rightarrow
\text{FORMALIZED}
\rightarrow
\text{REPRODUCED}.
}
]


No state may be skipped merely because an informal proof appears convincing.


Status


[
\boxed{\text{METHODOLOGICAL TARGET}}
]



28. P26 — CRYPTOGRAPHIC CLAIM MANIFEST


The proposed canonical manifest should contain:


claim_id
statement_sha256
hypothesis_sha256
proof_sha256
lean_commit
mathlib_version
compiler_version
data_sha256
test_command
test_count
independent_replay_count
status



The manifest is useful only if every field is generated from actual observed artifacts.


Placeholder values are prohibited in certification manifests.


Status


[
\boxed{\text{OPEN / INFRASTRUCTURE TASK}}
]



29. P27 — AQARION-FDS-BENCH


A formalization/adversarial benchmark should be developed around instances


[
(T,\Pi,K,P,D,G).
]


Candidate tasks:




compute D;


decide whether D=0;


compute \operatorname{rank}D;


predict c(G);


produce a kernel proof;


produce a rank proof;


generate Lean;


detect malformed theorem statements;


survive adversarial mutations.




Adversarial mutations should include




transpose convention;


pushforward/pullback reversal;


non-idempotent P;


empty blocks;


nondeterministic K;


reversed graph orientation;


dimension mismatch;


arbitrary-D substitution;


incorrect rank identity;


false D(KP)=D identity.




Proposed metrics


[
\text{SpecFaith}
]


Does the formal statement encode the intended theorem?


[
\text{CounterexampleResistance}
]


Does the system reject false/weakened variants?


[
\text{CertificateRepro}
]


Can an independent process reproduce the result?


[
\text{KillRate}
]


Does the system identify planted false claims?


Status


[
\boxed{\text{OPEN / RESEARCH DIRECTION}}
]


Priority


P12



30. P28 — AI/FORMAL-MATH REPRODUCIBILITY


AQARION should distinguish:


[
\boxed{
\text{LLM-generated proof}
\neq
\text{formal proof}
\neq
\text{reproduced formal proof}.
}
]


The project should retain adversarial records of:




failed proof attempts;


false theorem statements;


specification mismatches;


compilation failures;


counterexamples;


repaired proofs;


independent replays.




The goal is not merely to obtain a Lean script but to establish a reproducible chain from mathematical claim to independently checkable artifact.


Status


[
\boxed{\text{OPEN / METHODOLOGICAL}}
]



31. P29 — LITERATURE BOUNDARY


AQARION must not claim novelty for classical machinery merely because it is used in the project.


In particular, the following are established mathematical territories:




lumpability;


equitable partitions;


quotient transition systems;


graph connected-component rank;


partition refinement;


Abel summation;


Euler–Maclaurin summation;


Mellin-transform asymptotics;


Laplace asymptotics;


coalgebraic behavioral equivalence.




The potentially distinctive AQARION contribution must instead be stated narrowly.


Safe positioning


A defensible research claim is:




AQARION organizes an exact linear defect



D_\Pi=(I-P_\Pi)K_TP_\Pi



for deterministic finite observable quotients and relates its rank/kernel structure to connectivity of the associated bipartite block-transition graph.




No claim should be made that AQARION invented quotient theory, equitable partitions, lumpability, or classical asymptotic summation.


Status


[
\boxed{\text{GOVERNANCE CONSTRAINT}}
]



32. P30 — PUBLICATION GATE


Publication remains blocked until the following are closed:


Formal gate




[ ] compiler baseline pinned;


[ ] Mathlib revision pinned;


[ ] THM-BIP theorem specification repaired;


[ ] concrete kernel theorem formally proved;


[ ] component-indicator basis formally proved;


[ ] rank-nullity theorem formally connected;


[ ] required axiom audit completed.




Analytic gate




[ ] WU1 explicit uniform remainder constant;


[ ] independent reproduction of the final asymptotic bound;


[ ] no unresolved coefficient discrepancy.




Computational gate




[ ] corrected census provenance frozen;


[ ] stale conflicting counts removed or explicitly quarantined;


[ ] slack histogram replayed;


[ ] all published numerical claims linked to exact artifacts.




Provenance gate




[ ] RO-Crate validator operational;


[ ] actual certificates generated;


[ ] no placeholder hashes;


[ ] end-to-end independent validation.




Governance gate




[ ] C3 resolved or explicitly removed from publication claims;


[ ] 55-state minimality either proved or permanently quarantined;


[ ] congruence-lattice claims correctly bounded;


[ ] all refuted identities removed from active theorem paths.




Current status


[
\boxed{\text{PUBLICATION BLOCKED}}
]



33. CURRENT PRIORITY ORDER


The recommended order is:


[
\boxed{
\begin{array}{rcl}
P0 &:& \text{compiler/toolchain certificate}\
P1 &:& \text{repair concrete THM-BIP Lean statement}\
P2 &:& \text{formal kernel/component theorem}\
P3 &:& \text{formal rank-nullity theorem}\
P4 &:& \text{cycle-rank corollary}\
P5 &:& \text{WU1 explicit uniform remainder}\
P6 &:& \text{general Abel-transport coefficient theorem}\
P7 &:& \text{55-state minimality}\
P8 &:& \text{congruence-lattice classification}\
P9 &:& \text{fresh slack-histogram replay}\
P10&:& \text{C3 structural proof}\
P11&:& \text{RO-Crate certification}\
P12&:& \text{AQARION-FDS-Bench}.
\end{array}
}
]


This ordering deliberately puts formal specification correctness before formal proof optimization.



34. THINGS NOT TO DO


The following are explicitly frozen unless new evidence changes the situation.


34.1 Do not revive WU1-B original


The original transport/power law is refuted.


34.2 Do not return to contour shifting as the primary WU1 route


The Abel decomposition now provides the cleaner route.


34.3 Do not search indefinitely for another \lambda=2 anomaly


The former discrepancy has a concrete \delta^2 explanation.


34.4 Do not run the full n=9 computational hammer merely to replace the missing C3 proof


The current structural route is preferable.


34.5 Do not formalize Matrix.rank first


Formalize the kernel/component structure first.


34.6 Do not treat a comment as a theorem hypothesis


The concrete operator definition must occur in the Lean type.


34.7 Do not treat a passing finite census as a general proof


Finite computation validates a finite scope.


34.8 Do not call an uncompiled public Lean fork a compiler certificate


The toolchain must actually be pinned and observed.


34.9 Do not call an experimental RO-Crate profile a certified theorem


The complete validation chain must exist.


34.10 Do not promote quarantined claims


Especially:




55-state minimality;


complete congruence-lattice classification;


conflicting slack histograms;


C3;


publication readiness.





35. CANONICAL STATUS LEDGER




Claim / Object
Current status




D^2=0
PROVED


PD=0
PROVED


D(I-P)=0
PROVED


DP=D
PROVED


D(KP)=D
REFUTED


Two-block Frobenius norm formula
PROVED/DERIVED


\lambda_2=p_{BB}
PROVED


THM-BIP mathematics
PROVED


THM-BIP Lean statement
FORMAL-OPEN


THM-BIP Lean proof
OPEN


Kernel/component theorem
MATHEMATICS PROVED / LEAN OPEN


Rank =m-c(G)
MATHEMATICS PROVED / LEAN OPEN


e-m-\beta identity
DERIVED


D=0\iff\beta=0 in pinned setting
DERIVED/PROVED


Independent n\le5 census
166479 / REPRODUCED


Historical 166483 total
REFUTED AS EXACT TOTAL


55-state minimality
QUARANTINED


Congruence-chain length 6
EXHIBITED / NOT CLASSIFICATION


Full congruence-lattice height
OPEN


Slack histogram
OPEN / REPLAY REQUIRED


C3 \Gamma_T\ge1
OPEN


WU1 c_k ladder
LOCKED


WU1-B original
REFUTED


WU1-B revised through O(\delta)
DERIVED


\delta^{3/2} coefficient
EXACTLY ZERO


C_4(\lambda)
DERIVED + NUMERICALLY CONSISTENT


WU1 explicit uniform remainder
OPEN


General Abel-transport theorem
OPEN


Public Lean 4.33.1 certificate
OPEN


Public Mathlib/AQARION build certificate
OPEN


RO-Crate profile
EXPERIMENTAL


RO-Crate theorem certification
OPEN


AQARION-FDS-Bench
OPEN


C4
BLOCKED


Publication
BLOCKED





36. C4 GATE


The current gate is:


[
\boxed{
C4=
\text{FORMAL}
\cap
\text{REPRODUCIBLE}
\cap
\text{PROVENANCE-CERTIFIED}
\cap
\text{GOVERNANCE-CLEAN}.
}
]


Current state:


[
\boxed{
C4=\text{BLOCKED}.
}
]


The blockage is not caused by lack of mathematical progress.


It is caused by unresolved formal specification, compiler-baseline, remainder-certification, provenance, and governance requirements.



37. FINAL RESEARCH POSITION


The strongest current conclusion is:


[
\boxed{
\text{MATHEMATICS ADVANCED}
}
]


but not


[
\boxed{
\text{FORMALLY CERTIFIED}.
}
]


The WU1 development has moved from a numerical anomaly to an analytic mechanism:


[
\boxed{
\delta^{3/2}\text{ cancels exactly}
}
]


and


[
\boxed{
C_4(\lambda)


\frac{\lambda^4}{2880}
+
\frac1{40\lambda^4}.
}
]


The THM-BIP development has moved from a rank observation to a clean structural proof architecture:


[
\boxed{
\text{concrete defect}
\rightarrow
\text{pointwise kernel}
\rightarrow
\text{graph components}
\rightarrow
\text{component basis}
\rightarrow
\text{rank-nullity}.
}
]


The remaining work is therefore not to manufacture additional positive claims.


It is to close the certification boundary honestly.


[
\boxed{
\textbf{NO PROMOTION}
}
]


[
\boxed{
\textbf{C4 BLOCKED}
}
]


[
\boxed{
\textbf{PUBLICATION BLOCKED}
}
]



CHANGE CONTROL


This document supersedes the previous June-2026 v17.4-PUBLICATION-READY open-problems document.


Historical claims remain available through Git history.


Future updates should modify this document only when:




a new proof is actually established;


a counterexample is found;


an independent exact replay changes the evidence;


a formal theorem compiles under a pinned environment;


a provenance/certificate artifact is independently validated; or


governance explicitly changes the promotion state.




No status should be upgraded merely because a new draft, numerical fit, LLM proof, or uncompiled Lean source exists.
