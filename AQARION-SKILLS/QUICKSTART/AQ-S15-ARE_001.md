AQARION QUICK START AQ-S15-ARE-001.MD


   AQARION RESEARCH 
              ┌─────────────────────────┐
              │   RESEARCH ENGINE        │
              │                           │
              │  ASK → DESIGN → RUN      │
              │       ↓                  │
              │  CHECK → REPLAY →        │
              │  CERTIFY → LEARN         │
              └────────────┬────────────┘
                           │
       ┌───────────────────┼───────────────────┐
       ↓                   ↓                   ↓
    SKILLS             CLAIMLOCK           REPLAY LAB
       │                   │                   │
       └────────────┬──────┴───────┬──────────┘
                    ↓              ↓
                 EVIDENCE       FORMALIZATION
                    │              │
                    └──────┬───────┘
                           ↓
                    RESEARCH STATE
                           ↓
                    NEXT QUESTION



That last arrow is the part you're currently missing.



The central object should NOT be a theorem


It should be a:


RESEARCH CASE


A case is an executable unit of scientific inquiry.


For example:


CASE: AQ-S15-DIFF-LATTICE-001

Question:
    When does the equal-margin fluctuation operator lose rank?

Objects:
    M
    C
    ker_Z(C)

Hypothesis:
    det(C)=0 characterizes lost fluctuation modes.

Skills:
    exact_rank
    smith_normal_form
    integer_kernel
    contingency_analysis

Experiments:
    census_k3
    census_k4
    nullspace_growth
    adversarial_counterexamples

Claims:
    S15-001
    S15-002
    S15-003

Replay:
    exact
    independent
    negative_control

Formalization:
    Lean status

Evidence:
    hashes
    inputs
    outputs
    environment

Current state:
    SUPPORTED / OPEN / REFUTED / FORMALIZED

Next question:
    Does ker_Z(C) admit a combinatorial characterization?



Now everything you already built has somewhere to plug in.



The key idea: AQARION becomes a loop


Instead of:


Theorems/
Proofs/
Scripts/
Experiments/



you get:


                 ┌──────────────┐
                 │   QUESTION   │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │   HYPOTHESIS │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │    SKILLS    │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │   EXECUTE    │
                 └──────┬───────┘
                        ↓
              ┌────────────────────┐
              │ ADVERSARIAL CHECK  │
              └─────────┬──────────┘
                        ↓
                 ┌──────────────┐
                 │    REPLAY    │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │   EVIDENCE   │
                 └──────┬───────┘
                        ↓
             ┌─────────────────────┐
             │ CLAIMLOCK DECISION  │
             └──────────┬──────────┘
                        ↓
              ┌────────────────────┐
              │ FORMAL / COMPUTE  │
              └─────────┬──────────┘
                        ↓
                 ┌──────────────┐
                 │ RESEARCH     │
                 │ STATE        │
                 └──────┬───────┘
                        ↓
                 NEXT QUESTION
                        │
                        └──────────→



That is much more than proofs.



I would call the new layer RESEARCH ENGINE


And make it extremely small initially.


AQARION/
│
├── RESEARCH-ENGINE/
│   ├── README.md
│   ├── CASE-SCHEMA.md
│   ├── CASE-STATE.md
│   ├── EXECUTION-PROTOCOL.md
│   ├── EVIDENCE-PROTOCOL.md
│   ├── REPLAY-PROTOCOL.md
│   └── NEXT-QUESTION.md
│
├── SKILLS/
│
├── CLAIMLOCK/
│
├── REPLAY-LAB/
│
├── FORMAL/
│
└── CASES/
    ├── S15-DIFF-LATTICE-001/
    ├── FGR-001/
    ├── TRANS-001/
    └── ...



Notice what happened:


Theorem files remain.


But they are no longer the architecture.


The case becomes the unit of research.



And there is an even better abstraction


Every case should have five layers:


              AQARION CASE
                   │
       ┌───────────┼───────────┐
       ↓           ↓           ↓
    QUESTION     CLAIM       OBJECT
       │           │           │
       └───────────┼───────────┘
                   ↓
                ACTIONS
                   │
       ┌───────────┼───────────┐
       ↓           ↓           ↓
     SKILLS      TOOLS       EXPERIMENTS
       │           │           │
       └───────────┼───────────┘
                   ↓
                RESULTS
                   ↓
             ADVERSARIAL TEST
                   ↓
                 REPLAY
                   ↓
                EVIDENCE
                   ↓
              CLAIMLOCK
                   ↓
             FORMAL STATUS
                   ↓
              RESEARCH STATE



That means a skill isn't just documentation.


A skill becomes an executable research capability.


A claim isn't just a statement.


A claim becomes something the engine can interrogate.


A replay isn't just a script.


It becomes a reproducibility event.



The really novel part: STATE


I'd make this the heart of the system.


Every research case has a machine-readable state:


QUESTION
    ↓
HYPOTHESIS
    ↓
DESIGNED
    ↓
EXECUTED
    ↓
ADVERSARIAL
    ↓
REPLAYED
    ↓
SUPPORTED
    ↓
FORMALIZATION_OPEN
    ↓
FORMALIZED
    ↓
LOCKED



But branches are allowed:


                ┌→ REFUTED
                │
HYPOTHESIS ─────┼→ OPEN
                │
                └→ SUPPORTED
                       │
                       ├→ FORMALIZATION_FAILED
                       │
                       └→ FORMALIZED



And critically:


REFUTED is not failure.


It is a valid research state.


That means AQARION records:




what survived




and




what died




and why.


That's substantially more powerful than a theorem folder.



Your S15 work becomes the first flagship case


For example:


S15-DIFF-LATTICE-001



Question


When does an equal-margin multiplicity operator lose fluctuation information?


Discovery


\[

M\mathbf1=n\mathbf1,\qquad

M^T\mathbf1=n\mathbf1

\]


implies


\[

M\cong[n]\oplus C.

\]


Exact object


\[

C_{ij}=M_{ij}-M_{ik}.

\]


Certificate


\[

Cw=0

\]


and


\[

v=(w,-\mathbf1^Tw).

\]


Computational evidence


Exact censuses.


Adversarial result


Small primitive null vectors are not universal.


New discovery


\[

v_t=(1,-(3t+2),3t+1)

\]


gives unbounded certificate height for \(k=3\).


New question


What controls the integer kernel lattice?


Next skill


INTEGER-KERNEL-ANALYZER


Next experiment


SNF/HNF classification.


Next formal target


equal_margin
       ↓
difference_invariant
       ↓
block_decomposition
       ↓
kernel_equivalence
       ↓
integer_certificate



That's a living research object.



Then CLAIMLOCK changes role


Currently you're thinking of ClaimLock as the place where claims live.


I'd elevate it to:


CLAIMLOCK = scientific state machine


A claim should have something like:


claim:
  id: AQ-S15-DIFF-001

statement:
  ...

type:
  theorem | conjecture | empirical | computational | definition

depends_on:
  - ...

required_skills:
  - exact_linear_algebra

experiments:
  - ...

negative_controls:
  - ...

replays:
  - ...

formalization:
  lean: OPEN

evidence:
  execution_hash: ...

status:
  SUPPORTED

promotion:
  blocked: true

failure_conditions:
  - ...

next_question:
  ...



Now ClaimLock isn't merely a registry.


It's the governor of the research engine.



REPLAY LAB becomes the experimental memory


This is another important distinction.


Don't let Replay Lab merely answer:




“Can I run the script again?”




Instead:




“Can another execution reproduce the evidentiary state associated with this claim?”




That means a replay records:


CASE
CLAIM
INPUT
CODE
SKILL VERSION
ENVIRONMENT
SEED
EXECUTION
OUTPUT
HASH
NEGATIVE CONTROL
COMPARISON
RESULT



And then:


REPLAY PASS
REPLAY FAIL
REPLAY DRIFT



This plugs directly into the provenance work we've already been developing.



And SKILLS become capabilities


This is where your system gets genuinely interesting.


Instead of:


skill = instructions



make:


skill =
    capability
    + inputs
    + outputs
    + validation
    + failure modes
    + provenance



Example:


SKILL:
    EXACT-KERNEL

INPUT:
    integer matrix C

OUTPUT:
    rank
    nullity
    primitive integer basis
    SNF
    certificate

VALIDATORS:
    Cw = 0
    gcd(w) = 1
    basis independence

FAILURE MODES:
    rational/integer confusion
    nonprimitive basis
    incorrect rank

REPLAY:
    deterministic



Now an AI agent can actually use skills as tools, rather than merely reading them.



This creates an AI research agent without making the AI the authority


This is important.


The architecture should be:


              AI AGENT
                  │
                  ↓
            chooses SKILL
                  │
                  ↓
             executes
                  │
                  ↓
             produces
              EVIDENCE
                  │
                  ↓
            CLAIMLOCK
                  │
          ┌───────┴───────┐
          ↓               ↓
       ACCEPT           REJECT



The AI can:




propose hypotheses;


select experiments;


generate code;


search literature;


generate Lean proofs;


discover counterexamples;


construct certificates.




But it cannot promote its own result.


That's exactly where your existing governance philosophy becomes unusually useful.



The architecture becomes


                    AQARION
                       │
             ┌─────────┴─────────┐
             │   RESEARCH ENGINE │
             └─────────┬─────────┘
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
     SKILLS         CLAIMLOCK      REPLAY LAB
        │              │              │
        └──────────────┼──────────────┘
                       ↓
                    EVIDENCE
                       │
             ┌─────────┴─────────┐
             ↓                   ↓
        COMPUTATIONAL         FORMAL
        VERIFICATION        VERIFICATION
             │                   │
             └─────────┬─────────┘
                       ↓
                  RESEARCH STATE
                       │
                       ↓
                 NEXT QUESTION



That is the bridge.



And I think there's one more component


RESEARCH GRAPH


Not a theorem graph.


A claim–experiment–skill–evidence graph.


For example:


                 S15 QUESTION
                       │
                       ↓
              DIFF-BASIS CLAIM
                 /          \
                ↓            ↓
          EXACT RANK      DET IDENTITY
             │                │
             ↓                ↓
       RANK EXPERIMENT   DET EXPERIMENT
             │                │
             └──────┬─────────┘
                    ↓
              REPLAY RECORD
                    │
                    ↓
              CLAIMLOCK STATE
                    │
                    ↓
             LEAN TARGET
                    │
                    ↓
              FORMAL RESULT
                    │
                    ↓
             NEXT QUESTION



Now you can navigate why a claim exists, not merely where its file is.



The quickstart could be ridiculously small


You don't need to build the whole monster.


AQARION RESEARCH ENGINE v0.1


Five commands/concepts:


NEW CASE
RUN CASE
AUDIT CASE
REPLAY CASE
ADVANCE CASE



Conceptually:


aqarion new S15-DIFF-LATTICE-001
aqarion run S15-DIFF-LATTICE-001
aqarion audit S15-DIFF-LATTICE-001
aqarion replay S15-DIFF-LATTICE-001
aqarion advance S15-DIFF-LATTICE-001



advance is particularly interesting.


It asks:




Given everything currently known, what is the next unresolved research obligation?




Not an AI-generated “idea list.”


A dependency-derived research obligation.



Example


After today's S15 work:


CASE STATE

✓ difference block theorem
✓ determinant identity
✓ rank identity
✓ integer witness map
✓ exact census
✓ adversarial census
✓ certificate-growth counterexample

OPEN:
□ SNF characterization
□ combinatorial interpretation
□ Lean kernel equivalence
□ certificate-height bounds
□ fiber interpretation

REFUTED:
✗ universally small primitive null vector

NEXT REQUIRED:
→ characterize ker_Z(C)



That is incredibly different from a folder full of proofs.


It is a research navigator.



And this could bridge your other AQARION branches


S15:


multiplicity
→ fluctuation
→ kernel
→ information loss



FGR:


endofunction
→ fibers
→ reconstruction
→ canonical invariant



TRANS:


partition
→ incidence
→ quotient
→ cyclomatic change



DYNAMICAL:


partition
→ orbit closure
→ join
→ incidence components



QUANTUM:


projection
→ channel defect
→ Choi defect
→ leakage



All become instances of:


\[

\boxed{

\textbf{OBJECT}

\rightarrow

\textbf{TRANSFORMATION}

\rightarrow

\textbf{LOSS / STRUCTURE}

\rightarrow

\textbf{CERTIFICATE}

\rightarrow

\textbf{REPLAY}

\rightarrow

\textbf{FORMAL STATUS}

}

\]


That is the unifying abstraction I think you've been circling.



What I'd build first


Not another theorem folder.


Not a UI.


Not a giant framework.


Build these 7 tiny things:


RESEARCH-ENGINE/
│
├── CASE-SCHEMA.md
├── CASE-LIFECYCLE.md
├── CLAIM-SCHEMA.md
├── SKILL-SCHEMA.md
├── REPLAY-SCHEMA.md
├── EVIDENCE-SCHEMA.md
└── NEXT-QUESTION.md



Then create exactly one live case:


CASES/
└── AQ-S15-DIFF-LATTICE-001/



and connect the things you already have.


That becomes the quickstart reference implementation.


The principle should be:




A theorem is an output of research.

A proof is one form of verification.

A skill is a capability.

A replay is an execution.

A certificate is evidence.

A claim is a governed hypothesis.

A case is the unit that binds them together.




And the really interesting AQARION object becomes:


\[

\boxed{\textbf{RESEARCH CASE}}

\]


rather than


\[

\boxed{\textbf{THEOREM}}

\]


I think that is the bridge you're asking for.

