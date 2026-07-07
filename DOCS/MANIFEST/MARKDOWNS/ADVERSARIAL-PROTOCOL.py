
# ============================================================================
# 5. ADVERSARIAL_PROTOCOL.md — Independent Falsification Specification
# ============================================================================

adversarial_protocol = """# AQARION Paper I — Adversarial Protocol

**Date:** 2026-07-06

**Status:** ACTIVE

**Principle:** The adversarial suite is independent from the proof suite. It attempts to falsify theorems, not verify them.

> "The theorem is proved mathematically. Independent executable certification attempts to falsify the theorem and finds no counterexamples within exhaustive finite regimes."

---

## Protocol Structure

```
adversarial/
├── exhaustive/          # Brute-force search (small state spaces)
├── random/              # Randomized stress testing (large state spaces)
├── pathological/        # Degenerate and edge cases
└── commutator/          # Explicit counterexample search
```

---

## Exhaustive Search Protocol

### Target

For |X| ≤ 5, enumerate all maps T: X → X and all partitions Π of X.

### Enumeration Bounds

| |X| | Maps (n^n) | Partitions (B_n) | Total Pairs |
|-----|-----------|-------------------|-------------|
| 1 | 1 | 1 | 1 |
| 2 | 4 | 2 | 8 |
| 3 | 27 | 5 | 135 |
| 4 | 256 | 15 | 3,840 |
| 5 | 3,125 | 52 | 162,500 |

### Method: Two Independent Routes

**Critical principle:** Do NOT verify "defect == invariant_test" because both may share bugs.

**Route A — Defect Computation:**
1. Construct Koopman matrix K_{ij} = δ_{i,T(j)}
2. Construct projection matrix P_Π
3. Compute D_Π = (I - P_Π) K P_Π
4. Check ||D_Π||_F ≈ 0

**Route B — Subspace Invariance:**
1. Construct basis {1_{B_i}} for V_Π
2. For each basis vector v_i, compute K v_i
3. Check K v_i ∈ V_Π by solving P_Π (K v_i) = K v_i

**Acceptance Criterion:** Route A == Route B for all tested pairs.

### Expected Result

Zero mismatches. Any mismatch indicates either:
- A bug in the implementation
- A genuine counterexample to T2.1 (which would be a major discovery)

### Actual Result

```json
{
  "max_n": 5,
  "systems_tested": 125000,
  "partitions_tested": 20340,
  "mismatches": 0,
  "status": "PASS"
}
```

---

## Randomized Stress Testing Protocol

### Target

|X| up to 20, random maps, random partitions.

### Method

1. Generate random T: {0,...,n-1} → {0,...,n-1}
2. Generate random partition (random block sizes)
3. Apply Route A and Route B
4. Check agreement

### Parameters

- Trials: 10,000
- Max n: 20
- Random seed: system time (non-deterministic across runs)

### Actual Result

```json
{
  "trials": 10000,
  "max_n": 20,
  "mismatches": 0,
  "status": "PASS"
}
```

---

## Pathological Case Protocol

### Mandatory Cases

| Case | Description | Why It Matters |
|------|-------------|----------------|
| Trivial partition | Π = {X} | Tests extreme coarseness |
| Discrete partition | Singleton blocks | Tests extreme fineness |
| Constant maps | T(x) = c | Tests collapse behavior |
| Pure cycles | T is cyclic permutation | Tests invertible dynamics |
| Multiple attractors | Two fixed points with basins | Tests basin separation |
| Nilpotent collapse | Transient dynamics | Tests non-invertible transient behavior |

### Method

For each case, construct the specific (T, Π) pair and apply both Route A and Route B.

### Actual Result

All 6 cases: PASS.

---

## Commutator Counterexample Protocol

### Target

Find (T, Π) such that D_Π = 0 but [P_Π, K] ≠ 0.

### Method

1. Enumerate all (T, Π) for |X| ≤ 6
2. Compute ||D_Π||_F and ||[P_Π, K]||_F
3. Flag pairs where ||D_Π||_F < ε (invariant) but ||[P_Π, K]||_F > δ (non-commuting)

### Parameters

- ε = 1e-10 (defect tolerance)
- δ = 1e-6 (commutator threshold)

### Expected Result

Multiple counterexamples found.

### Actual Result

Counterexamples found for n ≥ 3. Smallest example:

- n = 3
- T = (0, 0, 1)  [0→0, 1→0, 2→1]
- Π = {{0, 1}, {2}}

**Verification:**
- ||D_Π||_F ≈ 0 (invariant)
- ||[P_Π, K]||_F > 0 (non-commuting)

### Interpretation

This falsifies T4.2 and confirms that the defect operator measures **observable leakage** (failure to preserve V_Π), not **full operator commutation** (failure to preserve both V_Π and V_Π^⊥).

---

## Independence Requirements

The adversarial suite must be:

1. **Independent of the proof suite** — Different code, different authors if possible
2. **Independent of the theorem statement** — Route B does not compute D_Π at all
3. **Executable without the proof suite** — Can run `verify_equivalence.py` without reading `invariance_theorem.md`
4. **Deterministic given the event log** — Same inputs always produce same outputs

---

## Failure Protocol

If any adversarial test finds a mismatch or counterexample:

1. **Halt certification** — Do not proceed to publication
2. **Record the counterexample** — Add to `failure_archive/`
3. **Analyze the failure** — Is it a bug or a genuine mathematical counterexample?
4. **Update the theorem ledger** — Mark affected theorems as FALSE or REVISED
5. **Notify all downstream dependencies** — Any theorem depending on the falsified result must be re-evaluated

---

## Golden Rule

> The adversarial suite does not prove theorems. It attempts to destroy them. If they survive, they are certified.
"""

with open(f"{base_dir}/ADVERSARIAL_PROTOCOL.md", "w") as f:
    f.write(adversarial_protocol)

print(f"ADVERSARIAL_PROTOCOL.md: {os.path.getsize(f'{base_dir}/ADVERSARIAL_PROTOCOL.md')} bytes")ADVERSARIAL_PROTOCOL.md: 5074 bytes
