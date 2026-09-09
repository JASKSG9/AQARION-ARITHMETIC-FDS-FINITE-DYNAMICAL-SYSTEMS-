import Mathlib

namespace AQARION

/-!
AQ-S9-ATK
Canonical transport artifact.

Governance:
  FROZEN · EXACT · NO PROMOTION · CANONICAL

Canonical convention:
  mT = rJM - rMeet

Canonical transport:
  sT = s0 + delta + mT

The previous subtractive transport theorem was invalid because:
  1. it used the wrong sign for mT under the historical definition; and
  2. the former sT used rJT while delta used rJU.

This file removes both ambiguities.
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

/-
Canonical S9 orientation.

mT is the JM-minus-Meet orientation:
  mT = rJM - rMeet
-/
def mT (rJM rMeet : ℤ) : ℤ :=
  rJM - rMeet

/-
Exact canonical transport identity.

No auxiliary sign hypothesis is required.
-/
theorem transport_identity
    (rP rQ rM rU rJP rJQ rJM rJU rMeet : ℤ) :
    sT rJP rJQ rMeet rJU =
      s0 rP rQ rM rU +
      delta rP rQ rM rU rJP rJQ rJM rJU +
      mT rJM rMeet := by
  unfold s0 sT delta mT
  ring

/-
Critical locus.

When mT = 0, transport reduces exactly to:
  sT = s0 + delta
-/
theorem transport_identity_m_zero
    (rP rQ rM rU rJP rJQ rJM rJU rMeet : ℤ)
    (hm : mT rJM rMeet = 0) :
    sT rJP rJQ rMeet rJU =
      s0 rP rQ rM rU +
      delta rP rQ rM rU rJP rJQ rJM rJU := by
  have hmeet : rJM = rMeet := by
    unfold mT at hm
    linarith
  unfold s0 sT delta
  rw [hmeet]
  ring

/-
Equivalent opposite-sign convention.

If one instead defines

  mOpp = rMeet - rJM,

then the same transport identity becomes

  sT = s0 + delta - mOpp.
-/
def mOpp (rJM rMeet : ℤ) : ℤ :=
  rMeet - rJM

theorem mOpp_eq_neg_mT
    (rJM rMeet : ℤ) :
    mOpp rJM rMeet = -(mT rJM rMeet) := by
  unfold mOpp mT
  ring

theorem transport_identity_opposite
    (rP rQ rM rU rJP rJQ rJM rJU rMeet : ℤ) :
    sT rJP rJQ rMeet rJU =
      s0 rP rQ rM rU +
      delta rP rQ rM rU rJP rJQ rJM rJU -
      mOpp rJM rMeet := by
  unfold s0 sT delta mOpp
  ring

end AQARION
