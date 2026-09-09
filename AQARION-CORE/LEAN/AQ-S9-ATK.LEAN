import Mathlib

namespace AQARION

/--
Exact transport identity.

Here `r` is the partition-lattice rank
`r(P) = n - |P|`, and
m = r(JP ∧ JQ) - r(JM).

With this convention the correction is SUBTRACTIVE.
-/
theorem transport_identity_minus
    (rP rQ rM rU rJP rJQ rJM rJU rMeet : ℤ) :
    rJP + rJQ - rMeet - rJU
      =
    (rP + rQ - rM - rU)
      + (rJP - rP)
      + (rJQ - rQ)
      - (rJM - rM)
      - (rJU - rU)
      - (rMeet - rJM) := by
  ring

theorem transport_identity_m_zero
    (rP rQ rM rU rJP rJQ rJM rJU rMeet : ℤ)
    (hm : rMeet = rJM) :
    rJP + rJQ - rMeet - rJU
      =
    (rP + rQ - rM - rU)
      + (rJP - rP)
      + (rJQ - rQ)
      - (rJM - rM)
      - (rJU - rU) := by
  rw [hm]
  ring

/--
The formerly proposed additive `+m` transport formula is false.
This is an explicit Lean-level refutation.
-/
theorem transport_identity_plus_false :
    ¬ (
      (4 : ℤ) + 4 - 3 - 5
        =
      (4 + 2 - 1 - 5)
        + (4 - 4)
        + (4 - 2)
        - (1 - 1)
        - (5 - 5)
        + (3 - 1)
    ) := by
  norm_num

end AQARION
