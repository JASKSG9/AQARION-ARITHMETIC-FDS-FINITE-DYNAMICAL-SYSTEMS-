# AUDIT_REPORT.md — Independent Reproduction Audit

**Method.** Every claim below was re-derived from `K(n) = desc(n)-asc(n)`
alone (D1), in a fresh script (`verify.py`), with no values copied from
CHECKPOINT.md. Where the reproduction is exact, that is stated plainly. No
claim was "corrected to match" — the script was written from the bare
definition before any comparison was made against the checkpoint's numbers.

| Checkpoint claim | Independent result | Verdict |
|---|---|---|
| C1: 54 states | 54 states | ✅ exact |
| C1: 10 admissible chambers | 10 order-type classes | ✅ exact |
| Memory/prior session: unique fixed point `(6,2)` ↔ 6174 | `(6,2)`, unique, no other fixed points, no nontrivial cycles | ✅ exact |
| Memory/prior session: `det(M_k) ∈ {0,±4}` | `{-4, 0, +4}` realized across all 10 chambers, nothing else | ✅ exact |
| C4: filtration `54→20→14→10→7→4→1` | `[54, 20, 14, 10, 7, 4, 1, 1]` (extra trailing `1` is the stabilization check, same sequence) | ✅ exact |
| C6: `σ(P_G)={1,0}`, `ν(N_G)=6` | spectrum `{0,1}`, nilpotency index `6` | ✅ exact |
| L1: `ν(N)=D` | `D=6`, `ν(N)=6` | ✅ exact, instance confirms the general lemma |
| C5: "Full Koopman" `ν(N)=7` | not tested — different (larger) state space, not built in this session | ⚪ out of scope, not contradicted |
| OP0: chamber structure has a "digit inequality / carry constraint" explanation | Found: exact 4-functional box characterization for all 10 chambers (`[CV]`), plus a fully symbolic borrow-based proof for the `g2=0` axis split (`[P]`) | 🟢 new partial progress |
| T12: minimal hypothesis for fiber independence | Found: "constant on fibers" is sufficient (`[P]`, proved); "fiber-respecting but non-constant" is **not** sufficient (counterexample, `[P+CV-toy]`); AQARION's own `π` satisfies the sufficient condition, so T12 holds for the project's central case (`[P]`) | 🟢 new partial progress, sharpens an underspecified statement into one with an actual proof |

## Process notes (for the killed-claims ledger, if any of this needs walking back)

- The branch-matrix fitting routine initially used an exact-3-point linear
  solve and **failed** to find a fit for 7 of 10 chambers. This was a method
  bug, not a mathematical finding: those 7 chambers are rank-deficient
  (`det=0`), and the 3-point combinatorial solver only searched for
  full-rank (invertible) fits. Switching to ordinary least squares (which
  handles rank-deficient systems via the minimum-norm solution) recovered
  exact fits (`residual < 1e-14`) for all 9 non-singleton chambers
  immediately. Recorded here per the project's zero-fabrication / honest-
  audit convention — the intermediate "no fit found, det=None" output should
  **not** be read as evidence against the checkpoint's `det∈{0,±4}` claim;
  it was an artifact of an incomplete first attempt, corrected in the same
  session before being reported.
- No claim in this package was asserted without either (a) a closed-form
  algebraic proof in PROOFS.md, or (b) a result printed directly from
  `verify.py`'s output with the exact field name cited. Nothing here is
  estimated, rounded from memory, or inferred from the checkpoint's prose.

## Reproducibility

```
sha256sum verify_report.json
423bfac14a7a110414fb5a4bcadc4aaf7b0915e68d9787d20f965f745c35ac4a
```
Re-run with `python3 verify.py` (pure stdlib + numpy, no network, no
external data) to regenerate `verify_report.json` from scratch and confirm
the hash.
