---
name: aqarion-fixture-replay
description: Independently recompute AQARION transport fixtures with DSU and relation-matrix routes. Use for TRANSPORT-K2R-BETA4, K2r family checks, or any published partition JSON. Reports PASS/FAIL only. Cannot promote claims or emit Lean receipts.
---

# Fixture replay (adapter)

## Rule

JSON field `"status": "INDEPENDENTLY_VERIFIED"` is **not** authority. This skill recomputes.

## Command

```bash
python3 aq/fixture_replay.py fixtures/AQ-S12-TRANSPORT-K2R-BETA4.JSON
```

## Acceptance for this skill

- DSU route and matrix route agree
- block counts, defects, s0, delta, kappa match expected object
- output ends with `PROMOTION: BLOCKED`

## Non-claims

- Does not prove \(\Delta=\kappa_S\) for all systems
- Does not prove \(K_{2,r}\) maximality
- Does not produce a Lean kernel receipt
