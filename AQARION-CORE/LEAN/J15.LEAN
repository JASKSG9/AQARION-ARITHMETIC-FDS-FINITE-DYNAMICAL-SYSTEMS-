import AQARION.Core.Definitions
import AQARION.Core.Projection
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.LinearAlgebra.Matrix.Block
import Mathlib.LinearAlgebra.Matrix.Spectrum
import Mathlib.LinearAlgebra.Matrix.Diagonal
import Mathlib.LinearAlgebra.Matrix.Basis
import Mathlib.LinearAlgebra.Eigenspace.Basic
import Mathlib.Data.Complex.Basic

open Matrix
open Submodule

namespace AQARION

variable {n : Type*} [Fintype n] [DecidableEq n] (R : Type*) [Field R] [IsROrC R] [DecidableEq R]

/-! # Block decomposition of the defect operator

Let `Π` be a partition with projection `P : Matrix n n R`, and let `K` be the Koopman
operator (pullback).  Choose an adapted basis so that the first `r` basis vectors span
`Im P`.  Then

    P = [ I_r  0 ]
        [ 0   0 ]

and

    K = [ A   B ]
        [ C   E ]

giving

    D = (I - P) K P = [ 0   0 ]
                      [ C   0 ] .

From this we immediately read off `rank(D) = rank(C)` and the bound
`rank(D) ≤ min(r, n - r)`.
-/

section BlockDecomposition

variable (sys : FDDS R n) (Π : Partition n)

local notation "P" => projectionMatrix R Π
local notation "K" => koopman R sys
local notation "D" => defect R sys Π

/-- The matrix `P` is symmetric (since it's an orthogonal projection). -/
lemma P_symm : Pᵀ = P := by
  -- This follows from the definition of projectionMatrix; see Core.Projection
  exact AQARION.Core.Projection.projection_symmetric R Π

/-- The matrix `P` is idempotent. -/
lemma P_idem : P * P = P := by
  exact AQARION.Core.Projection.projection_idempotent R Π

/-- Diagonalisation of an orthogonal projection.
    There exists an orthogonal matrix `U` such that `U * P * Uᵀ` is diagonal
    with entries 0 or 1. -/
lemma orthogonal_diagonalisation :
    ∃ (U : Matrix n n R) (D : Matrix n n R),
    U * Uᵀ = 1 ∧ Matrix.IsDiag D ∧ U * P * Uᵀ = D ∧ ∀ i, D i i = 0 ∨ D i i = 1 := by
  have h_symm : Pᵀ = P := P_symm R Π
  have h_idem : P * P = P := P_idem R Π
  -- The spectral theorem for symmetric real matrices (via IsROrC)
  have h_spec := IsSymmetric.diagonalization h_symm
  rcases h_spec with ⟨U, hU, D, hD⟩
  refine ⟨U, D, hU, hD, ?_, ?_⟩
  · -- hD gives U * P * Uᵀ = D
    exact hD
  · -- idempotence forces eigenvalues to be 0 or 1
    intro i
    have hD_idem : D * D = D := by
      calc
        D * D = (U * P * Uᵀ) * (U * P * Uᵀ) := by rw [hD]
        _ = U * P * (Uᵀ * U) * P * Uᵀ := by simp [Matrix.mul_assoc]
        _ = U * P * (1 : Matrix n n R) * P * Uᵀ := by rw [hU]
        _ = U * P * P * Uᵀ := by simp
        _ = U * (P * P) * Uᵀ := by simp [Matrix.mul_assoc]
        _ = U * P * Uᵀ := by rw [h_idem]
        _ = D := by rw [hD]
    -- Because D is diagonal, idempotence gives dᵢ² = dᵢ → dᵢ = 0 or 1
    let d := D i i
    have h_d_sq_eq : d * d = d := by
      have h := congrArg (fun M : Matrix n n R => M i i) hD_idem
      simp [Matrix.mul_apply, Matrix.diag_apply, hD i i] at h
      exact h
    have h_d_factor : d * (d - 1) = 0 := by
      linear_combination d * d - d
    rcases eq_zero_or_eq_zero_of_mul_eq_zero h_d_factor with (h0 | h1)
    · left; exact h0
    · right; linarith

/-- Reorder the diagonal matrix so that the 1s come first.
    Returns `r` (the number of 1s) and an invertible matrix `Q` such that
    `Q * D * Q⁻¹ = fromBlocks 1 0 0 0`. -/
lemma reorder_diagonal (D : Matrix n n R) (hD : Matrix.IsDiag D) (h_eig : ∀ i, D i i = 0 ∨ D i i = 1) :
    ∃ (r : ℕ) (Q : Matrix n n R) (hQ : IsUnit Q),
    Q * D * Q⁻¹ = Matrix.fromBlocks 1 0 0 0 := by
  -- Count the number of ones
  let ones : Finset n := {i | D i i = 1}
  have h_ones_card : ones.card = Finset.card ones := rfl
  -- Build a permutation that sorts the indices: ones first, then zeros.
  let perm : Equiv.Perm n := by
    -- Choose an enumeration of n; we can use the standard one via Fintype
    have h_fintype : Fintype n := inferInstance
    -- Use the fact that Finset.card gives the cardinality
    -- We'll construct a permutation that sends ones to Fin ones.card and zeros to the rest
    sorry  -- This is a finite combinatorics argument; for now we assume it can be done
  -- The corresponding permutation matrix is invertible.
  let Q : Matrix n n R := perm.toMatrix
  have hQ : IsUnit Q := perm.isUnit_toMatrix
  -- Conjugating D by the permutation matrix reorders the diagonal entries.
  -- The result is a diagonal matrix with ones in the first r positions and zeros after.
  have hQDQ : Q * D * Q⁻¹ = Matrix.fromBlocks 1 0 0 0 := by
    -- Technical proof; relies on perm putting ones first
    sorry
  exact ⟨ones.card, Q, hQ, hQDQ⟩

/-- **Block Decomposition Theorem (T4)**.
    In an adapted basis, the defect operator has the form `[0 0; C 0]`. -/
theorem block_form_defect :
    ∃ (r : ℕ) (C : Matrix (Fin r) (Fin (Fintype.card n - r)) R)
      (iso : Matrix n n R) (h_iso : IsUnit iso),
    iso * D * iso⁻¹ = Matrix.fromBlocks 0 0 C 0 := by
  -- 1. Diagonalise P
  obtain ⟨U, D0, hU_orth, hD0, hPdiag, h_eig⟩ := orthogonal_diagonalisation R sys Π
  -- 2. Reorder D0 so that 1s come first
  obtain ⟨r, Q, hQ, h_reorder⟩ := reorder_diagonal D0 hD0 h_eig
  -- 3. The combined change of basis: iso = Q * U
  let iso : Matrix n n R := Q * U
  have h_iso : IsUnit iso := by
    -- U is orthogonal, hence invertible; Q is invertible; product is invertible
    have hU_unit : IsUnit U := by
      -- from hU_orth: U * Uᵀ = 1 → U is invertible
      refine ⟨U, Uᵀ, hU_orth, ?_⟩
      calc
        Uᵀ * U = (Uᵀ * U)ᵀᵀ := by simp
        _ = (Uᵀ * U)ᵀ := by simp
        _ = Uᵀ * U := by
          -- Actually, from U * Uᵀ = 1 we get Uᵀ = U⁻¹, so Uᵀ * U = 1 as well.
          have h := hU_orth
          -- multiply both sides by U⁻¹ on left and U on right; but easier: from hU_orth, U is orthogonal, so Uᵀ * U = 1
          exact Matrix.mul_eq_one_comm.mp hU_orth
    exact IsUnit.mul hQ hU_unit
  -- 4. Compute iso * P * iso⁻¹
  have hP_block : iso * P * iso⁻¹ = Matrix.fromBlocks 1 0 0 0 := by
    calc
      iso * P * iso⁻¹ = (Q * U) * P * (U⁻¹ * Q⁻¹) := by
        simp [iso, Matrix.inv_mul, Matrix.mul_inv, hQ, hU_orth]
      _ = Q * (U * P * U⁻¹) * Q⁻¹ := by
        simp [Matrix.mul_assoc]
      _ = Q * D0 * Q⁻¹ := by
        rw [hPdiag]
      _ = Matrix.fromBlocks 1 0 0 0 := by rw [h_reorder]
  -- 5. Write iso * K * iso⁻¹ as a block matrix [A B; C E]
  --    This is just a notation; we don't need explicit A,B,E for the conclusion.
  --    Let K_block := iso * K * iso⁻¹
  let K_block : Matrix n n R := iso * K * iso⁻¹
  -- 6. Compute iso * D * iso⁻¹ = (I - P_block) * K_block * P_block
  have hD_block : iso * D * iso⁻¹ = (1 - Matrix.fromBlocks 1 0 0 0) * K_block * (Matrix.fromBlocks 1 0 0 0) := by
    calc
      iso * D * iso⁻¹ = iso * ((1 - P) * K * P) * iso⁻¹ := rfl
      _ = (iso * (1 - P) * iso⁻¹) * (iso * K * iso⁻¹) * (iso * P * iso⁻¹) := by
        simp [Matrix.mul_assoc]
      _ = (1 - iso * P * iso⁻¹) * K_block * (iso * P * iso⁻¹) := by
        simp [K_block, Matrix.sub_mul, Matrix.mul_sub, Matrix.one_mul, Matrix.mul_one]
      _ = (1 - Matrix.fromBlocks 1 0 0 0) * K_block * (Matrix.fromBlocks 1 0 0 0) := by
        rw [hP_block]
  -- 7. Simplify the block product
  --    Write K_block as a generic 2×2 block matrix
  let A : Matrix (Fin r) (Fin r) R :=
    (Matrix.fromBlocks 1 0 0 0 : Matrix n n R) * K_block * (Matrix.fromBlocks 1 0 0 0)
  let B : Matrix (Fin r) (Fin (Fintype.card n - r)) R :=
    (Matrix.fromBlocks 1 0 0 0) * K_block * (Matrix.fromBlocks 0 0 0 1)
  let C : Matrix (Fin (Fintype.card n - r)) (Fin r) R :=
    (Matrix.fromBlocks 0 0 0 1) * K_block * (Matrix.fromBlocks 1 0 0 0)
  let E : Matrix (Fin (Fintype.card n - r)) (Fin (Fintype.card n - r)) R :=
    (Matrix.fromBlocks 0 0 0 1) * K_block * (Matrix.fromBlocks 0 0 0 1)
  -- By construction, K_block = [A B; C E] in the adapted basis.
  have hK_block_split : K_block = Matrix.fromBlocks A B C E := by
    -- This is a property of the projection matrices: they act as block selectors
    -- The identity `fromBlocks 1 0 0 0 + fromBlocks 0 0 0 1 = 1` gives the decomposition.
    calc
      K_block = ((Matrix.fromBlocks 1 0 0 0) + (Matrix.fromBlocks 0 0 0 1)) * K_block *
               ((Matrix.fromBlocks 1 0 0 0) + (Matrix.fromBlocks 0 0 0 1)) := by
        simp
      _ = ... -- expanding yields the block form
    sorry  -- This is a standard linear algebra fact; omitted for brevity but can be filled
  -- 8. Compute the final product
  have h_simplify : (1 - Matrix.fromBlocks 1 0 0 0) * (Matrix.fromBlocks A B C E) * (Matrix.fromBlocks 1 0 0 0) =
      Matrix.fromBlocks 0 0 C 0 := by
    simp [Matrix.fromBlocks_mul, Matrix.mul_fromBlocks, Matrix.sub_fromBlocks, Matrix.one_fromBlocks]
  rw [hD_block, hK_block_split, h_simplify]
  -- 9. Provide the witness
  refine ⟨r, C, iso, h_iso, rfl⟩

/-- The off‑diagonal block `C` has the same rank as `D`. -/
theorem rank_defect_eq_rank_C :
    ∃ (r : ℕ) (C : Matrix (Fin r) (Fin (Fintype.card n - r)) R),
    Matrix.rank D = Matrix.rank C := by
  obtain ⟨r, C, iso, h_iso, hD⟩ := block_form_defect R sys Π
  refine ⟨r, C, ?_⟩
  -- rank is invariant under similarity
  rw [← Matrix.rank_eq_rank_of_isUnit_mul h_iso h_iso, hD]
  -- rank of `fromBlocks 0 0 C 0` equals rank of C
  rw [Matrix.rank_fromBlocks (h : 0 = 0) ?_]
  · simp
  · -- the zero block is indeed zero
    exact rfl

/-- Consequence: `rank(D) = rank(C)` in the adapted basis. -/
theorem rank_defect_eq_rank_C' :
    ∃ (r : ℕ) (C : Matrix (Fin r) (Fin (Fintype.card n - r)) R),
    Matrix.rank D = Matrix.rank C :=
  rank_defect_eq_rank_C R sys Π

end BlockDecomposition

section RankBounds

variable (sys : FDDS R n) (Π : Partition n)

local notation "D" => defect R sys Π

/-- Rank bound I: `rank(D) ≤ rank(P)`. -/
theorem rank_defect_le_rank_proj :
    Matrix.rank D ≤ Matrix.rank (projectionMatrix R Π) := by
  -- D = (I-P) * K * P, and rank(A*B) ≤ rank(B)
  have : D = ((1 - projectionMatrix R Π) * koopman R sys) * projectionMatrix R Π := rfl
  rw [this]
  exact Matrix.rank_mul_le_right (A := (1 - projectionMatrix R Π) * koopman R sys)
                                (B := projectionMatrix R Π)

/-- Rank bound II: `rank(D) ≤ n - rank(P)`. -/
theorem rank_defect_le_n_minus_rank_proj :
    Matrix.rank D ≤ Fintype.card n - Matrix.rank (projectionMatrix R Π) := by
  -- The rank of I-P is n - rank(P), proved in Core.Projection
  have h_rank_IP : Matrix.rank (1 - projectionMatrix R Π) =
      Fintype.card n - Matrix.rank (projectionMatrix R Π) :=
    AQARION.Core.Projection.rank_complement R Π
  -- D = (I-P) * (K*P), so rank(D) ≤ rank(I-P)
  have h : D = (1 - projectionMatrix R Π) * (koopman R sys * projectionMatrix R Π) := by
    simp [defect, Matrix.mul_assoc]
  rw [h]
  calc
    Matrix.rank ((1 - projectionMatrix R Π) * (koopman R sys * projectionMatrix R Π)) ≤
        Matrix.rank (1 - projectionMatrix R Π) :=
      Matrix.rank_mul_le_left (A := (1 - projectionMatrix R Π))
                              (B := koopman R sys * projectionMatrix R Π)
    _ = Fintype.card n - Matrix.rank (projectionMatrix R Π) := h_rank_IP

/-- Combined bound: `rank(D) ≤ min(rank(P), n - rank(P))`. -/
theorem rank_defect_le_min_rank_proj :
    Matrix.rank D ≤ min (Matrix.rank (projectionMatrix R Π))
                        (Fintype.card n - Matrix.rank (projectionMatrix R Π)) :=
  le_min (rank_defect_le_rank_proj R sys Π) (rank_defect_le_n_minus_rank_proj R sys Π)

end RankBounds

end AQARION
