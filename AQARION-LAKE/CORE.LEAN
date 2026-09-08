namespace AqarionLake

/--
Minimal EXP-001 transport theorem.

This theorem is intentionally independent of Mathlib.
It tests that a Lean declaration can serve as the
artifact referenced by an AQARION evidence receipt.
-/
theorem transport_identity_skeleton
    (sT s0 delta m : Int)
    (h : sT = s0 + delta + m) :
    delta = sT - s0 - m := by
  have h1 : sT - s0 - m = delta := by
    calc
      sT - s0 - m = (s0 + delta + m) - s0 - m := by
        rw [h]
      _ = delta := by
        ring
  exact h1.symm

end AqarionLake
