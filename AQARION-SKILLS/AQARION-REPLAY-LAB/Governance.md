
## 3. GOVERNANCE.md

```sh
cat > GOVERNANCE.md <<'EOF'
# AQARION Replay Lab Governance

## Non-promotion rules

- Numerical agreement is not a formal proof.
- Exact bounded replay does not establish a theorem outside its declared domain.
- An empirical experiment does not establish universal truth.
- A blocked or quarantined claim is not thereby false.
- AI-generated text, code, or proof sketches are not authority.
- A digest identifies bytes only relative to a known artifact chain.
- A successful compiler invocation does not establish that the intended theorem was encoded.
- A proof draft containing sorry, admit, or unapproved axioms is not a zero-sorry proof receipt.

## Current AQARION state

| Item | Status |
|---|---|
| C4 | BLOCKED |
| Mathematical publication | BLOCKED |
| Lean formalization | OPEN |
| SDS-002 | QUARANTINED |
| Promotable | false |

## v0.1 product boundary

AQARION Replay Lab v0.1 is a claim-evidence prototype.

It does not provide:

- arbitrary-code sandboxing;
- cryptographic signatures;
- RFC 8785/JCS receipt canonicalization;
- Rekor/Sigstore transparency-log verification;
- Lean proof validation;
- production claim-state authorization.

## Status meanings

```text
FORMALLY_PROVED:
  formal artifact accepted under configured policy

EXACTLY_VERIFIED:
  exact deterministic bounded replay completed

NUMERICALLY_MATCHED:
  numerical result matched under stated tolerance/model

REFUTED:
  admissible counterexample exists

OPEN:
  evidence or proof incomplete

INADMISSIBLE:
  semantic/evidence contract failure

BLOCKED:
  governance or dependency barrier
