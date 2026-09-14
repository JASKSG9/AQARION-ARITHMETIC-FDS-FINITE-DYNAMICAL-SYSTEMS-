cat > README.md <<'EOF'
# AQARION Replay Lab

> **Can you replay this claim—and can its evidence survive nearby wrong versions of the claim?**

AQARION Replay Lab is a prototype for deterministic, policy-bound replay of mathematical, computational, and AI-assisted claims.

It records:

- what was claimed;
- the declared domain and carrier;
- the fixture that was run;
- the verifier and observed facts;
- the verdict the evidence is authorized to support;
- semantic differences between two replays;
- rejected nearby mutations of a claim.

It is **not** a theorem prover, generic code-execution service, truth oracle, or system that turns AI text into evidence.

## Status

Prototype / curated fixtures only.

| Governance item | Status |
|---|---|
| AQARION C4 | BLOCKED |
| AQARION mathematical publication | BLOCKED |
| Lean receipts | OPEN |
| SDS-002 | QUARANTINED |
| Production cryptographic receipts | NOT IMPLEMENTED |

A replay result is never silently promoted:

```text
Numerical match != exact verification
Exact finite verification != formal proof
Formalization draft != kernel-accepted proof
Blocked != refuted
AI output != evidence
