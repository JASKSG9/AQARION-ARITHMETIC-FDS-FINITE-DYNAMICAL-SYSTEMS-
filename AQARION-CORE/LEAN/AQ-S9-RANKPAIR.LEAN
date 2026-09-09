import Mathlib

namespace AQARION

/-!
S9 rank-pair formalization boundary.

Mathematical identities:

  rank [P | KP]
    = rank P + rank ((1-P) K P)

and

  rank [P
        KP]
    = rank P

under the hypothesis P² = P.

The horizontal identity follows from

  KP = PKP + (1-P)KP,

with

  im(PKP) ⊆ im(P),
  im((1-P)KP) ⊆ ker(P),

and

  im(P) ∩ ker(P) = {0}.

The vertical identity follows from

  ker [P; KP] = ker P,

because Px = 0 implies KPx = 0.

The following declarations deliberately remain formal-open until
the exact Mathlib matrix/block-map representation and rank-additivity
lemmas are compiler-verified in the canonical Lean environment.
-/

variable {R : Type*} [DivisionRing R]
variable {n : Type*} [Fintype n] [DecidableEq n]

/--
Horizontal rank-pair identity.

FORMAL-OPEN:
The theorem statement is retained as the target formalization.
No `sorry` is promoted as a proof.
-/
theorem rank_horizontal
    (P K : Matrix n n R)
    (hP : P ^ 2 = P) :
    Matrix.rank (Matrix.fromCols P (K * P))
      =
    Matrix.rank P
      + Matrix.rank ((1 - P) * K * P) := by
  sorry

/--
Vertical rank-pair identity.

FORMAL-OPEN:
The mathematical kernel argument is established, but the exact
Matrix.rank/rank-nullity transport into this representation remains
to be compiler-certified.
-/
theorem rank_vertical
    (P K : Matrix n n R)
    (hP : P ^ 2 = P) :
    Matrix.rank (Matrix.fromRows P (K * P))
      =
    Matrix.rank P := by
  sorry

/-!
Formalization target:

1. Establish the concrete linear-map representation of
   `Matrix.fromCols P (K * P)`.

2. Prove the image decomposition

      range [P | KP]
        = range P ⊔ range ((1-P)KP)

   with zero intersection.

3. Transport direct-sum dimension to Matrix.rank.

4. For the vertical map, prove kernel equality

      ker [P; KP] = ker P

   and transport through rank-nullity.

5. Replace the `sorry` declarations only after an actual
   Lean 4.33.1 compiler receipt is available.

Governance:
  FORMAL-OPEN.
  No C4 promotion.
-/

end AQARION
