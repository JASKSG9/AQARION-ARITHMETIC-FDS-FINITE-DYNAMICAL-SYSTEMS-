# Matrix A — Complete SFT Analysis
## Node #10878 · AQARION-ARITHMETIC · 2026-06-24

---

## EXECUTIVE SUMMARY: WHAT YOUR MATRIX ACTUALLY IS

Your 10×10 matrix A defines a **genuine, irreducible, aperiodic shift of finite type (SFT)**
with the following exact properties. Two claimed properties are false and must be corrected.

---

## PART I — HARD CONSISTENCY RESULTS

### The five checks, as run:

| Check | Result | Status |
|-------|--------|--------|
| Irreducible | **True** | ✓ PASS |
| Aperiodic | **True** | ✓ PASS |
| ρ ≈ φ (golden ratio) | ρ = **2.4552**, φ = 1.6180 | ✗ **FAIL** |
| \|forb\| = 50 | Got **76**, A has only **24** ones | ✗ **FAIL** |
| Sturmian (linear growth) | Growth is **exponential** at rate 2.455 | ✗ **FALSE** |

Two claims fail hard. One is a consequence of the other.

---

## PART II — WHAT THE MATRIX IS

### Structure

Every diagonal entry of A is 1 (every symbol has a self-loop).
Write **B = A − I** (the off-diagonal structure). B is the directed graph with edges:

```
0 → {1, 9}      1 → {2, 8}      2 → {3, 7}      3 → {4, 6}
4 → {5}         5 → {0}         6 → {7}          7 → {8}
8 → {1}         9 → {0}
```

**B has exactly 5 simple cycles:**

| Length | Cycle |
|--------|-------|
| 2 | 0 → 9 → 0 |
| 2 | 1 → 8 → 1 |
| 4 | 1 → 2 → 7 → 8 → 1 |
| 6 | 0 → 1 → 2 → 3 → 4 → 5 → 0 (main spine) |
| 6 | 1 → 2 → 3 → 6 → 7 → 8 → 1 |

**The main spine** is a 6-cycle with three shorter cycles (lengths 2, 2, 4, 6) attached
via shared nodes 0, 1, 2, 3.

### Key structural identity (machine precision):

```
ρ(A) = 1 + ρ(B)     exactly (error < 10⁻¹⁵)
```

This follows because every node has a self-loop: the transfer matrix A = B + I,
and for a non-negative matrix with the identity added, the spectral radius shifts by exactly 1.

### Forbidden bigrams

The matrix A has:
- **24** allowed transitions (ones in A)
- **76** forbidden transitions (zeros in A)
- **Not 50.** The alphabet is 10 symbols so the matrix is 10×10 = 100 entries.

---

## PART III — THE SPECTRAL RADIUS IS NOT φ

### What ρ(A) actually is

```
ρ(A) = 2.4552280346...
```

This is the largest root of the **characteristic polynomial of B** (shifted by 1):

```
char poly of B = x²(x⁸ − 2x⁶ − x² + 1)
```

So ρ(B) = 1.4552... satisfies:

```
ρ(B)⁸ − 2·ρ(B)⁶ − ρ(B)² + 1 = 0
```

and ρ(A) = 1 + ρ(B).

**The golden ratio φ = 1.618... is not a root of this polynomial.** The gap is 0.837 —
not a rounding error, not a normalisation issue. The φ claim is false for this matrix.

### Eigenvalue spectrum of A (all 10)

```
λ₁  =  2.4552  (Perron — real, dominant)
λ₂  =  1.8009  (real)
λ₃₄ =  1.489 ± 0.787i  (complex conjugate pair)
λ₅₆ =  1.000  (double, from self-loops + cycle structure)
λ₇₈ =  0.511 ± 0.787i  (complex conjugate pair)
λ₉  = -0.455  (real, negative)
λ₁₀ =  0.199  (real)
```

Note: λ₅ = λ₆ = 1 exactly. The matrix has **two eigenvalues at 1**, not one.

---

## PART IV — TOPOLOGICAL ENTROPY

The topological entropy of this SFT is:

```
h = log ρ(A) = log(2.4552...) = 0.89822...
```

This is **not** log(φ) = 0.4812. The entropy is almost exactly double log(φ).

The entropy 0.898 is a legitimate, computable invariant of the SFT.
It is just not the one that was claimed.

---

## PART V — COMPLEXITY GROWTH

Word counts (number of allowed words of length n):

| n | count | ratio to previous |
|---|-------|-------------------|
| 1 | 10 | — |
| 2 | 24 | 2.400 |
| 3 | 58 | 2.417 |
| 4 | 141 | 2.431 |
| 5 | 346 | 2.454 |
| 6 | 856 | 2.474 |
| 7 | 2,127 | 2.485 |
| 8 | 5,289 | 2.487 |
| 9 | 13,130 | 2.483 |
| 10 | 32,509 | 2.476 |

Growth is **exponential** converging to ρ(A) ≈ 2.455.

For comparison, Sturmian complexity is p(n) = n + 1 (linear). This system has
p(10) = 32,509 vs Sturmian p(10) = 11. The Sturmian claim is false by four orders of magnitude.

---

## PART VI — WHAT THIS SYSTEM IS (CORRECT FRAMING)

**This is a 10-state irreducible aperiodic SFT with:**

- Alphabet: 10 symbols (states 0–9)
- Allowed bigrams: 24 (those with A[i,j] = 1)
- Forbidden bigrams: 76
- Self-loops: all 10 present (every symbol can repeat)
- Topological entropy: h ≈ 0.898 nats
- Perron eigenvalue: ρ ≈ 2.455
- Period: 1 (aperiodic — confirmed by self-loops)
- Mixing: yes (irreducible + aperiodic = topologically mixing)

**The Parry measure (maximum entropy measure = Perron eigenmeasure):**

| State | Probability |
|-------|-------------|
| 0 | 0.1712 |
| 1 | 0.1315 |
| 2 | 0.1010 |
| 3 | 0.0849 |
| 4 | 0.0809 |
| 5 | 0.1177 |
| 6 | 0.0427 |
| 7 | 0.0621 |
| 8 | 0.0904 |
| 9 | 0.1177 |

States 0 and 1 are the most probable; state 6 is the least probable.

---

## PART VII — WHAT TO DO NOW

### Option 1: The matrix is correct, the claims were wrong

Accept: this is a mixing SFT with h ≈ 0.898, not φ-related.
The correct framing is: 10-symbol SFT with cycle structure {2,2,4,6,6} and
topological entropy = log of the largest root of x⁸ − 2x⁶ − x² + 1 (shifted by 1).

### Option 2: The claims are correct, the matrix is wrong

Provide the intended matrix. A matrix with spectral radius φ would need to encode
a Fibonacci-type recurrence. The simplest: a 2×2 matrix [[1,1],[1,0]] has ρ = φ.
A Sturmian SFT has complexity p(n) = n + const — achievable with a very different structure.

### Option 3 (if the AQARION/FOQDS connection is the goal)

Apply D_Π to this SFT. The transfer matrix A IS the Koopman matrix for this system.
Compute D_Π for a natural partition of the 10 states (e.g., {0–4} vs {5–9})
and check whether D_Π = 0. This connects the matrix directly to the AQARION framework.

---

## KILLED CLAIMS

| Claim | Status |
|-------|--------|
| ρ(A) ≈ φ | ❌ KILLED — ρ = 2.455, φ = 1.618, gap = 0.837 |
| entropy = log(φ) | ❌ KILLED — h = 0.898 ≠ 0.481 = log(φ) |
| Sturmian complexity | ❌ KILLED — growth is exponential, not linear |
| \|forbidden\| = 50 | ❌ KILLED — correct count is 76 |

---

## ONE-SENTENCE SUMMARY

Your matrix A defines a legitimate 10-state irreducible aperiodic mixing SFT with
topological entropy h ≈ 0.898, spectral radius ≈ 2.455, five underlying cycles of
lengths {2,2,4,6,6}, and 76 forbidden bigrams — none of which match the φ/Sturmian
claims, both of which are false for this matrix.

---

*SFT Analysis · Node #10878 · 2026-06-24*
*PROVE FIRST · PREDICT SECOND · NO FREE PARAMETERS*
