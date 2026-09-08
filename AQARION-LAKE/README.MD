AQARION-LAKE


Evidence-Bound Lean/Lake Verification Surface


Project: AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS

Component: AQARION-LAKE

Experiment: AQ-LAKE-EXP-001C

Mode: FROZEN · EXACT · NO FORK · NO OVERCLAIM

Lean: leanprover/lean4:v4.33.1



1. Purpose


AQARION-LAKE is an experimental Lean/Lake verification surface for testing whether AQARION evidence artifacts can participate in a reproducible build dependency without confusing:




artifact integrity,


evidence validation,


provenance,


build success,


and mathematical proof.




The central architectural question is:


Evidence Receipt
       │
       ▼
Receipt Validation
       │
       ▼
Artifact / Source Binding
       │
       ▼
Lake Build Dependency
       │
       ▼
Lean Compilation



The purpose is deliberately narrow.


AQARION-LAKE does not claim that an evidence receipt automatically proves the mathematical statement associated with that receipt.



2. Core Principle


AQARION-LAKE follows:




No verified artifact binding → no verified evidence dependency → no promotion.




Equally important:


SHA-256 integrity
        ≠
cryptographic authenticity

Lean compilation
        ≠
mathematical truth of external claims

Evidence validation
        ≠
formal proof of the evidence claim



These distinctions are architectural requirements, not documentation preferences.



3. Current Repository Layout


The intended canonical package layout is:


AQARION-LAKE/
├── README.md
├── lakefile.lean
├── lean-toolchain
│
├── AqarionLake/
│   └── Core.lean
│
├── Main.lean
│
├── scripts/
│   ├── release_gate.py
│   └── validate_registry.py
│
└── Evidence/
    ├── transport.json
    ├── provenance_manifest.json
    ├── exp-001c_execution.json
    └── docs/



Filesystem case is significant on Linux.


Therefore the repository must not mix logically equivalent paths such as:


SCRIPTS/
scripts/

EVIDENCE/
Evidence/

CORE.LEAN
AqarionLake/Core.lean



The canonical path referenced by the build must be the actual path present in the repository.



4. Lean Layer


AqarionLake/Core.lean


The core Lean artifact provides a deliberately minimal theorem used to establish the Lean-side artifact binding.


The current theorem is:


theorem transport_identity_skeleton
  (sT s0 delta m : Int)
  (h : sT = s0 + delta + m) :
  delta = sT - s0 - m



It establishes the elementary identity:


[
s_T=s_0+\delta+m
\quad\Longrightarrow\quad
\delta=s_T-s_0-m.
]


This theorem is intentionally simple.


The experiment is testing the evidence/build architecture, not the difficulty of the theorem.



5. Main.lean


Main.lean provides the minimal executable surface that imports the AQARION Lake library.


Its purpose is to establish that the Lean artifact can be loaded through the package dependency graph.


The executable itself is not the evidence claim.


The dependency structure is.



6. Lake Layer


lakefile.lean defines the AQARION Lake package and connects the evidence-validation step to the Lean build.


Conceptually:


Evidence/transport.json
          │
          ▼
validate_registry.py
          │
          ▼
validateEvidence
          │
          ▼
AqarionLake
          │
          ▼
aqarionLakeTest



The desired property is:




the Lean build must not silently ignore the evidence dependency.




If evidence validation fails, the corresponding build path must fail closed.



7. Evidence Layer


Evidence/transport.json


transport.json is the current minimal evidence receipt.


It provides structured information about:




the evidence object;


its status;


the source scope;


the claim;


referenced artifacts;


source hashes;


dependencies;


schema version.




The artifact binding includes the Lean declaration:


AqarionLake.Core.transport_identity_skeleton



The source artifact is identified together with its SHA-256 digest.


The receipt is therefore an explicit provenance object rather than an informal assertion.



8. Provenance Manifest


Evidence/provenance_manifest.json


The provenance manifest records the broader experiment context.


It is intended to capture:


experiment identity
repository/root identity
artifact scope
hash algorithm
canonicalization policy
toolchain information
execution requirements
promotion requirements



The manifest must distinguish exact byte hashes from canonical-content hashes.


AQARION must not label a serialization method as a formal standard such as RFC 8785/JCS unless that standard is actually implemented.



9. Registry Validator


scripts/validate_registry.py


The registry validator is responsible for validating the evidence receipt against the actual repository state.


At minimum, validation covers:


Receipt existence


The referenced receipt must exist.


JSON validity


The receipt must parse successfully.


Required structure


Required fields must be present.


Status


The evidence status must satisfy the release policy.


Artifact structure


Referenced artifacts must contain the required fields.


Source resolution


Referenced source files must exist.


SHA-256 verification


The validator computes:


[
H_{\text{actual}}


\operatorname{SHA256}(\text{source bytes})
]


and compares it with the recorded digest:


[
H_{\text{actual}}


H_{\text{receipt}}.
]


A mismatch is a fail-closed condition.



10. Release Gate


scripts/release_gate.py


The release gate evaluates the execution receipt for AQ-LAKE-EXP-001C.


It exists to prevent an incomplete experiment from being promoted merely because individual artifacts exist.


The release gate distinguishes:


PASS
FAIL
PENDING
BLOCKED
LIMITATION



A pending execution item cannot be silently interpreted as a successful test.



11. EXP-001C Execution Receipt


Evidence/exp-001c_execution.json


The execution receipt is the authoritative record of the current experiment state.


The experiment contains explicit gates covering:


T1   Lakefile elaboration
T2   Lean build
T3   valid receipt
T4   invalid schema
T5   stale source
T6   invalid artifact
T7   bare Lake build
T8   receipt materialization
T9   incremental caching
T10  mutation without rehash
T11  mutation with rehash
T12  signed receipt
T13  parent-chain break



The receipt must preserve the actual result of every gate.



12. Current Execution State


The current experiment is not yet fully executed.


The remaining execution blockers include:


T1   Lakefile elaboration
T2   Lean build
T7   bare Lake build
T8   receipt materialization
T9   incremental caching
T12  signed receipt
T13  parent-chain integrity



Accordingly:


FULL LAKE EXECUTION = PENDING
RELEASE PROMOTION   = BLOCKED



This README intentionally does not promote those states.



13. Verified Architectural Behavior


The experiment has already established useful fail-closed behavior around the evidence layer.


Valid receipt


A structurally valid receipt can be consumed by the validator.


Invalid schema


Invalid receipt structure is rejected.


Stale source


Changing the source without changing its recorded hash is detected.


Invalid artifact


Malformed artifact descriptions are rejected.


Mutation without rehash


Source mutation with the original digest is detected.


These are evidence/provenance properties.


They are not mathematical theorem claims.



14. Important Security Limitation


Hash validation alone cannot establish authenticity.


Suppose an attacker changes:


source



and also changes:


recorded_sha256



to the hash of the modified source.


Then:


SHA256(modified source)
=
recorded modified SHA256



and hash comparison alone succeeds.


Therefore:


[
\boxed{
\text{Integrity} \neq \text{Authenticity}
}
]


This is why T11 is treated as a demonstrated limitation rather than incorrectly marked as a complete security proof.


A future signed-receipt gate is required for authenticity.



15. Signed Evidence


T12 is reserved for signed receipts.


The intended future structure is:


Evidence Receipt
      │
      ├── Content Hash
      ├── Source Hashes
      ├── Signer Identity
      ├── Signature
      └── Signature Verification



The signature does not replace source hashing.


It supplements the integrity mechanism with authenticity.



16. Parent-Chain Integrity


T13 addresses evidence ancestry.


The intended dependency model is:


Root Evidence
      │
      ▼
Experiment Evidence
      │
      ▼
Derived Evidence
      │
      ▼
Certificate



A child receipt must not be treated as independently authoritative if its required parent evidence has disappeared or changed.


A broken ancestry chain must therefore fail closed.



17. Evidence Status Vocabulary


AQARION uses explicit evidence states.




Status
Meaning




[P]
Formally proved


[V]
Computationally/procedurally verified


[C]
Conjecture


[R]
Research program


PENDING
Not yet executed


BLOCKED
Promotion prohibited


LIMITATION
Known limitation demonstrated




A status must describe the evidence actually available.


No promotion by implication.



18. What AQARION-LAKE Does Prove


At the current stage, the strongest defensible claim is:




AQARION-LAKE provides an evidence-bound Lean/Lake architecture in which a structured receipt can identify repository artifacts, validate their recorded hashes, and fail closed when specified integrity conditions are violated.




That is an architectural verification claim.


It is not a claim that the complete Lake execution experiment has passed.



19. What AQARION-LAKE Does Not Yet Prove


The current experiment does not establish:


[P] complete AQARION evidence formalization
[P] cryptographic authenticity
[P] signed receipt verification
[P] parent-chain verification
[P] complete Lake build reproducibility
[P] incremental cache correctness
[P] successful receipt materialization
[P] complete T1–T13 execution
[P] publication-grade evidence certification



These remain explicit gates.



20. Release Criteria


A future AQARION-LAKE release may be promoted only when:


receipt exists
        AND
receipt parses
        AND
required fields validate
        AND
artifact references resolve
        AND
source hashes match
        AND
all required execution gates complete
        AND
no blocking failure remains
        AND
release status permits promotion



Formally:


[
\boxed{
R =
E
\land S
\land A
\land H
\land X
\land G
\land \neg B
}
]


where:




(E) = evidence exists;


(S) = schema/structure valid;


(A) = artifact references valid;


(H) = hashes match;


(X) = execution complete;


(G) = release gates satisfied;


(B) = blocking condition.





21. Determinism


For reproducible evidence, AQARION-LAKE should make the following deterministic:




artifact enumeration;


receipt serialization;


hashing;


test ordering;


failure ordering;


witness ordering;


generated evidence records;


build inputs.




Determinism is necessary for reproducibility.


It is not, by itself, a proof of correctness.



22. Recommended Next Execution


The next exact gate sequence is:


1. Normalize filesystem paths/casing.
2. Align Lakefile paths with repository paths.
3. Align receipt paths with repository paths.
4. Recompute affected SHA-256 values.
5. Validate transport.json.
6. Execute Lakefile elaboration.
7. Execute Lean build.
8. Execute bare Lake build.
9. Verify evidence materialization.
10. Verify incremental caching.
11. Execute signed-receipt adversarial tests.
12. Execute parent-chain adversarial tests.
13. Regenerate EXP-001C execution receipt.
14. Run the release gate.
15. Freeze the resulting hashes and root.



No later status should be inferred before these gates are actually executed.



23. Canonical Architecture


The intended AQARION-LAKE architecture is:


                    ┌─────────────────────┐
                    │ Evidence Receipt    │
                    │ transport.json      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Registry Validator  │
                    │ validate_registry   │
                    └──────────┬──────────┘
                               │
                     hash / structure
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Validated Evidence  │
                    └──────────┬──────────┘
                               │
                         Lake dependency
                               │
                               ▼
                    ┌─────────────────────┐
                    │ AqarionLake.Core    │
                    │ Lean declarations   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Lean/Lake Build     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Release Gate        │
                    └─────────────────────┘



The key property is that evidence is not merely stored beside the code.


It participates in the controlled build path.



24. Final Status


AQARION-LAKE

Evidence architecture             [V]
Receipt validation                [V]
Source-hash binding               [V]
Fail-closed stale-source check    [V]
Invalid-artifact rejection        [V]
Mutation-without-rehash check     [V]
Hash-only authenticity            LIMITATION
Full Lake execution               PENDING
Lean build                        PENDING
Receipt materialization           PENDING
Incremental caching               PENDING
Signed receipt                    PENDING
Parent-chain verification         PENDING
Release promotion                 BLOCKED




Governing Statement


AQARION-LAKE is built around one non-negotiable distinction:


[
\boxed{
\text{Verified provenance}
\neq
\text{verified mathematics}
}
]


The Lake surface is therefore treated as an evidence transport and verification boundary.


It may establish that a specific artifact was present, identified, hashed, validated, and admitted to a build dependency.


It must not silently transform that fact into a stronger mathematical or scientific claim.


FROZEN · EXACT · NO FORK · NO OVERCLAIM


