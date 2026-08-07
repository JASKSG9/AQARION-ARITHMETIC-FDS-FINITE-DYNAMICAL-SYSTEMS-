/-
AQARION J30-B — Pure Graph Theorem
dim(ConstOnComp G) = |π₀(G)|
No defect / Koopman / partition imports.
-/

import Mathlib.Combinatorics.SimpleGraph.Connectivity
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.Data.Fintype.Card
import Mathlib.Algebra.Module.Submodule.Basic

universe u
variable {V : Type u} [Fintype V] [DecidableEq V]

namespace AQARION.PureGraph

def ConstOnComp (G : SimpleGraph V) : Submodule ℝ (V → ℝ) where
  carrier := {f | ∀ ⦃u v⦄, G.Reachable u v → f u = f v}
  zero_mem' := by intro u v _; rfl
  add_mem'  := by intro f g hf hg u v h; dsimp; rw [hf h, hg h]
  smul_mem' := by intro c f hf u v h; dsimp; rw [hf h]

noncomputable def pullback (G : SimpleGraph V) :
    (G.ConnectedComponent → ℝ) →ₗ[ℝ] (V → ℝ) where
  toFun a v := a (G.connectedComponentMk v)
  map_add'  := by intros; ext; rfl
  map_smul' := by intros; ext; rfl

lemma pullback_mem (G : SimpleGraph V) (a : G.ConnectedComponent → ℝ) :
    pullback G a ∈ ConstOnComp G := by
  intro u v h
  -- Replace with the lemma your Mathlib provides:
  -- ConnectedComponent.eq_of_reachable / .sound / Quot.sound
  have : G.connectedComponentMk u = G.connectedComponentMk v :=
    SimpleGraph.ConnectedComponent.eq_of_reachable _ h
  simp [pullback, this]

noncomputable def pullbackSub (G : SimpleGraph V) :
    (G.ConnectedComponent → ℝ) →ₗ[ℝ] ConstOnComp G :=
  LinearMap.codRestrict (ConstOnComp G) (pullback G) (pullback_mem G)

/-- Descent via Quot.lift — no representative choice. -/
noncomputable def descent (G : SimpleGraph V) (f : ConstOnComp G) :
    G.ConnectedComponent → ℝ :=
  Quot.lift (fun v => f.1 v) (fun u v huv => f.2 huv)

@[simp] lemma descent_mk (G : SimpleGraph V) (f : ConstOnComp G) (v : V) :
    descent G f (G.connectedComponentMk v) = f.1 v := rfl

lemma pullbackSub_descent (G : SimpleGraph V) (f : ConstOnComp G) :
    pullbackSub G (descent G f) = f := by
  ext v; exact (descent_mk G f v).symm

lemma descent_pullbackSub (G : SimpleGraph V) (a : G.ConnectedComponent → ℝ) :
    descent G (pullbackSub G a) = a := by
  -- Prefer Quot.inductionOn if ConnectedComponent.ind is unavailable
  refine Quot.inductionOn a.val ?_  -- adapt to your ConnectedComponent representation
  intro v; rfl

noncomputable def constOnCompEquiv (G : SimpleGraph V) :
    ConstOnComp G ≃ₗ[ℝ] (G.ConnectedComponent → ℝ) where
  toFun      := descent G
  invFun     := pullbackSub G
  left_inv   := pullbackSub_descent G
  right_inv  := descent_pullbackSub G
  map_add'   := by intros; rfl
  map_smul'  := by intros; rfl

theorem dim_constOnComp (G : SimpleGraph V) :
    Module.finrank ℝ (ConstOnComp G) = Fintype.card G.ConnectedComponent := by
  rw [LinearEquiv.finrank_eq (constOnCompEquiv G)]
  -- Use the exact name from your Mathlib:
  exact Module.finrank_fintype_fun_eq_card _

end AQARION.PureGraph

RUN AND AUDIT EVEN IF YOU HSVE TO WITH PYTHON IN YOUR SANDBOX THEN REPORT
