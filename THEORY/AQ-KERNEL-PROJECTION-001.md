# AQ-KERNEL-PROJECTION-001

**2026-09-27**

## Status

CLOSED analytically; Lean OPEN.

Let Phi be the partition projection and D_Phi the corresponding
defect operator.

Let G^con be the target-coincidence/constraint graph:

- vertices are target partition blocks;
- a source block induces a clique on the target blocks reached from it.

Then

    dim ker(D_Phi) = c(G^con)

and

    rank(D_Phi) = m - c(G^con),

where m is the number of target blocks.

## Proof status

The analytic proof is the block-constant nullspace argument.

Independent modular-rank verification:

    166,483 / 166,483

at primes

    p = 97, 101, 103

with zero failures.

## Definition lock

G^con is NOT the ordinary directed quotient graph.

Replacing G^con by the ordinary quotient graph changes the invariant and is prohibited.

## Governance

Analytic theorem: CLOSED.
Computational verification: CLOSED.
Lean: OPEN.
Publication promotion: BLOCKED pending formal/evidence policy requirements.
