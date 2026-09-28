# AQ-DYN-PULL-PREIMAGE-JOIN-001

**2026-09-27**

## Status

REFUTED — NEGATIVE CONTROL.

The candidate inclusion

    T^{-1}(E∨F)
      <=
    T^{-1}(E)∨T^{-1}(F)

is false.

## Counterexample

    X = {0,1,2}
    T = (0,0,1)

    E = {{0,2},{1}}
    F = {{0},{1,2}}

Then

    E∨F = {{0,1,2}}

and

    T^{-1}(E∨F) = {{0,1,2}}.

But

    T^{-1}(E) = {{0,1},{2}}

    T^{-1}(F) = {{0},{1,2}}

and therefore

    T^{-1}(E)∨T^{-1}(F)
      = {{0,1},{2}}.

The left side does not refine the right side.

## Significance

Pullback-stable join closure remains a verified candidate theorem.

It cannot be proved by the failed preimage-distributivity route.

The negative control is permanent and must remain in the test corpus.

## Governance

REFUTED / C4 BLOCKED / PROMOTION FALSE.
