CLAIMLOCK/
│
├── README.md
├── LICENSE
├── pyproject.toml
│
├── claimlock/
│   ├── scan.py
│   ├── replay.py
│   ├── provenance.py
│   ├── semantic.py
│   ├── dependency.py
│   ├── promotion.py
│   └── explain.py
│
├── schema/
│   ├── claim.schema.json
│   ├── evidence.schema.json
│   └── receipt.schema.json
│
├── reason-codes/
│   └── codes.yaml
│
├── verifiers/
│   ├── python_replay/
│   ├── matrix_dual_route/
│   ├── hash/
│   └── lean/
│
├── fixtures/
│   ├── aqarion-k2r-beta4/
│   ├── circular-proof/
│   ├── self-certified-json/
│   └── stale-hash/
│
├── benchmark/
│   └── ClaimLock-100/
│
└── docs/
    ├── THREAT_MODEL.md
    ├── TRUST_MODEL.md
    └── CLAIM_LIFECYCLE.md
CLAIMLOCK


Claims don't promote themselves.


AI agents can write code, run tests, generate proofs, and label their own output as:




verified




That label is not evidence.


CLAIMLOCK is an open-source claim-level verification gate for research, code, and AI-agent workflows.


It separates:




what an artifact asserts


what a verifier recomputes


what provenance can establish


what formal systems prove


what remains blocked




ASSERTED ≠ VERIFIED



A claim cannot become stronger because its own metadata says it is stronger.


Example


A fixture may contain:


{
  "status": "INDEPENDENTLY_VERIFIED"
}



CLAIMLOCK treats that field as self-reported.


Only replayable evidence produced by an allowed verifier can change the claim's effective status.


claimlock explain AQ-T10-001



CLAIM: Δ = κ_S

ASSERTED STATUS:
  DERIVED

EVIDENCE:
  ✓ Fixture hash pinned
  ✓ DSU replay passed
  ✓ Matrix replay passed

NOT EVIDENCE:
  ✗ Fixture status field
  ✗ AI discovery record
  ✗ Session-generated verifier

MISSING:
  ○ General theorem
  ○ Formal kernel receipt

EFFECTIVE STATUS:
  BLOCKED

REASON:
  Instance replay does not establish a universal theorem.



Trust model


CLAIMLOCK distinguishes:


CANDIDATE
COMPUTED
REPLAYED
INDEPENDENTLY_VERIFIED
FORMALLY_PROVED
BLOCKED



These are evidence states, not decorative labels.


Core invariant


No claim may be promoted unless the required evidence is present, content-addressed, and produced by an admissible verifier.


A claim is not trusted because an agent wrote:


verified



It is trusted because the evidence required for that claim can be inspected and replayed.


CLAIM: AQ-T10-001
────────────────────────────────────────────

Statement:
  Δ = κ_S

Current status:
  COMPUTATIONALLY_REPLAYED

What supports it:
  ✓ Fixture SHA256 pinned
  ✓ DSU replay passed
  ✓ Matrix replay passed
  ✓ Expected values matched

What does NOT support it:
  ✗ JSON status field
  ✗ AI discovery record
  ✗ Session-generated skill
  ✗ Circular provenance artifact

What is missing:
  ○ General transport theorem
  ○ Lean kernel certificate

Promotion:
  BLOCKED

Reason:
  Fixture agreement does not establish universal identity.
CLAIMLOCK treats that field as self-reported.


Only replayable evidence produced by an allowed verifier can change the claim's effective status.


claimlock explain AQ-T10-001



CLAIM: Δ = κ_S

ASSERTED STATUS:
  DERIVED

EVIDENCE:
  ✓ Fixture hash pinned
  ✓ DSU replay passed
  ✓ Matrix replay passed

NOT EVIDENCE:
  ✗ Fixture status field
  ✗ AI discovery record
  ✗ Session-generated verifier

MISSING:
  ○ General theorem
  ○ Formal kernel receipt

EFFECTIVE STATUS:
  BLOCKED

REASON:
  Instance replay does not establish a universal theorem.



Trust model


CLAIMLOCK distinguishes:


CANDIDATE
COMPUTED
REPLAYED
INDEPENDENTLY_VERIFIED
FORMALLY_PROVED
BLOCKED



These are evidence states, not decorative labels.


Core invariant


No claim may be promoted unless the required evidence is present, content-addressed, and produced by an admissible verifier.


A claim is not trusted because an agent wrote:


verified



It is trusted because the evidence required for that claim can be inspected and replayed.

AQARION: I would not build another agent skill.

Your strongest move is to turn the thing you just discovered—“a skill's own output is not authority”—into a reusable open-source primitive.

Proposal: CLAIMLOCK

A claim-level verification gate for AI-generated research, code, and agent skills.

The core product is:

> A claim cannot become stronger merely because an agent says it is verified.



That sounds simple, but your S12 replay exposed a real missing layer.

Agent skills are exploding, yet recent research shows the ecosystem has millions of copied skill files, substantial provenance/reuse problems, and widespread packaging defects.  At the same time, recent work is converging on provenance-aware skill infrastructure and verified skill synthesis—but AQARION has a sharper opportunity: make the claim itself the executable unit of verification. 


---

The unique idea: evidence cannot self-promote

Your S12 fixture already demonstrates the rule.

The JSON may contain:

{
  "status": "INDEPENDENTLY_VERIFIED"
}

But CLAIMLOCK treats that as merely:

SELF_REPORTED

until an allowed verifier independently produces evidence.

That distinction is the product.

The invariant

\[
\boxed{
\text{asserted status}
\neq
\text{verified status}
}
\]

More formally:

\[
\boxed{
\operatorname{Trust}(C)
=
\operatorname{join}\bigl(
\text{independent evidence atoms}
\bigr)
}
\]

and never:

\[
\operatorname{Trust}(C)
=
\text{metadata supplied by the claimant}.
\]

That is exactly what your provenance audit did correctly.


---

CLAIMLOCK architecture

┌─────────────────────┐
                    │   CLAIM / ASSERTION │
                    │ "Δ = κ for fixture" │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ ASSERTION FIREWALL  │
                    │                    │
                    │ self_reported ≠     │
                    │ independently true │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
    ┌───────────┐       ┌─────────────┐      ┌─────────────┐
    │ REPLAY    │       │ PROVENANCE  │      │ FORMAL      │
    │ verifier  │       │ verifier    │      │ verifier    │
    │ DSU       │       │ hash/path   │      │ Lean/kernel │
    │ matrix    │       │ echo check  │      │ receipt     │
    └─────┬─────┘       └──────┬──────┘      └──────┬──────┘
          │                    │                    │
          └────────────────────┼────────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ EVIDENCE LEDGER     │
                    │ content addressed   │
                    │ verifier identified │
                    │ replayable          │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ PROMOTION GATE      │
                    │                     │
                    │ CANDIDATE           │
                    │ COMPUTED             │
                    │ INDEPENDENT_REPLAY   │
                    │ FORMALLY_PROVED      │
                    │                     │
                    │ or BLOCKED           │
                    └─────────────────────┘

The key difference from a generic benchmark or agent framework is:

CLAIMLOCK does not evaluate whether the agent succeeded.

It evaluates whether a particular claim earned its label.


---

Your existing AQARION work is already the seed

You already have four unusually good primitives.

1. Fixture replay

aq fixture-replay FIXTURE.json

Produces something like:

{
  "claim": "AQ-T10-001",
  "fixture_sha256": "...",
  "routes": {
    "dsu": "PASS",
    "relation_matrix": "PASS"
  },
  "agreement": true,
  "promotion": "BLOCKED"
}

The important part is not the computation.

It is:

> The verifier ignores the fixture's claimed epistemic status.



That should become a first-class protocol rule.


---

2. Provenance audit

Your current rule:

SESSION_ECHO_SUSPECT

is more interesting than it initially looks.

I would generalize it.

Instead of merely:

grep suspicious strings

build a provenance graph:

\[
\text{Claim}
\leftarrow
\text{Evidence}
\leftarrow
\text{Artifact}
\leftarrow
\text{Producer}
\leftarrow
\text{Inputs}
\]

Then detect forbidden cycles:

\[
C
\rightarrow
A
\rightarrow
V
\rightarrow
C
\]

where the alleged verifier ultimately derives from the same generated session that asserted the claim.

Call this:

ECHO-CYCLE DETECTION

A verifier is not independent merely because it has a different filename.


---

3. Semantic diff

This is another piece that should be promoted into the core.

Most verification systems ask:

> Did the program pass?



CLAIMLOCK asks:

> Did the claim change?



Example:

- status: CANDIDATE
+ status: INDEPENDENTLY_VERIFIED

is not a harmless metadata diff.

It is a claim escalation.

Likewise:

- "computationally observed"
+ "proved"

must trigger a different class of gate.

I would make semantic claim escalation impossible without new evidence.


---

4. Claim debt

This becomes the killer dashboard.

Instead of GitHub Issues full of vague TODOs:

Open proof
Need verification
Check later

you get:

Claim	Current label	Required evidence	Missing

Δ=κ general	CANDIDATE	formal transport theorem	Lean
K2R fixture	COMPUTED	independent replay	external
support envelope	DERIVED	formal arithmetic lemma	Lean
phase-fiber	EMPIRICAL	structural theorem	proof
K₃,₄ witness	CONSTRUCTED	transport theorem	dependency


That is something researchers, agent builders, formal methods people, and open-source projects could actually use.


---

The star-worthy command line

I would make the interface absurdly simple.

claimlock init

claimlock scan

claimlock replay

claimlock prove

claimlock audit

But the killer command is:

claimlock explain AQ-T10-001

Output:

CLAIM: AQ-T10-001
────────────────────────────────────────────

Statement:
  Δ = κ_S

Current status:
  COMPUTATIONALLY_REPLAYED

What supports it:
  ✓ Fixture SHA256 pinned
  ✓ DSU replay passed
  ✓ Matrix replay passed
  ✓ Expected values matched

What does NOT support it:
  ✗ JSON status field
  ✗ AI discovery record
  ✗ Session-generated skill
  ✗ Circular provenance artifact

What is missing:
  ○ General transport theorem
  ○ Lean kernel certificate

Promotion:
  BLOCKED

Reason:
  Fixture agreement does not establish universal identity.

That command is extremely shareable because it answers the question everyone actually has:

“What exactly is stopping this claim from being trusted?”


---

The differentiator: refusal with a machine-readable reason

Your product should not just say:

FAIL

It should say:

{
  "promotion": "BLOCKED",
  "reason_code": "MISSING_INDEPENDENT_VERIFIER",
  "claim_id": "AQ-T10-001",
  "required_evidence": [
    "FORMAL_THEOREM",
    "KERNEL_CHECK"
  ],
  "present_evidence": [
    "COMPUTATIONAL_REPLAY"
  ]
}

I would make these stable reason codes.

Examples:

CL001  SELF_REPORTED_STATUS
CL002  SESSION_ECHO_PROVENANCE
CL003  HASH_UNPINNED
CL004  SINGLE_ROUTE_COMPUTATION
CL005  ROUTE_DISAGREEMENT
CL006  MISSING_CARRIER_CERTIFICATE
CL007  CLAIM_ESCALATION_WITHOUT_EVIDENCE
CL008  FORMAL_RECEIPT_MISSING
CL009  DEPENDENCY_CLAIM_OPEN
CL010  VERIFIER_NOT_INDEPENDENT

This is where AQARION can become genuinely useful outside mathematics.


---

I would build a format: CLAIM.yaml

Example:

claim_id: AQ-T10-001

statement:
  text: "Delta equals kappa_S"

status:
  asserted: DERIVED
  effective: BLOCKED

requires:
  - TRANSPORT_THEOREM
  - KERNEL_CERTIFICATE

evidence:
  - type: COMPUTATIONAL_REPLAY
    artifact: fixtures/K2R-BETA4.JSON
    sha256: 33eb2dc9de2781267c450ec86d7ac57585ab4309c5fa0b22a1e63e233524a1b7
    verifier: aq.fixture_replay
    result: PASS

non_authoritative:
  - type: SELF_REPORTED_STATUS
    source: fixture.status

dependencies:
  - AQ-INC-IDENTITY
  - AQ-TRANSPORT

promotion:
  state: BLOCKED
  reason_codes:
    - CL008
    - CL009

The distinction between:

asserted

and:

effective

should be non-negotiable.

That single design decision prevents a huge class of AI-generated overclaim.


---

Why now?

Recent research is pointing in almost exactly the direction where CLAIMLOCK can differentiate.

There are now millions of public SKILL.md files, with large-scale duplication and no inherent compiler or type checker for skill selection.  A recent empirical study found major reuse and packaging problems across public skills, including routing and safety defects. 

Meanwhile:

[SkillWiki](https://www.microsoft.com/en-us/research/publication/skillwiki-a-living-knowledge-infrastructure-for-agent-skills/?utm_source=chatgpt.com) focuses on knowledge-to-skill lifecycle and provenance-aware evolution.

[SkillGen](https://www.microsoft.com/en-us/research/publication/skillgen-verified-inference-time-agent-skill-synthesis/?utm_source=chatgpt.com) focuses on synthesizing and empirically validating skills.

[Repo-To-Skill](https://arxiv.org/abs/2609.02749?utm_source=chatgpt.com) focuses on distilling operational knowledge into reusable verified skills.

[F(AI)2R](https://arxiv.org/abs/2607.25637?utm_source=chatgpt.com) pushes executable AI provenance.

[RethinkSkill](https://github.com/HKUST-KnowComp/rethinkskill?utm_source=chatgpt.com) explicitly frames provenance-first research code.

[skillerr](https://github.com/dot-skill/skillerr?utm_source=chatgpt.com) addresses cryptographic integrity and provenance of skill packages.


AQARION should not duplicate those.

Its gap is narrower:

> A package can be authentic and still contain an unsupported claim.



That is the space CLAIMLOCK owns.

Cryptographic provenance answers:

> Did these bytes come from the claimed producer?



CLAIMLOCK answers:

> Did this claim earn the label attached to it?



Those are fundamentally different questions.


---

The first public artifact should be a benchmark, not just a tool

This is my strongest recommendation.

ClaimLock-100

A small open corpus of deliberately adversarial research claims.

Each case contains:

claim/
artifact/
asserted_status/
evidence/
verifier/
expected_disposition/

Categories:

A. Self-certification

"status": "PROVED"

with no proof.

Expected:

BLOCKED: CL001


---

B. Circular verification

An AI generates:

claim.md

then generates:

verify_claim.py

which simply checks the claim's expected output.

Expected:

BLOCKED: CL002 / CL010


---

C. Two computations agree but theorem absent

Exactly your K2R fixture pattern.

Expected:

COMPUTATIONALLY_REPLAYED
GLOBAL_CLAIM_BLOCKED


---

D. Hash changed after certificate

Expected:

BLOCKED: CL003


---

E. Claim language escalation

"observed"
→
"proved"

without evidence.

Expected:

BLOCKED: CL007


---

F. Genuine formal proof

Lean artifact checks successfully.

Expected:

FORMALLY_PROVED


---

That benchmark could be more important for adoption than the AQARION mathematics itself.

Because every AI coding agent, research agent, and skill ecosystem can understand the problem immediately.


---

My recommended repository structure

CLAIMLOCK/
│
├── README.md
├── LICENSE
├── pyproject.toml
│
├── claimlock/
│   ├── scan.py
│   ├── replay.py
│   ├── provenance.py
│   ├── semantic.py
│   ├── dependency.py
│   ├── promotion.py
│   └── explain.py
│
├── schema/
│   ├── claim.schema.json
│   ├── evidence.schema.json
│   └── receipt.schema.json
│
├── reason-codes/
│   └── codes.yaml
│
├── verifiers/
│   ├── python_replay/
│   ├── matrix_dual_route/
│   ├── hash/
│   └── lean/
│
├── fixtures/
│   ├── aqarion-k2r-beta4/
│   ├── circular-proof/
│   ├── self-certified-json/
│   └── stale-hash/
│
├── benchmark/
│   └── ClaimLock-100/
│
└── docs/
    ├── THREAT_MODEL.md
    ├── TRUST_MODEL.md
    └── CLAIM_LIFECYCLE.md

And AQARION itself becomes:

AQARION
    ↓
first serious dogfood corpus
    ↓
CLAIMLOCK

That relationship is much stronger than trying to market AQARION itself as a generic agent platform.


---

The theorem-level bridge remains useful

Your mathematical work can supply the flagship examples.

For example:

Claim

\[
\Delta=\kappa_S
\]

CLAIMLOCK knows that the fixture supports:

INSTANCE_REPLAY

but not:

UNIVERSAL_THEOREM

Likewise:

\[
\beta(H)\le s-\lceil2\sqrt{s}\rceil+1
\]

could have:

DERIVATION
COMPUTATIONAL_CENSUS
LEAN_OPEN

And the corrected disconnected-safe proof becomes a perfect test case for claim dependency tracking:

beta_support_bound
    depends on
        component_vertex_bound
        F_subadditivity
        cyclomatic_decomposition

No parent claim can outrun its weakest unresolved dependency.

That is a genuinely elegant connection between your AQARION research governance and a reusable software product.


---

My adversarial verdict on your current S12 work

What survives

PASS

Fixture-bound replay is useful.

Ignoring self-reported verification metadata is exactly right.

DSU + matrix dual-route agreement is materially stronger than one implementation.

PROMOTION: BLOCKED is correctly preserved.

Provenance fingerprinting found a genuine governance problem worth productizing.


What I would tighten

1. Two routes are not automatically independent

DSU and matrix implementations can share the same semantic bug.

CLAIMLOCK should distinguish:

MULTI_IMPLEMENTATION

from:

INDEPENDENT_VERIFICATION

Do not call two algorithms independent merely because their code differs.


---

2. Fingerprint matching is only a heuristic

/home/workdir/artifacts is strong evidence of contamination in your context, but it is not a general proof of circularity.

So split:

SESSION_ECHO_SUSPECT

from:

PROVENANCE_CYCLE_PROVED

The latter requires an actual dependency/provenance graph.


---

3. The fixture hash discrepancy must be treated carefully

Your pasted report contains more than one SHA256 value for the fixture across the narrative.

That may simply reflect different file snapshots, but CLAIMLOCK should never silently collapse that.

It should emit:

CL003 HASH_IDENTITY_AMBIGUOUS

until the exact byte-level fixture identity is pinned.

This is precisely the kind of adversarial detail the product should catch automatically.


---

The name I would actually use

I like:

CLAIMLOCK

Tagline:

> Claims don't promote themselves.



Alternatives:

ProofGate

ClaimGraph

EvidenceLock

NoReceiptNoClaim

AuditGate


But CLAIMLOCK is memorable, technical, and immediately understandable.


---

My recommended first README opening

CLAIMLOCK

Claims don't promote themselves.

AI agents can write code, run tests, generate proofs, and label their own output as:

«verified»

That label is not evidence.

CLAIMLOCK is an open-source claim-level verification gate for research, code, and AI-agent workflows.

It separates:

- what an artifact asserts
- what a verifier recomputes
- what provenance can establish
- what formal systems prove
- what remains blocked

ASSERTED ≠ VERIFIED

A claim cannot become stronger because its own metadata says it is stronger.

Example

A fixture may contain:

{
  "status": "INDEPENDENTLY_VERIFIED"
}

CLAIMLOCK treats that field as self-reported.

Only replayable evidence produced by an allowed verifier can change the claim's effective status.

claimlock explain AQ-T10-001

CLAIM: Δ = κ_S

ASSERTED STATUS:
  DERIVED

EVIDENCE:
  ✓ Fixture hash pinned
  ✓ DSU replay passed
  ✓ Matrix replay passed

NOT EVIDENCE:
  ✗ Fixture status field
  ✗ AI discovery record
  ✗ Session-generated verifier

MISSING:
  ○ General theorem
  ○ Formal kernel receipt

EFFECTIVE STATUS:
  BLOCKED

REASON:
  Instance replay does not establish a universal theorem.

Trust model

CLAIMLOCK distinguishes:

CANDIDATE
COMPUTED
REPLAYED
INDEPENDENTLY_VERIFIED
FORMALLY_PROVED
BLOCKED

These are evidence states, not decorative labels.

Core invariant

No claim may be promoted unless the required evidence is present, content-addressed, and produced by an admissible verifier.

A claim is not trusted because an agent wrote:

verified

It is trusted because the evidence required for that claim can be inspected and replayed.
---

My strongest recommendation

Do this as a separate repo and make AQARION the first hostile test corpus.

Do not launch another 500 KB SKILL.md.

Build the smallest possible working CLAIMLOCK:

1. claimlock scan


2. claimlock replay


3. claimlock provenance


4. claimlock explain


5. ClaimLock-20 adversarial fixtures



Then make the first demo brutally compelling:

> “Here are 20 AI-generated claims that look verified. CLAIMLOCK explains why 17 of them are not.”



That is something people can star, fork, benchmark, integrate into CI, and argue about.

And it is directly grounded in the real problem your S12 audit just exposed—not a speculative rebrand. The surrounding agent-skill literature increasingly emphasizes provenance, verification, reusable skill quality, and lifecycle governance, which makes this a timely gap rather than another generic skill wrapper. 

Governance verdict: your AQARION mathematics remains C4 BLOCKED / Publication BLOCKED / Lean OPEN. But CLAIMLOCK itself can be built and publicly useful without promoting any AQARION mathematical claim. That separation is strategically important.

https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/blob/main/AQARION-SKILLS/fixture-replay.py

https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/blob/main/AQARION-SKILLS/aqarion-fixture-replay.md

https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/tree/main/AQARION-SKILLS

https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/blob/main/AQARION-SKILLS/AQ-S12.MD

https://arxiv.org/abs/2607.25637?utm_source=chatgpt.com

