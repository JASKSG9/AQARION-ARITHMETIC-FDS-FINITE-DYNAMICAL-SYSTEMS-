import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.LinearAlgebra.Dimension.Finrank

variable {F : Type*} [Field F] {n : ℕ}

-- Horizontal detects defect, vertical does not — NC-01
-- Math: KP = PKP + QKP, im(PKP)⊆im P, im(QKP)⊆ker P, im P ∩ ker P =0
-- Hence rank[P|KP] = rank P + rank D

theorem rank_horizontal (P K : Matrix (Fin n) (Fin n) F) (hP : P * P = P) :
  (Matrix.fromCols P (K * P)).rank = P.rank + ((1 - P) * K * P).rank := by
  sorry -- needs finrank image/kernel lemma, field formulation

theorem rank_vertical (P K : Matrix (Fin n) (Fin n) F) (hP : P * P = P) :
  (Matrix.fromRows P (K * P)).rank = P.rank := by
  -- ker[P;KP] = ker P because Px=0 => KPx=0
  have hker : (Matrix.fromRows P (K * P)).mulVecLin.ker = P.mulVecLin.ker := by
    ext x
    simp [Matrix.mulVec, Matrix.fromRows_mulVec]
    constructor
    · intro h; exact h.1
    · intro h; constructor; exact h; simp [h]
  -- rank via rank-nullity
  have hr1 := LinearMap.rank_nullity (Matrix.fromRows P (K * P)).mulVecLin
  have hr2 := LinearMap.rank_nullity P.mulVecLin
  simp [Matrix.rank] at *
  rw [hker] at hr1
  linarith
