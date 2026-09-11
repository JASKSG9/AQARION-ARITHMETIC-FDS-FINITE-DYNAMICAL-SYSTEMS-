import Mathlib.Data.Setoid.Basic
import Mathlib.Data.Fintype.Card

variable {α : Type*} [Fintype α] [DecidableEq α]

def setoidMap (f : α ≃ α) (s : Setoid α) : Setoid α where
  r x y := s.r (f.symm x) (f.symm y)
  iseqv := ⟨fun x => s.iseqv.refl _, fun h => s.iseqv.symm h, fun h1 h2 => s.iseqv.trans h1 h2⟩

def blockCount (s : Setoid α) : ℕ := Fintype.card (Quotient s)

lemma blockCount_map (f : α ≃ α) (s : Setoid α) :
  blockCount (setoidMap f s) = blockCount s :=
  Fintype.card_congr (Equiv.quotientCongr f (by intro x y; rfl))

lemma blockCount_strict_mono {s t : Setoid α} (h : s < t) :
  blockCount t < blockCount s := by
  -- surjective Quotient.mapId not injective
  sorry

def orbitJoin (f : α ≃ α) : ℕ → Setoid α → Setoid α
  | 0, s => s
  | k+1, s => (orbitJoin f k s) ⊔ (setoidMap f (orbitJoin f k s))

theorem orbit_expansion (f : α ≃ α) (s : Setoid α) (k : ℕ) :
  orbitJoin f k s = (Finset.range (k+1)).sup (fun j => setoidMap (f ^ j) s) := by sorry

-- Anchored-Cycle
variable (a c : Fin d → α) (f : α ≃ α) (ha : f a = a)
  (hc : ∀ i, f (c i) = c ((i+1) % d))

def R_anchored : Setoid α := -- {{a,c 0}, singletons}
  sorry

theorem anchored_step (k : ℕ) (hk : k < d) :
  blockCount (orbitJoin f k R_anchored) = Fintype.card α - k := by sorry

theorem anchored_cycle_lemma :
  orbitJoin f d R_anchored = ⊤ ∧ blockCount (orbitJoin f (d-1) R_anchored) = 1 + 1 := by sorry
-- K2R specialization a=2r, d=2r, R=M_r
