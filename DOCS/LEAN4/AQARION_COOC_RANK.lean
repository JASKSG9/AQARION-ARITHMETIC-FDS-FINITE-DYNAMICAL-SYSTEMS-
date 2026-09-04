import Mathlib.Combinatorics.SimpleGraph.LapMatrix
import Mathlib.LinearAlgebra.Dimension.RankNullity
import Mathlib.LinearAlgebra.FiniteDimensional

/-!
AQARION — THM-COOC
Defect Rank via Target-Cooccurrence Components

PASS XVIII FORMALIZATION TARGET

IMPORTANT:
* This file formalizes the corrected one-copy target-cooccurrence graph.
* The withdrawn bipartite theorem is deliberately absent.
* This file is a proof target until compiled in the repository's pinned
  Lean/Mathlib environment.
-/

namespace AQARION

section Cooccurrence

variable {X ι : Type*}

/-- A target block `t` occurs from source block `s`. -/
def TargetSet
    (T : X → X) (block : ι → Set X)
    (s t : ι) : Prop :=
  ∃ x, x ∈ block s ∧ T x ∈ block t

/-- Two distinct target blocks co-occur from one source block. -/
def HAdj
    (T : X → X) (block : ι → Set X)
    (t u : ι) : Prop :=
  t ≠ u ∧
    ∃ s,
      TargetSet T block s t ∧
      TargetSet T block s u

/-- The one-copy target-cooccurrence graph. -/
def H
    (T : X → X) (block : ι → Set X) : SimpleGraph ι where
  Adj := HAdj T block
  symm := by
    intro t u h
    rcases h with ⟨hne, s, ht, hu⟩
    exact ⟨hne.symm, s, hu, ht⟩
  loopless := by
    intro t h
    exact h.1 rfl

/--
The graph constraint says that the coefficient function is equal
on every co-occurring pair of target blocks.
-/
def HConstant
    (T : X → X) (block : ι → Set X)
    (α : ι → ℝ) : Prop :=
  ∀ t u, H T block t u → α t = α u

/--
Equality propagates along graph reachability.
This is the interface needed by the Laplacian kernel theorem.
-/
theorem HConstant.reachable
    {T : X → X} {block : ι → Set X}
    {α : ι → ℝ}
    (hα : HConstant T block α) :
    ∀ {t u : ι},
      (H T block).Reachable t u →
      α t = α u := by
  intro t u hreach
  induction hreach with
  | refl =>
      rfl
  | tail hreach hadj ih =>
      exact (hα _ _ hadj).trans ih

/--
The reverse implication: equality on reachable vertices implies
equality on adjacent vertices.
-/
theorem reachable_to_HConstant
    {T : X → X} {block : ι → Set X}
    {α : ι → ℝ}
    (hα :
      ∀ {t u : ι},
        (H T block).Reachable t u →
        α t = α u) :
    HConstant T block α := by
  intro t u hadj
  exact hα (SimpleGraph.Reachable.single hadj)

/--
Laplacian kernel characterization of the co-occurrence constraint.

The exact final proof should use the current Mathlib theorem
`SimpleGraph.lapMatrix_mulVec_eq_zero_iff_forall_reachable`
together with `Matrix.toLin'`.
-/
theorem HConstant_iff_lapKernel
    {T : X → X} {block : ι → Set X}
    {α : ι → ℝ} :
    HConstant T block α ↔
      α ∈ LinearMap.ker
        (Matrix.toLin'
          (SimpleGraph.lapMatrix ℝ (H T block))) := by
  constructor
  · intro hα
    have hreach :
        ∀ {t u : ι},
          (H T block).Reachable t u →
          α t = α u :=
      hα.reachable
    -- Finish with the current Mathlib Laplacian/reachability theorem.
    -- The exact simp/rw shape depends on the pinned Mathlib revision.
    simpa [Matrix.mem_ker, Matrix.toLin'] using hreach
  · intro hker
    have hreach :
        ∀ {t u : ι},
          (H T block).Reachable t u →
          α t = α u := by
      -- Finish by applying the current Mathlib theorem in the
      -- reverse direction.
      simpa [Matrix.mem_ker, Matrix.toLin'] using hker
    exact reachable_to_HConstant hreach

end Cooccurrence

end AQARION



Important repository note: the two simpa endpoints above are intentionally the only API-sensitive portion of this first slice. The exact theorem argument order and the reduction of Matrix.toLin' to mulVec must be compiled against the repository's pinned Mathlib revision. They are not represented here as an already-observed successful build.

