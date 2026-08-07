import Mathlib.Algebra.Module.Basic
import Mathlib.Algebra.Module.LinearMap.Basic
import Mathlib.Data.Fin.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Set.Basic
import Mathlib.Data.Set.Finite
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Card
import Mathlib.Algebra.BigOperators.Group.Finset
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.Combinatorics.SimpleGraph.Connectivity

universe u

variable {n : ℕ}

/-- Structural representation of an indexed partition of `Fin n`. -/
structure Partition (n : ℕ) where
  ι : Type
  [fintype_ι : Fintype ι]
  [decidableEq_ι : DecidableEq ι]
  blocks : ι → Set (Fin n)
  nonempty : ∀ i : ι, (blocks i).Nonempty
  disjoint : ∀ i j : ι, i ≠ j → Disjoint (blocks i) (blocks j)
  cover : (⋃ i : ι, blocks i) = Set.univ

attribute [instance] Partition.fintype_ι Partition.decidableEq_ι

namespace Partition

/-- Canonical coordinate selector induced by the partition. -/
noncomputable def blockOf (π : Partition n) (x : Fin n) : π.ι :=
  Classical.choose
    (Set.mem_iUnion.mp (by
      rw [π.cover]
      exact Set.mem_univ x))

/-- Every point belongs to its selected block. -/
lemma blockOf_mem (π : Partition n) (x : Fin n) :
    x ∈ π.blocks (π.blockOf x) := by
  classical
  unfold blockOf
  exact Classical.choose_spec
    (Set.mem_iUnion.mp (by
      rw [π.cover]
      exact Set.mem_univ x))

/-- A point cannot belong to two distinct partition blocks. -/
lemma blockOf_eq_of_mem (π : Partition n) {i : π.ι} {x : Fin n}
    (hx : x ∈ π.blocks i) :
    π.blockOf x = i := by
  classical
  by_contra hne
  have hd : Disjoint (π.blocks i) (π.blocks (π.blockOf x)) :=
    π.disjoint i (π.blockOf x) hne
  exact (Set.disjoint_left.mp hd) hx (π.blockOf_mem x)

/-- All points in one block have the same canonical block coordinate. -/
lemma blockOf_block (π : Partition n) {i : π.ι} {x y : Fin n}
    (hx : x ∈ π.blocks i) (hy : y ∈ π.blocks i) :
    π.blockOf x = π.blockOf y := by
  rw [π.blockOf_eq_of_mem hx, π.blockOf_eq_of_mem hy]

/-- A chosen representative has the expected block coordinate. -/
lemma blockOf_rep (π : Partition n) (i : π.ι) :
    π.blockOf (π.nonempty i).some = i := by
  exact π.blockOf_eq_of_mem (π.nonempty i).some_mem

/-- Canonical equivalence between block membership and block coordinates. -/
lemma mem_blockOf_iff (π : Partition n) (x : Fin n) (i : π.ι) :
    π.blockOf x = i ↔ x ∈ π.blocks i := by
  constructor
  · intro h
    rw [← h]
    exact π.blockOf_mem x
  · intro hx
    exact π.blockOf_eq_of_mem hx

/-- Finite finset version of block `i`. -/
noncomputable def blockFinset (π : Partition n) (i : π.ι) : Finset (Fin n) :=
  (π.blocks i).toFinset

lemma mem_blockFinset_iff (π : Partition n) (i : π.ι) (x : Fin n) :
    x ∈ π.blockFinset i ↔ x ∈ π.blocks i := by
  exact Set.mem_toFinset

lemma blockFinset_nonempty (π : Partition n) (i : π.ι) :
    (π.blockFinset i).Nonempty := by
  rcases π.nonempty i with ⟨x, hx⟩
  use x
  rwa [mem_blockFinset_iff]

lemma blockFinset_card_pos (π : Partition n) (i : π.ι) :
    0 < (π.blockFinset i).card := by
  exact Finset.card_pos.mpr (π.blockFinset_nonempty i)

end Partition

-- ============================================================
-- 01A — BLOCK-CONSTANT SUBSPACE & VALUE EQUIVALENCE
-- ============================================================

/-- Subspace of block-constant observables. -/
def V_Pi (π : Partition n) : Submodule ℝ (Fin n → ℝ) where
  carrier :=
    {f | ∀ (i : π.ι) (x y : Fin n),
      x ∈ π.blocks i →
      y ∈ π.blocks i →
      f x = f y}
  zero_mem' := by
    intro i x y hx hy
    rfl
  add_mem' := by
    intro f g hf hg i x y hx hy
    dsimp
    rw [hf i x y hx hy, hg i x y hx hy]
  smul_mem' := by
    intro c f hf i x y hx hy
    dsimp
    rw [hf i x y hx hy]

/-- Block-value expansion from coordinates to observables. -/
def blockFunction (π : Partition n) (a : π.ι → ℝ) : Fin n → ℝ :=
  fun x => a (π.blockOf x)

/-- The expanded block-value function is block-constant. -/
lemma blockFunction_mem_V_Pi (π : Partition n) (a : π.ι → ℝ) :
    blockFunction π a ∈ V_Pi π := by
  intro i x y hx hy
  dsimp [blockFunction]
  rw [π.blockOf_eq_of_mem hx, π.blockOf_eq_of_mem hy]

/-- Linear equivalence between block coordinates and `V_Pi`. -/
noncomputable def blockValueEquiv (π : Partition n) :
    V_Pi π ≃ₗ[ℝ] (π.ι → ℝ) where
  toFun f i :=
    f.1 (π.nonempty i).some
  invFun a :=
    ⟨blockFunction π a, blockFunction_mem_V_Pi π a⟩
  left_inv f := by
    ext x
    let i := π.blockOf x
    have hx : x ∈ π.blocks i := π.blockOf_mem x
    have hr : (π.nonempty i).some ∈ π.blocks i := (π.nonempty i).some_mem
    exact f.2 i x (π.nonempty i).some hx hr
  right_inv a := by
    ext i
    dsimp [blockFunction]
    rw [π.blockOf_rep i]
  map_add' f g := rfl
  map_smul' c f := rfl

/-- Dimension of the block-constant observable space. -/
theorem dim_V_Pi (π : Partition n) :
    Module.finrank ℝ (V_Pi π) = Fintype.card π.ι := by
  rw [LinearEquiv.finrank_eq (blockValueEquiv π)]
  simp [Module.finrank_fintype_fun]

/-- A block-constant function has the value of its block representative. -/
lemma blockValue_of_mem (π : Partition n) {f : Fin n → ℝ}
    (hf : f ∈ V_Pi π) {i : π.ι} {x : Fin n}
    (hx : x ∈ π.blocks i) :
    f x = f (π.nonempty i).some := by
  exact hf i x (π.nonempty i).some hx (π.nonempty i).some_mem

-- ============================================================
-- 01B — CONCRETE FIBRE-AVERAGING PROJECTION OPERATOR
-- ============================================================

/-- Fibre-averaging projection operator `P_Pi`. -/
noncomputable def P_Pi (π : Partition n) : (Fin n → ℝ) →ₗ[ℝ] (Fin n → ℝ) where
  toFun f x :=
    let i := π.blockOf x
    (∑ y in π.blockFinset i, f y) / ((π.blockFinset i).card : ℝ)
  map_add' f g := by
    ext x
    dsimp
    rw [← Finset.sum_add_distrib]
    ring
  map_smul' c f := by
    ext x
    dsimp
    rw [Finset.mul_sum]
    ring

/-- The image of `P_Pi` always lies in the block-constant subspace `V_Pi`. -/
lemma P_Pi_mem_V_Pi (π : Partition n) (f : Fin n → ℝ) :
    P_Pi π f ∈ V_Pi π := by
  intro i x y hx hy
  dsimp [P_Pi]
  rw [π.blockOf_eq_of_mem hx, π.blockOf_eq_of_mem hy]

/-- `P_Pi` acts as identity on block-constant functions. -/
lemma P_Pi_apply_of_mem_V_Pi (π : Partition n) {f : Fin n → ℝ}
    (hf : f ∈ V_Pi π) (x : Fin n) :
    P_Pi π f x = f x := by
  dsimp [P_Pi]
  let i := π.blockOf x
  have hx : x ∈ π.blocks i := π.blockOf_mem x
  have h_const : ∀ y ∈ π.blockFinset i, f y = f x := by
    intro y hy
    rw [π.mem_blockFinset_iff] at hy
    exact hf i y x hy hx
  rw [Finset.sum_congr rfl h_const]
  rw [Finset.sum_const, smul_eq_mul]
  have hcard : ((π.blockFinset i).card : ℝ) ≠ 0 := by
    exact Nat.cast_ne_zero.mpr (ne_of_gt (π.blockFinset_card_pos i))
  exact mul_div_cancel_left₀ (f x) hcard

/-- Range of projection `P_Pi` is exactly the subspace `V_Pi`. -/
theorem range_P_Pi_eq_V_Pi (π : Partition n) :
    LinearMap.range (P_Pi π) = V_Pi π := by
  ext f
  constructor
  · rintro ⟨g, rfl⟩
    exact P_Pi_mem_V_Pi π g
  · intro hf
    use f
    ext x
    exact P_Pi_apply_of_mem_V_Pi π hf x

-- ============================================================
-- OPERATOR DEFINITIONS (KOOPMAN & DEFECT)
-- ============================================================

/-- Koopman pullback operator induced by map `T : Fin n → Fin n`. -/
def KoopmanOp (T : Fin n → Fin n) : (Fin n → ℝ) →ₗ[ℝ] (Fin n → ℝ) where
  toFun f x := f (T x)
  map_add' f g := rfl
  map_smul' c f := rfl

/-- Defect operator `D_Pi = (I - P_Pi) ∘ K ∘ P_Pi`. -/
noncomputable def DefectOp (π : Partition n) (T : Fin n → Fin n) :
    (Fin n → ℝ) →ₗ[ℝ] (Fin n → ℝ) :=
  (LinearMap.id - P_Pi π) ∘ₗ (KoopmanOp T) ∘ₗ (P_Pi π)

/-- Defect operator restricted to `V_Pi`. -/
noncomputable def DefectRestricted (π : Partition n) (T : Fin n → Fin n) :
    V_Pi π →ₗ[ℝ] (Fin n → ℝ) :=
  (DefectOp π T).comp (V_Pi π).subtype

-- ============================================================
-- 02 — KERNEL ↔ EDGE EQUALITY
-- ============================================================

/-- Bipartite incidence graph on `π.ι ⊕ π.ι`. -/
def G_Pi (π : Partition n) (T : Fin n → Fin n) : SimpleGraph (π.ι ⊕ π.ι) where
  Adj u v := match u, v with
    | Sum.inl i, Sum.inr j => ∃ x ∈ π.blocks i, T x ∈ π.blocks j
    | Sum.inr j, Sum.inl i => ∃ x ∈ π.blocks i, T x ∈ π.blocks j
    | _, _ => False
  symm := by
    rintro (i | i) (j | j) h <;> try contradiction
    exact h
  loopless := by
    rintro (i | i) h <;> contradiction

/-- Subspace of block coordinates equal along graph edges. -/
def E_G (π : Partition n) (T : Fin n → Fin n) : Submodule ℝ (π.ι → ℝ) where
  carrier := {a | ∀ i j, (G_Pi π T).Adj (Sum.inl i) (Sum.inr j) → a i = a j}
  zero_mem' := fun _ _ _ => rfl
  add_mem' := fun h1 h2 i j h => by dsimp; rw [h1 i j h, h2 i j h]
  smul_mem' := fun c h i j h => by dsimp; rw [h i j h]

/-- Characterization theorem: block function in defect kernel iff coordinates are edge-equal. -/
theorem defect_kernel_iff_edge_equal (π : Partition n) (T : Fin n → Fin n) (a : π.ι → ℝ) :
    DefectOp π T (blockFunction π a) = 0 ↔ a ∈ E_G π T := by
  constructor
  · intro hDefect i j hAdj
    have hD : ∀ x, DefectOp π T (blockFunction π a) x = 0 := fun x => by rw [hDefect]; rfl
    rcases hAdj with ⟨x, hx_i, hTx_j⟩
    have hmem : blockFunction π a ∈ V_Pi π := blockFunction_mem_V_Pi π a
    have hP : P_Pi π (blockFunction π a) = blockFunction π a := by
      ext z; exact P_Pi_apply_of_mem_V_Pi π hmem z
    have h_eval : (KoopmanOp T (blockFunction π a)) x = a j := by
      dsimp [KoopmanOp, blockFunction]
      rw [π.blockOf_eq_of_mem hTx_j]
    have h_block_x : π.blockOf x = i := π.blockOf_eq_of_mem hx_i
    have h_proj := hD x
    dsimp [DefectOp, LinearMap.comp, LinearMap.sub_apply, LinearMap.id_apply] at h_proj
    rw [hP] at h_proj
    have h_zero : (KoopmanOp T (blockFunction π a) - P_Pi π (KoopmanOp T (blockFunction π a))) x = 0 := h_proj
    rw [sub_eq_zero] at h_zero
    rw [h_eval] at h_zero
    have h_avg : P_Pi π (KoopmanOp T (blockFunction π a)) x = a i := by
      dsimp [P_Pi]
      rw [h_block_x]
      rw [← h_zero]
      rfl
    exact h_zero.symm
  · intro hE
    ext x
    have hmem : blockFunction π a ∈ V_Pi π := blockFunction_mem_V_Pi π a
    have hP : P_Pi π (blockFunction π a) = blockFunction π a := by
      ext z; exact P_Pi_apply_of_mem_V_Pi π hmem z
    dsimp [DefectOp, LinearMap.comp, LinearMap.sub_apply, LinearMap.id_apply]
    rw [hP]
    let i := π.blockOf x
    have hx : x ∈ π.blocks i := π.blockOf_mem x
    let j := π.blockOf (T x)
    have hTx : T x ∈ π.blocks j := π.blockOf_mem (T x)
    have hAdj : (G_Pi π T).Adj (Sum.inl i) (Sum.inr j) := ⟨x, hx, hTx⟩
    have h_eq : a i = a j := hE i j hAdj
    have h_koop : KoopmanOp T (blockFunction π a) x = a j := by
      dsimp [KoopmanOp, blockFunction]
      rw [π.blockOf_eq_of_mem hTx]
    have h_proj : P_Pi π (KoopmanOp T (blockFunction π a)) x = a j := by
      dsimp [P_Pi]
      rw [π.blockOf_eq_of_mem hx]
      have h_all : ∀ y ∈ π.blockFinset i, KoopmanOp T (blockFunction π a) y = a j := by
        intro y hy
        rw [π.mem_blockFinset_iff] at hy
        let j_y := π.blockOf (T y)
        have hTy : T y ∈ π.blocks j_y := π.blockOf_mem (T y)
        have hAdj_y : (G_Pi π T).Adj (Sum.inl i) (Sum.inr j_y) := ⟨y, hy, hTy⟩
        have h_eq_y := hE i j_y hAdj_y
        dsimp [KoopmanOp, blockFunction]
        rw [π.blockOf_eq_of_mem hTy]
        rw [← h_eq_y, h_eq]
      rw [Finset.sum_congr rfl h_all, Finset.sum_const, smul_eq_mul]
      have hcard : ((π.blockFinset i).card : ℝ) ≠ 0 := by
        exact Nat.cast_ne_zero.mpr (ne_of_gt (π.blockFinset_card_pos i))
      exact mul_div_cancel_left₀ (a j) hcard
    rw [h_koop, h_proj, sub_self]

-- ============================================================
-- 03 — EDGE EQUALITY ↔ CONNECTED COMPONENTS
-- ============================================================

/-- Functions on graph vertices constant on connected components. -/
def ConstOnComp {V : Type u} [Fintype V] [DecidableEq V] (G : SimpleGraph V) : Submodule ℝ (V → ℝ) where
  carrier := {f | ∀ u v, G.Reachable u v → f u = f v}
  zero_mem' := fun _ _ _ => rfl
  add_mem' := fun h1 h2 u v h => by dsimp; rw [h1 u v h, h2 u v h]
  smul_mem' := fun c h u v h => by dsimp; rw [h u v h]

/-- Isomorphism between restricted defect kernel and edge-equal coordinate subspace `E_G`. -/
noncomputable def ker_defect_restricted_equiv_E_G (π : Partition n) (T : Fin n → Fin n) :
    LinearMap.ker (DefectRestricted π T) ≃ₗ[ℝ] E_G π T where
  toFun f := ⟨blockValueEquiv π ⟨f.1.1, f.1.2⟩, by
    intro i j hAdj
    have hker := f.2
    dsimp [DefectRestricted, LinearMap.mem_ker] at hker
    have h_block : f.1.1 = blockFunction π (blockValueEquiv π ⟨f.1.1, f.1.2⟩) := by
      ext x
      dsimp [blockFunction, blockValueEquiv]
      rw [← blockValue_of_mem π f.1.2 (π.blockOf_mem x)]
    rw [h_block] at hker
    rw [defect_kernel_iff_edge_equal] at hker
    exact hker i j hAdj⟩
  invFun a := ⟨⟨blockFunction π a.1, blockFunction_mem_V_Pi π a.1⟩, by
    dsimp [DefectRestricted, LinearMap.mem_ker]
    rw [defect_kernel_iff_edge_equal]
    exact a.2⟩
  left_inv f := by
    ext x
    dsimp [blockFunction, blockValueEquiv]
    rw [← blockValue_of_mem π f.1.2 (π.blockOf_mem x)]
  right_inv a := by
    ext i
    dsimp [blockValueEquiv, blockFunction]
    rw [π.blockOf_rep i]
  map_add' f g := rfl
  map_smul' c f := rfl

/-- Dimension theorem for functions constant on connected graph components. -/
theorem dim_constOnComp {V : Type u} [Fintype V] [DecidableEq V] (G : SimpleGraph V) :
    Module.finrank ℝ (ConstOnComp G) = Fintype.card (G.ConnectedComponent) := by
  sorry

/-- Coordinate subspace dimension equals connected component count of `G_Pi(T)`. -/
theorem dim_E_G_eq_cComp (π : Partition n) (T : Fin n → Fin n) :
    Module.finrank ℝ (E_G π T) = Fintype.card ((G_Pi π T).ConnectedComponent) := by
  sorry

-- ============================================================
-- 04 — RANK-NULLITY & FINAL IDENTITY
-- ============================================================

/-- Main theorem: Kernel dimension of restricted defect matches graph component count. -/
theorem AQ_LEAN_RANK_01 (π : Partition n) (T : Fin n → Fin n) :
    Module.finrank ℝ (LinearMap.ker (DefectRestricted π T)) =
    Fintype.card ((G_Pi π T).ConnectedComponent) := by
  rw [LinearEquiv.finrank_eq (ker_defect_restricted_equiv_E_G π T)]
  exact dim_E_G_eq_cComp π T

/-- Final rank identity: `rank(D_Pi) = |Pi| - c_comp(G_Pi(T))`. -/
theorem defect_rank_identity (π : Partition n) (T : Fin n → Fin n) :
    Module.finrank ℝ (LinearMap.range (DefectOp π T)) =
    Fintype.card π.ι - Fintype.card ((G_Pi π T).ConnectedComponent) := by
  have h_range : LinearMap.range (DefectOp π T) = LinearMap.range (DefectRestricted π T) := by
    ext y
    constructor
    · rintro ⟨f, rfl⟩
      use ⟨P_Pi π f, P_Pi_mem_V_Pi π f⟩
      dsimp [DefectRestricted, DefectOp, LinearMap.comp, LinearMap.sub_apply, LinearMap.id_apply]
      have hP2 : P_Pi π (P_Pi π f) = P_Pi π f := by
        ext z; exact P_Pi_apply_of_mem_V_Pi π (P_Pi_mem_V_Pi π f) z
      rw [hP2]
    · rintro ⟨⟨f, hf⟩, rfl⟩
      use f
      dsimp [DefectRestricted, DefectOp, LinearMap.comp, LinearMap.sub_apply, LinearMap.id_apply]
      rw [P_Pi_apply_of_mem_V_Pi π hf]
  rw [h_range]
  have h_rn := LinearMap.finrank_range_add_finrank_ker (DefectRestricted π T)
  have h_dim_V := dim_V_Pi π
  have h_ker := AQ_LEAN_RANK_01 π T
  omega
