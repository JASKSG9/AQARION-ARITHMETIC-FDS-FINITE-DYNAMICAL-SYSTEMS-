
##`ENGINES/README.md`

```md
# ENGINES

ENGINES contains deterministic logic used by AQARION Replay Lab.

## Intended responsibilities

| Engine | Purpose |
|---|---|
| `policy-evaluator.js` | Applies semantic and verdict rules |
| `receipt-builder.js` | Produces development receipt objects |
| `replay-diff.js` | Compares two receipts and detects semantic drift |
| `mutation-compiler.js` | Produces nearby invalid claim mutations |
| `fixture-router.js` | Selects a permitted curated fixture verifier |

## Non-authority rule

```text
An engine may compute facts.
An engine may evaluate policy.
An engine may not silently redefine a claim.
