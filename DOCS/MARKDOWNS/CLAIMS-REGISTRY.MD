AQARION Claims Registry (Referee Edition)


                                   AQARION CLAIMS REGISTRY
══════════════════════════════════════════════════════════════════════════════

                        FORMAL MATHEMATICAL KNOWLEDGE GRAPH

                               Paper I Foundation
                                       │
                                       ▼
                           D1–D7 Core Definitions
                                       │
                  ┌────────────────────┴────────────────────┐
                  ▼                                         ▼
        Projection Algebra                        Koopman Algebra
                  │                                         │
                  └────────────────────┬────────────────────┘
                                       ▼
                           T1 Invariant Subspace
                                       │
               ┌───────────────────────┴──────────────────────┐
               ▼                                              ▼
        T2 Exact Descent                               T3 Commutator
               │                                          Fallacy
               │                                              │
               └───────────────┬───────────────────────────────┘
                               ▼
                    Certification Infrastructure
                               │
                 verify_atlas_exact.py
                               │
                               ▼
                        CERT-01 Verified Atlas
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
      Observatory                           Future Research
            │                                     │
            ▼                                     ▼
       O12 Plastic                    C7 Pisot Defect Bound
       Statistics                            (Open)
            │
            ▼
        NR-002
  Padovan Greedy Blocked




Claim Lifecycle


Every claim should live in exactly one maturity state.


IDEA
 │
 ▼
Research Note
 │
 ▼
Candidate Definition
 │
 ▼
Frozen Definition
 │
 ▼
Lemma
 │
 ▼
Theorem
 │
 ▼
Executable Certification
 │
 ▼
Lean Verification
 │
 ▼
Publication
 │
 ▼
Long-Term Maintenance



Nothing skips stages.



Registry Status Dashboard




Category
Count
Frozen




Definitions
7
✅


Lemmas
5
5


Theorems
4
4


Corollaries
8
8


Computational Certificates
12
12


Observatory Projects
6
0


Conjectures
9
0


Negative Results
4
4





Claim Card


Every claim should have the exact same layout.



T3 — Commutator Fallacy


Classification


Type:
Theorem

Status:
PROVEN

Maturity:
★★★★★




Statement


DΠ=0

does NOT imply

[P,K]=0.




Mathematical Dependencies


D1
 │
 ▼
Projection Algebra

D2
 │
 ▼
Koopman Operator

D3
 │
 ▼
Partition Projection

        │
        ▼
Invariant Subspace

        │
        ▼
Commutator Fallacy




Computational Evidence


Script

verify_commutator.py

↓

166,484 finite systems

↓

Complete census

↓

No counterexample




Formal Verification




System
Status




Lean
⏳


SMT
Planned


Exhaustive Search
✅


Independent Reproduction
Pending





Publication Mapping


Paper I

Section 4

Theorem 3




Risk Level


Mathematics
██████████ 100%

Implementation
█████████░ 90%

Formalization
██████░░░░ 60%




Evidence Pyramid


One of the most valuable additions would be to explicitly distinguish kinds of evidence.


                     FORMAL PROOF
                           ▲
                           │
                 Lean Verification
                           ▲
                           │
              Exhaustive Certification
                           ▲
                           │
             Independent Replication
                           ▲
                           │
               Observatory Evidence
                           ▲
                           │
                    Initial Discovery



Every claim should indicate where it currently sits.



Observatory Separation


I would visually isolate Observatory work.


═══════════════════════════════════════

OBSERVATORY

These are NOT certified mathematics.

These are reproducible experiments.

They may later become:

Definition

Lemma

Theorem

or

Negative Result.

═══════════════════════════════════════



That makes it impossible for readers to confuse experiments with established results.



Negative Results Registry


Instead of hiding failed ideas:


NEGATIVE RESULTS

NR-001

Rank≤24

REFUTED

Evidence

Counterexample B=31

────────────────────────────

NR-002

Greedy Padovan

BLOCKED

Reason

Admissibility theorem missing

────────────────────────────

NR-003

Universal Complement Identity

REFUTED

Counterexample

Base 12



A referee will appreciate seeing failed hypotheses documented transparently.



Readiness Matrix


Every claim can be scored for publication readiness.




Dimension
Score




Mathematical Proof
5/5


Computational Verification
5/5


Independent Reproduction
3/5


Lean Formalization
2/5


Documentation
5/5


Literature Positioning
4/5




Overall


Publication Readiness

█████████░ 92%




One additional feature I would add


The registry is already becoming a catalogue of results. The next step is to make it a knowledge graph rather than just a database. Each claim should explicitly record not only what it depends on, but also what depends on it.


For example:


T1 Invariant Subspace Theorem

Depends on
──────────
• D1–D7

Supports
────────
• T2 Exact Descent
• T3 Commutator Fallacy
• CERT-01
• Paper I
• Lean LC2

---

version: "14.1.0"
project: "AQARION-ARITHMETIC-STATUS"
last_updated: 2026-07-01

readiness_matrix:
  - id: "D1_D7"
    definition: "complete"
    proof: "complete"
    implementation: "complete"
    expected_artifacts: "frozen"
    independent_verification: "passed"
    lean: "complete"
    paper: "included"

  - id: "T1"
    definition: "complete"
    proof: "complete"
    implementation: "complete"
    expected_artifacts: "frozen"
    independent_verification: "passed"
    lean: "partial"
    paper: "included"

  - id: "T3"
    definition: "complete"
    proof: "complete"
    implementation: "complete"
    expected_artifacts: "frozen"
    independent_verification: "pending"
    lean: "partial"
    paper: "included"

  - id: "CERT-01"
    definition: "complete"
    proof: "not_applicable"
    implementation: "complete"
    expected_artifacts: "frozen"
    independent_verification: "passed"
    lean: "not_applicable"
    paper: "included"

  - id: "O12"
    definition: "partial"
    proof: "not_applicable"
    implementation: "partial"
    expected_artifacts: "mutable"
    independent_verification: "pending"
    lean: "not_applicable"
    paper: "omitted"

  - id: "C7"
    definition: "partial"
    proof: "unstarted"
    implementation: "not_applicable"
    expected_artifacts: "none"
    independent_verification: "pending"
    lean: "unstarted"
    paper: "omitted"

  - id: "NR-002"
    definition: "failed"
    proof: "disproven"
    implementation: "halted"
    expected_artifacts: "none"
    independent_verification: "not_applicable"
    lean: "unstarted"
    paper: "documented_as_negative"

---

https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/blob/main/DOCS/YAML/CLAIMS.yml

https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/blob/main/DOCS/YAML/CLAIMS-STATUS.yml
