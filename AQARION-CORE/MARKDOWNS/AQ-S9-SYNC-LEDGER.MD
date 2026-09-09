AQARION S9 — PUBLIC SYNCHRONIZATION LEDGER


Governance: FROZEN · EXACT · NO PROMOTION · CANONICAL


Artifact status




Artifact
Current disposition




AQ-S9-ATK.LEAN
🔴 QUARANTINED — replaced transport semantics required


AQ-S9-DEFECT.LEAN
🟢 SOURCE-SYNCHRONIZED


DEFECT.LEAN
🟢 SOURCE-SYNCHRONIZED where present


VERIFY-CENSUS.PY
🟢 CARDINALITY CHECK VERIFIED


AQ-S9-RANKPAIR.LEAN
🟡 PUBLIC SYNC OPEN


Lean compiler receipt
🟡 OPEN


C3
🟡 OPEN


C4
🔴 BLOCKED


Publication
🔴 BLOCKED




ATK transport


The previous public ATK artifact defined


[
m_T=r_{JM}-r_{\mathrm{Meet}}
]


but asserted a subtractive transport identity.


It also used r_{JT} in s_T while using r_{JU} in \Delta.


The exact relation under those definitions is


[
s_T=s_0+\Delta+m_T+(r_{JU}-r_{JT}).
]


Therefore the previous theorem is not accepted.


Canonical replacement


The canonical artifact uses


[
s_T=r_{JP}+r_{JQ}-r_{\mathrm{Meet}}-r_{JU},
]


[
m_T=r_{JM}-r_{\mathrm{Meet}},
]


and proves


[
\boxed{s_T=s_0+\Delta+m_T}.
]


The opposite convention is explicitly recorded:


[
m_{\mathrm{opp}}=-m_T,
]


giving


[
s_T=s_0+\Delta-m_{\mathrm{opp}}.
]


DEFECT


The synchronized source contains


[
Q=I-P,\qquad D=QKP,
]


and the identities


[
PQ=QP=0,
]


[
PD=0,\qquad DQ=0,
]


[
DP=D,\qquad QD=D,
]


[
D^2=0.
]


Disposition:


[
\boxed{\text{SOURCE-SYNCHRONIZED / COMPILER OPEN}}
]


Source synchronization does not imply compilation.


Census


The arithmetic verifier establishes


[
\boxed{166483},
]


[
\boxed{20503},
]


[
\boxed{223587231}.
]


These are cardinality checks only.


No structural theorem follows from these values.


RankPair


The RankPair public artifact remains OPEN until its exact source is publicly observable and independently inspected.


No RankPair theorem is promoted by this ledger.


Compiler gate


Lean certification requires:




pinned Lean version;


exact Mathlib revision;


project configuration;


successful build;


zero unintended sorry;


relevant #print axioms;


captured reproducible build receipt.




Until those are observed:


[
\boxed{\text{LEAN CERTIFICATION OPEN}}
]


Governance


[
\boxed{\text{C3 OPEN}}
]


[
\boxed{\text{C4 BLOCKED}}
]


[
\boxed{\text{PUBLICATION BLOCKED}}
]


Ledger is the argument.


