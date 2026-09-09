AQARION S9 — RANKPAIR STATUS


Governance: FROZEN · EXACT · NO PROMOTION


Current disposition


[
\boxed{\text{OPEN — PUBLIC SYNCHRONIZATION NOT ESTABLISHED}}
]


No RankPair source theorem is promoted by this status document.


Mathematical target


The intended finite-dimensional identities remain:


[
\rank(P\mid KP)


\rank(P)+\rank((I-P)KP),
]


and


[
\rank
\begin{bmatrix}
P\
KP
\end{bmatrix}


\rank(P).
]


These are mathematical targets, not compiler-certified results.


Formalization architecture


The preferred Lean route is:




concrete linear maps;


range;


kernel;


finite-dimensionality;


rank-nullity;


matrix wrappers only afterward.




No theorem should be promoted merely from an informal rank argument or a source file that has not been compiled.


Certification gate


RankPair certification requires:




publicly observable exact source;


pinned Lean version;


exact Mathlib revision;


successful compilation;


zero unintended sorry;


relevant #print axioms;


reproducible build receipt.




Until those conditions are observed:


[
\boxed{\text{RANKPAIR OPEN}}
]


No promotion.


