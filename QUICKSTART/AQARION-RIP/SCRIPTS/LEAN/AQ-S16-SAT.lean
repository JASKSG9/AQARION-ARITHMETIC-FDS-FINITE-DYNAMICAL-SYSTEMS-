/-
AQ-S16-SAT-001 Lean sketch (NOT a completed proof)
Status: OPEN — collaboration target, zero claim of [FV]

Algebraic core to formalize:
  For A : Matrix (Fin 3) (Fin 3) ℚ with A 1 = 1,
  G = 1 - Aᵀ A,
  λ_max(G) = 1 ↔ ∃ v ≠ 0, v ⟂ 1, A v = 0 ↔ rank A < 3
  (since 1 ∉ ker A when A1 = 1).

This file is intentionally full of sorry and is not machine-checked.
-/

#check "AQ-S16-SAT-001 Lean target: rank(M)<3 ↔ λ_max(G)=1 under equal margins"
