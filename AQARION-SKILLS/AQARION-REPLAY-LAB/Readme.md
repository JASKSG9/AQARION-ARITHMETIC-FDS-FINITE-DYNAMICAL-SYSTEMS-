# AQARION Replay Lab

> **Can you replay this claimâ€”and can its evidence survive nearby wrong versions of the claim?**

AQARION Replay Lab is a prototype for deterministic, policy-bound replay of mathematical, computational, and AI-assisted claims. It records the declared claim, exact scope, fixture, verifier, observed facts, and the verdict that the available evidence is authorized to support.

It is **not** a theorem prover, a generic code-execution service, a truth oracle, or a system that turns an AI-generated answer into evidence.

## Status

**Prototype / curated fixtures only.**

- C4: `BLOCKED`
- Publication of AQARION mathematical claims: `BLOCKED`
- Lean receipts: `OPEN`
- SDS-002: `QUARANTINED`
- Production cryptographic receipt support: `NOT IMPLEMENTED`

A successful replay is never silently promoted to a stronger evidence tier.

## Core model

```text
Claim Contract
  -> Semantic Firewall
  -> Fixture / Replay Plan
  -> Pinned Verifier
  -> Fact Record
  -> Verdict Policy
  -> Receipt + Replay Diff
```

The contract specifies what a result is allowed to mean. The verifier emits facts. The policy assigns a typed verdict.

```text
Verifier facts != policy verdict
Numerical match != exact verification
Exact finite verification != formal proof
Formalization draft != kernel-accepted proof
Blocked != refuted
```

## Verdicts

| Verdict | Meaning |
|---|---|
| `FORMALLY_PROVED` | A policy-approved formal proof has passed in a pinned environment. |
| `EXACTLY_VERIFIED` | A deterministic exact replay completed over the declared finite domain. |
| `NUMERICALLY_MATCHED` | A numerical comparison matched within the declared numeric model and tolerance. |
| `EMPIRICALLY_SUPPORTED` | An experiment supports a bounded empirical statement. |
| `REFUTED` | An admissible counterexample exists within the stated scope. |
| `OPEN` | Evidence or proof obligations are incomplete. |
| `INADMISSIBLE` | The claim/evidence pair fails a semantic or schema requirement. |
| `BLOCKED` | A policy, dependency, security, or governance gate prevents promotion. |

## Included demos

### 1. Spectral Defect Explorer

A curated numerical fixture for the equal-block defect operator

\[
D=(I-P)K_sP.
\]

It compares a from-scratch Float64 Gram computation against

\[
U^*D^*DU = \frac{r(k-r)}{k^2}(2I-S-S^{-1}),\qquad r=s\bmod k.
\]

The correct two-block convention is

\[
L_{\mathrm{cyc}}^{(2)}=\begin{pmatrix}2&-2\\-2&2\end{pmatrix}.
\]

A passing run is `NUMERICALLY_MATCHED`, not `FORMALLY_PROVED`.

### 2. Regression Museum

Replayable records for rejected inferences and semantic failures:

- `SV001-NEG-001`: simple-edge normalization is wrong at \(m=2\).
- `SDS-R013`: partition invariance does not imply identity of the induced action.
- `AQ-T10-001`: instance replay does not authorize a universal theorem.
- `CP-009`: statements over unequal carriers are not an identity merely because labels resemble each other.

### 3. Toy finite replay

A deliberately simple non-AQARION fixture establishes a finite-domain property using exact integer arithmetic. It demonstrates the product boundary without implying universality beyond its declared domain.

## Claim Contract

Every executable claim must declare:

- a stable identifier and human statement;
- a claim type;
- a finite/numeric/formal domain;
- exact carrier and object conventions;
- the permitted evidence tier;
- forbidden inference upgrades;
- source and verifier artifact identities;
- governance status.

See `schemas/claim-contract.v0.1.schema.json` and `fixtures/spectral-defect/contract.json`.

## Semantic Firewall

The initial firewall rejects semantic promotions such as:

| Code | Meaning |
|---|---|
| `DOMAIN_VIOLATION` | Finite or sampled evidence was promoted beyond its declared domain. |
| `EVIDENCE_PROMOTION_FAIL` | A numerical or replay result was promoted to formal proof. |
| `CARRIER_MISALIGNMENT` | Compared expressions belong to incompatible carriers. |
| `PROJECTION_OVERCLAIM` | A quotient/projection fact was promoted to a full-object identity. |
| `SEMANTIC_OPERATOR_MISMATCH` | Singular values, eigenvalues, Gram operators, and operators were conflated. |
| `INVARIANCE_IDENTITY_CONFUSION` | Invariance was promoted to pointwise identity. |
| `COUNT_SEMANTIC_FAIL` | The same integer was reused for different predicates. |
| `FORMAL_TARGET_MISMATCH` | A formal artifact does not encode the asserted theorem. |
| `GOVERNANCE_BLOCK` | A required gate remains blocked or quarantined. |

## Claim Mutation Compiler

The mutation compiler begins as deterministic templates, not an AI authority. It asks whether nearby invalid versions of a claim would be rejected:

```text
finite-domain result     -> universal theorem
numeric match            -> exact proof
D*D is Laplacian-like    -> D is the Laplacian
singular values          -> eigenvalues
invariance               -> identity
tested-case count        -> extremizer count
blocked                  -> refuted
```

Expected output is often `INADMISSIBLE`, not `REFUTED`.

## Repository layout

```text
schemas/     JSON schemas for contracts, receipts, regressions, and diffs
policy/      Semantic-firewall and verdict policy data
fixtures/    Curated, non-arbitrary replay fixtures
engine/      Minimal policy, receipt, diff, and mutation helpers
web/         Static demo shell
receipts/    Generated development receipts; not cryptographic attestations
tests/       Schema, policy, fixture, and mutation regression tests
```

## Security boundary

v0.1 intentionally does **not** execute arbitrary uploaded code. Fixtures are curated and verifiers are repository-controlled. Browser-generated receipt JSON is a development artifact.

No v0.1 receipt claims:

- RFC 8785/JCS canonicalization;
- a digital signature;
- Sigstore/Rekor inclusion;
- immutable provenance solely from a digest;
- independent verification merely because two labels appear;
- Lean kernel acceptance without a captured build receipt.

## Roadmap

1. Validate Claim Contract documents.
2. Evaluate the Semantic Claim Firewall deterministically.
3. Run curated fixtures and emit typed facts.
4. Export development JSON receipts.
5. Add Replay Diff.
6. Add deterministic claim-mutation regression cases.
7. Export compatible provenance metadata such as Workflow Run RO-Crate.
8. Add RFC 8785 canonicalization, signing, immutable artifact pins, and transparent-log support only after the trust model is implemented.
9. Add Lean as a high-evidence adapter after exact environment pinning, zero-sorry checks, and captured `#print axioms` reports.

## Development principle

```text
AI may suggest a claim, mutation, witness, or proof obligation.
A verifier emits facts.
A pinned policy assigns a verdict.
Only an admissible formal artifact can support FORMALLY_PROVED.
```

## License and governance

Add an explicit license before publication. Add `SECURITY.md` before accepting external reports or artifacts. This repository starts as an educational and research prototype; it is not a production security service.
