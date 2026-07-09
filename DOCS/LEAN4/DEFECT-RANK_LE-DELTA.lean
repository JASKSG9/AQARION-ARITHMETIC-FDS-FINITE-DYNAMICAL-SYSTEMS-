import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Data.Matrix.Basic

open Matrix

variable (n : ℕ) (T : Fin n → Fin n) (π : Partition n)

-- Existing definitions assumed:
--   KoopmanMatrix T : Matrix (Fin n) (Fin n) ℝ
--   ProjectionMatrix π : Matrix (Fin n) (Fin n) ℝ
--   Partition.card π : ℕ

-- For each block B, count the number of distinct image blocks
def numTargets (B : Partition n) : ℕ :=
  -- cardinality of {π(T(x)) | x ∈ B}
  sorry

-- Δ_π(T) = Σ_{B∈π} (|image blocks from B| - 1)
def Delta (π : Partition n) : ℕ :=
  ∑ B in π.blocks, (numTargets B - 1)

-- Lemma: the local contribution δ(B) = |targets(B)|-1 bounds the defect
lemma local_rank_bound (B : Partition n) :
    (rank ((1 : Matrix (Fin n) (Fin n) ℝ) - ProjectionMatrix π) * KoopmanMatrix T *
      (ProjectionMatrix π).submatrix (B : Set (Fin n)).val) ≤ numTargets B - 1 := by
  -- Proof: D restricted to block B maps into the span of centered indicators
  -- of the target blocks, whose dimension is at most |targets|-1.
  sorry

theorem defect_rank_le_Delta : rank (defect_operator n T π) ≤ Delta π := by
  -- The defect operator decomposes as sum over blocks of the local restrictions.
  calc
    rank (defect_operator n T π)
        = rank (∑ B, ((1 - ProjectionMatrix π) * KoopmanMatrix T *
                  (ProjectionMatrix π).submatrix (B : Set (Fin n)).val)) := by
          -- block decomposition lemma
    _ ≤ ∑ B, rank (...) := rank_sum_le _ _
    _ ≤ ∑ B, (numTargets B - 1) := by
          apply Finset.sum_le_sum; intro B hB; exact local_rank_bound B
    _ = Delta π := rfl
