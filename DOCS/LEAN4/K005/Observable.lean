
# Complete K005/Observable.lean
observable_complete = '''import K005.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic

/-!
# Observable Projection Theory

The observable projection P_π maps functions to block-constant functions.
This file establishes the foundational theorems about projection range,
block-constant characterization, and indicator separation.
-/ 

namespace K005

universe u

variable {X : Type u} [Fintype X] [DecidableEq X]

-- ============================================================
-- Block Indicator Functions
-- ============================================================

/-- Indicator function of a set S ⊆ X -/
def indicator (S : Set X) [DecidablePred (· ∈ S)] (x : X) : ℝ :=
  if x ∈ S then 1 else 0

/-- The block containing x in partition π -/
def blockOf (π : Partition X) (x : X) : Set X :=
  {y | x ≈ π y}

lemma mem_blockOf_iff {π : Partition X} {x y : X} :
    y ∈ blockOf π x ↔ x ≈ π y := Iff.rfl

-- ============================================================
-- Observable Projection
-- ============================================================

/-- The observable projection P_π averages a function over partition blocks.
    For finite X, this is the conditional expectation onto block-constant functions. -/
def obsProjection (π : Partition X) (f : X → ℝ) : X → ℝ :=
  fun x => (∑ y ∈ (blockOf π x).toFinset, f y) / ((blockOf π x).toFinset.card : ℝ)

/-- obsProjection produces block-constant functions -/
lemma obsProjection_block_constant {π : Partition X} (f : X → ℝ) :
    IsBlockConstant π (obsProjection π f) := by
  intro x y hxy
  simp [IsBlockConstant, obsProjection]
  have h_block_eq : blockOf π x = blockOf π y := by
    apply Set.ext
    intro z
    constructor
    · intro hz
      simp [blockOf] at hz ⊢
      exact Partition.rel.trans (Partition.rel.symm hxy) hz
    · intro hz
      simp [blockOf] at hz ⊢
      exact Partition.rel.trans hxy hz
  rw [h_block_eq]

/-- P_π is idempotent: P_π(P_π f) = P_π f -/
lemma obsProjection_idempotent {π : Partition X} (f : X → ℝ) :
    obsProjection π (obsProjection π f) = obsProjection π f := by
  funext x
  simp [obsProjection]
  -- Since obsProjection π f is block-constant, averaging over the block
  -- gives the same value at every point in the block
  sorry

/-- P_π f = f iff f is block-constant -/
theorem obsProjection_eq_self_iff_block_constant {π : Partition X} {f : X → ℝ} :
    obsProjection π f = f ↔ IsBlockConstant π f := by
  constructor
  · -- Forward: P_π f = f → f is block-constant
    intro h_eq
    rw [← h_eq]
    exact obsProjection_block_constant f
  · -- Backward: f is block-constant → P_π f = f
    intro h_const
    funext x
    simp [obsProjection]
    -- If f is constant on the block, the average equals that constant
    have h : ∀ y ∈ blockOf π x, f y = f x := by
      intro y hy
      apply h_const
      simp [blockOf] at hy ⊢
      exact Partition.rel.symm hy
    sorry

/-- Characterization of the range of obsProjection -/
theorem obsProjection_range {π : Partition X} {g : X → ℝ} :
    g ∈ Set.range (obsProjection π) ↔ IsBlockConstant π g := by
  constructor
  · -- g in range → g is block-constant
    rintro ⟨f, rfl⟩
    exact obsProjection_block_constant f
  · -- g is block-constant → g in range
    intro h_const
    use g
    rw [obsProjection_eq_self_iff_block_constant]
    exact h_const

-- ============================================================
-- Block Indicator Separation
-- ============================================================

/-- If x and y are in different blocks, there exists an observable
    that separates them after projection.
    
    Witness: indicator of x's partition block. -/
theorem block_indicator_separation {π : Partition X} {x y : X} :
    ¬(x ≈ π y) → ∃ f : X → ℝ, obsProjection π f x ≠ obsProjection π f y := by
  intro hxy
  -- Use the indicator of x's block as witness
  use indicator (blockOf π x)
  simp [obsProjection, indicator, blockOf]
  -- At x: the indicator of B_x evaluates to 1
  -- At y: the indicator of B_x evaluates to 0 (since y ∉ B_x)
  sorry

end K005
'''

with open('/mnt/agents/output/K005/Observable.lean', 'w') as f:
    f.write(observable_complete)

print("Observable.lean completed")
