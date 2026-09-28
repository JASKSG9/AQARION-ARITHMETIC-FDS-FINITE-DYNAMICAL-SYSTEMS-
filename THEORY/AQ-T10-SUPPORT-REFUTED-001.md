# AQ-T10-SUPPORT-REFUTED-001

**2026-09-27**

## Status

T10 SUPPORT-DETERMINACY — KILLED.

The support of the defect operator is NOT determined solely by the
constraint graph.

A minimal n=3 witness gives two instances with the same constraint
graph but different supp(D).

Therefore graph connectivity correctly determines the kernel/rank
invariant, but not the entrywise support pattern.

## Correct replacement

For source block r and target block q,

    D_ij =
      [ 1_{T(i) in B_q} - V_{rq} ] / |B_q|,

where V_{rq} is the normalized target incidence of source block r.

Hence

    (i,j) ∈ supp(D)

exactly when

    0 < V_{rq} < 1.

## Consequence

The support formula is a separate invariant.

The kernel/rank theorem remains valid.

## Governance

T10: KILLED.
Replacement support formula: CLOSED.
No promotion of the old support-determinacy claim.
