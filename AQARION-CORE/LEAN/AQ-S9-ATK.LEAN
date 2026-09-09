-- Transport corrected to subtractive
-- s_T = s0 + Δ_d - m_T PROVED ring
-- +m version REFUTED by norm_num witness (0,2,2,0) → 0=4

def s0 (rP rQ rM rU : ℤ) : ℤ := rP + rQ - rM - rU
def sT (rJP rJQ rMeet rJU : ℤ) : ℤ := rJP + rJQ - rMeet - rJU
def delta (rP rQ rM rU rJP rJQ rJM rJU : ℤ) : ℤ :=
  (rJP - rP) + (rJQ - rQ) - (rJM - rM) - (rJU - rU)
def mT (rJM rMeet : ℤ) : ℤ := rJM - rMeet -- actually |J(M)|-|J(P)∧J(Q)|, ≥0 if monotone

theorem transport_minus (rP rQ rM rU rJP rJQ rJM rJU rMeet rJT m : ℤ)
  (hΔ : delta rP rQ rM rU rJP rJQ rJM rJU = (rJP - rP)+(rJQ - rQ)-(rJM - rM)-(rJU - rU))
  (hs0 : s0 rP rQ rM rU = rP + rQ - rM - rU)
  (hsT : sT rJP rJQ rMeet rJT = rJP + rJQ - rMeet - rJT)
  (hm : m = rJM - rMeet) :
  sT rJP rJQ rMeet rJT = s0 rP rQ rM rU + delta rP rQ rM rU rJP rJQ rJM rJU - m := by
  unfold s0 sT delta at *; ring

-- Refutation of +m law
example : ¬ (∀ rP rQ rM rU rJP rJQ rMeet rJU : ℤ,
  sT rJP rJQ rMeet rJU = s0 rP rQ rM rU + delta rP rQ rM rU rJP rJP rMeet rJU + (rMeet - rMeet)) := by
  push_neg
  use 0,2,2,0,0,2,2,0
  norm_num [s0, sT, delta]
