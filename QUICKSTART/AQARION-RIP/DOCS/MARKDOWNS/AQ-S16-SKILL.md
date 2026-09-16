---
name: aqarion-replay
description: >
  Capture, verify, and close AQARION Replayable Research Objects (ARROs).
  Use when the user asks to run a claim, produce a receipt, check object closure,
  or ensure failed experiments still write complete receipts (RPL-001).
license: MIT
---

# AQARION Replay Skill

## When to use
- Running a mathematical claim engine under a receipt contract
- Checking OBJECT_CLOSURE for a claim_id
- Diffing two runs or inspecting residuals

## Procedure
1. Ensure claim YAML exists under claims/
2. `python aqreplay.py capture CLAIM_ID RUN_ID -- python ENGINES/...`
3. `python aqreplay.py verify RUN_ID`
4. `python aqreplay.py closure CLAIM_ID`
5. `python aqreplay.py diff RUN_A RUN_B`
6. Never promote COMPUTED → PROVEN without a separate formal axis

## Invariants
- FAILED RUN ⇒ COMPLETE RECEIPT
- promotion_allowed defaults false
- residual is first-class on failure
