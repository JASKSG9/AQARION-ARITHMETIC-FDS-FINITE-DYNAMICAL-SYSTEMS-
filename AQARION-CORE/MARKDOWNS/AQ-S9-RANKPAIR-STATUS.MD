AQARION S9 — RANKPAIR STATUS


Date: 2026-09-09

Status: OPEN · UNSYNCHRONIZED

Governance: FROZEN · EXACT · NO PROMOTION


Finding


The expected public artifact


AQARION-CORE/LEAN/AQ-S9-RANKPAIR.LEAN



is currently not available at the checked repository path.


The corresponding public artifact is therefore not synchronized.


Required RankPair targets


The intended identities under audit are:


[
\operatorname{rank}[P\mid KP]


\operatorname{rank}(P)
+
\operatorname{rank}((I-P)KP)
]


and


[
\operatorname{rank}
\begin{bmatrix}
P\
KP
\end{bmatrix}


\operatorname{rank}(P).
]


These identities must not be promoted from specification to certified theorem until:




the exact Lean statement is restored;


the assumptions are explicit;


the source compiles;


the compilation receipt is retained;


the finite-dimensional rank conventions match the computational implementation.




Current status


RankPair specification: PRESENT IN RESEARCH LEDGER
RankPair public source: OPEN / 404
RankPair Lean certification: OPEN
RankPair publication status: BLOCKED
RankPair promotion status: BLOCKED



Prohibition


Do not recreate a theorem-looking RankPair file merely to eliminate the 404.


The missing artifact must be reconstructed from the intended mathematical statement and then independently compiled.


Governance


Until synchronization and compilation are complete:


C4 = BLOCKED
PUBLICATION = BLOCKED
PROMOTION = BLOCKED


