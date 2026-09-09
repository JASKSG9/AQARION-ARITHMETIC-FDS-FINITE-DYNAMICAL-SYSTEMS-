AQARION S9 — TRANSPORT ERRATA


Date: 2026-09-09

Status: FROZEN · EXACT · NO PROMOTION

Governance: C4 BLOCKED · PUBLICATION BLOCKED · Lean compilation receipt OPEN


1. Scope


This erratum corrects the public AQ-S9 transport artifact:


AQARION-CORE/LEAN/AQ-S9-ATK.LEAN


The previously published theorem transport_minus is mathematically false under its own definitions.


2. Public-source finding


The previous public source defined


[
s_0=r_P+r_Q-r_M-r_U
]


[
s_T=r_{JP}+r_{JQ}-r_{\rm Meet}-r_{JU}
]


and


[
\Delta=
(r_{JP}-r_P)+(r_{JQ}-r_Q)
-(r_{JM}-r_M)-(r_{JU}-r_U).
]


It also defined


[
m_T=r_{JM}-r_{\rm Meet}.
]


The source nevertheless asserted


[
s_T=s_0+\Delta-m_T.
]


That sign is incorrect.


3. Correct identity


Direct expansion gives


[
s_0+\Delta


r_{JP}+r_{JQ}-r_{JM}-r_{JU}.
]


Since


[
m_T=r_{JM}-r_{\rm Meet},
]


we obtain


[
s_0+\Delta+m_T


r_{JP}+r_{JQ}-r_{\rm Meet}-r_{JU}


s_T.
]


Therefore the corrected identity is


[
\boxed{s_T=s_0+\Delta+m_T}.
]


4. Explicit counterexample to the subtractive law


Set


[
r_P=r_Q=r_M=r_U=r_{JP}=r_{JQ}=r_{JU}=r_{\rm Meet}=0
]


and


[
r_{JM}=1.
]


Then


[
s_0=0,\qquad
\Delta=-1,\qquad
m_T=1,\qquad
s_T=0.
]


The subtractive expression gives


[
s_0+\Delta-m_T


0-1-1


-2.
]


Thus the claimed theorem would assert


[
0=-2,
]


which is false.


5. Additional defect in the previous theorem


The previous theorem introduced a separate variable rJT in sT rJP rJQ rMeet rJT, while m depended on rJM and rMeet.


Consequently, even independently of the sign error, the theorem statement did not correctly bind the intended transport quantities.


The corrected theorem uses the same rJU variable consistently.


6. Previous “+m refutation”


The previous source also contained a purported refutation of the additive law.


That refutation is not a valid refutation of


[
s_T=s_0+\Delta+m_T.
]


Its delta invocation substitutes rJP for the rJQ argument and rMeet for the rJM argument, and its alleged correction term is


[
r_{\rm Meet}-r_{\rm Meet}=0.
]


Therefore that example does not test the intended +m_T identity.


It is removed from the corrected ATK.


7. Corrected repository action


The canonical AQ-S9 ATK shall use:


transport_additive


with conclusion


[
s_T=s_0+\Delta+m_T.
]


The old transport_minus theorem shall not remain in the canonical source.


8. Verification status


Established by direct algebra




The additive identity follows by ring normalization.


The subtractive identity is false under the published definitions.


The previous additive refutation was malformed.




Not yet certified




No Lean compiler receipt is claimed by this erratum.


No Mathlib/toolchain build receipt is claimed.


No publication promotion is authorized.




9. Governance decision


ATK: CORRECTED SOURCE REQUIRED

Old transport_minus: KILLED

Old +m refutation: INVALID / REMOVED

Correct transport_additive: CANDIDATE — COMPILATION OPEN

C4: BLOCKED

Publication: BLOCKED

Promotion: BLOCKED until pinned Lean compilation succeeds.

