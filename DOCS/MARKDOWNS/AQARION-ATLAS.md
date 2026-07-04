# AQARION ATLAS
## System Atlas · Notation Glossary · Mathematical Object Definitions
## Louisville Node #1 · Paper A8 · Kaprekar Spectral Geometry
## Updated: M21 2026

---

## §1. Core Systems — Three Distinct Objects (MUST NOT CONFLATE)

### System I: 715-State Digit-Multiset Quotient
- **ID:** AQ-DEF-001
- **States:** Unordered multisets of 4 digits from {0,...,9} = C(13,4) = 715
- **Map:** Induced by Kaprekar on multiset representatives
- **Status:** VERIFIED
- **Warning:** This is NOT the same as the image or the gap-pair quotient

### System II: 55-State Gap-Pair Quotient
- **ID:** AQ-DEF-002
- **States:** Equivalence classes under gap-pair structure = 55 states
- **Status:** VERIFIED
- **Warning:** MUST NOT conflate with System I or System III

### System III: 54-State Corrected Canonical Quotient (= Image)
- **ID:** AQ-DEF-003
- **States:** |Image(K_{10,4})| = 54 = T_{10} - 1 = C(11,2) - 1
- **Identity:** 54 = triangular number T_{10} minus 1 = C(11,2) - 1
- **Status:** VERIFIED [AQ-THM-001]
- **This is the primary object for Paper A8**

---

## §2. Domain Definitions

### Domain A
- **Contents:** Integers 1000–9999 without leading zeros
- **Size:** 8999 non-repdigit states
- **Depth sum:** ≈8990
- **Label correction:** Pre-M20 documents had A and B reversed [K-03]

### Domain B
- **Contents:** Padded 4-digit strings 0000–9999 (includes 0000–0999)
- **Size:** 9999 non-repdigit states (excludes repdigits 0000, 1111, ..., 9999)
- **Depth sum:** ≈9989
- **N_τ:** [383, 576, 2400, 1272, 1518, 1656, 2184] for τ=1,...,7
- **τ=3 peak:** N_τ(3) = 2400 is the dominant depth
- **Label correction:** Pre-M20 documents had A and B reversed [K-03]

---

## §3. Notation Glossary

| Symbol | Definition | Status |
|--------|-----------|--------|
| K_{b,d} | Kaprekar map in base b, d digits | V |
| |Image(K_{10,4})| | Size of image set = 54 | V |
| μₖ | k-th eigenvalue of normalized Laplacian | V |
| μ₁ | Fiedler eigenvalue (algebraic connectivity) | V |
| μ₁(A) | Fiedler eigenvalue, Domain A ≈ 0.16144 | V |
| μ₁(B) | Fiedler eigenvalue, Domain B ≈ 0.16243 | V |
| F_H | Gauge invariant ≈ 4.222 | V |
| N_τ | Count of states at depth τ | V |
| τ | Transient depth to attractor | V |
| D_τ | Defect operator for depth partition | V |
| defect_nonmarkov | = 0 universally | V |
| H_norm | Normalized basin entropy ∈ [0,1] | V |
| ρ(τ) | Recurrence density field (scaling limit) | C |
| μ_N | Empirical measure (1/N)Σδ(τ−τᵢ) | V |
| F[ρ] | Free energy functional | H |
| κ | Interaction coupling | H |
| κ_c(d,B) | Critical coupling (phase boundary) | C |
| ℒ | Transfer operator (Koopman approx) | C |
| φ(state) | Difference coordinate = max − min = p − r | V |
| δ | = φ(state) = p − r ∈ {1,...,B−1} | V |
| F(δ) | 1D map on difference coordinate | V |
| x* | Fixed point of Kaprekar map | V |
| T_{n} | Triangular number n(n+1)/2 | V |
| ι_3 | Image size map for d=3 negabase | H |
| Ω_{b,3} | State space of d=3 base-b Kaprekar | V |
| SPD-CCS | Spectral Phase Dynamics engine | V |
| AML | Adversarial Mathematics Laboratory | framework |
| AMF | Adversarial Mathematics Framework (12 modules) | framework |

---

## §4. The Kaprekar Map — Formal Definition

**d-digit base-b Kaprekar map** K_{b,d}: S → S where

S = {(x₀,...,x_{d-1}) : xᵢ ∈ {0,...,|b|−1}, not all xᵢ equal}

**Step 1:** Sort digits descending: desc = sort(x, ↓)  
**Step 2:** Sort digits ascending: asc = sort(x, ↑)  
**Step 3:** Compute diff = val(desc, b) − val(asc, b)  
where val uses standard positional notation  
**Step 4:** Represent diff as d-digit base-b number → next state

**Key identity for d=3:**
```
val(desc, B) - val(asc, B) = p·B² + q·B + r - (r·B² + q·B + p)
                           = (p-r)·B² + (r-p)
                           = (p-r)·(B² - 1)
```
Middle digit q **cancels completely**. [AQ-THM-010 Component A]

---

## §5. d=3 Theorem — Formal Statement and Proof Outline

**Theorem AQ-THM-010:** For any integer base B ≥ 2, the map K on 
non-repdigit 3-digit states with digits in {0,...,B−1} has exactly one 
fixed-point attractor. All trajectories converge to it. H_norm = 0.

**Proof outline:**

1. **Middle-digit cancellation** [VERIFIED]:  
   diff = (p−r)·(B²−1) where p=max, r=min of state

2. **Semiconjugacy to 1D** [VERIFIED]:  
   φ(state) = p−r defines F(δ) = next δ on {1,...,B−1}  
   Next state depends only on φ(current state)

3. **Fixed point formula** [VERIFIED for even B; INCOMPLETE for odd B — K-14]:  
   Even B: x* = (B/2−1, B−1, B/2)  
   Odd B: x* = ((B−1)/2, B−1, (B+1)/2)  

4. **Uniqueness** [VERIFIED computationally for B=2,...,16]:  
   F(δ) has unique fixed point on {1,...,B−1}  
   All trajectories converge → H_norm = 0

5. **Open:** Algebraic proof of uniqueness for all B (direct F(δ) analysis, not Banach)

---

## §6. Phase Diagram Summary

| Base | d=2 H | d=3 H | d=4 H | d=5 H | d=2 N |
|------|-------|-------|-------|-------|-------|
| −6   | 0.9915 | **0.0000** | 0.9579 | 0.7432 | 30 |
| −8   | 0.9794 | **0.0000** | 0.9419 | 0.8384 | 56 |
| −10  | 0.9848 | **0.0000** | **0.0000** | 0.9263 | 90 |
| −12  | 0.9969 | **0.0000** | 0.9355 | **0.0955** | 132 |
| −14  | 0.9970 | **0.0000** | 0.9724 | — | 182 |
| −16  | 0.9874 | **0.0000** | 0.8747 | — | 240 |

**Peak entropy: d=2 universally** [K-01 killed d=5 claim]  
**Anomalies:** b=−10,d=4 and b=−12,d=5 collapse [TARGET-05]

---

## §7. AMF Module Registry

| Module | Name | Function |
|--------|------|----------|
| A | Universal System Generator | GenerateFDDS(n, constraints, seed) over 13 families |
| B | Property Specification Language | Executable theorem properties, not hardcoded |
| C | Adversary Generator | 20+ mutation operators, tagged |
| D | Counterexample Reduction | Delta-debug to minimal witness |
| E | Collision Discovery Engine | Signature → Hash → Bucket → GI test → Atlas |
| F | Independent Oracle Layer | WL / nauty / Lean / sage / networkx |
| G | Mathematical Mutation Testing | Detect weak verification |
| H | Literature Adversary | Novel / Extension / Equivalent / Known / Conflict |
| I | Proof Pressure Score | Quantified verification strength |
| J | Autonomous Observatory | Continuous generation, anomaly clustering |
| K | Research Memory | Persistent failure archive, never rediscover |
| L | Research Graph | Full dependency/refutation/formalization graph |

---

## §8. Validation Pipeline

```
V0 Structure    → file exists, parses, fields present
V1 SHA256       → hash recorded, immutable
V2 Replay       → script reruns, same output
V3 Provenance   → seed, version, hardware documented
V4 Math Pred    → formal predicate verified (Lean target)
V5 Promotion    → claim advances in OVCR
```

---

## §9. Epistemic Tag Definitions

| Tag | Meaning |
|-----|---------|
| [V] VERIFIED | Exhaustive computational verification complete |
| [T] THEOREM | Proof exists (may have minor gaps) |
| [H] HEURISTIC | Motivated guess, partial support, not verified |
| [C] CONJECTURE | Stated precisely, no proof, not contradicted |
| [K] KILLED | False, flawed, or conflated — permanent record |

---

## §10. Open Problems Bounty

| # | Problem | Reward |
|---|---------|--------|
| 1 | Prove or disprove: F(δ) has unique FP for ALL B≥2 algebraically | A8 authorship acknowledgment |
| 2 | Derive κ_c(d,B) in closed form from N_τ | A8 co-authorship |
| 3 | Prove iota_3 universality: |T(Ω_{b,3})|=b for all b≥2 | A8 acknowledgment |
| 4 | Explain b=−12,d=5 collapse mechanism | A8 supplementary authorship |
| 5 | Lean proof of AQ-THM-001 (|Image|=54) | A8 formal methods section |

---

*AQARION · Louisville Node #1 · github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-*
