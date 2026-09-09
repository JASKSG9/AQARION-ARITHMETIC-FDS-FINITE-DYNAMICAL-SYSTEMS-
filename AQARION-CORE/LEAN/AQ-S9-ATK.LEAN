import Mathlib

namespace AQARION

/-
AQ-S9-ATK
Transport identity — corrected 2026-09-09

Governance:
  FROZEN · EXACT · NO PROMOTION
  Lean compilation receipt OPEN

Definitions:
  s0  = rP + rQ - rM - rU
  sT  = rJP + rJQ - rMeet - rJU
  Δ   = (rJP-rP) + (rJQ-rQ) - (rJM-rM) - (rJU-rU)
  mT  = rJM - rMeet

Exact algebra:
  sT = s0 + Δ + mT

The previous public version incorrectly stated:
  sT = s0 + Δ - m

and therefore must not be retained.
-/

def s0 (rP rQ rM rU : ℤ) : ℤ :=
  rP + rQ - rM - rU

def sT (rJP rJQ rMeet rJU : ℤ) : ℤ :=
  rJP + rJQ - rMeet - rJU

def delta
    (rP rQ rM rU rJP rJQ rJM rJU : ℤ) : ℤ :=
  (rJP - rP) +
  (rJQ - rQ) -
  (rJM - rM) -
  (rJU - rU)

def mT (rJM rMeet : ℤ) : ℤ :=
  rJM - rMeet

/-
Correct transport identity.
This is purely algebraic and requires no monotonicity,
rank, lattice, or dynamical-system assumptions.
-/
theorem transport_additive
    (rP rQ rM rU rJP rJQ rJM rJU rMeet : ℤ) :
    sT rJP rJQ rMeet rJU =
      s0 rP rQ rM rU +
      delta rP rQ rM rU rJP rJQ rJM rJU +
      mT rJM rMeet := by
  unfold s0 sT delta mT
  ring

/-
The previously published subtractive law is false under
the same definitions.

Witness:
  rP=rQ=rM=rU=rJP=rJQ=rJU=rMeet=0
  rJM=1

Then:
  sT = 0
  s0 = 0
  delta = -1
  mT = 1

so the subtractive RHS is -2.
-/
example :
    ¬ (
      sT 0 0 0 0 =
        s0 0 0 0 0 +
        delta 0 0 0 0 0 0 1 0 -
        mT 1 0
    ) := by
  norm_num [s0, sT, delta, mT]

end AQARION
