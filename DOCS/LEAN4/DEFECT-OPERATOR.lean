-- Lean 4 structure definition
structure CoarseGrainedSystem where
  domain : Type
  partition : domain → Nat
  transition : domain → domain

def DefectOperator (P : projection) (K : Koopman) : Operator := 
  (I - P) * K * P
