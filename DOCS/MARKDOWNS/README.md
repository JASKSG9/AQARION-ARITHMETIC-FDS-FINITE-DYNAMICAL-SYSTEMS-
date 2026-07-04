url=https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/blob/main/README.md
# 🧮 AQARION — Arithmetic & Finite Dynamical Systems

[![AQARION](https://img.shields.io/badge/AQARION-v38%20Hardening-blueviolet)](https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-)
[![Status](https://img.shields.io/badge/status-submission--ready-success)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![Lean](https://img.shields.io/badge/Lean-4-blue)]()
[![Reproducible](https://img.shields.io/badge/reproducibility-make%20verify-orange)]()

A formal, reproducible framework for certifying exact observable quotients in finite deterministic dynamical systems via an operator obstruction test.

One line
---------
AQARION provides a computable, basis‑independent certificate that decides whether a user‑specified observable (partition) induces an exact quotient dynamics.

Essence (core operator)
------------------------
The descent obstruction measures failure of observable closure:
\[
D_\Pi \;=\; (I - P_\Pi)\, K^T\, P_\Pi
\]
- \(K^T\): Koopman pullback (action \(f \mapsto f\circ T\))
- \(P_\Pi\): orthogonal projection onto partition‑constant observables
- \(D_\Pi=0 \iff K^T(V_\Pi)\subseteq V_\Pi\) (observable subspace invariant)

Why this matters
----------------
- Separates exact descent (invariance) from the stronger commutator condition \(C_\Pi=[P_\Pi,K^T]\).
- Explains the "Commutator Fallacy": many exact descents do not require \(C_\Pi=0\).
- Provides machine‑checkable certificates (symbolic + hashed computational artifacts) for research reproducibility and publication.

Key claims & evidence
---------------------
- T1 (Invariant Subspace): \(D_\Pi=0 \iff K^T(V_\Pi)\subseteq V_\Pi\) — Proven (Lean + symbolic).
- T2 (Quotient Certification): Under observable separation assumptions, \(D_\Pi=0 \Rightarrow\) quotient exists — Conditional/verified.
- T3 (Reduction Hierarchy): \(C_\Pi=0 \Rightarrow D_\Pi=0\) — Proven.
- Exhaustive census (n ≤ 5): 166,484 configurations — exactly 3/16 binary profiles realized; evidence: deterministic, hashed artifacts.
- Kaprekar benchmark (54/55 states): characteristic polynomial, Jordan decomposition, nilpotent index 6 — SymPy audit + verification suite.

Repository at a glance
----------------------
```
AQARION/
├── core/               # Lean 4 formalization & core definitions
├── scripts/            # generation, verification, export utilities
├── verification/       # verification suite & reproducibility helpers
├── output/             # hashed artifacts (finite_census.json, transient_block.json, ...)
├── DOCS/               # detailed documentation & claims registries
├── Makefile            # one-command reproducibility: `make verify`
├── README.md
└── LICENSE
```

How it fits together (runtime shape)
-----------------------------------
- User supplies (X, T, Π) where Π is a partition / observable.
- scripts/generate_* constructs transition tables and Koopman matrices.
- verification/* runs symbolic audits (SymPy), numerical checks (NumPy/SciPy), and produces machine‑readable certificates (SHA-256).
- core/ (Lean) encodes definitions and formal proofs; generated Lean constants embed computational artifacts for mechanized verification.

Quick start — run the verification pipeline
-------------------------------------------
Requirements
- Python 3.10+, pip, git
- Recommended: use the provided Docker image (see docker/)

Minimal local run
```bash
git clone https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-.git
cd AQARION
pip install -r requirements.txt          # or: pip install -e .[dev]
make clean verify
```

What `make verify` does (high level)
- regenerate artifacts (scripts/generate_census.py, derive_transient_block.py)
- compile / run Lean proofs (lake build / lake file)
- run symbolic audits (verify_operator.py)
- generate figures and proof provenance
- compute and compare SHA‑256 artifact hashes
Expected final output:
```
Definitions: PASS
Theorems: PASS (Lean)
Experiments: PASS
Artifacts: PASS (hash verified)
Claim Audit: PASS
ALL VERIFICATIONS PASSED
```

CI & reproducibility
--------------------
- .github/workflows/verify.yml runs `make verify` on each push.
- All computational artifacts are stored in output/ and validated against artifacts_schema.json.
- Each artifact file includes a frozen SHA‑256 hash and a provenance entry in claim_provenance.yaml.

Developer & contributor workflow
-------------------------------
1. Fork & branch: use descriptive branch names, e.g., `feat/lean-census` or `ci/docker-repro`.
2. Run locally: `make verify` (or run subset scripts).
3. Open PR with:
   - CI green
   - Added/updated tests (verification/ tests)
   - Claim provenance updated (DOCS/MARKDOWNS/CLAIMs-REGISTRY.md)
4. Tag releases with the master artifact hash in SOURCE_OF_TRUTH.md.

Recommended contribution targets (high leverage)
------------------------------------------------
- (Formalize) Complete remaining Lean `sorry` placeholders in core/ to mechanize T1–T3 and the census.
- (Repro) Harden Docker + CI to guarantee identical artifacts between local and CI runs.
- (Bridge) Add scripts to auto‑generate Lean constants from output/*.json so proofs can import verified computational artifacts.

Visual dependency flow
----------------------
```mermaid
flowchart TD
  Input[(X, T, Π)]
  Gen[generate_* scripts]
  Koop[Koopman Matrix K^T]
  Project[Projection P_Π]
  Obstruction[D_Π = (I-P) K^T P]
  Audit[verify_operator.py (SymPy + numeric)]
  Lean[core/ (Lean 4) formalization]
  Artifacts[output/ (json, yaml, hashes)]
  CI[.github/workflows/verify.yml]

  Input --> Gen --> Koop
  Koop --> Project --> Obstruction
  Obstruction --> Audit --> Artifacts
  Artifacts --> Lean
  Lean --> CI --> Artifacts
```

Data & artifacts (important files)
----------------------------------
- output/finite_census.json — exhaustive truth table (n ≤ 5; deterministic)
- output/transient_block.json — Kaprekar transient block + nilpotent index
- output/claim_provenance.yaml — claim ↔ evidence mapping (V4)
- core/*.lean — formal definitions, statements, and partial proofs
- scripts/generate_census.py, derive_transient_block.py — reproduction code

Example: minimal Commutator Fallacy witness
-------------------------------------------
System:
```
X = {0,1}, T(0)=0, T(1)=0, Π = {{0,1}}
```
Result:
- \(D_\Pi = 0\) (exact descent)
- \(C_\Pi \ne 0\) (commutator nonzero)
This small witness is encoded in the counterexamples.json and the census artifacts.

Evidence & verification policy
------------------------------
- Every public claim is labeled with an evidence type: [P] proof, [CV] computational verification, [P+CV] both.
- No computation is presented as a proof alone — symbolic proofs and mechanized checks are preferred for central theorems.
- All artifacts are hashed and tracked; scripts verify hashes and abort on mismatch.

Roadmap (next high‑impact milestones)
------------------------------------
1. Mechanize census in Lean: convert finite_census.json → Lean definitions → complete mechanized proof of T5 (n ≤ 5).
2. OP0: symbolic derivation of affine branches for Kaprekar gap space.
3. Publish Paper I: attach certificate.json + claim provenance; submit to arXiv.

Contact & community
-------------------
- Issues: use the repository Issues (label: verification, formalization, or OP0 contribution).
- Contribution guide: see CONTRIBUTING.md and .github/ISSUE_TEMPLATE/op0_contribution.md
- Maintainer: AQARION Research Node (#10878) — open PRs for review.

Citation
--------
If you use AQARION in research, cite:
```bibtex
@misc{aqarion2026,
  title={AQARION: Behavioral Quotient Certification via Operator Obstruction},
  author={AQARION Team},
  year={2026},
  archivePrefix={arXiv},
  primaryClass={math.DS}
}
```

License
-------
MIT (code). Documentation CC‑BY‑4.0 unless otherwise specified.

---

Status: research‑grade • reproducible • claim‑traceable
```
