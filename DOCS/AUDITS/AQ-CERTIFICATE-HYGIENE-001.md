# AQ-CERTIFICATE-HYGIENE-001

**2026-09-27**

## Required corrections

### 54-state docstring

Incorrect:

    {1:29, 2:2, 3:1, 6:3}

because the multiplicities sum to 54.

Correct:

    {1:28, 2:2, 3:1, 6:3}

which sums to 53.

### Runner count

Incorrect:

    25 tests

Correct:

    40 FAST + 3 exhaustive = 43

### Spectral language

Replace:

    acquires additional eigenvalues

with:

    can introduce additional eigenvalues

The latter is supported by the counterexample

    T = (0,0,0,1).

Replace:

    mixing time ~ 1/(1-lambda_2)

with:

    spectral relaxation scale.

### Power-map theorem

Restrict the theorem to odd prime powers, or replace Jacobi-symbol
language with the appropriate Kronecker-symbol formulation for
composite powers such as

    N = 4, 8.

## Governance

These are certificate/documentation corrections.

They do not constitute new mathematical theorems.
