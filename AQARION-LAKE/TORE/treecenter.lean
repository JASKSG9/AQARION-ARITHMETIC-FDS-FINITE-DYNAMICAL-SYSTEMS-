theorem finite_tree_aut_fixed_vertex_or_edge
  (G : FiniteTree Ω) (T : Perm) (hAut : IsAutomorphism G T) (hTree : IsTree G) :
  ∃ v, T v = v ∨ ∃ u v, G.Adj u v ∧ (T u = u ∧ T v = v ∨ T u = v ∧ T v = u)
