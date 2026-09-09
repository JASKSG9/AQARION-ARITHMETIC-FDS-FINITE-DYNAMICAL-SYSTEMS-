AQARION S9 — TRANSPORT ERRATA


Date: 2026-09-09

Governance: FROZEN · EXACT · NO PROMOTION · CANONICAL

C4: BLOCKED

Publication: BLOCKED

Lean certification: OPEN


1. Critical transport correction


The previous S9 transport artifact contained two semantic inconsistencies.


First, it asserted a subtractive transport identity while defining


[
m_T=r_{JM}-r_{\mathrm{Meet}}.
]


Second, the target quantity s_T used a rank variable r_{JT}, while the increment \Delta used r_{JU}.


Therefore the previous theorem was not established by its definitions.


2. Exact relation under the previous definitions


The previous definitions imply


[
s_0=r_P+r_Q-r_M-r_U,
]


[
\Delta=
(r_{JP}-r_P)+(r_{JQ}-r_Q)
-(r_{JM}-r_M)-(r_{JU}-r_U),
]


[
m_T=r_{JM}-r_{\mathrm{Meet}},
]


and


[
s_T=r_{JP}+r_{JQ}-r_{\mathrm{Meet}}-r_{JT}.
]


Consequently,


[
s_T


s_0+\Delta+m_T+(r_{JU}-r_{JT}).
]


Thus neither


[
s_T=s_0+\Delta-m_T
]


nor, without an additional identification,


[
s_T=s_0+\Delta+m_T
]


follows from the previous source.


3. Canonical repair


The canonical S9 artifact now defines


[
s_T=r_{JP}+r_{JQ}-r_{\mathrm{Meet}}-r_{JU}.
]


The canonical correction remains


[
m_T=r_{JM}-r_{\mathrm{Meet}}.
]


Therefore the exact canonical identity is


[
\boxed{
s_T=s_0+\Delta+m_T.
}
]


An equivalent opposite-sign convention is


[
m_{\mathrm{opp}}


r_{\mathrm{Meet}}-r_{JM}


-m_T,
]


under which


[
\boxed{
s_T=s_0+\Delta-m_{\mathrm{opp}}.
}
]


These are the same identity under opposite definitions of the correction variable.


4. Critical locus


When


[
m_T=0,
]


the canonical transport identity reduces to


[
\boxed{
s_T=s_0+\Delta.
}
]


This preserves the critical-locus algebra provided all downstream computations use the canonical signed definition.


5. Status of the previous ATK artifact


The previous transport_minus theorem is not accepted as certified.


The previous +m refutation is also rejected because its argument list does not represent the intended transport identity.


Disposition:


[
\boxed{\text{PREVIOUS ATK TRANSPORT QUARANTINED}}
]


6. Census correction


The independent census arithmetic is unaffected.


[
2(2^2)+5(3^3)+15(4^4)+52(5^5)









]


Therefore


[
\boxed{166483\text{ VERIFIED}}
]


and the earlier value 166479 is rejected.


Also,


[
\binom{203}{2}=20503,
]


[
\binom{21147}{2}=223587231.
]


7. Governance


This erratum promotes no theorem.


C3 remains OPEN.


C4 remains BLOCKED.


Publication remains BLOCKED.


Lean certification remains OPEN.


Ledger is the argument.

