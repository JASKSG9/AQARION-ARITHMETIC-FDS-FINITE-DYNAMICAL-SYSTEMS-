import Mathlib.LinearAlgebra.Projection
import Mathlib.Algebra.Module.LinearMap.Basic

variable {R : Type*} [Ring R] {M : Type*} [AddCommGroup M] [Module R M]

def Q_of {P : Module.End R M} (hP : P * P = P) : Module.End R M := 1 - P

theorem PQ_zero {P : Module.End R M} (hP : P * P = P) : P * Q_of hP = 0 := by
  unfold Q_of; rw [mul_sub, mul_one, hP, sub_self]

theorem QP_zero {P : Module.End R M} (hP : P * P = P) : Q_of hP * P = 0 := by
  unfold Q_of; rw [sub_mul, one_mul, hP, sub_self]

def D_of (P K : Module.End R M) (hP : P * P = P) : Module.End R M :=
  Q_of hP * K * P

theorem PD_zero {P K : Module.End R M} (hP : P * P = P) :
  P * D_of P K hP = 0 := by
  unfold D_of; rw [← mul_assoc, PQ_zero hP, zero_mul]

theorem DQ_zero {P K : Module.End R M} (hP : P * P = P) :
  D_of P K hP * Q_of hP = 0 := by
  unfold D_of Q_of
  calc Q_of hP * K * P * (1 - P)
      = Q_of hP * K * (P * (1 - P)) := by simp [mul_assoc]
    _ = Q_of hP * K * 0 := by
      have : P * (1 - P) = 0 := by rw [mul_sub, mul_one, hP, sub_self]
      rw [this]
    _ = 0 := by simp

theorem D_sq_zero {P K : Module.End R M} (hP : P * P = P) :
  D_of P K hP * D_of P K hP = 0 := by
  have hPD := PD_zero (P:=P) (K:=K) hP
  calc D_of P K hP * D_of P K hP
      = Q_of hP * K * (P * D_of P K hP) := by simp [mul_assoc, D_of]
    _ = Q_of hP * K * 0 := by rw [hPD]
    _ = 0 := by simp

theorem DP_eq_D {P K : Module.End R M} (hP : P * P = P) :
  D_of P K hP * P = D_of P K hP := by
  unfold D_of; rw [mul_assoc, mul_assoc, hP]

theorem QD_eq_D {P K : Module.End R M} (hP : P * P = P) :
  Q_of hP * D_of P K hP = D_of P K hP := by
  unfold D_of Q_of
  have hQ : (1 - P) * (1 - P) = 1 - P := by
    rw [sub_mul, one_mul, mul_sub, mul_one, hP]; abel
  calc (1 - P) * ((1 - P) * K * P)
      = ((1 - P) * (1 - P)) * K * P := by simp [mul_assoc]
    _ = (1 - P) * K * P := by rw [hQ]

-- Freeze D=QKP, D=KPQ quarantined. No assumption on K.
-- DQ=0 now present — fixes public sync failure.
import Mathlib.LinearAlgebra.Projection
import Mathlib.Algebra.Module.LinearMap.Basic

namespace AQARION

variable {R : Type*} [Ring R]
variable {M : Type*} [AddCommGroup M] [Module R M]

/-
AQ-S9-DEFECT

Canonical definitions:

  Q = I - P
  D = Q K P

No assumption on K is required for the algebra below.
-/

def Q_of {P : Module.End R M}
    (hP : P * P = P) : Module.End R M :=
  1 - P

theorem PQ_zero
    {P : Module.End R M}
    (hP : P * P = P) :
    P * Q_of hP = 0 := by
  unfold Q_of
  rw [mul_sub, mul_one, hP, sub_self]

theorem QP_zero
    {P : Module.End R M}
    (hP : P * P = P) :
    Q_of hP * P = 0 := by
  unfold Q_of
  rw [sub_mul, one_mul, hP, sub_self]

def D_of
    (P K : Module.End R M)
    (hP : P * P = P) : Module.End R M :=
  Q_of hP * K * P

theorem PD_zero
    {P K : Module.End R M}
    (hP : P * P = P) :
    P * D_of P K hP = 0 := by
  unfold D_of
  rw [← mul_assoc, PQ_zero hP, zero_mul]

theorem DQ_zero
    {P K : Module.End R M}
    (hP : P * P = P) :
    D_of P K hP * Q_of hP = 0 := by
  unfold D_of Q_of
  calc
    (1 - P) * K * P * (1 - P)
        = (1 - P) * K * (P * (1 - P)) := by
            simp [mul_assoc]
    _ = (1 - P) * K * 0 := by
          have h : P * (1 - P) = 0 := by
            rw [mul_sub, mul_one, hP, sub_self]
          rw [h]
    _ = 0 := by simp

theorem D_sq_zero
    {P K : Module.End R M}
    (hP : P * P = P) :
    D_of P K hP * D_of P K hP = 0 := by
  have hPD := PD_zero (P := P) (K := K) hP
  calc
    D_of P K hP * D_of P K hP
        = Q_of hP * K * (P * D_of P K hP) := by
            simp [mul_assoc, D_of]
    _ = Q_of hP * K * 0 := by rw [hPD]
    _ = 0 := by simp

theorem DP_eq_D
    {P K : Module.End R M}
    (hP : P * P = P) :
    D_of P K hP * P = D_of P K hP := by
  unfold D_of
  rw [mul_assoc, mul_assoc, hP]

theorem QD_eq_D
    {P K : Module.End R M}
    (hP : P * P = P) :
    Q_of hP * D_of P K hP = D_of P K hP := by
  unfold D_of Q_of
  have hQ : (1 - P) * (1 - P) = 1 - P := by
    rw [sub_mul, one_mul, mul_sub, mul_one, hP]
    abel
  calc
    (1 - P) * ((1 - P) * K * P)
        = ((1 - P) * (1 - P)) * K * P := by
            simp [mul_assoc]
    _ = (1 - P) * K * P := by
          rw [hQ]
    _ = D_of P K hP := by
          rfl

end AQARION
