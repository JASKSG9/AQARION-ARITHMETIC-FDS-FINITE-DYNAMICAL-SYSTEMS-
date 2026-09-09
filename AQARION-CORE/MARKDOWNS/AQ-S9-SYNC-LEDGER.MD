AQARION S9 — SYNCHRONIZATION LEDGER


Date: 2026-09-09


Governance


FROZEN · EXACT · NO PROMOTION




C4: BLOCKED


Publication: BLOCKED


Lean certification: OPEN


Source synchronization: ACTIVE


Ledger: CANONICAL STATUS RECORD





Artifact Status




Artifact
Status
Action




AQ-S9-ATK.LEAN
CORRECTION REQUIRED
Replace false subtractive theorem with additive theorem


AQ-S9-TRANSPORT-ERRATA-2026-09-09.MD
READY
Add to repository


AQ-S9-DEFECT.LEAN
SOURCE PRESENT
Retain; compiler receipt still OPEN


VERIFY-CENSUS.PY
VERIFIED ARITHMETIC
Retain unchanged


AQ-S9-RANKPAIR.LEAN
PUBLIC SYNC OPEN
File currently 404


C4
BLOCKED
Do not close


Publication
BLOCKED
Do not promote





ATK Correction


The previous theorem


transport_minus



claimed


sT = s0 + delta - m



under definitions


m = rJM - rMeet



This is false.


The corrected theorem is


transport_additive



with


sT = s0 + delta + mT



The correction is an exact algebraic identity.



ATK Counterexample


Use


rP = 0
rQ = 0
rM = 0
rU = 0
rJP = 0
rJQ = 0
rJM = 1
rJU = 0
rMeet = 0



Then


s0    = 0
delta = -1
mT    = 1
sT    = 0



Therefore


s0 + delta - mT = -2



and the old subtractive theorem is false.



DEFECT


The public DEFECT source defines


Q = 1 - P
D = Q * K * P



and contains proofs for:


P * Q = 0
Q * P = 0
P * D = 0
D * Q = 0
D * D = 0
D * P = D
Q * D = D



These source-level results are retained.


Important: source presence is not a Lean compiler receipt.



Census


The canonical arithmetic verifier gives


B2 = 2
B3 = 5
B4 = 15
B5 = 52



and


[
2(2^2)+5(3^3)+15(4^4)+52(5^5)=166483.
]


Therefore:


166483 = VERIFIED ARITHMETIC
166479 = KILLED



This verifier is a cardinality/arithmetic sanity check only. It is not a proof of the underlying census theorem.



RankPair


Expected artifact:


AQARION-CORE/LEAN/AQ-S9-RANKPAIR.LEAN



Current public path is unavailable/404.


Therefore:


RANKPAIR = PUBLIC SYNC OPEN



Do not claim public RankPair synchronization.



Promotion Gate


The following conditions are required before promotion:




Corrected ATK committed.


Exact Lean toolchain pinned.


Corrected ATK compiled successfully.


Clean compiler receipt retained.


DEFECT compiled under the same pinned environment.


RankPair source synchronized and independently checked.


No unresolved contradiction remains in the transport definitions.


C4 audit gate explicitly reopened.




Until then:


NO PROMOTION
NO PUBLICATION
NO C4 CLOSURE


