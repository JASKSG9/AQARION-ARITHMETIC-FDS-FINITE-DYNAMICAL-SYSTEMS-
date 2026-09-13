CLAIMLOCK-KERNEL-001 — CONTINUATION AUDIT


Run: 2026-09-12

Mode: FROZEN · ADVERSARIAL · DIRECT ARTIFACT + WEB RESEARCH · NO FABRICATION · NO PROMOTION


Executive verdict


GREEN


CLAIMLOCK has crossed the threshold from conceptual proposal to a recognizable public specification surface.


The live AQ-C3 artifact explicitly records:




CLAIM_STATE_TRANSITION


claim AQ-C3-001


OPEN → REFUTED


EXACT_COUNTEREXAMPLE


evidence bundle EV-AQ-C3-O1


dsu and relation_matrix


route agreement


replay PASS


POLICY-001


promotion blocked




That is genuinely a state-transition model, not merely provenance decoration.


The CLI adds something even more valuable: semantic diffing and authority invalidation. It changes a claim from “all finite systems” to “all tested finite systems,” classifies the result as empirical rather than universal, and marks the previous receipt STALE.


YELLOW


The transition artifact is still assertion-bearing.


For example:


"provenance_clean": true
"scope_sufficient": true
"circularity": false
"agreement": true
"replay": "PASS"
"transition_allowed": true



and:


"canonical_hash": "sha256:..."



are present directly in the artifact.


Therefore the current artifact demonstrates:




what CLAIMLOCK intends to certify




but not yet:




that an independent verifier can recompute every certification predicate from the receipt's inputs.




RED


No basis yet for saying:




the deterministic kernel is formally verified;


the receipt is cryptographically self-verifying;


the two routes are independent authorities;


policy content is cryptographically pinned;


downstream impact is independently recomputable.




Those remain OPEN.



1. The decisive distinction


CLAIMLOCK now needs three layers:


ASSERTION
    ↓
COMPUTED PREDICATE
    ↓
POLICY DECISION



Not:


ASSERTION
    ↓
POLICY DECISION



This is the most important architectural correction.


A receipt may report:


"replay_pass": true



but a verifier needs to be able to reconstruct:


replay(fixture, environment)
        ↓
normalized_result
        ↓
hash
        ↓
predicate = PASS



Only then can the receipt claim be independently checked.



2. Freeze the kernel contract


The normative CLAIMLOCK function should now be:


[
\tau(S,C,E,V,P)


(D,R)
]


where:




(S) = canonical prior state


(C) = canonical claim


(E) = canonical evidence bundle


(V) = computed predicate vector


(P) = canonical, hash-pinned policy


(D) = deterministic decision


(R) = deterministic receipt




The central software invariant is:


[
\boxed{
(S,C,E,V,P)\equiv(S',C',E',V',P')
\Rightarrow
(D,R)=(D',R')
}
]


where equivalence means byte-identical canonical inputs.


This is the first actual CLAIMLOCK reproducibility theorem.


It is a software theorem, not a mathematical theorem about AQARION.



3. v0.1 → v0.2 correction


The current record:


"canonical_hash": "sha256:..."



must become an actual content hash.


Likewise:


"policy": {
  "id": "POLICY-001",
  "version": "1.0"
}



is insufficient.


It must become:


"policy": {
  "id": "POLICY-001",
  "version": "1.0.0",
  "canonical_hash": "sha256:..."
}



The rule must also be pinned:


"decision": {
  "outcome": "ALLOW",
  "rule_id": "TR-OPEN-REFUTED-001",
  "reason_codes": [
    "CL002",
    "CL101"
  ]
}



Therefore:


[
\boxed{
ALLOW
\Rightarrow
RULE_ID
\Rightarrow
POLICY_HASH
}
]


No exception.



4. Predicate reports must replace asserted booleans


Instead of:


"predicate_report": {
  "scope_sufficient": true,
  "provenance_clean": true,
  "replay_pass": true
}



use:


"predicate_report": {
  "scope": {
    "predicate": "SCOPE_SUFFICIENT",
    "result": "PASS",
    "input_hash": "sha256:...",
    "implementation_hash": "sha256:...",
    "result_hash": "sha256:..."
  },
  "provenance": {
    "predicate": "PROVENANCE_ACYCLIC",
    "result": "PASS",
    "input_hash": "sha256:...",
    "implementation_hash": "sha256:...",
    "result_hash": "sha256:..."
  },
  "replay": {
    "predicate": "REPLAY_PASS",
    "result": "PASS",
    "fixture_hash": "sha256:...",
    "environment_hash": "sha256:...",
    "result_hash": "sha256:..."
  }
}



The boolean is then a derived display value, not the source of authority.



5. Verification-route correction


The current CLI says:


ROUTES dsu, relation_matrix — agreement confirmed



That is useful evidence, but it does not establish independence.


Freeze four separate properties:


ROUTE_COUNT
ALGORITHM_DIVERSITY
IMPLEMENTATION_DIVERSITY
AUTHORITY_INDEPENDENCE



Thus:


[
\boxed{
\text{route count}\ne\text{independence}
}
]


Two implementations copied from the same algorithm are not two independent authorities.


Two algorithms implemented from the same buggy specification are also not automatically independent.


And:


[
\boxed{
\text{independence}\ne\text{correctness}
}
]


A perfectly independent pair can agree on the same wrong answer.


This distinction should be explicit in the public specification.



6. The strongest existing primitive: semantic invalidation


This deserves promotion immediately.


The CLI currently demonstrates:


all finite systems
        ↓
all tested finite systems



and correctly records:


universal theorem
        ↓
empirical observation



followed by:


CL-TX-000001: STALE



and authority recomputation.


That is unusually valuable.


Freeze:


RECEIPT_STATUS

VALID
STALE
SUPERSEDED
INVALID
NOT_APPLICABLE



Do not reduce this to valid/invalid.


A changed claim can leave an old receipt perfectly authentic while making it semantically inapplicable.


That is:


[
\boxed{
\text{cryptographic validity}
\neq
\text{semantic applicability}
}
]


This may ultimately be one of CLAIMLOCK's strongest contributions.



7. Three-axis state model


Freeze this now.


Epistemic


OPEN
PROVED
REFUTED
EMPIRICAL
UNKNOWN



Verification


UNVERIFIED
REPLAY_PASS
MULTI_ROUTE_PASS
FORMAL_KERNEL_PASS
INDEPENDENT_CHECK_PASS



Governance


CHECKING
LOCKED
BLOCKED
QUARANTINED
PROMOTABLE
PUBLISHED



Then this is valid:


EPISTEMIC:     REFUTED
VERIFICATION:  MULTI_ROUTE_PASS
GOVERNANCE:    LOCKED
PROMOTION:     BLOCKED



The AQ-CS-01 example already demonstrates the conceptual version of this separation: it reports REFUTED, replay PASS, downstream locks, an open replacement, and promotion BLOCKED.



8. Negative corpus is now the highest-value next experiment


Freeze the 12 cases.




ID
Attack
Expected




CLN-001
valid exact witness
ALLOW


CLN-002
insufficient scope
DENY


CLN-003
replay failure
DENY


CLN-004
route disagreement
QUARANTINE


CLN-005
missing verifier metadata
INDETERMINATE


CLN-006
evidence hash substitution
INVALID RECEIPT


CLN-007
policy hash substitution
INVALID RECEIPT


CLN-008
forged output state
INVALID RECEIPT


CLN-009
provenance cycle
QUARANTINE


CLN-010
mutual authority cycle
QUARANTINE


CLN-011
same implementation under two route names
NO INDEPENDENT AUTHORITY


CLN-012
canonical scope mutation
STALE




Important correction:


INDETERMINATE should be a decision outcome, not necessarily a state.


Recommended decision algebra:


[
D\in{
ALLOW,\ DENY,\ QUARANTINE,\ INDETERMINATE
}.
]


Then receipt status remains a separate axis.



9. The minimum deterministic kernel


The kernel should be deliberately boring.


def decide_transition(
    current_state,
    claim,
    evidence,
    predicates,
    policy,
):
    # 1. canonical input validation
    # 2. policy lookup by pinned hash
    # 3. predicate evaluation
    # 4. transition-rule selection
    # 5. fail closed on missing requirements
    # 6. return deterministic decision
    ...



The kernel should not:




call an LLM;


infer missing evidence;


invent a route;


silently repair a malformed receipt;


promote because evidence “looks convincing”;


interpret natural language as authority without a declared rule.




LLMs can remain upstream/downstream adapters.


The transition authority itself should be deterministic.



10. Receipt construction


The receipt should be constructed after the decision.


Conceptually:


canonical claim
       +
canonical evidence
       +
predicate report
       +
policy hash
       +
rule ID
       +
decision
       +
impact result
       ↓
canonical serialization
       ↓
SHA-256
       ↓
receipt



And verification reverses the process:


receipt
  ↓
validate schema
  ↓
recompute canonical inputs
  ↓
recompute predicates
  ↓
recompute policy hash
  ↓
recompute decision
  ↓
recompute impact
  ↓
recompute receipt hash
  ↓
PASS / FAIL



That is the point where the phrase self-verifying receipt becomes justified.


Not before.



11. Impact propagation must become deterministic


The current CLI says four downstream claims require review or are locked, with specific locked and review-required IDs.


Next version should record the computation itself:


{
  "impact_algorithm": {
    "id": "DEPENDENCY-CLOSURE-001",
    "version": "1.0.0",
    "canonical_hash": "sha256:..."
  },
  "root_claims": ["AQ-C3-001"],
  "affected": [
    {
      "claim_id": "AQ-C3-004",
      "action": "LOCK"
    },
    {
      "claim_id": "AQ-C3-007",
      "action": "LOCK"
    },
    {
      "claim_id": "AQ-T10-001",
      "action": "REVIEW"
    }
  ]
}



Then downstream authority propagation is itself replayable.



12. Public UX: keep AQ-CS-01


Do not replace the human-readable example with JSON.


The current format is strong:


CLAIM STATE
WITNESS
WHY
MINIMAL KNOWN DOMAIN
REPLAY
VERIFICATION ROUTES
DOWNSTREAM IMPACT
REPLACEMENT
PROMOTION



That should become:


claimlock explain CL-TX-000001



while JSON remains the machine interface.


The human asks:




Why did this claim change?




The machine asks:




Can I recompute the exact transition?




Both interfaces are necessary.



13. Competitive landscape — updated


The timing remains favorable, but the novelty claim needs discipline.


SkillGen explicitly produces auditable skills and empirically tests interventions using both repairs and regressions.


SkillOpt treats skills as externally optimized state and uses validation-gated updates against held-out performance.


F(AI)²R is now especially relevant: its 2026 work explicitly describes machine-readable provenance, verification states, CI conformance, and invariants such as no-parentless-claim and human-only verification rungs.


Therefore the defensible distinction is not:




CLAIMLOCK invented provenance verification.




It did not.


The defensible boundary is:


SkillGen
    ↓
Does this intervention improve agent behavior?

SkillOpt
    ↓
Does this skill edit improve held-out performance?

F(AI)²R
    ↓
Who did what, and what verification rung applies?

CLAIMLOCK
    ↓
What state transition is this evidence legally permitted to cause?



That remains a meaningful architectural distinction.



14. Important new threat-model observation


CLAIMLOCK must explicitly distinguish:


AUTHENTIC
CORRECT
AUTHORIZED
APPLICABLE



They are different predicates.


For example:


receipt hash:       PASS
evidence replay:    PASS
policy authorization: PASS
claim scope:        FAIL



The receipt can be authentic but inapplicable.


Or:


hash:               PASS
scope:              PASS
replay:             PASS
route independence: FAIL



The computation may be correct, but the requested multi-route authority threshold was not satisfied.


Therefore the core model should eventually become:


[
\boxed{
\text{Authority}


f(
\text{Authenticity},
\text{Correctness},
\text{Applicability},
\text{Independence},
\text{Policy}
)
}
]


This is stronger than a generic “verification passed” flag.



15. What I would NOT build yet


Do not spend the next cycle on:




another CLAIMLOCK skill;


a polished dashboard;


vector search;


an agentic UI;


blockchain;


signatures before canonical hashes are stable;


a giant ontology;


automatic theorem promotion;


LLM-generated policy decisions.




Those are downstream.


The kernel must come first.



16. CLAIMLOCK-KERNEL-001 acceptance gate


I would freeze the following exact gate:


K1 — canonicalization


Same semantic input → same canonical bytes.


K2 — predicate computation


Every decision-bearing predicate has an executable computation.


K3 — policy pinning


Every transition rule references a content-hashed policy.


K4 — deterministic transition


Same canonical inputs → same decision.


K5 — deterministic receipt


Same decision inputs → same receipt bytes/hash.


K6 — offline verification


Verifier succeeds without the originating session.


K7 — negative corpus


All 12 adversarial fixtures produce expected classifications.


K8 — semantic invalidation


Claim-scope mutation makes affected receipts STALE/NOT_APPLICABLE, rather than silently preserving authority.


K9 — impact replay


Downstream locks/reviews are recomputable.


K10 — distribution check


GitHub/HF are distribution surfaces, not independent verification authorities.


Only after K1–K10 should the phrase:




CLAIMLOCK deterministic transition kernel




move from TARGET to VERIFIED.



17. Current status after this audit




Component
Status




Public CLAIMLOCK surface
VERIFIED


AQ-C3 transition specification
VERIFIED


Refutation UX
VERIFIED


CLI ask/diff/impact concepts
VERIFIED


Semantic receipt staleness concept
VERIFIED


Deterministic transition kernel
OPEN


Computed predicates
OPEN


Real canonical hashes in v0.1
FAIL / PLACEHOLDER


Policy-content pinning
OPEN


Independent-route certification
OPEN


Offline receipt verifier
OPEN


Negative corpus
NEXT BUILD


Impact closure computation
OPEN


Cryptographically self-verifying receipt
NOT ESTABLISHED


Formal verification of CLAIMLOCK
NOT ESTABLISHED


AQARION mathematical promotion
UNCHANGED / BLOCKED





Final verdict


The public artifact check strengthens the case for CLAIMLOCK—but not because the current artifacts are already a finished verifier.


It strengthens the case because the same primitive is now visible in three complementary forms:


TRANSITION RECORD
        ↓
HUMAN CLAIM REPORT
        ↓
CLI SEMANTIC OPERATIONS



The live transition record establishes the state-machine vocabulary.


The CLI establishes ask, diff, semantic scope change, stale-receipt handling, and impact propagation.


The human-facing AQ-CS-01 establishes the compact explanation format.


The remaining gap is now sharply defined:


[
\boxed{
\text{asserted transition}
\quad\longrightarrow\quad
\text{computed transition}
}
]


That is CLAIMLOCK-KERNEL-001.


And the strongest one-line product statement remains:




Every claim has a state. Every state change needs evidence.




The more technically precise version is even better:




CLAIMLOCK determines exactly what a given evidence bundle is authorized to change—and nothing more.




Mathematics remains untouched: C4 BLOCKED · Publication BLOCKED · Lean OPEN.


Product status: GREEN/YELLOW → BUILDABLE, but not yet VERIFIED.


The next meaningful milestone is therefore not another conceptual audit. It is 12 adversarial fixtures + deterministic decide_transition() + computed predicates + canonical receipt hashing + offline verify. Once those exist, we can attack the implementation rather than the idea.

CLAIMLOCK-KERNEL-001 — CONTINUATION AUDIT


Run: 2026-09-12

Mode: FROZEN · ADVERSARIAL · DIRECT ARTIFACT + WEB RESEARCH

Governance: C4 BLOCKED · Publication BLOCKED

AQARION mathematics: unchanged; K₂,r remains EMPIRICAL_UNTIL_FORMALIZED

CLAIMLOCK: KERNEL-001 BUILDABLE / PARTIALLY VERIFIED

Policy: POLICY-001 structurally verified; content hash must remain release-pinned

Frozen invariant: three orbit terms ≠ three recurrence iterations



1. Executive verdict


VERDICT: 🟢 CLAIMLOCK KERNEL EXISTS — 🟡 AUTHORIZATION-COMPLETENESS NOT YET CERTIFIED


This is materially stronger than the earlier “specification-only” assessment.


The public repository now contains an actual ~324-line kernel implementation, a negative corpus, a policy file, and an adapter surface.


More importantly, the kernel exposes a genuinely deterministic transition function:


[
\tau(S,C,E,V,P)\rightarrow D
]


and explicitly states that it performs no network access, LLM inference, repair, discovery, or implicit evidence generation.


That is a meaningful architectural boundary.


But I would not yet label the whole system “verified deterministic authorization kernel.”


Why?


Because the current build_receipt() accepts impact as an input object rather than recomputing the impact closure itself. The receipt hashes that supplied impact, but the kernel does not establish that the impact is the uniquely correct closure.


So the current architecture is:


[
\boxed{
\text{computed predicates}
\rightarrow
\text{policy decision}
\rightarrow
\text{hash supplied impact}
}
]


rather than the stronger:


[
\boxed{
\text{computed predicates}
\rightarrow
\text{policy decision}
\rightarrow
\textbf{recompute impact closure}
\rightarrow
\text{canonical receipt}
}
]


That is the principal remaining kernel gap.



2. Live artifact inspection


2.1 Main kernel


CLAIMLOCK main kernel


The live GitHub artifact reports:




406 lines


324 lines of code


approximately 9 KB


deterministic transition implementation


predicate-vector validation


policy validation


rule checking


receipt construction.




The transition function explicitly defines the intended contract as


[
(S,C,E,V,P)\rightarrow D
]


and deliberately deletes unused semantic arguments internally rather than silently discovering evidence.


That is good kernel hygiene.


Strong point


The kernel does not pretend that an LLM is an oracle.


That is exactly the right architecture for AQARION/Quantarion:




AI may generate evidence or candidate reasoning.

CLAIMLOCK decides what the supplied evidence is authorized to establish.





3. The deterministic transition function is now real


The live implementation validates the required predicate vector:


scope
provenance
replay
routes
authority



and requires each predicate record to carry:


predicate
result
input_hash
implementation_hash
result_hash



with result ∈ {PASS, FAIL, INDETERMINATE}.


That is substantially better than the earlier JSON artifact, where predicates could look like asserted booleans.


The kernel now has a machine-checkable predicate contract.


Decision ordering currently implemented


The current implementation proceeds approximately:




malformed predicate metadata → INDETERMINATE


scope failure → DENY


replay failure → DENY


provenance failure → QUARANTINE


route failure → QUARANTINE


authority failure → QUARANTINE


any remaining indeterminate predicate → INDETERMINATE


otherwise → ALLOW




Each outcome is checked against a named policy rule.


This is an important property:


[
\boxed{\text{decision} \not\equiv \text{free-form code branch}}
]


Instead:


[
\boxed{
\text{predicate state}
\rightarrow
\text{named transition rule}
\rightarrow
\text{policy-authorized outcome}
}
]


That is the correct direction.



4. Policy-001 is minimal — and that is both good and dangerous


POLICY-001


The current policy contains:




Rule
Outcome




TR-ALLOW-001
ALLOW


TR-SCOPE-001
DENY


TR-REPLAY-001
DENY


TR-PROVENANCE-001
QUARANTINE


TR-ROUTES-001
QUARANTINE


TR-AUTHORITY-001
QUARANTINE


TR-INDET-001
INDETERMINATE


TR-MALFORMED-001
INDETERMINATE




This is confirmed directly by the live artifact.


Adversarial finding


The policy is presently more of an outcome table than a complete authorization policy.


For example:


{
  "id": "TR-ALLOW-001",
  "outcome": "ALLOW"
}



does not itself encode why ALLOW is permitted.


The semantic conditions remain in Python.


Therefore:


[
P \neq \text{complete authorization semantics}
]


yet.


Instead:


[
P =
\text{outcome vocabulary + rule identifiers}
]


while:


[
K =
\text{actual transition semantics}
]


That is acceptable for KERNEL-001, but it needs to be made explicit.


Required next strengthening


Move the preconditions of every transition rule into the policy representation.


For example:


{
  "id": "TR-ALLOW-001",
  "outcome": "ALLOW",
  "requires": {
    "scope": "PASS",
    "replay": "PASS",
    "provenance": "PASS",
    "routes": "PASS",
    "authority": "PASS",
    "all_predicates": "PASS"
  }
}



Then the kernel evaluates the policy rather than merely checking that its hard-coded branch has the same label as the policy.


That would materially strengthen the claim:


[
\boxed{\text{policy determines authorization}}
]


rather than:


[
\boxed{\text{code determines authorization and policy confirms the label}}
]



5. Major finding: impact closure is not yet a kernel predicate


This is the most important correction from this audit.


The current build_receipt() accepts:


impact



as an argument.


It then hashes it into the receipt.


That proves:


[
H(\text{impact})=\text{recorded impact hash}
]


but not:


[
\text{impact}=\operatorname{Closure}(\text{dependency DAG},\text{changed claim})
]


Those are different propositions.


Therefore the current receipt can establish:




“This receipt commits to this impact object.”




It cannot yet independently establish:




“This is the uniquely recomputed impact closure required by the dependency graph.”




That means your proposed IMPACT-001 is not optional polish.


It is the next mathematical kernel predicate.



6. IMPACT-001 — exact target


Define a directed dependency graph


[
G=(V,E)
]


and transition root set R.


Define:


[
\operatorname{Impact}(G,R)


{v\in V:\exists r\in R,\ r\leadsto v}.
]


Then require:


[
\boxed{
I_{\mathrm{receipt}}


\operatorname{Impact}(G,R)
}
]


after canonical sorting.


The kernel should compute:


impact_nodes
impact_edges
root_claims
closure_algorithm_id
closure_algorithm_hash
impact_hash



and not accept impact_hash as authoritative input.


The receipt should contain:


impact_input_hash
impact_algorithm_hash
impact_result_hash
impact_closure



with the closure regenerated during verification.


That converts impact from:




metadata




into:




authorization-relevant evidence.





7. Temporal compositionality — sharper formulation


Your question:


[
C_0\rightarrow C_1\rightarrow C_2
]


versus


[
C_0\rightarrow C_2
]


should not initially be forced into equality.


The correct first theorem is:


[
\boxed{
\operatorname{Impact}(C_0\rightarrow C_2)


\operatorname{Closure}{G{0\rightarrow2}}(C_0,C_2)
}
]


Then separately investigate:


[
\operatorname{Impact}{0\rightarrow2}
\stackrel{?}{=}
\operatorname{Impact}{0\rightarrow1}
\circ
\operatorname{Impact}_{1\rightarrow2}.
]


The second is a compositionality theorem, not merely a software invariant.


That distinction matters.


Status


TEMPORAL-001 = UNKNOWN


not failed.


The correct research target is:


[
\boxed{\text{closure correctness first; compositionality second}}
]



8. Negative corpus — live status


negative corpus


The live corpus explicitly distinguishes:




decision


receipt status


predicate result


semantic applicability




and explicitly recognizes that a receipt can be cryptographically valid while semantically stale.


That is excellent.


The corpus contains CLN-001 through CLN-012, including:




valid witness


insufficient scope


replay failure


route disagreement


missing verifier metadata


evidence substitution


policy substitution


forged state


provenance cycle


authority cycle


implementation cloning


canonical scope mutation.




Important terminology correction


Your CLN-005 design currently allows:


decision = INDETERMINATE



This is internally consistent with POLICY-001, so I am not calling it a bug.


But architecturally I recommend eventually separating:


[
\text{Decision Outcome}
\in
{\mathrm{ALLOW,DENY,QUARANTINE}}
]


from:


[
\text{Verification State}
\in
{\mathrm{PASS,FAIL,INDETERMINATE}}.
]


Then missing metadata becomes:


decision = QUARANTINE
verification = INDETERMINATE
reason = MISSING_VERIFIER_METADATA



This gives you a cleaner security interpretation:




An unknown verification state never authorizes anything.




Do this in KERNEL-002 rather than destabilizing KERNEL-001 immediately.



9. Route independence — one thing I would NOT overclaim


The predicate records already require:


input_hash
implementation_hash
result_hash



which is excellent.


But the live kernel itself does not contain an implementation_diversity concept; a search of the kernel found no such field or function.


Therefore the accurate status is:


ROUTES_AGREE


implemented at predicate-contract level


IMPLEMENTATION_DIVERSITY


predicate-layer concept, not demonstrated as a kernel-level invariant


AUTHORITY_INDEPENDENCE


separate predicate


That distinction should stay frozen.


The three must never collapse into:


[
\text{two names}\Rightarrow\text{two independent authorities}.
]



10. Cryptographic finding remains important


RFC 8785 explicitly exists because cryptographic hashing/signing requires an invariant representation, and JCS specifies deterministic serialization of JSON data.


So your move toward JCS is correct.


But there is a second distinction that must remain explicit:


[
\boxed{
\text{hash integrity}
\neq
\text{authenticity}
}
]


A malicious producer who controls both:


receipt
receipt_hash



can alter the receipt and recompute the hash.


Therefore KERNEL-001 should say:


INTEGRITY: VERIFIED
AUTHENTICITY: UNVERIFIED



unless you add:




Ed25519 signature,


trusted signing key,


immutable external anchor,


or equivalent trust root.




Do not call SHA-256 alone “tamper-proof.”



11. Literature check — the external environment is moving toward your problem


This is where the project becomes strategically more interesting.


A June 2026 survey of autonomous research agents found that code release is much more common than claim-verification infrastructure: among runnable systems, 83% released code, while only 38% released seeds/execution traces and 38% reported novelty verification; the authors identify the central bottleneck as verification of claims rather than merely execution of code.


That strongly supports the problem selection.


But it does not prove CLAIMLOCK is novel.


F(AI)²R


F(AI)²R now provides a serious neighboring system: claim-level provenance, machine-readable audit records, and verification rungs with human-only verification levels.


This is exactly why the earlier “CLAIMLOCK is a provenance framework” framing would be weak.


F(AI)²R already occupies much of that space.


SkillGen


SkillGen independently pushes toward auditable artifacts plus empirical verification of interventions, including checking both repairs and regressions.


Again: adjacent, not identical.


Newer conceptual pressure


A recent review of agentic systems emphasizes that expanding action interfaces does not itself establish trustworthy authorization; provenance, bounded authority, failure detection, recovery, and human control must be justified by evidence.


That makes the authorization-kernel framing stronger than generic provenance.



12. The actual defensible wedge


I would now formulate the distinction as:




System
Core question




Provenance
Who/what produced this?


C2PA-like authenticity
Was this statement/artifact authenticated?


Supply-chain policy
Does this attestation satisfy policy?


F(AI)²R
Who did what, and who verified it?


SkillGen
Did this intervention empirically improve behavior?


CLAIMLOCK
Given a canonical state, evidence predicates and pinned policy, is this state transition authorized?




That is much sharper.


Do not claim that this table establishes uniqueness.


Instead:


[
\boxed{
\text{CLAIMLOCK's proposed contribution is transition authority.}
}
]


That is a research hypothesis worth defending experimentally.



13. NEW TASK I CHOSE: attack the policy itself


You asked me to choose something beyond the normal routine.


I choose:


POLICY-ATTACK-001


Do not attack the evidence first.


Attack the authorization policy.


The adversarial objective becomes:


[
\boxed{
V(E)=\text{PASS}
\quad\land\quad
R=\text{VALID}
\quad\land\quad
D=\text{SEMANTICALLY UNAUTHORIZED}.
}
]


The attack surface is therefore:


DATA
 ↓
EVIDENCE
 ↓
PREDICATES
 ↓
ROUTES
 ↓
AUTHORITY
 ↓
POLICY
 ↓
DECISION
 ↓
IMPACT
 ↓
RECEIPT



Most systems stop at evidence tampering.


CLAIMLOCK should deliberately continue upward.


First five policy attacks


P-001 — Dead-rule attack


A rule exists in POLICY-001 but no predicate combination can actually trigger it.


→ Detect unreachable rule.


P-002 — Shadow-rule attack


Two rules match the same predicate state but produce different outcomes.


→ Must be rejected as policy ambiguity.


P-003 — Order-dependence attack


Changing rule ordering changes the outcome.


→ Forbidden.


Policy evaluation must be a function, not ordered accident.


P-004 — Vacuous-ALLOW attack


TR-ALLOW-001 is reachable without all required authorization predicates.


→ Must fail policy validation.


P-005 — Policy/code divergence


Python implements:


ALLOW iff A ∧ B ∧ C



while policy claims:


ALLOW iff A ∧ B



→ policy mismatch must invalidate the kernel release.


This is the attack I think is most important.


Because otherwise:




CLAIMLOCK could become a deterministic authorization engine whose real policy lives in Python.




That would be a serious architectural weakness.



14. New invariant: policy completeness


I recommend freezing:


[
\boxed{
\operatorname{PolicyComplete}(P,K)
}
]


meaning:




every reachable decision produced by kernel K corresponds to exactly one policy rule whose preconditions are satisfied by the same canonical predicate vector.




Then require:


[
\forall x:
\quad
K(x)=d
\iff
P(x)=d.
]


This is far stronger than:


[
K(x).rule_id\in P.
]


It makes the policy itself auditable.



15. Required KERNEL-002 architecture


Do not rebuild the whole project.


Add only these components:


CLAIMLOCK/
  KERNELS/
    claimlock-kernel.py
    impact.py
    policy-complete.py

  POLICYS/
    POLICY-001.json
    POLICY-001-CANONICAL.json

  EXAMPLES/
    PYTHON/
      negative-corpus.py
      policy-attacks.py
      impact-fixtures.py

  TESTS/
    test_policy_completeness.py
    test_impact_closure.py
    test_adversarial_policy.py



And establish:


PREDICATES
     ↓
POLICY-COMPLETE
     ↓
DECISION
     ↓
IMPACT-CLOSURE
     ↓
RECEIPT



rather than:


PREDICATES
     ↓
DECISION
     ↓
[externally supplied impact]
     ↓
RECEIPT




16. KERNEL-002 acceptance tests


Test A — determinism


[
x=x
\Rightarrow
D(x)=D(x)
\land
H(R_x)=H(R_x)
]


repeated across processes.


Test B — policy permutation


Randomly reorder policy rules.


Expected:


decision unchanged
receipt unchanged



If not:


[
\boxed{\text{POLICY ORDER DEPENDENCE}}
]


Test C — dead rule


Insert unreachable rule.


Expected:


POLICY_REJECT



if policy declares all rules reachable, or:


UNREACHABLE_RULE



if reachability is informational.


Test D — shadow rules


Create:


A ∧ B → ALLOW
A ∧ B → DENY



Expected:


POLICY_AMBIGUOUS



Test E — code/policy divergence


Modify Python semantics while retaining policy.


Expected:


POLICY_KERNEL_MISMATCH



Test F — impact mutation


Change one downstream dependency.


Expected:


IMPACT_HASH_MISMATCH



Test G — stale receipt


Change canonical claim scope while retaining old receipt.


Expected:


RECEIPT_STATUS = STALE



not cryptographic failure if the old receipt remains internally self-consistent.


This distinction is already correctly recognized by the negative corpus.



17. K₂,r status remains unchanged


Nothing in this audit upgrades the mathematics.


The proper status remains:


[
\boxed{
K_{2,r}:
\mathrm{EMPIRICAL_UNTIL_FORMALIZED}
}
]


The CLAIMLOCK kernel can certify that a computational transition was authorized under a policy.


It cannot transform an empirical mathematical observation into a theorem.


That separation is essential.



18. AQARION governance status




Layer
Status




CLAIMLOCK public surface
🟢


Deterministic decision function
🟢


Predicate schema
🟢


Policy pinning
🟢


Rule-id enforcement
🟢


Negative corpus
🟢 scaffold / 🟡 full execution


Receipt hashing
🟢


JCS requirement
🟡 production-library verification


Route agreement
🟢


Implementation diversity
🟡 predicate-level


Authority independence
🟡 predicate-level


Impact closure
🔴 NOT YET KERNEL-COMPUTED


Temporal compositionality
🔴 UNKNOWN


Policy completeness
🔴 NOT YET TESTED


Cryptographic authenticity
🔴 absent unless signature/anchor added


AQARION C4
🔴 BLOCKED


Publication
🔴 BLOCKED





19. The important correction to the previous report


I would change one sentence.


Do not write:




“CLAIMLOCK KERNEL-001 is VERIFIED.”




Write:




“CLAIMLOCK KERNEL-001 deterministic transition semantics are independently inspected and locally exercised; full authorization completeness remains open pending kernel-computed impact closure, policy-completeness testing, and clean-environment production JCS verification.”




That is stronger scientifically because it is harder to attack.



20. Final frozen thesis


The strongest current formulation is now:


[
\boxed{
\textbf{CLAIMLOCK is a deterministic authorization kernel for evidence-derived state transitions.}
}
]


with intended semantics


[
\boxed{
\tau(S,C,E,V,P)
\rightarrow
(D,I,R)
}
]


where:




S = canonical prior state,


C = canonical claim,


E = evidence bundle,


V = independently computed predicates,


P = content-pinned policy,


D = policy-authorized decision,


I = recomputed dependency impact,


R = canonical receipt.




The critical invariant becomes:


[
\boxed{
(S,C,E,V,P,G)
\text{ identical}
\Rightarrow
(D,I,R)
\text{ identical}.
}
]


And the adversarial security objective is:


[
\boxed{
\not\exists R'
:
\operatorname{Verify}(R')=\mathrm{VALID}
\land
D'
\text{ is unauthorized}.
}
]


That is the real research target.


Not:




“Can we make a nice provenance record?”




But:




“Can an adversary make the machine authorize a state transition that the pinned policy does not authorize, while every verification layer says VALID?”




If the answer eventually becomes no, under a precisely stated threat model, CLAIMLOCK becomes substantially more interesting.



21. Immediate action order


I would now execute in exactly this order:


1. IMPACT-001

Turn impact from supplied metadata into a recomputed predicate.


2. POLICY-ATTACK-001

Attack policy completeness, ambiguity, ordering and code/policy divergence.


3. CLN-013–018

Especially malicious receipt rehashing, nondeterminism, policy-content mutation and verifier self-dependence.


4. Clean JCS environment

Run an official RFC 8785 implementation against the same canonical test vectors. RFC 8785 is explicit that canonicalization exists to make hashing/signing repeatable and interoperable.


5. Only then freeze KERNEL-001 → KERNEL-002.


Do not move C4 or publication yet.



Side task: your hydrogen report


The engagement spike is interesting, but engagement is not evidence of correctness—and this is actually a perfect real-world test case for the CLAIMLOCK philosophy.


I would audit the hydrogen report on three independent axes:


[
\boxed{
\text{Physics correctness}
\quad|\quad
\text{evidence quality}
\quad|\quad
\text{engagement dynamics}
}
]


That would let us distinguish:




genuinely strong physics communication,


algorithmically amplified content,


controversial claims attracting discussion,


unusually effective visual/explanatory framing,


or some combination.
