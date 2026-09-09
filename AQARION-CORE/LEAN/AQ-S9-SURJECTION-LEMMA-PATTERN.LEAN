import Mathlib.Data.Fintype.Card
import Mathlib.Data.Setoid.Partition

def surjQuotOfLe {α : Type*} {s t : Setoid α} (h : s ≤ t) :
  Quotient s → Quotient t :=
  Quotient.map id h

lemma surjQuotOfLe_surjective {α} {s t : Setoid α} (h : s ≤ t) :
  Function.Surjective (surjQuotOfLe h) := by
  intro q; induction q using Quotient.ind with
  | _ x => exact ⟨Quotient.mk s x, rfl⟩

lemma card_quotient_le_of_le {α : Type*} [Fintype α] [DecidableRel s.r] [DecidableRel t.r]
  {s t : Setoid α} (h : s ≤ t) :
  Fintype.card (Quotient t) ≤ Fintype.card (Quotient s) :=
  Fintype.card_le_of_surjective _ (surjQuotOfLe_surjective h)

lemma delta_nonneg {n} (P Q : Setoid (Fin n)) [Fintype (Fin n)] :
  0 ≤ (Fintype.card (Quotient P) - Fintype.card (Quotient (P ⊔ Q))) := by
  have : Fintype.card (Quotient (P ⊔ Q)) ≤ Fintype.card (Quotient P) :=
    card_quotient_le_of_le (le_sup_left)
  omega
