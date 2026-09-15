import Mathlib

namespace AQS15

open Matrix

variable {ι κ : Type*}
variable [Fintype ι] [Fintype κ]
variable [DecidableEq ι] [DecidableEq κ]
variable {R : Type*} [Field R]

structure PenroseData
    (B G : Matrix κ κ R) : Prop where
  bgb : B * G * B = B
  gbg : G * B * G = G
  bg_symm : (B * G)ᵀ = B * G
  gb_symm : (G * B)ᵀ = G * B

theorem penrose_transport
    (U : Matrix ι κ R)
    (B G : Matrix κ κ R)
    (hU : Uᵀ * U = 1)
    (h : PenroseData B G) :
    PenroseData (U * B * Uᵀ) (U * G * Uᵀ) := by
  constructor
  · calc
      (U * B * Uᵀ) * (U * G * Uᵀ) * (U * B * Uᵀ)
          = U * (B * G * B) * Uᵀ := by
              simp_rw [Matrix.mul_assoc]
              rw [← Matrix.mul_assoc Uᵀ U, hU]
              simp_rw [Matrix.mul_one]
      _ = U * B * Uᵀ := by rw [h.bgb]
  · calc
      (U * G * Uᵀ) * (U * B * Uᵀ) * (U * G * Uᵀ)
          = U * (G * B * G) * Uᵀ := by
              simp_rw [Matrix.mul_assoc]
              rw [← Matrix.mul_assoc Uᵀ U, hU]
              simp_rw [Matrix.mul_one]
      _ = U * G * Uᵀ := by rw [h.gbg]
  · calc
      ((U * B * Uᵀ) * (U * G * Uᵀ))ᵀ
          = (U * (B * G) * Uᵀ)ᵀ := by
              simp_rw [Matrix.mul_assoc]
              rw [← Matrix.mul_assoc Uᵀ U, hU]
              simp_rw [Matrix.mul_one]
      _ = U * (B * G)ᵀ * Uᵀ := by
              simp [Matrix.transpose_mul]
      _ = U * (B * G) * Uᵀ := by rw [h.bg_symm]
      _ = (U * B * Uᵀ) * (U * G * Uᵀ) := by
              simp_rw [Matrix.mul_assoc]
              rw [← Matrix.mul_assoc Uᵀ U, hU]
              simp_rw [Matrix.mul_one]
  · calc
      ((U * G * Uᵀ) * (U * B * Uᵀ))ᵀ
          = (U * (G * B) * Uᵀ)ᵀ := by
              simp_rw [Matrix.mul_assoc]
              rw [← Matrix.mul_assoc Uᵀ U, hU]
              simp_rw [Matrix.mul_one]
      _ = U * (G * B)ᵀ * Uᵀ := by
              simp [Matrix.transpose_mul]
      _ = U * (G * B) * Uᵀ := by rw [h.gb_symm]
      _ = (U * G * Uᵀ) * (U * B * Uᵀ) := by
              simp_rw [Matrix.mul_assoc]
              rw [← Matrix.mul_assoc Uᵀ U, hU]
              simp_rw [Matrix.mul_one]

end AQS15
