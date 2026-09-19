AQ-FLOQUET-DMD-REPRO-CHECK-001


Date: 2026-09-19

Governance: FROZEN / EXACT / NO PROMOTION

C4: BLOCKED

Publication: BLOCKED

Promotable: false


Purpose


This checkpoint records an adversarial reproduction audit of the AQ-FLOQUET-DMD-001 numerical claims and the current repository state.


Repository identity


Canonical live repository:


JASKSG9/Aqarion-Quantarion-AI


Default branch:


main


Audited revision:


f483b43b4961bee2553b2fd70bed9ce23d82fe95


Finding 1 — DMD source is not currently present in the live repository


The supplied checkpoint references evidence-kernel/run_final_team.py and associated DMD receipt material.


Those paths were not found in the recursive live main tree during this audit.


Therefore the supplied DMD checkpoint is treated as conversation/checkpoint evidence, not as a currently verified repository artifact.


Finding 2 — Exact supplied DMD implementation does not reproduce the reported H5/H10 values


The supplied run_final_team.py logic was independently executed.


Observed in-sample residuals:




Delay
Embedded dimension
Residual




0
2
0.3311485565


2
6
0.0984445528


5
12
0.0499751386


10
22
0.0193948663


20
42
7.0373e-14




These do not reproduce the previously reported H5 value 4.99e-06 or H10 value 5.76e-12.


Therefore the prior E2b H5/H10 numerical claims are NOT REPRODUCED and must not be represented as verified results.


The H20 value is numerically close to the previously reported value, but its near-machine-precision in-sample residual does not establish generalization or physical memory.


Finding 3 — Receipt provenance defect


The supplied run_final_team.py writes previously reported E0/E1/E2b values into final_receipt.json rather than deriving every reported value directly from the execution that generated the receipt.


A certification-grade receipt must be generated from the actual execution output.


Hard-coded scientific result fields are not accepted as computational provenance.


Finding 4 — Strict Floquet interpretation requires separation


The supplied toy system contains a Gaussian time-dependent envelope.


Consequently, the complete trajectory is not a strictly periodic-coefficient system.


Two benchmarks shall therefore be separated:




strict periodic benchmark;


slowly modulated periodically driven benchmark.




No strict Floquet conclusion shall be drawn from the second benchmark.


Finding 5 — Stroboscopic sampling requires correction


The supplied implementation uses dt = 0.01 and int(2*pi/dt) = 628.


The resulting sampling interval is 6.28, not exactly 2*pi.


The corrected benchmark shall sample at exact forcing periods or use a documented interpolation/integration procedure.


Finding 6 — In-sample residual is insufficient


Increasing delay increases the embedded dimension:




H0 → 2 dimensions


H2 → 6 dimensions


H5 → 12 dimensions


H10 → 22 dimensions


H20 → 42 dimensions




A near-zero training residual at high dimension can result from interpolation/overfitting.


The next acceptance test therefore requires held-out one-step and multi-step validation.


E2c acceptance protocol


For delays 0 through 20:




split data into training and validation regions;


fit only on training data;


report numerical rank and SVD tolerance;


evaluate one-step validation error;


evaluate multi-step validation error;


repeat under predefined noise levels;


record all parameters and outputs in the generated receipt.




Noise levels:




0


1e-4


1e-3


1e-2




The smallest delay meeting the predeclared validation criterion may be reported as a candidate minimum.


No delay shall be called "minimal" merely because its training residual is small.


Interpretation boundary


The following claims remain prohibited pending further evidence:




"H5 is the minimal working observable."


"The plasma surface has memory."


"Isochrons/isostables live in delay space."


universal prediction across geometries;


identification of a physical Floquet eigenvalue from this toy benchmark.




Evidence state


E2b H5: NOT REPRODUCED

E2b H10: NOT REPRODUCED

E2b H20: COMPUTED IN-SAMPLE; not a physical certification

E2c: OPEN

Physical plasma interpretation: OPEN / NOT ESTABLISHED

Publication: BLOCKED

Promotion: false


Research rationale


The revised experiment is consistent with published use of DMD/OPT-DMD for plasma reduced-order modeling while adopting a stricter held-out validation requirement.


The methodological objective is not to make DMD appear successful. It is to determine whether delay coordinates produce a reproducible and generalizable improvement under a predefined test.


AI-assisted provenance


This checkpoint records an AI-assisted adversarial audit.


The AI contribution is treated as a research action requiring independent verification, not as mathematical authority.


The relevant chain is:


AI observation → exact source execution → discrepancy → downgraded claim → corrected experiment


No AI-generated statement is itself evidence of mathematical truth.

                 ┌──────────────────┐
                 │  AI proposes     │
                 │  / analyzes      │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Exact artifact   │
                 │ is executed      │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Independent      │
                 │ check / oracle   │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Discrepancy?     │
                 └──────┬─────┬─────┘
                        │     │
                       YES    NO
                        │     │
                        ↓     ↓
                   downgrade  retain
                        │     │
                        └──┬──┘
                           ↓
                  ┌──────────────────┐
                  │ Human-reviewed   │
                  │ disposition      │
                  └────────┬─────────┘
                           ↓
                  new reproducible
                  evidence state                 E2c
                  |
       +----------+----------+
       |                     |
   DETERMINISTIC          STOCHASTIC
   BASELINE               ROBUSTNESS
       |                     |
       v                     v
 exact sampling          noise replicas
 explicit rank           bootstrap/block bootstrap
 full spectrum           confidence interval
       |                     |
       +----------+----------+
                  |
                  v
          PREDECLARED GATE
                  |
                  v
             H* or NONEH0
H1
H2
...
H20
NONE

exact algebra
→ exact Gram identity
→ exact kernel/rank
→ exact minor
→ exact Smith structure

source
→ exact generator
→ exact stroboscopic sampling
→ SVD/rank policy
→ train/validation
→ forecast
→ noise
→ receipt

AI suggestion
→ preserved artifact
→ independent execution
→ discrepancy
→ correction
→ ledger

generator
sampling
delay set
train/validation split
SVD algorithm
rcond
full-spectrum recording
retained-rank definition
full vs retained condition numbers
one-step validation metric
5-step forecast metric
noise distributions
noise seeds
replicate count
bootstrap/block-bootstrap policy
H* decision rule
failure state = NONE

LIVE REPO
   ↓
workflow/path audit
   ↓
DMD artifact introduced only after source exists
   ↓
source-derived receipt
   ↓
independent reproduction
   ↓
held-out validation
   ↓
noise/rank sensitivity
   ↓
only then physical interpretation

https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/blob/main/AI/REPLAY-%20RECEIPTS/AQ-2026-9-19-FLOQUET-DMD/AQ-S19-E2C.md
