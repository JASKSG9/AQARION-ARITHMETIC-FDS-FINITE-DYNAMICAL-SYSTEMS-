# CLAIMLOCK Offline Verification Contract

Status:
TARGET / KERNEL-001

This document defines the verifier contract.
It does not claim formal verification.

---

## 1. Inputs

The verifier consumes:

    S = canonical prior state
    C = canonical claim
    E = canonical evidence
    V = computed predicate vector
    P = canonical policy
    R = receipt

No network access is required.

---

## 2. Canonicalization

All cryptographic JSON hashes MUST use RFC 8785.

Pretty-printed JSON MUST NOT be hashed directly.

Equivalent JSON representations MUST produce identical
canonical bytes.

Non-equivalent semantic inputs MUST NOT be normalized
into equivalence merely because their formatting differs.

---

## 3. Predicate verification

For every predicate:

    predicate
    result
    input_hash
    implementation_hash
    result_hash

MUST be present.

The verifier recomputes:

    input_hash'
    implementation_hash'
    result_hash'

and compares them with the receipt.

A reported PASS without recomputation is not authoritative.

---

## 4. Policy verification

The verifier:

1. loads policy content;
2. canonicalizes it;
3. computes SHA-256;
4. compares the result with the policy hash;
5. confirms that the selected rule exists;
6. confirms the rule's declared outcome;
7. recomputes the transition.

The receipt MUST NOT supply its own authoritative policy hash.

---

## 5. Transition verification

The verifier computes:

    D' = decide_transition(S,C,E,V,P)

and compares:

    D' == D_receipt

Mismatch => INVALID.

---

## 6. Impact verification

The verifier recomputes dependency closure.

The receipt's affected-claim list is informational only
until independently recomputed.

Mismatch => INVALID.

---

## 7. Receipt verification

The verifier reconstructs the receipt body without
the receipt_hash field.

It computes:

    SHA256(JCS(receipt_body))

and compares that value with receipt_hash.

Mismatch => INVALID.

---

## 8. Semantic applicability

Cryptographic validity is distinct from applicability.

A receipt may be:

    VALID

but:

    STALE

if the claim's canonical scope has changed.

Therefore:

    authentic != applicable

and:

    hash-valid != currently-authorized

---

## 9. Independence

The verifier MUST distinguish:

    route_count
    algorithm_diversity
    implementation_diversity
    authority_independence

Two route names do not constitute two authorities.

Two algorithms with the same implementation hash do not
constitute independent implementations.

Two independent implementations agreeing does not prove
mathematical correctness.

It proves only route agreement.

---

## 10. Failure behavior

The verifier MUST fail closed.

It MUST NOT:

- infer missing evidence;
- repair malformed receipts;
- invent predicates;
- silently substitute policies;
- fetch missing dependencies from the network;
- invoke an LLM;
- promote an empirical claim to universal scope;
- treat a stale receipt as currently authoritative.

---

## 11. Acceptance

A receipt is self-verifying only when:

    schema validation PASS
    +
    predicate recomputation PASS
    +
    policy recomputation PASS
    +
    transition recomputation PASS
    +
    impact recomputation PASS
    +
    receipt hash recomputation PASS

No earlier artifact should use the phrase
"self-verifying receipt" as a certification claim.
