import Mathlib.Data.Finset.Basic
import Mathlib.Data.Set.Basic

/-!
# AQARION: Certified Invariant Boundary Framework
Status: Machine-checked Lean 4 formal proofs for Core Boundary Equivalence.
-/

namespace AQARION

variable {n : ℕ}

def IsBlockConstant (f : Fin n → ℝ) (P : Finset (Finset (Fin n))) : Prop :=
  ∀ B ∈ P, ∀ x ∈ B, ∀ y ∈ B, f x = f y

def IsInvariant (T : Fin n → Fin n) (P : Finset (Finset (Fin n))) : Prop :=
  ∀ f : Fin n → ℝ, IsBlockConstant f P → IsBlockConstant (f ∘ T) P

def IsCongruence (T : Fin n → Fin n) (P : Finset (Finset (Fin n))) : Prop :=
  ∀ B ∈ P, ∀ x ∈ B, ∀ y ∈ B, ∃ B' ∈ P, T x ∈ B' ∧ T y ∈ B'

def IsLumpable (T : Fin n → Fin n) (P : Finset (Finset (Fin n))) : Prop :=
  ∀ Bj ∈ P, ∃ Br ∈ P, ∀ x ∈ Bj, T x ∈ Br

/-- Auxiliary Indicator Function for a Block -/
noncomputable def indicatorBlock (B : Finset (Fin n)) (x : Fin n) : ℝ :=
  if x ∈ B then 1 else 0

lemma indicator_is_block_constant (B : Finset (Fin n)) (P : Finset (Finset (Fin n))) 
    (hB : B ∈ P) (h_disjoint : ∀ B1 ∈ P, ∀ B2 ∈ P, B1 ≠ B2 → Disjoint B1 B2) :
    IsBlockConstant (indicatorBlock B) P := by
  intro B' hB' x hx y hy
  by_cases hEQ : B' = B
  · subst hEQ
    simp [indicatorBlock, hx, hy]
  · have hdis : Disjoint B' B := h_disjoint B' hB' B hB hEQ
    have hx_not : x ∉ B := fun h => Finset.disjoint_left.mp hdis hx h
    have hy_not : y ∉ B := fun h => Finset.disjoint_left.mp hdis hy h
    simp [indicatorBlock, hx_not, hy_not]

/-- Theorem AQ-THM-INVARIANTBOUNDARY-001: Machine-Checked Equivalence of Lumpability and Invariance -/
theorem lumpable_iff_invariant (T : Fin n → Fin n) (P : Finset (Finset (Fin n)))
    (h_cover : ∀ x : Fin n, ∃! B ∈ P, x ∈ B)
    (h_nonempty : ∀ B ∈ P, B.Nonempty)
    (h_disjoint : ∀ B1 ∈ P, ∀ B2 ∈ P, B1 ≠ B2 → Disjoint B1 B2) :
    IsLumpable T P ↔ IsInvariant T P := by
  constructor
  · intro h_lump f h_const Bj hBj x hx y hy
    rcases h_lump Bj hBj with ⟨Br, hBr, hmap⟩
    have hTx : T x ∈ Br := hmap x hx
    have hTy : T y ∈ Br := hmap y hy
    exact h_const Br hBr (T x) hTx (T y) hTy
  · intro h_inv Bj hBj
    rcases h_nonempty Bj hBj with ⟨x0, hx0⟩
    rcases (h_cover (T x0)).exists with ⟨Br, hBr, hTx0⟩
    use Br, hBr
    intro y hy
    have h_ind_const : IsBlockConstant (indicatorBlock Br) P :=
      indicator_is_block_constant Br P hBr h_disjoint
    have h_pullback_const : IsBlockConstant ((indicatorBlock Br) ∘ T) P :=
      h_inv (indicatorBlock Br) h_ind_const
    have h_eval : ((indicatorBlock Br) ∘ T) x0 = ((indicatorBlock Br) ∘ T) y :=
      h_pullback_const Bj hBj x0 hx0 y hy
    dsimp [Function.comp] at h_eval
    rw [indicatorBlock, if_pos hTx0] at h_eval
    by_contra h_not_in
    rw [indicatorBlock, if_neg h_not_in] at h_eval
    exact absurd h_eval.symm zero_ne_one

/-- Lemma AQ-LEM-LATTICE-BRIDGE-001: Machine-Checked Congruence Bridge -/
theorem congruence_iff_lumpable (T : Fin n → Fin n) (P : Finset (Finset (Fin n)))
    (h_cover : ∀ x : Fin n, ∃! B ∈ P, x ∈ B)
    (h_nonempty : ∀ B ∈ P, B.Nonempty) :
    IsCongruence T P ↔ IsLumpable T P := by
  constructor
  · intro h_cong Bj hBj
    rcases h_nonempty Bj hBj with ⟨x0, hx0⟩
    rcases h_cong Bj hBj x0 hx0 x0 hx0 with ⟨Br, hBr, hTx0, _⟩
    use Br, hBr
    intro y hy
    rcases h_cong Bj hBj x0 hx0 y hy with ⟨Br', hBr', hTx0', hTy'⟩
    have h_uniq := (h_cover (T x0)).unique ⟨hBr, hTx0⟩ ⟨hBr', hTx0'⟩
    subst h_uniq
    exact hTy'
  · intro h_lump Bj hBj x hx y hy
    rcases h_lump Bj hBj with ⟨Br, hBr, hmap⟩
    use Br, hBr
    exact ⟨hmap x hx, hmap y hy⟩

end AQARION
