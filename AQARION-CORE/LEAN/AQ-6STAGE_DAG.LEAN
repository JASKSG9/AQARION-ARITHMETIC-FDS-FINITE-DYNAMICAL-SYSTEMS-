-- Stage 1: blockConst
def blockConst {X : Type*} [Fintype X] (Π : Partition X) :
  (Π.blocks → ℝ) →ₗ[ℝ] (X → ℝ) := sorry -- ι_Π

lemma finrank_blockConst : finrank ℝ (range (blockConst Π)) = Π.blocks.card := sorry

-- Stage 2: defectRestricted
def defectRestricted (T : X → X) (Π : Partition X) :
  (Π.blocks → ℝ) →ₗ[ℝ] (X → ℝ) :=
  (1 - P Π) ∘ₗ (pullback T) ∘ₗ (blockConst Π)

-- Stage 3: kernel iff component constant
def cooccurrenceGraph (T) (Π) : SimpleGraph (Fin m) := sorry
theorem kernel_iff_component_constant (v) :
  v ∈ ker (defectRestricted T Π) ↔
  ∀ i j, Connected (cooccurrenceGraph T Π) i j → v i = v j := sorry

-- Stage 4: indicator basis
def componentIndicator (C : ConnectedComponent) : (Fin m → ℝ) := sorry
theorem componentIndicatorBasis : Basis (componentIndicator) := sorry

-- Stage 5: dim ker = c
theorem dim_ker_eq_components :
  finrank ℝ (ker (defectRestricted T Π)) = (cooccurrenceGraph T Π).nComponents := sorry

-- Stage 6: rank-nullity → Matrix.rank = m - c
theorem rank_defect_eq_block_minus_components (T) (Π) :
  (defectMatrix T Π).rank = m - c := by
  rw [Matrix.rank_eq_finrank_range_toLin, finrank_range_add_finrank_ker,
      finrank_blockConst, dim_ker_eq_components]
