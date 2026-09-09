import Mathlib.Data.Fintype.Card
import Mathlib.LinearAlgebra.Dimension.Finrank

-- Stage 1: blockConst ι_Π : (Fin m → ℝ) →ₗ (X → ℝ)
-- Stage 2: defectRestricted = (1-P) ∘ₗ pullback T ∘ₗ blockConst
-- Stage 3: kernel_iff_component_constant
-- Stage 4: componentIndicator basis
-- Stage 5: dim_ker = c(G)
-- Stage 6: rank = m - c via Matrix.rank_eq_finrank_range_toLin

-- Keep def not opaque/axiom to avoid contamination
-- Pin Lean 4.33.1 post-soundness-fix
