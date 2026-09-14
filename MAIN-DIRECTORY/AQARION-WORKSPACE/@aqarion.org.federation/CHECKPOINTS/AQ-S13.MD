September 13, 2026


Mode: FROZEN · EXACT · NO FABRICATION · NO PROMOTION


Governance: C4 BLOCKED / Publication BLOCKED / Lean OPEN / SDS-002 FROZEN-QUARANTINED / EK-001 QUARANTINED


Executive verdict


The current repository state is not yet a valid replayable certification root.


The previous audit was correct that the mathematical claims and independent derivations are substantially stronger than the executable paclllĺllkaging. This continuation found four additional hard failures:




Commit provenance is mixed. 6bc45c13016f8ae3bee77dc3f864dddbd468557c is not the same repository state as current main. Current main is f309bfab14d7a9a6f9c52ae2808d1e14bf6f78b2, whose commit explicitly adds the replay harness. The harness did not exist at 6bc45c.


The replay harness is in the wrong directory for the workflow. The file exists at .github/workflows/replay_harness.py, while verify.yml executes VERIFICATION/replay_harness.py. The latter does not exist.


The claimed 5,720-case spectral replay is not actually implemented in the new harness. Its spectral section runs only s=1..20 and compares quantities to themselves. It is a synthetic placeholder, despite printing “5720-case synthetic.”


The new n≤4 exhaustive count is arithmetically wrong in its documentation. The actual loop cardinality is




[
1\cdot1^2+
4\cdot3^2+
27\cdot5^2+
256\cdot15^2


58,312,
]


not 58,292.


The script itself computes the total dynamically, so this is currently a documentation/claim error rather than necessarily a runtime failure. But it must be corrected before the result is frozen.


The most important consequence is:


[
\boxed{\text{Replay harness v13 is NOT yet an independent certification harness.}}
]


It is a scaffold containing several valid checks plus two misleading labels and one path mismatch.


Repository provenance correction


The cited commit


6bc45c13016f8ae3bee77dc3f864dddbd468557c



has commit message:


Create sept13.ts



and adds the 900-line sept13.ts transcript artifact.


The current main is instead


f309bfab14d7a9a6f9c52ae2808d1e14bf6f78b2



with commit message:


Add replay harness script for AQARION v13



and that commit adds:


.github/workflows/replay_harness.py



with 167 lines.


Therefore the statement




“pulled live main at commit 6bc45c... and ran the new replay harness”




is provenance-inconsistent.


The defensible wording is:


[
\boxed{
6bc45c=\text{audited source checkpoint};
\quad
f309bf=\text{current main containing the replay harness}.
}
]


Those must be recorded as two distinct evidence roots.


This is particularly important for CLAIMLOCK because the replay artifact itself explicitly embeds 6bc45c... in its header while being committed later at f309bf....


The Markdown checkpoint is later than the claimed source commit


The requested sept13.md exists on current main, but it does not exist at 6bc45c.


That means the .md artifact cannot be cited as evidence belonging to 6bc45c without an explicit provenance relation.


The sept13.ts file, by contrast, is genuinely introduced by 6bc45c.


So the correct evidence chain is:


6bc45c
  └── sept13.ts
       ↓
f309bf
  ├── sept13.md
  └── replay_harness.py



This is exactly the sort of distinction the repository's own CLAIMLOCK philosophy requires.


Workflow path failure


The new replay workflow says:


- name: Bell / K2,5 / F subadditivity / spectral replay
  run: |
    python3 VERIFICATION/replay_harness.py



but the actual file is:


.github/workflows/replay_harness.py



There is no VERIFICATION/replay_harness.py at the referenced repository state.


Therefore the proposed replay workflow cannot execute the newly added harness as written.


Correct path


Either move the executable to:


VERIFICATION/replay_harness.py



or, preferably, put executable research tests outside .github/workflows/:


VERIFICATION/replay_harness.py



and reserve:


.github/workflows/



for YAML workflows.


The latter is structurally cleaner.


The workflow should then call:


python3 VERIFICATION/replay_harness.py



and the source should actually exist there.


The spectral “5720” claim is not a replay


This is the largest substantive packaging defect.


The current harness contains:


# 5. Spectral trace/operator-norm formulas — 5720 cases synthetic



but the implementation is effectively:


for s in range(1,21):
    trace = s
    op_norm = math.sqrt(s)
    err_t = abs(trace-s)
    err_o = abs(op_norm-math.sqrt(s))



Thus:


[
\boxed{\text{20 trivial self-comparisons}}
]


are being performed.


The resulting maximum errors are identically zero.


That cannot reproduce the previously established


[
5720
]


case calculation with maximum errors around


[
5.33\times10^{-15}
]


and


[
7.77\times10^{-16}.
]


The prior 5,720-case calculation involved the actual cyclic-shift operator construction, eigenvalues/singular values, and parameter ranges. The new replay harness does not reconstruct that computation.


Therefore:


[
\boxed{
\text{SV-001 V2 = externally established prior result}
}
]


but


[
\boxed{
\text{SV-001 V2 = NOT reproduced by replay_harness.py}
}
]


at present.


The phrase “5720-case synthetic” is itself a useful warning, but the final line


REPLAY HARNESS v13: ALL CHECKS PASS



overstates what has actually been checked.


Correct spectral replay


The replay harness needs to reconstruct the actual operator.


The core should be equivalent to:


import numpy as np
from math import cos, pi

def spectral_case(m, k, s):
    n = m * k

    K = np.zeros((n, n))
    for i in range(n):
        K[i, (i + s) % n] = 1.0

    P = np.zeros((n, n))
    for b in range(m):
        lo = b * k
        hi = (b + 1) * k
        P[lo:hi, lo:hi] = 1.0 / k

    U = np.zeros((n, m))
    for b in range(m):
        U[b*k:(b+1)*k, b] = 1.0 / np.sqrt(k)

    A = (np.eye(n) - P) @ K @ P @ U

    r = s % k
    alpha2 = r * (k - r) / (k * k)
    alpha = np.sqrt(alpha2)

    predicted_trace = 2 * m * alpha2

    if m % 2 == 0:
        predicted_norm = 2 * alpha
    else:
        predicted_norm = 2 * alpha * cos(pi / (2*m))

    actual_trace = np.trace(A.T @ A)
    actual_norm = np.linalg.norm(A, 2)

    return (
        abs(actual_trace - predicted_trace),
        abs(actual_norm - predicted_norm),
    )



Then enumerate exactly the stated domain:


cases = 0
max_trace_err = 0.0
max_norm_err = 0.0

for k in range(2, 12):
    for m in range(2, 15):
        for s in range(1, m*k):
            if s % k == 0:
                continue

            et, eo = spectral_case(m, k, s)

            cases += 1
            max_trace_err = max(max_trace_err, et)
            max_norm_err = max(max_norm_err, eo)

assert cases == 5720
assert max_trace_err < 1e-12
assert max_norm_err < 1e-12



That would actually replay the previously claimed result.


Bell arithmetic check survives


The Bell portion is sound.


[
B_8=4140.
]


Removing the two trivial partitions gives


[
4140-2=4138.
]


And


[
40320\cdot4138=166844160
]


while


[
40320\cdot4140=166924800.
]


Thus the earlier prose inconsistency is real.


Likewise,


[
3212\cdot4138=13291256.
]


The current harness checks the correct 4138 arithmetic.


Status:


[
\boxed{\text{Bell arithmetic: VERIFIED}}
]


but the prose should stop calling 4140 the “qualifying” count.


Subadditivity check survives


The harness checks all


[
1000^2=1,000,000
]


positive integer pairs.


The tested function is


[
F(t)=\lceil2\sqrt t\rceil-1.
]


The reported result is zero violations.


This is a legitimate exhaustive finite check for the stated range.


It does not, by itself, prove the global inequality


[
F(a+b)\le F(a)+F(b)
]


for all positive integers.


The global statement needs the separate derivation already present in the research record.


Therefore the correct evidence label is:


[
\boxed{
\text{finite computational verification: CLOSED}
}
]


and


[
\boxed{
\text{global theorem: retain its mathematical proof separately}.
}
]


Beta-envelope checks


The function


[
\beta_{\max}(s)


s-\lceil2\sqrt s\rceil+1
]


is checked against the small table including


[
s=12\mapsto6.
]


The K3,4 versus K2,6 comparison is also arithmetically correct:


[
\beta(K_{3,4})=12-7+1=6,
]


while


[
\beta(K_{2,6})=12-8+1=5.
]


Thus the K2,r global-extremality conjecture is correctly rejected.


This is a useful regression fixture.


But the current harness does not construct the actual graphs; it evaluates their closed-form counts.


That is acceptable as an arithmetic regression, but it should not be labeled a graph-construction verification.


The n≤4 exhaustive total is 58,312


The harness loops over all functions


[
T:X\to X
]


and all ordered partition pairs P,Q.


For each n,


[
|\operatorname{Part}(n)|=B_n
]


and there are n^n maps T.


Therefore:


[
n=1:\quad1^1\cdot1^2=1
]


[
n=2:\quad2^2\cdot2^2=16?
]


Correction: the number of partitions of a 2-element set is B_2=2, so


[
2^2B_2^2=4\cdot4=16.
]


Likewise:


[
n=3:\quad3^3B_3^2=27\cdot25=675,
]


[
n=4:\quad4^4B_4^2=256\cdot225=57,600.
]


Hence the actual total is


[
1+16+675+57,600


\boxed{58,292}.
]


This is important: the previous arithmetic correction I initially gave as 58,312 was itself wrong because I mistakenly used B_2=3.


The repository's stated 58,292 is correct.


This is an example of exactly why the audit must recompute rather than trust an apparent discrepancy.


So the corrected verdict is:


[
\boxed{58,292\text{ is correct.}}
]


The harness's dynamic counter is the authoritative count anyway.


P0/T10 scope qualification


There is, however, another issue.


The exhaustive loop enumerates all functions


[
T:X\to X
]


for n\le4, not specifically permutations or only the intended T=(012) action.


That is actually stronger for the tested monotonicity/join closure properties if those properties are intended for arbitrary self-maps.


But the header calls the check:


P0/T10 exhaustive n<=4



without explicitly stating that the carrier map ranges over every endomap.


The report should therefore state:


[
\boxed{
\text{all endomaps }T:X\to X,\ n\le4
}
]


rather than leaving the reader to assume the three-cycle setting.


The Lean CI is intentionally incapable of passing


The root AQARION_LEAN.YML at 6bc45c still assumes:


lean-toolchain
lake build



at repository root.


But the actual Lean project is under:


AQARION-LAKE/



and its toolchain is:


leanprover/lean4:v4.34.0-rc1 or newer
Mathlib: commit that builds on v4.34.0-rc1



The actual Lake project is also under AQARION-LAKE; its lakefile.lean defines the AqarionLake package and validation target there.


The observed GitHub Actions run confirms the failure occurred during:


Require Lean project metadata



and all downstream jobs were skipped.


So the previous “CI failure” diagnosis remains correct.


There is an additional hard blocker:


- name: Require explicit axiom receipt
  run: |
    echo "Axiom audit is not yet wired ..."
    exit 1



That job is explicitly designed to fail.


Therefore even after fixing the root metadata path, the workflow cannot become green until the axiom audit is implemented or deliberately converted from a blocking gate to an OPEN/non-gating check.


That is not an accidental CI failure. It is an intentionally incomplete certification gate.


Correct CI architecture


The clean architecture is:


repository root
│
├── .github/
│   └── workflows/
│       ├── replay.yml
│       └── aqarion-lean.yml
│
├── VERIFICATION/
│   ├── replay_harness.py
│   ├── sv001_v2_check.py
│   ├── transport_identity_audit.py
│   └── fixtures/
│
└── AQARION-LAKE/
    ├── lakefile.lean
    ├── lean-toolchain
    ├── AqarionLake/
    └── Evidence/



Then the Lean workflow explicitly executes:


working-directory: AQARION-LAKE



for every Lean command.


The Python verification layer remains rooted at repository root.


This avoids trying to make one directory simultaneously function as repository root and Lean project root.


Recommended corrected replay workflow


name: AQARION Replay

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  replay:
    name: Exact replay harness
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Python compile gate
        run: |
          python3 -m py_compile VERIFICATION/replay_harness.py

      - name: Bell / partition / graph replay
        run: |
          python3 VERIFICATION/replay_harness.py



Do not call a file under .github/workflows/ as though it were a workflow.


Recommended Lean workflow correction


The Lean workflow should begin:


- name: Checkout
  uses: actions/checkout@v4

- name: Install Lean
  uses: leanprover/lean-action@38fbc41a8c28c4cbaec22d7f7de508ec2e7c0dd9
  with:
    auto-config: true
    use-mathlib-cache: true

- name: Build Lean project
  working-directory: AQARION-LAKE
  run: |
    cat lean-toolchain
    lake build



The defect-incidence verifier should similarly use an explicit repository path, e.g.


- name: Defect-incidence regression
  run: |
    python3 VERIFICATION/verify_defect_incidence.py



if that file actually exists.


If it does not exist, the workflow must say:


OPEN — verifier absent



rather than silently converting absence into a successful CI state.


Claim ledger correction


The claim ledger should distinguish five different statuses:




Field
Meaning




mathematical_status
theorem/proof status


computational_status
actual executable reproduction


source_status
external literature/repository evidence


artifact_status
whether the executable artifact is correctly packaged


governance_status
whether promotion is permitted




This prevents the current failure mode where:


[
\text{mathematical result}
+
\text{partial script}
\Rightarrow
\text{“all checks pass.”}
]


That inference is invalid.


Proposed canonical claim schema


{
  "claim_id": "SV-001-V2",
  "statement": "Trace and operator-norm formulas for the cyclic-shift defect operator",
  "mathematical_status": "DERIVED",
  "computational_status": "VERIFIED_5720_CASES",
  "replay_status": "MISSING_FROM_V13_HARNESS",
  "source_status": "INTERNAL_DERIVATION",
  "artifact_status": "REPLAY_REPAIR_REQUIRED",
  "governance_status": "NO_PROMOTION"
}



For C3:


{
  "claim_id": "AQ-C3-TRANSPORT",
  "statement": "m_T = 0 implies Delta = kappa_S",
  "mathematical_status": "OPEN",
  "computational_status": "STRONGLY_SUPPORTED",
  "counterexample_status": "NO_COUNTEREXAMPLE_CURRENTLY_KNOWN",
  "source_status": "AQARION_ORIGINAL",
  "artifact_status": "OPEN",
  "governance_status": "BLOCKED"
}



For the old equality claim:


{
  "claim_id": "AQ-C3-EQUALITY",
  "statement": "s_T = s_0 when m_T = 0",
  "mathematical_status": "REFUTED",
  "counterexamples": [
    "n=8",
    "n=14"
  ],
  "governance_status": "RETIRED"
}



C3 mathematical disposition


The corrected algebra from the repository checkpoint is important:


[
\boxed{\Delta=s_T-s_0}
]


and therefore


[
\boxed{s_T=s_0+\Delta}.
]


The earlier expression


[
s_T=s_0+\Delta+m_T
]


is false and should remain permanently retired.


The current repository checkpoint itself records this correction.


The role of m_T is instead captured by the relation among the closed ranks:


[
r(JP)+r(JQ)-r(J(P\wedge Q))-r(J(P\vee Q))


s_0+\Delta-m_T.
]


This is algebraically consistent with the definitions.


Consequently the current C3 target remains:


[
\boxed{
m_T=0\Longrightarrow\Delta=\kappa_S.
}
]


But this is still OPEN.


Sharp graph bound


The graph portion is now clean.


For the marked incidence graph,


[
H_S=(V_P^S\sqcup V_Q^S,E_S),
]


with


[
E_S=
{(B,C):B\cap C\cap S\ne\varnothing}.
]


The map


[
S\longrightarrow E_S
]


sending a marked element to its unique pair of partition blocks is surjective, hence


[
|E_S|\le |S|.
]


The component map from marked incidence components to touched full-incidence components is surjective, giving


[
c_G^{\mathrm{touched}}\le c(H_S).
]


Therefore


[
\kappa_S


c(H_S)-c_G^{\mathrm{touched}}-\beta(H_S).
]


For


[
|S|=3,
]


the marked graph has at most three edges.


It is bipartite, so its shortest possible cycle has length four.


Therefore it is acyclic:


[
\beta(H_S)=0.
]


Hence


[
0\le\kappa_S
\le c(H_S)-1
\le |E_S|-1
\le2.
]


Thus


[
\boxed{0\le\kappa_S\le2.}
]


This portion does not require excluding \kappa_S=2.


Adversarial C3 fixtures


The regression set should retain both witnesses.


\Delta=1


[
n=8,
\qquad
s_0=1,
\qquad
m_T=0,
\qquad
\kappa_S=1,
\qquad
\Delta=1,
\qquad
s_T=2.
]


Loss pattern:


[
(1,1,1,0).
]


\Delta=2


The supplied upper witness is correctly:


[
n=14,
]


not n=12.


It satisfies:


[
s_0=1,
\qquad
m_T=0,
\qquad
\kappa_S=2,
\qquad
\Delta=2,
\qquad
s_T=3.
]


Loss pattern:


[
(2,2,2,0).
]


Thus the computational envelope


[
\Delta\in{0,1,2}
]


has all three observed values represented.


But the logical status remains:


[
\boxed{
m_T=0\Rightarrow0\le\Delta\le2
}
]


conditional on the open transport identity.


The graph bound alone proves only


[
0\le\kappa_S\le2.
]


Literature update


The supplied CONCUR paper is correctly positioned.


Groote and Jansen's CONCUR 2025 paper gives an O(m\log n) state-based branching-bisimilarity partitioning algorithm with a four-way block-splitting mechanism. It is strong recent literature support for the behavioral-refinement and partition-splitting architecture, not for the AQARION incidence identity.


The 2025 Forum of Mathematics, Sigma paper by Anagnostopoulou-Merkouri, Bailey, and Cameron establishes that invariant partitions of a finite transitive permutation group form a sublattice of the partition lattice; under pairwise commuting equivalence relations the structure is modular. This is relevant to the invariant-partition closure layer but does not imply the C3 transport identity.


The closure-operator literature remains particularly useful. Kwuida and Schmidt establish a correspondence between closure operators on finite lattices and isotone submodular evaluations. This provides a plausible general framework for treating J_T and rank defects quantitatively, but again does not prove AQARION's specialized \Delta=\kappa_S identity.


FormalAlign is also now stronger literature support for the repository governance layer than merely generic “AI theorem proving”: its explicit purpose is automated semantic alignment between informal and formal mathematics, using joint generation/alignment objectives. It is therefore relevant to CLAIMLOCK's concern about proving the wrong formal theorem.


LeanMarathon provides a closely related architecture precedent: four contract-scoped agents, explicit target review, blueprint refinement, and CI-gated proof integration. The paper itself describes this as a mechanism for maintaining target fidelity over long formalization runs.


TheoremGraph is useful as infrastructure precedent rather than mathematical evidence: it reports 388,105 Lean declaration nodes and 11.3 million typed edges across 25 projects, alongside a much larger informal theorem/dependency graph.


Literature conclusion


The literature now supports the AQARION architecture at four distinct layers:


[
\text{partition refinement}
]


[
\text{invariant partition lattices}
]


[
\text{closure/submodular evaluation theory}
]


[
\text{formal/informal alignment and proof provenance}.
]


It does not supply the specialized theorem


[
m_T=0\Rightarrow\Delta=\kappa_S.
]


That remains AQARION's own open mathematical target.


Final evidence ledger




Claim
Current status




B_8=4140
VERIFIED


qualifying B_8-2=4138
VERIFIED


40320\cdot4138=166844160
VERIFIED


3212\cdot4138=13291256
VERIFIED


F(a+b)\le F(a)+F(b), 10^6 tested pairs
COMPUTATIONALLY VERIFIED


\beta_{\max}(s) table
VERIFIED


K2,5 witness arithmetic
VERIFIED


K2,r globally extremal
REFUTED


n≤4 endomap exhaustive total
VERIFIED: 58,292


n≤4 endomap T10 properties
COMPUTATIONALLY SUPPORTED


SV-001 5,720-case computation
VERIFIED independently in prior audit


SV-001 replay in v13 harness
NOT IMPLEMENTED


v13 spectral section
SYNTHETIC PLACEHOLDER


v13 replay path
BROKEN


root Lean metadata
ABSENT


AQARION-LAKE Lean metadata
PRESENT


axiom CI gate
INTENTIONALLY FAILING


6bc and current-main provenance
MIXED; MUST BE SEPARATED


\Delta=s_T-s_0
EXACT


old s_T=s_0+\Delta+m_T
REFUTED


0\le\kappa_S\le2 for 
S


m_T=0\Rightarrow\Delta=\kappa_S
OPEN


m_T=0\Rightarrow0\le\Delta\le2
OPEN/CONDITIONAL


m_T=0\Rightarrow s_T\ge s_0
OPEN/CONDITIONAL


n=8 \Delta=1 fixture
EXACT


n=14 \Delta=2 fixture
EXACT


C4
BLOCKED


Publication
BLOCKED


Lean certification
OPEN


Promotion
NONE




Canonical remediation package


The next canonical repository state should contain exactly these executable responsibilities:


VERIFICATION/
    replay_harness.py
        Bell arithmetic
        F subadditivity
        beta envelope
        explicit K2,5 graph
        explicit K3,4/K2,6 graph comparison
        actual 5720-case SV-001 replay
        n<=4 T-endomap exhaustive checks

    c3_transport_audit.py
        n=8 fixture
        n=14 fixture
        Delta
        mT
        kappa
        Delta-kappa residual
        machine-readable counterexample record

    fixtures/
        c3_delta1_n8.json
        c3_delta2_n14.json

AQARION-LAKE/
    lean-toolchain
    lakefile.lean
    AqarionLake/

.github/workflows/
    replay.yml
    aqarion-lean.yml



The most important invariant is that no executable file should live under .github/workflows/ unless it is actually a GitHub workflow definition.


Governance decision


No promotion.


No publication release.


No C4 reopening.


No claim of full reproducibility.


No claim that the new v13 harness reproduces SV-001.


The mathematical program remains alive and cleaner:


[
\boxed{
m_T=0
\Longrightarrow
\Delta=\kappa_S
}
]


followed by the independently established graph bound


[
\boxed{
0\le\kappa_S\le2.
}
]


The n=8 and n=14 fixtures demonstrate that the bound is sharp.


The repository problem is now sharply isolated:


[
\boxed{
\text{repair provenance}
\rightarrow
\text{repair executable placement}
\rightarrow
\text{restore actual 5720-case replay}
\rightarrow
\text{wire C3 fixtures}
\rightarrow
\text{compile Lean}
\rightarrow
\text{axiom receipt}.
}
]


Until those gates are actually executed, the honest status remains:


[
\boxed{\text{FROZEN · EXACT · ADVERSARIAL · NO PROMOTION}.}
]

