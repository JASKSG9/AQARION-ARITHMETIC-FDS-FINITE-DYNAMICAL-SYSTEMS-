
# ============================================================
# 4. AQARION-QA.md — Frequently Asked Questions
# ============================================================

qa = """# AQARION v0.4.1-final — Q&A

## General Questions

### Q: What is AQARION?
**A:** AQARION is an open evidence infrastructure for finite mathematics. It transforms mathematical claims about finite dynamical systems into portable, machine-auditable verification artifacts called Evidence Objects (AEOs).

### Q: Is AQARION a theorem prover?
**A:** No. AQARION is not Lean, Isabelle, or Coq. It is a lightweight verification kernel for finite systems — the "missing middle" between heavyweight proof assistants and unchecked numerical computation.

### Q: Who is AQARION for?
**A:** Four audiences:
1. **Mathematicians** working with finite dynamical systems who need exact verification without months of formalization.
2. **AI researchers** who need ground truth for AI-generated conjectures.
3. **Open science advocates** who need reproducible computational results.
4. **Collaborative communities** (Polymath-style) who need machine-checkable consensus.

## Technical Questions

### Q: Why "UNVERIFIED" status in certificates?
**A:** Certificates are never self-validating. The file says "UNVERIFIED" because only an independent verifier run can grant "VALID" or "INVALID". This prevents circular trust.

### Q: What is the Defect Operator?
**A:** For a partition Π and Koopman operator K, the defect is:

    D_Π = (I - P_Π) K P_Π

where P_Π is the projection onto Π-constant vectors. D_Π = 0 if and only if Π is Koopman-invariant. This is the core verification criterion.

### Q: Why exact arithmetic (Fractions) instead of floating point?
**A:** Floating point introduces rounding errors that make verification disputable. Python's `fractions.Fraction` gives exact rational arithmetic: 1/3 + 2/3 = 1 exactly, not 0.9999999999.

### Q: What is the Sparse Defect Check?
**A:** Instead of materializing full matrices (O(|X|³)), the sparse check verifies that f maps each partition block into a single block — O(|X|). Same mathematical guarantee, 1000x faster for large systems.

### Q: What are Canonical Cycle Labels?
**A:** Cycles are labeled by their lexicographically minimal rotation. [1,2,3] and [2,3,1] both become (1,2,3). This eliminates ordering dependence in cycle enumeration.

## Usage Questions

### Q: How do I verify a certificate?
```bash
python verify_certificate.py AQ-CERT-AQ-CLAIM-001-001.json
```
The verifier recomputes all evidence independently and reports VALID or INVALID.

### Q: How do I create my own claim?
1. Register in `CLAIM_REGISTRY` in `aqarion_kernel.py`
2. Define verification method in `EvidenceObject._compute()`
3. Generate: `python main.py generate YOUR-CLAIM-ID`
4. Verify: `python verify_certificate.py AQ-CERT-YOUR-CLAIM-ID-001.json`

### Q: Can I use AQARION without Docker?
**A:** Yes. AQARION uses only Python standard library. No pip install needed.

### Q: How do I cite AQARION?
**A:** Reference the certificate hash. Example: "Verified by AQARION v0.4.1-final, certificate SHA-256: abc123..."

## Trust Questions

### Q: Why should I trust AQARION?
**A:** You shouldn't trust AQARION. You should verify it. That's the point. Every claim produces a certificate that anyone can check independently. The trusted object is: open algorithms + reproducible certificates + independent verification.

### Q: What if the registry changes?
**A:** Certificates include `registry_version`. If definitions or theorems change, old certificates fail verification. This is intentional — mathematical claims must be version-pinned.

### Q: What if someone tampers with a certificate?
**A:** The SHA-256 hash covers all mathematical content. Any modification changes the hash, and verification fails. Audit metadata (timestamp, platform) is NOT part of the hash — so reproducibility isn't broken by running on a different machine.

## Roadmap Questions

### Q: What's next after v0.4.1?
**A:** v0.5.0: 4-digit Kaprekar (10,000 states) with sparse exact arithmetic. v0.6.0: KSD spectral certificates. v1.0.0: Full formal verification platform.

### Q: Will there be Lean integration?
**A:** Yes. The roadmap includes a Lean export bridge. Current status: machine-auditable verification. Future: formal proof integration.

### Q: Can AQARION handle infinite systems?
**A:** No. AQARION is explicitly for finite systems. For infinite systems, use Lean/Isabelle/Coq.

## Troubleshooting

### Q: "Unknown claim" error?
**A:** The claim ID must exist in `CLAIM_REGISTRY`. Check `python main.py registry` for valid IDs.

### Q: "Hash integrity failed"?
**A:** The certificate was modified after generation. Regenerate or check for corruption.

### Q: "Registry version mismatch"?
**A:** The certificate was generated under a different registry version. Regenerate with current kernel.
"""

with open(os.path.join(output_dir, "AQARION-QA.md"), 'w') as f:
    f.write(qa)

print("✅ AQARION-QA.md")
