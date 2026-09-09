theorem rank_horizontal (P K : Matrix n n R) (hP : P^2=P) :
  rank (fromCols P (K*P)) = rank P + rank ((1-P)*K*P) := by
  -- KP = PKP + QKP, im(PKP)⊂im P, im(QKP)⊂ker P, direct sum
  sorry -- rank additivity lemma im P ⊓ ker P =0

theorem rank_vertical (P K : Matrix n n R) (hP : P^2=P) :
  rank (fromRows P (K*P)) = rank P := by
  -- ker [P;KP] = {x|Px=0 ∧ KPx=0} = {x|Px=0} because Px=0 → KPx=0
  have hker : ker (fromRows P (K*P)) = ker P := by ext x; simp
  rw [rank_nullity, rank_nullity, hker]
