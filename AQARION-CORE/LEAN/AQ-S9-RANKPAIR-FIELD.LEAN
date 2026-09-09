import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.LinearAlgebra.Dimension.Finrank

variable {F : Type*} [Field F] {n : ℕ}

-- Concrete defect D = (1-P)KP
def Dmat (P K : Matrix (Fin n) (Fin n) F) : Matrix (Fin n) (Fin n) F :=
  (1 - P) * K * P

-- Horizontal: im(PKP) ⊆ im P, im(QKP) ⊆ ker P, im P ∩ ker P = 0
-- Hence rank[P | KP] = rank P + rank D
theorem rank_horizontal_field (P K : Matrix (Fin n) (Fin n) F) (hP : P * P = P) :
  (Matrix.fromCols P (K * P)).rank = P.rank + (Dmat P K).rank := by
  sorry -- requires LinearMap range additivity lemma: rank (fromCols) = finrank (range P ⊔ range D)

-- Vertical: ker[P ; KP] = ker P because Px=0 => KPx=0 unconditional any K
theorem rank_vertical_uncond (P K : Matrix (Fin n) (Fin n) F) (hP : P * P = P) :
  (Matrix.fromRows P (K * P)).rank = P.rank := by
  have hker : (Matrix.fromRows P (K * P)).mulVecLin.ker = P.mulVecLin.ker := by
    ext x
    simp only [Matrix.fromRows_mulVec, Matrix.mulVecLin_apply]
    constructor
    · intro h; exact h.1
    · intro h; constructor; exact h; simp [Matrix.mulVec_mulVec, h]
  have hr1 := LinearMap.rank_nullity (Matrix.fromRows P (K * P)).mulVecLin
  have hr2 := LinearMap.rank_nullity P.mulVecLin
  simp [Matrix.rank] at *
  rw [hker] at hr1
  linarith
