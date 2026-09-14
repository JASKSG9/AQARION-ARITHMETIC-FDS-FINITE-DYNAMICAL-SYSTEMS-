import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Setoid.Basic
import Mathlib.GroupTheory.GroupAction.Basic

namespace Aqarion

/-- Base structure for an incidence graph with voltage assignments over ZMod g. -/
structure VoltageGraph (V : Type*) (g : ℕ) [Fact (g > 0)] where
  adj : V → V → Prop
  voltage : V → V → ZMod g
  anti_symm : ∀ u v, voltage u v = - voltage v u

/-- Lifted cover graph vertex set. -/
def LiftedVertex (V : Type*) (g : ℕ) := V × ZMod g

/-- Lifted cover graph adjacency relation. -/
def LiftedAdj {V : Type*} {g : ℕ} [Fact (g > 0)] (G : VoltageGraph V g) 
    (u1 u2 : LiftedVertex V g) : Prop :=
  G.adj u1.1 u2.1 ∧ u2.2 = u1.2 + G.voltage u1.1 u2.1

/-- Push-forward of a binary relation along a map T. -/
def relPush {V : Type*} (r : V → V → Prop) (T : V → V) (x y : V) : Prop :=
  ∃ u v, r u v ∧ x = T u ∧ y = T v

/-- Lemma verifying component map equivariance over join relations. -/
theorem T_star_join {V : Type*} (P Q : V → V → Prop) (T : V → V)
    (hP : ∀ x y, P x y → P (T x) (T y))
    (hQ : ∀ x y, Q x y → Q (T x) (T y)) :
    ∀ x y, (relPush P T x y ∨ relPush Q T x y) → relPush (fun a b => P a b ∨ Q a b) T x y := by
  intro x y h
  rcases h with ⟨u, v, huv, rfl, rfl⟩ | ⟨u, v, huv, rfl, rfl⟩
  · exact ⟨u, v, Or.inl huv, rfl, rfl⟩
  · exact ⟨u, v, Or.inr huv, rfl, rfl⟩

/-- Fiber decoupling under zero cyclomatic potential condition. -/
theorem voltage_decoupling_isomorphism {V : Type*} {g : ℕ} [Fact (g > 0)]
    (G : VoltageGraph V g) (potential : V → ZMod g)
    (h_pot : ∀ u v, G.adj u v → G.voltage u v = potential v - potential u) :
    ∀ (u v : V) (k : ZMod g),
      LiftedAdj G (u, k) (v, k + G.voltage u v) ↔
      (G.adj u v ∧ (k + G.voltage u v - potential v = k - potential u)) := by
  intro u v k
  constructor
  · intro h
    refine ⟨h.1, ?_⟩
    rw [h_pot u v h.1]
    ring
  · intro h
    refine ⟨h.1, ?_⟩
    rw [h_pot u v h.1]

end Aqarion
