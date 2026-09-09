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


# AQARION S9 — TRANSPORT ERRATUM

Date: 2026-09-09

Status: CANONICAL CORRECTION · FROZEN · EXACT · NO PROMOTION

Scope:
- S9 cycle-transport identity
- signed definition of the meet-compatibility correction
- synchronization of Lean source, computational verifier, and ledger

---

## 1. Purpose

This document corrects an earlier sign-convention mismatch in the S9 transport documentation.

The earlier documentation defined the correction term with the opposite orientation from the current canonical S9 source.

The mathematical transport identity itself is elementary algebra. The defect was documentation-level: the same symbol `m` had been assigned two opposite meanings in different artifacts.

This document establishes the canonical convention.

---

## 2. Canonical Definitions

Let

    P, Q

be partitions, with

    M = P ∧ Q
    U = P ∨ Q.

Let `J_T(R)` denote the full forward orbit closure of partition `R` under the transformation `T`.

Write

    JP = J_T(P)
    JQ = J_T(Q)
    JM = J_T(M)
    JU = J_T(U).

Define the initial curvature quantity

    s0 = rP + rQ - rM - rU.

Define the transported quantity

    sT = rJP + rJQ - rMeet - rJU,

where

    rMeet = r(JP ∧ JQ).

Define

    Δ =
        (rJP - rP)
      + (rJQ - rQ)
      - (rJM - rM)
      - (rJU - rU).

---

## 3. CANONICAL SIGN CONVENTION

The canonical S9 definition is

    m = rMeet - rJM.

Equivalently,

    m = r(JP ∧ JQ) - r(JM).

This orientation is now frozen.

The canonical transport identity is therefore

    sT = s0 + Δ - m.

---

## 4. Exact Algebraic Verification

Substitution gives

    s0 + Δ - m

    = rP + rQ - rM - rU
      + (rJP-rP)
      + (rJQ-rQ)
      - (rJM-rM)
      - (rJU-rU)
      - (rMeet-rJM)

which simplifies exactly to

    rJP + rJQ - rMeet - rJU

and hence

    sT = s0 + Δ - m.

No dynamical assumption is required for this identity once the quantities are defined.

The Lean implementation verifies this algebra by `ring`.

---

## 5. Opposite Convention

An earlier version used

    m_old = rJM - rMeet.

This is exactly the negative of the canonical quantity:

    m_old = -m.

Under that convention the same identity is

    sT = s0 + Δ + m_old.

Therefore the earlier statement

    sT = s0 + Δ - m_old

was a sign error.

That earlier formulation is RETRACTED.

---

## 6. What Is Corrected

The following interpretation is canonical:

    m = rMeet - rJM

and

    sT = s0 + Δ - m.

Any artifact using

    m = rJM - rMeet

must either:

1. be updated to the canonical orientation, or
2. explicitly rename the quantity, e.g. `m_old` or `m_opposite`.

No artifact may silently use the opposite orientation under the same symbol `m`.

---

## 7. m = 0 Locus

If

    m = 0,

then

    rMeet = rJM

and therefore

    sT = s0 + Δ.

In particular, on the critical locus

    s0 = 1
    m  = 0,

the transport equation becomes

    sT = 1 + Δ.

This is the form used for the current S9 critical-cycle analysis.

---

## 8. Relation to κ_S

For the marked support

    S = {a,b,c}

define

    q_S(R)
      = number of blocks of R intersecting S.

Define

    κ_S
      = q_S(P) + q_S(Q) - q_S(M) - q_S(U).

The currently verified computational statement is:

    on the s0 = 1, m = 0 locus,

    κ_S = Δ.

This equality is NOT asserted globally for every critical pair with m ≠ 0.

The distinction is important.

---

## 9. Verified Computational Scope

Current S9 computational results establish:

- n = 5:
  105 cases with s0 = 1;
  zero cases with m = 0.

- n = 6:
  2,955 cases with s0 = 1;
  57 cases with m = 0;
  κ_S = Δ in all 57 m = 0 cases.

- n = 7:
  82,320 cases with s0 = 1;
  2,979 cases with m = 0;
  κ_S = Δ in all 2,979 m = 0 cases.

- n = 8:
  198,630 critical cases with s0 = 1 and m = 0;
  κ_S = Δ in all 198,630 cases.

For n = 8 the transformed cyclomatic quantity satisfies:

    Γ_T = 1 : 197,550 cases
    Γ_T = 2 :   1,080 cases

with no observed Γ_T < 1 in the audited critical census.

The n = 8 critical census also contains:

    C4 : 178,410
    C6 :  20,220

and no observed critical C8-or-larger cycle class.

These are computationally verified statements, not analytic theorems.

---

## 10. Stronger Verified n = 8 Observation

For all 198,630 n = 8 critical cases,

    image_JT(C)

has

    β = 1.

Thus every audited critical case preserves a projected cycle under the full orbit closure.

This observation is stronger than merely recording survival of some cycle edge.

It remains a computational invariant until independently derived.

---

## 11. Known Negative Result

The equality

    κ_S = Δ

is NOT valid on the entire s0 = 1 locus.

At n = 6 there are 2,592 mismatches.

Observed mismatch categories include:

    Δ=1, κ=0 : 621
    Δ=2, κ=0 : 1002
    Δ=2, κ=1 : 279
    Δ=3, κ=1 : 630
    Δ=4, κ=2 : 60

Therefore the statement

    s0 = 1 ⇒ κ_S = Δ

is RETRACTED.

The surviving restricted statement is

    s0 = 1 ∧ m = 0 ⇒ κ_S = Δ

within the currently audited computational range.

---

## 12. Current Research Target

The next proof target is not another unrestricted equality.

The target is:

    κ_S ≥ 0

on the critical locus,

together with the restricted compatibility identity

    m = 0 ⇒ Δ = κ_S.

If both are established analytically, then

    s0 = 1 ∧ m = 0

implies

    sT = 1 + κ_S ≥ 1.

This is the current C3 research programme.

It is NOT yet promoted to theorem status.

---

## 13. Historical Status

Previous documentation asserting that the current subtractive transport identity was false because

    m = rJM - rMeet

is obsolete.

The current canonical source uses

    m = rMeet - rJM.

Accordingly:

    sT = s0 + Δ - m

is algebraically correct under the current definition.

The remaining work is synchronization of all documentation and verification artifacts.

---

## 14. Evidence Classification

[D]
Definitions of s0, sT, Δ, m, κ_S.

[P]
The transport identity follows by exact algebra from the definitions.

[V]
Finite census results reported above.

[C]
Analytic nonnegativity of κ_S on the full critical locus.

[C]
The marked-incidence structural explanation of the m = 0 equality.

[R]
Finite marked-incidence-core classification as the next proof route.

[RETRACTED]
The unrestricted claim κ_S = Δ for all s0 = 1.

[RETRACTED]
The old sign convention in which `m = rJM - rMeet` was used with the subtractive transport formula.

---

## 15. Canonical Statement

The S9 transport convention is frozen as:

    m := r(J_T(P) ∧ J_T(Q)) - r(J_T(P ∧ Q))

and

    sT = s0 + Δ - m.

This is the canonical convention for all subsequent S9 artifacts.# AQARION S9 — SYNCHRONIZATION LEDGER

Date: 2026-09-09

Governance:
FROZEN · EXACT · NO PROMOTION · CANONICAL

Evidence policy:
[D] Definition
[P] Proved
[V] Computationally verified
[PV] Proved + computationally verified
[C] Conjecture
[R] Research programme
[RETRACTED] False, superseded, or withdrawn

The ledger is the argument.

---

# 1. CANONICAL S9 STATE

## 1.1 Transport convention

[D][P]

The canonical meet-compatibility correction is

    m = rMeet - rJM

where

    rMeet = r(J_T(P) ∧ J_T(Q))
    rJM   = r(J_T(P ∧ Q)).

The canonical transport identity is

    sT = s0 + Δ - m.

The identity is exact algebra.

No dynamical assumptions are required for the identity itself.

---

# 2. SIGN ERRATUM

## 2.1 Historical convention

[RETRACTED]

An earlier artifact used

    m_old = rJM - rMeet

while retaining the subtractive formula

    sT = s0 + Δ - m_old.

That pairing is incorrect.

Because

    m_old = -m,

the corresponding formula under that old orientation would have been

    sT = s0 + Δ + m_old.

---

## 2.2 Canonical replacement

The canonical source now uses

    m = rMeet - rJM

with

    sT = s0 + Δ - m.

All current S9 documents must use this convention.

No silent sign changes are permitted.

---

# 3. TRANSPORT DEFINITIONS

[D]

Let

    M = P ∧ Q
    U = P ∨ Q

and

    JP = J_T(P)
    JQ = J_T(Q)
    JM = J_T(M)
    JU = J_T(U).

Define

    s0 = rP + rQ - rM - rU.

Define

    sT = rJP + rJQ - rMeet - rJU.

Define

    Δ =
        (rJP-rP)
      + (rJQ-rQ)
      - (rJM-rM)
      - (rJU-rU).

Define

    m = rMeet-rJM.

Then

    sT = s0 + Δ - m.

---

# 4. m = 0 SPECIALIZATION

[P]

If

    m = 0,

then

    rMeet = rJM

and

    sT = s0 + Δ.

On the critical locus

    s0 = 1
    m  = 0,

we obtain

    sT = 1 + Δ.

---

# 5. MARKED SUPPORT

[D]

For the 3-cycle support

    S = {a,b,c},

define

    q_S(R)
      = |{B ∈ R : B ∩ S ≠ ∅}|.

Define

    κ_S
      = q_S(P) + q_S(Q) - q_S(M) - q_S(U).

---

# 6. CRITICAL COMPUTATIONAL RESULTS

[V]

## n = 5

    s0 = 1 cases: 105
    m  = 0 cases: 0

No m = 0 critical cases occur.

---

## n = 6

    s0 = 1 cases: 2,955
    m  = 0 cases: 57

On all 57 cases:

    κ_S = Δ.

No negative κ_S was observed.

Critical κ distribution:

    κ=0 : 1,878
    κ=1 : 1,017
    κ=2 :    60

The distribution shown above is for the complete s0=1 population, not only m=0.

---

## n = 7

    s0 = 1 cases: 82,320
    m  = 0 cases: 2,979

On all 2,979 cases:

    κ_S = Δ.

No negative κ_S was observed.

Critical κ distribution:

    κ=0 : 44,238
    κ=1 : 34,170
    κ=2 :  3,912

---

## n = 8

    s0 = 1, m = 0 cases: 198,630

On all 198,630:

    κ_S = Δ.

Distribution:

    κ=0 : 197,550
    κ=1 :   1,080

No negative κ_S was observed.

---

# 7. n = 8 CYCLE RESULT

[V]

For all 198,630 audited critical cases:

    Γ_T = 1 : 197,550
    Γ_T = 2 :   1,080

No Γ_T < 1 was observed.

The critical cycle census is:

    C4 : 178,410
    C6 :  20,220
    C8+ :      0

These are census results, not analytic classification theorems.

---

# 8. PROJECTED-CYCLE INVARIANT

[V]

For every audited n = 8 critical case,

    β(image_JT(C)) = 1.

This is a computationally verified strengthening of the cycle-survival observation.

It does not by itself establish a general theorem for arbitrary n.

---

# 9. GLOBAL κ = Δ CLAIM — KILLED

[RETRACTED]

The unrestricted statement

    s0 = 1 ⇒ κ_S = Δ

is false.

At n = 6:

    mismatches = 2,592.

Observed mismatch categories:

    Δ=1, κ=0 : 621
    Δ=2, κ=0 : 1002
    Δ=2, κ=1 : 279
    Δ=3, κ=1 : 630
    Δ=4, κ=2 : 60

Therefore no global κ=Δ promotion is permitted.

---

# 10. SURVIVING RESTRICTED STATEMENT

[V]

The currently verified restricted statement is:

    s0 = 1 ∧ m = 0
        ⇒ κ_S = Δ

for the audited finite ranges through n = 8.

The computational evidence is strong.

The analytic proof remains OPEN.

---

# 11. CURRENT C3 TARGET

[C][R]

The current mathematical target is:

    κ_S ≥ 0

on the critical locus,

together with

    m = 0 ⇒ Δ = κ_S.

If proved, then

    s0 = 1 ∧ m = 0

gives

    sT
      = s0 + Δ - m
      = 1 + κ_S
      ≥ 1.

This would provide a structural proof of cycle survival on the compatible critical locus.

No such proof is currently promoted.

---

# 12. PROOF ROUTE

[R]

The next route is a finite marked-incidence-core analysis.

Construct the bipartite incidence multigraph

    G(P,Q)

with:

    left vertices  = P-blocks
    right vertices = Q-blocks

and one edge for each ground element x:

    P(x) -- Q(x).

Mark the edges corresponding to

    S = {a,b,c}.

The intended reduction is:

    partition pair
        ↓
    marked incidence graph
        ↓
    support/core reduction
        ↓
    suppression of irrelevant trees/fibres
        ↓
    finite marked core
        ↓
    direct evaluation of κ_S
        ↓
    κ_S ≥ 0.

This route must derive the relevant incidence formula from the actual definitions.

No Euler-characteristic or graphic-matroid interpretation is to be promoted merely because it looks plausible.

---

# 13. INCIDENCE FORMULA — OPEN

[R]

Before a finite-core classification is accepted, derive κ_S exactly from the P/Q incidence data.

Required checks:

1. Determine the exact contribution of marked and unmarked incidence edges.
2. Determine the effect of meet and join on the incidence representation.
3. Identify any fibre-size correction.
4. Verify the resulting formula exhaustively against direct partition calculations.
5. Only then classify marked cores.

This is a proof-development task, not yet a theorem.

---

# 14. OLD LOCAL PLACEMENT MODEL — REJECTED

[RETRACTED]

A bare local placement model based only on cycle vertices is insufficient.

For the 3-cycle:

    C4 local placements = 4^3 = 64
    C6 local placements = 6^3 = 216.

The observed `(m, β)` distributions contain violations of the proposed local implication.

Therefore the state cannot be reduced solely to cycle placement.

Relevant additional information includes:

    off-cycle cells
    fibre attachments
    P/Q incidence
    T-incidence
    T²-incidence
    fixed attachments.

No local-placement theorem should be promoted.

---

# 15. DEFECT OPERATOR STATUS

[D][P]

For

    Q = I-P
    D = QKP,

the current defect algebra includes:

    P Q = 0
    Q P = 0
    P D = 0
    D² = 0
    D P = D
    Q D = D.

Mathematically,

    D Q = 0

also follows immediately:

    DQ
      = QKPQ
      = QK(PQ)
      = 0.

---

# 16. SOURCE SYNCHRONIZATION NOTE

[OPEN]

The current public defect Lean source contains the core defect identities listed above.

The source currently documents DQ=0 in commentary but does not contain a corresponding theorem declaration.

Therefore:

    DQ_zero theorem = OPEN

Recommended addition:

    theorem DQ_zero ...

The theorem should be compiled and independently checked before being marked [PV].

---

# 17. LEAN STATUS

[OPEN]

Lean formalization is not promoted merely because source text exists.

Required publication-grade evidence:

    pinned Lean version
    clean build
    zero `sorry`
    explicit axiom audit
    reproducible command/receipt.

Lean 4.33.1 is an available pin target, but AQARION compilation on that target must be independently executed before claiming [PV].

---

# 18. RANKPAIR STATUS

[OPEN]

`AQ-S9-RANKPAIR.LEAN` is not promoted as a publicly synchronized artifact unless its current source is independently located and checked.

Do not claim successful public synchronization merely from an expected filename or prior local artifact.

---

# 19. CENSUS VERIFIER

[V]

The census verifier checks:

    B2 = 2
    B3 = 5
    B4 = 15
    B5 = 52
    B6 = 203
    B7 = 877
    B8 = 4140
    B9 = 21147

and:

    Σ B_n n^n, n=2..5 = 166483

as well as:

    203 × 6^6

and:

    C(203,2) = 20503
    C(21147,2) = 223587231.

The corrected n=9 pair count is:

    223,587,231.

The previously circulated value

    223,574,931

is incorrect.

---

# 20. GOVERNANCE

The following are frozen:

    canonical m orientation
    canonical transport identity
    evidence labels
    no silent theorem promotion
    no unrestricted κ=Δ claim
    no local-placement classification claim
    Lean OPEN until independently compiled
    public synchronization OPEN where source has not been checked.

---

# 21. CURRENT CLAIM REGISTER

| ID | Claim | Status |
|---|---|---|
| S9-D1 | m = rMeet-rJM | [D] CANONICAL |
| S9-P1 | sT = s0+Δ-m | [P] |
| S9-P2 | m=0 ⇒ sT=s0+Δ | [P] |
| S9-V1 | n=8 critical census = 198,630 | [V] |
| S9-V2 | n=8 Γ distribution 197,550 / 1,080 | [V] |
| S9-V3 | n=8 β=1 for all critical cases | [V] |
| S9-V4 | κ=Δ on n=8 m=0 locus | [V] |
| S9-V5 | κ=Δ on n=6 m=0 locus | [V] |
| S9-V6 | κ=Δ on n=7 m=0 locus | [V] |
| S9-X1 | κ=Δ for all s0=1 | [RETRACTED] |
| S9-X2 | old m orientation with subtractive transport | [RETRACTED] |
| S9-R1 | κ_S ≥ 0 on critical locus | [C] |
| S9-R2 | finite marked-core proof | [R] |
| S9-O1 | DQ_zero Lean theorem | [OPEN] |
| S9-O2 | public RANKPAIR synchronization | [OPEN] |
| S9-O3 | Lean clean-build receipt | [OPEN] |

---

# 22. CANONICAL TRANSPORT BLOCK

For copy/paste into synchronized artifacts:

    M  = P ∧ Q
    U  = P ∨ Q

    JP = J_T(P)
    JQ = J_T(Q)
    JM = J_T(M)
    JU = J_T(U)

    s0 = rP + rQ - rM - rU

    sT = rJP + rJQ - rMeet - rJU

    Δ =
        (rJP-rP)
      + (rJQ-rQ)
      - (rJM-rM)
      - (rJU-rU)

    m = rMeet-rJM

    sT = s0 + Δ - m

This block is canonical.

---

# 23. FINAL S9 POSITION

The S9 transport algebra is no longer blocked by the sign issue.

The sign issue is resolved by freezing:

    m = rMeet-rJM.

The remaining mathematical problem is structural:

    prove or refute κ_S ≥ 0

and explain the verified identity

    m=0 ⇒ κ_S=Δ

through marked incidence geometry.

The next work item is therefore:

    MARKED-INCIDENCE-CORE ATTACK

not another documentation-level sign debate.

Governance remains:

    FROZEN · EXACT · NO PROMOTION · CANONICAL.# AQARION S9 — DELIVERABLE MAP

Date: 2026-09-09

Status:
FROZEN · EXACT · NO PROMOTION · CANONICAL

---

## 1. CANONICAL SOURCE SET

### Transport

`AQ-S9-ATK.LEAN`

Purpose:

    exact algebraic transport identity.

Canonical convention:

    m = rMeet-rJM

Canonical identity:

    sT = s0 + Δ - m

Status:

    [P] algebraically established
    [OPEN] independent clean-build receipt

---

### Defect Algebra

`AQ-S9-DEFECT.LEAN`

Purpose:

    finite-dimensional projection/defect identities.

Current identities:

    PQ = 0
    QP = 0
    PD = 0
    D² = 0
    DP = D
    QD = D

Mathematical consequence still requiring explicit source theorem:

    DQ = 0

Status:

    [P] mathematics
    [OPEN] explicit DQ_zero theorem/build receipt

---

### Census

`VERIFY-CENSUS.PY`

Purpose:

    Bell-number and finite-count sanity checks.

Verified values:

    B2 = 2
    B3 = 5
    B4 = 15
    B5 = 52
    B6 = 203
    B7 = 877
    B8 = 4140
    B9 = 21147

Correct:

    C(21147,2) = 223587231

Status:

    [V]

---

## 2. DOCUMENTATION

### `AQ-S9-TRANSPORT-ERRATA-2026-09-09.MD`

Purpose:

    historical sign correction.

Canonical result:

    m = rMeet-rJM
    sT = s0+Δ-m

Status:

    replacement document.

---

### `AQ-S9-SYNC-LEDGER.MD`

Purpose:

    single synchronization state for S9.

Status:

    canonical replacement.

---

## 3. RESEARCH RESULTS

### Critical n=8 census

Status:

    [V]

Result:

    198630 critical cases

    Γ=1 : 197550
    Γ=2 :   1080

Cycle classes:

    C4 : 178410
    C6 :  20220
    C8+ :     0

Projected-cycle result:

    β(image_JT(C)) = 1

for every audited critical case.

---

## 4. KAPPA STATUS

Definition:

    κ_S
      = q_S(P)+q_S(Q)-q_S(P∧Q)-q_S(P∨Q)

Current verified restricted equality:

    s0=1 ∧ m=0
    ⇒ κ_S=Δ

Current global equality:

    s0=1 ⇒ κ_S=Δ

STATUS:

    [RETRACTED]

Reason:

    2592 mismatches at n=6.

---

## 5. CURRENT C3 PROGRAM

Target:

    κ_S ≥ 0

on the critical locus.

Together with:

    m=0 ⇒ κ_S=Δ

this would imply:

    s0=1 ∧ m=0
    ⇒ sT=1+κ_S≥1.

Status:

    [C] / [R]

No theorem promotion.

---

## 6. NEXT PROOF ATTACK

Use the marked bipartite incidence multigraph:

    left  = P-blocks
    right = Q-blocks
    edge x = (P(x),Q(x))

mark:

    S={a,b,c}.

Then derive, rather than assume, an exact formula for κ_S.

Target pipeline:

    incidence graph
          ↓
    marked support
          ↓
    core reduction
          ↓
    finite marked core
          ↓
    exact κ evaluation
          ↓
    κ≥0

---

## 7. EXCLUDED ROUTES

Do NOT promote:

    κ=Δ globally.

Do NOT promote:

    bare cycle-placement classification.

Do NOT promote:

    publication readiness from computational census alone.

Do NOT promote:

    Lean formalization merely because `.lean` source exists.

Do NOT use:

    old m = rJM-rMeet

under the canonical symbol `m`.

---

## 8. OPEN ITEMS

1. Explicit `DQ_zero` Lean theorem.
2. Clean pinned Lean build.
3. Public synchronization of `AQ-S9-RANKPAIR.LEAN`, only after source verification.
4. Signed manifest synchronization.
5. Independent C3 marked-incidence derivation.
6. Finite marked-core classification.
7. Analytic proof/refutation of κ_S ≥ 0.

---

## 9. GOVERNANCE

Current state:

    FROZEN
    EXACT
    NO PROMOTION
    CANONICAL

The ledger remains authoritative for claim status.import Mathlib

namespace AQARION

def s0 (rP rQ rM rU : ℤ) : ℤ :=
  rP + rQ - rM - rU

def sT (rJP rJQ rMeet rJU : ℤ) : ℤ :=
  rJP + rJQ - rMeet - rJU

def delta
    (rP rQ rM rU rJP rJQ rJM rJU : ℤ) : ℤ :=
  (rJP - rP) +
  (rJQ - rQ) -
  (rJM - rM) -
  (rJU - rU)

-- Canonical S9 convention:
-- mT = r(Meet(JP,JQ)) - r(JM)
def mT (rJM rMeet : ℤ) : ℤ :=
  rMeet - rJM

theorem transport_identity
    (rP rQ rM rU rJP rJQ rJM rJU rMeet : ℤ) :
    sT rJP rJQ rMeet rJU =
      s0 rP rQ rM rU +
      delta rP rQ rM rU rJP rJQ rJM rJU -
      mT rJM rMeet := by
  unfold s0 sT delta mT
  ring

theorem transport_identity_m_zero
    (rP rQ rM rU rJP rJQ rJM rJU rMeet : ℤ)
    (hm : rMeet = rJM) :
    sT rJP rJQ rMeet rJU =
      s0 rP rQ rM rU +
      delta rP rQ rM rU rJP rJQ rJM rJU := by
  unfold sT s0 delta
  rw [hm]
  ring

end AQARION

Computational observations remain [V] until converted into mathematical proof.

Conjectures remain [C].

Research routes remain [R].

Historical false statements remain [RETRACTED].
