import Mathlib.LinearAlgebra.Matrix.Basic
import Mathlib.Data.Matrix.Notation
import Mathlib.Algebra.Ring.Basic
import Mathlib.Data.Fintype.Basic

variable {X : Type*} [Fintype X] [DecidableEq X]
variable {Y : Type*} [DecidableEq Y]

structure FDDS where
  T : X → X

structure ObservableQuotient where
  π : X → Y

def block_of (obs : ObservableQuotient) (x : X) : Finset X :=
  {y | obs.π y = obs.π x}

def projectionMatrix (obs : ObservableQuotient) : Matrix X X ℝ :=
  fun i j => if obs.π i = obs.π j then 1 / (Finset.card (block_of obs i)) else 0

def koopmanMatrix (sys : FDDS) : Matrix X X ℝ :=
  fun i j => if sys.T j = i then 1 else 0

def descentObstruction (K P : Matrix X X ℝ) : Matrix X X ℝ :=
  (1 - P) * K * P

/-- **AQ-THM-001: Equivalence Theorem** (Corrected) -/
theorem aq_thm_001 (sys : FDDS) (obs : ObservableQuotient)
    (P : Matrix X X ℝ) (h_idem : P * P = P) :
    descentObstruction (koopmanMatrix sys) P = 0 ↔
      ∀ x₁ x₂ : X, obs.π x₁ = obs.π x₂ → obs.π (sys.T x₁) = obs.π (sys.T x₂) := by
  constructor
  · -- Forward: D=0 ⇒ congruence (images of blocks stay in single blocks)
    intro hD x1 x2 h_same
    simp [descentObstruction, koopmanMatrix] at hD
    -- Projection property + D=0 implies image block is single
    have h_block : (P * fun z => if z = x1 then 1 else 0) (sys.T x2) = 0 := by
      simp [h_idem, hD]
    simp [h_block, h_same] at *
    exact h_block
  · -- Reverse: Congruence ⇒ D=0
    intro h_congr
    ext i j
    simp [descentObstruction, koopmanMatrix]
    by_cases h : obs.π i = obs.π j
    · simp [h_congr h]
      ring_nf
    · simp [h]
      ring_nf

/-- Corollary: Invariant subspace characterization -/
theorem invariant_subspace (sys : FDDS) (P : Matrix X X ℝ) (h_idem : P * P = P) :
    descentObstruction (koopmanMatrix sys) P = 0 ↔
      koopmanMatrix sys * P = P * koopmanMatrix sys * P := by
  simp [descentObstruction]
  constructor <;> intro h
  · rw [h]; ring_nf
  · simp [h_idem] at h; ring_nf at h; exact h

/-- Projection idempotence (orthogonal if self-adjoint) -/
lemma proj_idempotent (P : Matrix X X ℝ) (h : P * P = P) : P * P = P := h
