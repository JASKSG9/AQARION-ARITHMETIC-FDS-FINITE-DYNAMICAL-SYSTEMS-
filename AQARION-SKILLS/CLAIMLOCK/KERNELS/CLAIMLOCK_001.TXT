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

