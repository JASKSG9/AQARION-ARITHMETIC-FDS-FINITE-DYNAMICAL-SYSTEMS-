import Mathlib.Data.Fintype.Card
import Mathlib.Data.Setoid.Partition

def surjQuotOfLe {α : Type*} {s t : Setoid α} (h : s ≤ t) :
  Quotient s → Quotient t :=
  Quotient.map id h

lemma surjQuotOfLe_surjective {α : Type*} {s t : Setoid α} (h : s ≤ t) :
  Function.Surjective (surjQuotOfLe h) := by
  intro q; induction q using Quotient.ind with
  | _ x => exact ⟨Quotient.mk s x, rfl⟩

lemma card_quotient_le_of_le {α : Type*} [Fintype α] {s t : Setoid α}
  (h : s ≤ t) [DecidableRel s.r] [DecidableRel t.r] :
  Fintype.card (Quotient t) ≤ Fintype.card (Quotient s) :=
  Fintype.card_le_of_surjective _ (surjQuotOfLe_surjective h)
