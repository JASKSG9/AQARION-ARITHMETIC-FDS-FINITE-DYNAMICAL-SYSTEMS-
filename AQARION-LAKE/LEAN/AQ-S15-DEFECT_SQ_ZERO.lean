theorem defect_sq_zero (P K : Matrix n n ℚ) (hP : P*P=P) :
  let D := (1-P)*K*P; D*D = 0 := by simp [mul_assoc, hP]
