# AQ-DYN-PULL-CLOSURE-001

**2026-09-27**

## Target theorem

For an equivalence relation E on finite X define

    Phi(E) = E ∨ T^{-1}(E).

Iterating Phi from E gives the pullback closure

    C^-(E).

## Elementary properties

The construction is intended to establish:

    E <= C^-(E)

    E <= F  ->  C^-(E) <= C^-(F)

    C^-(C^-(E)) = C^-(E)

and finite stabilization.

The fixed points are exactly the backward-stable equivalence
relations:

    C^-(E)=E
      iff
    T^{-1}(E)<=E.

## Important directional distinction

Backward stability is

    E(Tx,Ty) -> E(x,y).

Forward congruence is

    E(x,y) -> E(Tx,Ty).

They are different conditions and must not be conflated.

## Quotient formulation

For q_E : X -> X/E,

    T^{-1}(E) = ker(q_E ∘ T).

Thus backward stability is

    ker(q_E ∘ T) <= ker(q_E).

This means q_E factors through q_E∘T.

It does NOT in general mean

    q_E∘T factors through q_E.

That latter statement corresponds to the opposite kernel inclusion.

## Open theorem

Prove that the fixed points of C^- are closed under arbitrary joins.

This is the direct route to AQ-DYN-PULL-JOIN-001.
