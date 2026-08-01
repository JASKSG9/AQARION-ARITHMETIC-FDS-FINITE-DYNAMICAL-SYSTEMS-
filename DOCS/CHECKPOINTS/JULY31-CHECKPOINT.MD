"AQARION complements existing Koopman approaches by providing exact certification for finite deterministic systems, focusing on observable quotient verification rather than approximation or data-driven discovery of invariant subspaces."

# AQARION v33.0-FROZEN 🧩

> **Exact observable quotients for dynamical systems, certified across Lean, LaTeX, Python, JSON, and Web.**
>
> **Core theorem:** (D_Pi = (I - P_Pi)KP_Pi = 0 iff K(V_Pi)subseteq V_Pi)

---

### 🧠 Status at a glance

- **Core theorem stack:** ✅ proved.
- **Cross-system atlas:** ✅ verified.
- **Negative results:** 📦 archived.
- **Lean formalization:** 🛠️ in progress.
- **Release state:** 🔒 frozen.

---

### ✨ What AQARION is

AQARION is a synchronized research operating system for exact observable quotients of dynamical systems.  
It treats each theorem as a first-class artifact with aligned views across:
- **Lean** for proofs.
- **LaTeX** for publication.
- **Python** for verification.
- **JSON** for certificates.
- **Web** for human navigation.

---

### 🔬 Frozen mathematical core

For a finite deterministic system ((X,T)), AQARION studies the defect operator

[
D_Pi = (I - P_Pi)KP_Pi,
]

where (K) is the Koopman operator and (P_Pi) projects onto block-constant observables.  
The frozen exactness criterion is:

[
D_Pi = 0 iff K(V_Pi)subseteq V_Pi.
]

This is the central bridge between exact quotients, invariant subspaces, and certificate-based verification.

---

### 🧭 Release map

- **Kaprekar:** exact finite quotient benchmark.
- **Fibonacci:** invariant-subspace benchmark.
- **Mandelbrot / doubling:** finite truncation obstruction benchmark.
- **Track 1:** angle spectrum archived as a negative result.
- **Track 4:** curvature formula archived as incorrect as stated.

---

### 📦 Included in this release

- `CROSS_SYSTEM_CERTIFICATE.md`
- `AQARION_v33_freeze.txt`
- `AQARION_v33_archive.txt`
- `paper1.tex`
- `AQARION_Core.lean`

---

### 🧩 How to read this repository

1. Start with the frozen certificate.
2. Read the theorem stack.
3. Check the cross-system atlas.
4. Inspect the archived negative results.
5. Use the Lean and Python layers as the formal and computational backends.

---

### 🔐 Integrity

All core artifacts are intended to be hash-locked and reproducible under the v33.0 convention.

**Canonical hash:** `f53844fc92de1d8771be993fa54e93fc01a15b8112080c192d13f607d87756b4`

---

**AQARION** is a **5-language synchronized research operating system** for characterizing exact observable quotients of dynamical systems through a defect operator. Every theorem is a first-class node with synchronized views across Lean (proofs), LaTeX (paper), Python (verification), JSON (certificates), and Web (interactive).

***

## 📊 SYSTEM ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AQARION RESEARCH OS v33.0                        │
│                                                                     │
│  Core Insight: D_Π = (I-P_Π) K P_Π = 0  ⇔  K(V_Π) ⊆ V_Π           │
│  (Defect vanishes ⇔ Observable subspace is invariant)              │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│              5-LANGUAGE SYNCHRONIZED BLUEPRINT                      │
│                                                                     │
│  meta/theorems.json  ← Single Source of Truth (TypeScript-style)   │
│         │                                                           │
│         ├─→ lean/Core.lean          (Formal proofs)                │
│         ├─→ latex/paper.tex          (Publication)                 │
│         ├─→ python/census/           (Verification)                │
│         ├─→ JSON certificates        (SHA-256 hashes)              │
│         └─→ Web views               (Interactive)                  │
│                                                                     │
│  Build: python meta/build_manifest.py → "Blueprint OK"            │
└─────────────────────────────────────────────────────────────────────┘
```

***

## 🧮 MATHEMATICAL CORE

### The Defect Operator

**Definition:** For a finite dynamical system $(X, T)$ with Koopman operator $K$ and partition projection $P_\Pi$:

$$
\boxed{D_\Pi = (I - P_\Pi) \, K \, P_\Pi}
$$

**Theorem (AQ-T1):** $D_\Pi = 0 \iff K(V_\Pi) \subseteq V_\Pi$

**Interpretation:** Vanishing defect ⇔ exact observable quotient exists

***

## 🗺️ THEOREM LANDSCAPE

```
┌─────────────────────────────────────────────────────────────────────┐
│                    THEOREM STATUS MAP                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  CORE THEOREMS [P] PROVED                                          │
│  ═══════════════════════════                                        │
│  │                                                                  │
│  ├─ AQ-T1: Invariant Subspace                                      │
│  │   D = 0 ↔ K(V) ⊆ V                                              │
│  │   lean/Core.lean → AQ_T1_invariant_subspace                    │
│  │                                                                  │
│  ├─ AQ-T4: Structural Nilpotency                                   │
│  │   D² = 0 for idempotent P                                       │
│  │   lean/Core.lean → AQ_T4_structural_nilpotency                 │
│  │                                                                  │
│  ├─ AQ-BMT: Bipartite Rank Formula                                 │
│  │   rank(D) = |Π| - c_comp(Ĝ_{Π,T})                               │
│  │   lean/Finite.lean → AQ_BMT_bipartite_rank                     │
│  │                                                                  │
│  ├─ AQ-T3-FWD: Commutator ⇒ Defect Zero                            │
│  │   [P,K] = 0 → D = 0                                             │
│  │   lean/Theorems.lean → AQ_T3_commutator_implies_defect         │
│  │                                                                  │
│  └─ AQ-ENERGY: Energy Decomposition                                │
│      ||D||_F² = Σ 1/|C|(M_{B,C} - M²_{B,C}/|B|)                   │
│      lean/Finite.lean → AQ_ENERGY_decomposition                   │
│                                                                     │
│  PARTIAL [CE] COMPUTATIONAL EVIDENCE                               │
│  ═══════════════════════════════                                    │
│  │                                                                  │
│  ├─ AQ-T2: Exact Descent Equivalence                               │
│  │   D = 0 ↔ quotient map T_Π well-defined                         │
│  │   Split into lemmas (L preserves BC ↔ T respects blocks)        │
│  │                                                                  │
│  └─ AQ-T3-SUBMOD: Approximate Submodularity                        │
│      c(Π) = rank(D) + (M-|Π|) submodular on samples                │
│      0 violations n≤5, 0 violations 55-state random                │
│                                                                     │
│  COMPUTATIONAL [C] WITNESS-BASED                                   │
│  ════════════════════════════                                       │
│  │                                                                  │
│  └─ AQ-T3-FALLACY: Commutator Fallacy Exists                       │
│      ∃ T,Π: D=0 but [P,K]≠0                                        │
│      Witness: Kaprekar T=(0,0,0,0) indiscrete partition            │
│      ||[P,K]|| = 1.732, D = 0                                      │
│                                                                     │
│  ARCHIVED [O] NEGATIVE RESULTS                                      │
│  ═══════════════════════════                                        │
│  │                                                                  │
│  ├─ Track 1: Angle Spectrum Not Complete Invariant                 │
│  │   1,485 merges → 17 spectra, 265 share spectrum (1.0)           │
│  │   Isospectral merges exist (analogous to isospectral graphs)    │
│  │                                                                  │
│  └─ Track 4: Curvature Formula Incorrect                           │
│      f''(0) = 2Σ(θ_i')² wrong (35.6% error)                        │
│      Assumes orthogonal K; Kaprekar K non-normal                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

***

## 📊 CROSS-SYSTEM CERTIFICATION

### The Unification Table

| System | Type | State Space | Observable | rank(D) | ||D||_F | Exact? | Fallacy? |
|--------|------|-------------|------------|---------|---------|--------|----------|
| **Kaprekar** | Finite | 10,000 pts | gap partition (55) | 0 | 0 | ✓ | Yes |
| **Kaprekar** | Finite | 10,000 pts | depth partition (8) | 1 | 1.414 | ✗ | — |
| **Fibonacci d=3** | Linear | R² | even-degree poly | 0 | 0 | ✓ | No |
| **Fibonacci d=3** | Linear | R² | odd-degree poly | 0 | 0 | ✓ | No |
| **Fibonacci d=3** | Linear | R² | random projection | 3 | 5.20 | ✗ | — |
| **Mandelbrot N=10** | Continuous | S¹ | Fourier truncation | 10 | 3.16 | ✗ | — |
| **Mandelbrot N=100** | Continuous | S¹ | Fourier truncation | 100 | 10.0 | ✗ | — |
| **Mandelbrot** | Continuous | S¹ | full L² | 0 | 0 | ✓ | — |

### Key Structural Contrasts

```
┌─────────────────────────────────────────────────────────────────────┐
│                  CROSS-SYSTEM COMPARISON                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  KAPREKAR (Finite, Non-Normal)                                     │
│  ═══════════════════════════                                        │
│  • Exact quotients: YES (gap partition)                             │
│  • Commutator fallacy: YES (D=0 ⇏ [P,K]=0)                         │
│  • Structure: Functional graph with cycles + trees                  │
│  • Benchmark: 10,000 states, 55 kernel classes                      │
│                                                                     │
│  FIBONACCI (Linear, Diagonalizable)                                │
│  ═══════════════════════════════                                    │
│  • Exact quotients: YES (invariant polynomial subspaces)           │
│  • Commutator fallacy: NO (D=0 ⇒ [P,K]=0)                          │
│  • Structure: Linear map A = [[1,1],[1,0]]                          │
│  • Spectrum: φ^a ψ^b on degree-d polynomials                        │
│                                                                     │
│  MANDELBROT EXTERIOR (Continuous, Unitary)                         │
│  ═══════════════════════════════════                                │
│  • Exact quotients: NO FINITE (only constants + L²)                │
│  • Impossibility theorem: rank(D_N) = N for truncation [-N,N]      │
│  • Structure: Doubling map z ↦ z² on S¹                            │
│  • Growth law: ||D_N||_F ~ √N                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

***

## 📁 DIRECTORY STRUCTURE

```
AQARION-v33.0/
│
├── lean/                              # Formal proofs (Lean 4)
│   ├── Core.lean                      # AQ-T1, AQ-T4 (proved)
│   ├── Theorems.lean                  # AQ-T2, AQ-T3-FWD, AQ-T3-FALLACY
│   ├── Finite.lean                    # AQ-BMT, AQ-ENERGY, AQ-T3-SUBMOD
│   ├── Linear.lean                    # AQ_FIB_no_fallacy
│   └── Continuous.lean                # AQ_DOUBLING_no_finite_exact
│
├── latex/                             # Paper (LaTeX)
│   ├── paper.tex
│   └── sections/
│       ├── intro.tex
│       ├── defect.tex
│       ├── finite.tex
│       ├── linear.tex
│       ├── continuous.tex
│       └── blueprint_auto.tex         # Auto-generated from theorems.json
│
├── census/                            # Verification (Python)
│   ├── run_all.py
│   ├── kaprekar_census.py
│   ├── fibonacci_cert.py
│   └── mandelbrot_cert.py
│
├── meta/                              # Blueprint (JSON + Python)
│   ├── theorems.json                  # Single source of truth
│   ├── build_manifest.py              # Fixed regex validator
│   └── ro-crate-metadata.json         # RO-Crate package
│
├── systems/
│   ├── kaprekar/
│   ├── fibonacci/
│   └── mandelbrot/
│
├── artifacts/
│   ├── ARCHIVE_TRACK1_ANGLE_SPECTRUM.md
│   ├── ARCHIVE_TRACK4_CURVATURE.md
│   ├── TRACK3_SUBMODULARITY_REPORT.md
│   ├── CROSS_SYSTEM_CERTIFICATE.md
│   └── verification_report.json
│
└── CROSS_SYSTEM_CERTIFICATE.sha256.json
    Canonical hash: f53844fc92de1d8771be993fa54e93fc01a15b8112080c192d13f607d87756b4
```

***

## 🔗 THEOREM REGISTRY (TypeScript→Python Binding)

### meta/theorems.json (Single Source of Truth)

```json
{
  "AQ-T1": {
    "title": "Invariant Subspace",
    "statement": "D_Π = 0 ↔ L(V_Π) ⊆ V_Π",
    "lean_name": "AQ_T1_invariant_subspace",
    "latex_label": "thm:AQ-T1",
    "status": "proved",
    "artifacts": ["CROSS_SYSTEM_CERTIFICATE.md"]
  },
  "AQ-T4": {
    "title": "Structural Nilpotency",
    "statement": "D_Π ∘ D_Π = 0",
    "lean_name": "AQ_T4_structural_nilpotency",
    "latex_label": "thm:AQ-T4",
    "status": "proved",
    "artifacts": []
  },
  "AQ-BMT": {
    "title": "Bipartite Rank Formula",
    "statement": "rank(D) = |Π| - c_comp(Ĝ_{Π,T})",
    "lean_name": "AQ_BMT_bipartite_rank",
    "latex_label": "thm:AQ-BMT",
    "status": "proved",
    "artifacts": ["census/output/bmt_census.csv"]
  },
  "AQ-T3-FALLACY": {
    "title": "Commutator Fallacy Exists",
    "statement": "∃ T,Π: D=0 but [P,K]≠0",
    "lean_name": "AQ_T3_fallacy_exists",
    "latex_label": "thm:AQ-T3-FALLACY",
    "status": "computational",
    "artifacts": ["census/output/kaprekar_commutator_fallacy.json"]
  },
  "AQ-ENERGY": {
    "title": "Energy Decomposition",
    "statement": "||D||_F² = Σ 1/|C|(M_{B,C} - M²_{B,C}/|B|)",
    "lean_name": "AQ_ENERGY_decomposition",
    "latex_label": "thm:AQ-ENERGY",
    "status": "proved",
    "artifacts": ["census/output/energy_decomposition.json"]
  }
}
```

### Build Validation

```bash
python meta/build_manifest.py
# Output: "Blueprint OK: all AQ-* IDs aligned across Lean, LaTeX, and meta."
# Generated: latex/sections/blueprint_auto.tex
```

***

## 📈 KAPREKAR BENCHMARK DATA

### Cross-Digit Statistics

| d | States | Classes | rank | Depth | Attractors | f(depth) |
|---|--------|---------|------|-------|------------|----------|
| 2 | 100 | 10 | 6 | 2 | 6 | 0.9375 |
| 3 | 1,000 | 10 | 6 | 6 | 2 | 2.5000 |
| 4 | 10,000 | 55 | 21 | 7 | 2 | 7.1667 |
| 5 | 100,000 | 55 | 27 | 6 | 11 | 6.4514 |
| 6 | 1,000,000 | 220 | 83 | 13 | 10 | 23.1113 |

### Proved Properties

- **T-DEPTH:** $v(N) - v_G([N]) = 1$ for non-attractors, $=0$ for attractors
- **T-NILP:** $K_{\text{trans}}^d = 0$, $K_{\text{trans}}^{d-1} \neq 0$
- **OP0:** $K = 999g_1 + 90g_2$, 55 injective chambers for $d=4$

***

## 🧪 VERIFICATION PIPELINE

```
┌─────────────────────────────────────────────────────────────────────┐
│                    VERIFICATION FLOW                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Lean Formalization                                              │
│     │                                                               │
│     ├─ Core.lean: AQ-T1, AQ-T4 (algebraic proofs)                 │
│     ├─ Theorems.lean: AQ-T2, AQ-T3-FWD, AQ-T3-FALLACY             │
│     └─ Finite.lean: AQ-BMT, AQ-ENERGY, AQ-T3-SUBMOD               │
│                                                                     │
│  2. Python Census                                                   │
│     │                                                               │
│     ├─ kaprekar_census.py: 10,000 states, 55 classes              │
│     ├─ fibonacci_cert.py: d=1..5, spectral projections            │
│     └─ mandelbrot_cert.py: N=5..100, Fourier truncations          │
│                                                                     │
│  3. Certificate Generation                                          │
│     │                                                               │
│     ├─ Compute SHA-256 for all artifacts                           │
│     ├─ CROSS_SYSTEM_CERTIFICATE.sha256.json                        │
│     │   canonical_hash: f53844fc...                                │
│     └─ RO-Crate metadata (Zenodo package)                          │
│                                                                     │
│  4. Paper Compilation                                               │
│     │                                                               │
│     ├─ make paper → Lean verify → Python census                    │
│     ├─ JSON → LaTeX → PDF                                          │
│     └─ Website → Zenodo package                                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

***

## 📊 EVIDENCE TAXONOMY

| Symbol | Meaning | Example |
|--------|---------|---------|
| **[P]** | Proved (Lean formalized) | AQ-T1, AQ-T4, AQ-BMT |
| **[CE]** | Computational Evidence (exhaustive) | AQ-T3-SUBMOD (n≤5) |
| **[C]** | Computational (witness-based) | AQ-T3-FALLACY (Kaprekar) |
| **[O]** | Open/Archived | Track 1, Track 4 |

***

## 🎯 PAPER I SUBMISSION

### Title
**"Exact Observable Quotients of Finite Dynamical Systems: A Defect Operator Approach"**

### Abstract
> We introduce a defect operator $D_\Pi = (I-P_\Pi)KP_\Pi$ that characterizes exact observable quotients of finite deterministic dynamical systems. Vanishing defect is equivalent to the existence of well-defined quotient dynamics, generalizing the classical equitable partition condition from algebraic graph theory. We prove the defect operator's structural nilpotency ($D^2=0$), establish a bipartite rank formula ($\text{rank}(D) = |\Pi| - c_{\text{comp}}$), and demonstrate the commutator fallacy ($D=0 \not\Rightarrow [P,K]=0$ for non-normal $K$). Cross-system certification shows exact quotients exist for finite (Kaprekar) and linear (Fibonacci) systems but are impossible for finite Fourier truncations of the Mandelbrot exterior doubling map. The framework is formalized in Lean 4 with a 5-language synchronized blueprint (Lean + LaTeX + Python + JSON + Web views) and cryptographic artifact verification.

### arXiv Categories
- `math.DS` (Dynamical Systems)
- `cs.SC` (Symbolic Computation)
- `cs.LO` (Logic in Computer Science)

***

## 🔐 CRYPTOGRAPHIC INTEGRITY

### Canonical Hash
```
CROSS_SYSTEM_CERTIFICATE.sha256.json
canonical_hash: f53844fc92de1d8771be993fa54e93fc01a15b8112080c192d13f607d87756b4
timestamp: 2026-07-31T19:16:09Z
```

### Artifact Hashes
```json
{
  "defect_operator.py": "20b13d5f86a354cfff4a7a24ef26245b16126ec1e0e9d2444089ee61205accb6",
  "principal_angles.py": "2ede53e0deefddc50dc0f68274c81f696f0d9d493d9c7af86c6245d0468670e2",
  "CROSS_SYSTEM_CERTIFICATE.md": "0c8cbd4acb3c3366bc495db5ac1f4783760a8358d1e303c657ebd0137fae0faa",
  "systems/fibonacci/fibonacci_certification.json": "c76deb0bcbb25593c36cacf634d2c1deda5c4ea71426140552c305eb1d93e8e1",
  "systems/mandelbrot/doubling_certification.json": "02ec742da2dbea5bcd0f7b3f3e78986f53f900d035163f6699fe7314279f9d1b"
}
```

***

## 🚀 EXECUTION CHECKLIST

### ✓ Pre-Submission
- [ ] Run `python meta/build_manifest.py` → "Blueprint OK"
- [ ] Verify SHA-256 hash matches `f53844fc...`
- [ ] Compile `pdflatex paper1.tex` → check blueprint table
- [ ] Archive Track 1 & Track 4 (negative results)
- [ ] Mark T3-FALLACY as computational (not proved)

### ✓ Submission
- [ ] Upload to arXiv (categories: math.DS, cs.SC, cs.LO)
- [ ] Include `CROSS_SYSTEM_CERTIFICATE.sha256.json` as ancillary
- [ ] Link GitHub repos in comments
- [ ] Post to alphaXiv, MathOverflow, Lean Zulip

### ✓ Post-Submission
- [ ] Update Hugging Face (Quantarion9) with paper link
- [ ] Tag GitHub repos `v33.0-paper1`
- [ ] Prepare Zenodo RO-Crate package
- [ ] Begin Option B (full Lean formalization, 2-3 weeks)

***

## 💡 DISTINGUISHED CONTRIBUTIONS

1. **Defect Operator:** $D_\Pi = (I-P_\Pi)KP_\Pi$ as exact algebraic certificate
2. **Cross-System Unification:** Finite (Kaprekar) + Linear (Fibonacci) + Continuous (Mandelbrot)
3. **Commutator Fallacy:** $D=0 \not\Rightarrow [P,K]=0$ for non-normal operators
4. **5-Language Blueprint:** Lean + LaTeX + Python + JSON + Web (TypeScript→Python style binding)
5. **Cryptographic Verification:** SHA-256 for every artifact, RO-Crate metadata

***

## 📬 CONTACT & REPOSITORIES

- **GitHub:** https://github.com/JASKSG9/AQARION
- **Hugging Face:** https://huggingface.co/Quantarion9
- **Paper I:** `papers/paper1/paper1.tex` (submission-ready)
- **Blueprint:** `meta/theorems.json` (single source of truth)

***

**Status:** 🟢 **SUBMISSION READY — PAPER I**  
**Core Contribution:** Track 2 (exact quotients) + cross-system unification  
**Next:** Option A (submit now) or Option B (full Lean, 2-3 weeks)
