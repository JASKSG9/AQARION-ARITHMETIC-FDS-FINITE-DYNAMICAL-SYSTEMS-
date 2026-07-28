import json, hashlib, datetime

# Load final registry
with open("/mnt/agents/output/AQARION_registry_v25_FINAL.json") as f:
    registry = json.load(f)

# PUBLICATION KERNEL — only entries marked for peer review
# Criteria: PROVED+VERIFIED status, Theorem/Corollary mathematical status, not refuted
kernel_entries = []
for entry in registry:
    if entry["status"].startswith("PROVED") and entry.get("mathematical_status") in ["Theorem", "Corollary"]:
        kernel_entries.append(entry)

# Add the closure operator theorem (newly proven)
for entry in registry:
    if entry["id"] == "AQ-THM-CLOSURE-OPERATOR":
        kernel_entries.append(entry)

# Sort by dependency order
kernel_ids = [e["id"] for e in kernel_entries]

# Build publication kernel object
pub_kernel = {
    "metadata": {
        "project": "AQARION",
        "version": "v1.0-PUBLICATION-KERNEL",
        "date_frozen": "2026-07-28",
        "description": "Defensible publication kernel: operator-theoretic framework for finite deterministic endofunctions. Core framework stabilized. Remaining symbolic proofs (submodularity formalization) are open work, not blocking.",
        "total_entries": len(kernel_entries),
        "registry_hash": "957b203023ee91c2",
        "assessment": "Core framework stabilized. Publication kernel frozen. Computational verification extensive (10M+ cases). Formalization in progress."
    },
    "central_theorem": {
        "id": "AQ-THM-BIPARTITE-MASTER",
        "statement": "rank(D_Pi) = m - c_comp for all T, all partitions",
        "evidence_summary": "Exhaustive n=2..6 all T (9.64M cases), Monte Carlo n=7 (1.5M samples), cyclic n=2..7 (7,419 cases). Zero violations.",
        "proof_path": "Classical incidence matrix rank = n - c, applied to bipartite G(Pi,T)",
        "lean_status": "PLANNED — Priority 1"
    },
    "kernel_entries": kernel_entries,
    "refuted_claims": [e for e in registry if e["status"] == "REFUTED" or "REFUTED" in e["status"]],
    "experimental_results": [e for e in registry if e.get("mathematical_status") == "Experimental result"],
    "open_work": [
        "Lean formalization of Bipartite Master (Priority 1)",
        "Submodularity formal proof (verified computationally, needs symbolic)",
        "Minimal implication basis for n >= 5",
        "Quantitative defect geometry bound theorem",
        "FOQDS optimality characterization"
    ],
    "what_not_to_claim": [
        "Mathematics is closed — false, Lean proofs pending",
        "Submodularity is formally proved — false, only computationally verified",
        "FOQDS is uniquely optimal — false, experimental evidence shows multiple valid paths",
        "Pushforward congruence fails — false, preimage-union definition is equivalent to pullback"
    ]
}

kernel_json = json.dumps(pub_kernel, sort_keys=True, indent=2)
kernel_hash = hashlib.sha256(kernel_json.encode()).hexdigest()[:16]

kernel_path = "/mnt/agents/output/AQARION_PUBLICATION_KERNEL_v1.json"
with open(kernel_path, "w") as f:
    f.write(kernel_json)

# Also create a minimal citation-ready summary
citation_summary = """AQARION: An Operator-Theoretic Framework for Finite Deterministic Endofunctions

AUTHORS: [Your name]
DATE: 2026-07-28
VERSION: v1.0-PUBLICATION-KERNEL

ABSTRACT:
We present AQARION, an operator-theoretic framework for finite deterministic 
endofunctions based on observable partitions, invariant subspaces, and a 
computable defect operator. The central result is the Bipartite Master Theorem:
for any map T:X->X and partition Pi, the rank of the defect operator D_Pi 
equals m - c_comp, where m = |Pi| and c_comp is the number of connected 
components of the bipartite incidence graph G(Pi,T). This subsumes and unifies 
multiple prior rank formulas, congruence criteria, and descent results. The 
framework is supported by extensive computational verification (10.6M+ cases 
zero violations), a transparent evidence taxonomy, and a developing Lean 
formalization effort.

CORE RESULTS (frozen for publication):
- Bipartite Master Theorem: rank(D) = m - c_comp
- Congruence criterion: D = 0 iff Pi is a congruence
- Closure operator: FOQDS exact refinement is extensive, monotone, idempotent
- Submodularity: c(Pi) = rank(D) + n - |Pi| is submodular on partition lattice
- Equal-blocks formula, [1,1,2] correction, uniform-binary, descent theory

COMPUTATIONAL VERIFICATION:
- Exhaustive: n=2..6 all T (9,637,651 cases)
- Monte Carlo: n=6 (500K), n=7 (1M) random samples
- Cyclic shifts: n=2..7 exhaustive (7,419 cases)
- Closure axioms: n=5 exhaustive (162,500 cases)
- Submodularity: n=2..4 exhaustive + n=5..7 random (515K+ pairs)
- All zero violations

WHAT IS NOT CLAIMED:
- Mathematics is not "closed"; Lean formalization is ongoing
- Submodularity is computationally verified, not yet formally proved
- FOQDS is not uniquely optimal among refinement strategies
- The framework does not claim novelty for classical linear algebra facts

STATUS: Core framework stabilized. Publication kernel frozen. 
Open work: Lean formalization, minimal basis n>=5, quantitative bounds.
"""

citation_path = "/mnt/agents/output/AQARION_CITATION_READY_v1.txt"
with open(citation_path, "w") as f:
    f.write(citation_summary)

print("=" * 70)
print("PUBLICATION KERNEL FROZEN")
print("=" * 70)
print(f"Kernel entries:      {len(kernel_entries)}")
print(f"Kernel hash:         {kernel_hash}")
print(f"Registry hash:       957b203023ee91c2")
print(f"\nFiles generated:")
print(f"  1. {kernel_path}")
print(f"  2. {citation_path}")
print(f"  3. {final_path}")
print(f"  4. {certs_path}")
print(f"  5. {summary_path}")

print(f"\nKernel entry IDs:")
for e in kernel_entries:
    print(f"    {e['id']}: {e['title'][:60]}...")======================================================================
PUBLICATION KERNEL FROZEN
======================================================================
Kernel entries:      17
Kernel hash:         f1d3d0f7fa4435d4
Registry hash:       957b203023ee91c2

Files generated:
  1. /mnt/agents/output/AQARION_PUBLICATION_KERNEL_v1.json
  2. /mnt/agents/output/AQARION_CITATION_READY_v1.txt
Error:
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[3], line 122
    120 print(f"  1. {kernel_path}")
    121 print(f"  2. {citation_path}")
--> 122 print(f"  3. {final_path}")
    123 print(f"  4. {certs_path}")
    124 print(f"  5. {summary_path}")

NameError: name 'final_path' is not defined
final_path = "/mnt/agents/output/AQARION_registry_v25_FINAL.json"
certs_path = "/mnt/agents/output/AQARION_certificates_experiments_3_7.json"
summary_path = "/mnt/agents/output/AQARION_FINAL_SUMMARY_v25.txt"

print("=" * 70)
print("PUBLICATION KERNEL FROZEN — ALL FILES")
print("=" * 70)
print(f"Kernel entries:      17")
print(f"Kernel hash:         f1d3d0f7fa4435d4")
print(f"Registry hash:       957b203023ee91c2")
print(f"\nFiles generated:")
print(f"  1. Publication Kernel JSON:  {kernel_path}")
print(f"  2. Citation-ready summary:   {citation_path}")
print(f"  3. Full registry (25 entries): {final_path}")
print(f"  4. Experiment certificates:    {certs_path}")
print(f"  5. Human summary:            {summary_path}")

print(f"\n{'='*70}")
print("DEFENSIBLE CLAIMS SUMMARY")
print(f"{'='*70}")
print("""
CAN CLAIM:
  - Bipartite Master Theorem verified to 10.6M+ cases, zero violations
  - Defect operator framework connects finite dynamics to partition lattice
  - Closure operator structure proven (extensive, monotone, idempotent)
  - Submodularity verified computationally to n=7
  - All special-case rank formulas are corollaries of one master theorem
  - Transparent evidence taxonomy with refuted claims preserved

CANNOT YET CLAIM:
  - "Mathematics is closed" — Lean proofs pending
  - "Submodularity is proved" — only computationally verified
  - "FOQDS is optimal" — experimental evidence shows non-uniqueness
  - Pushforward vs pullback confusion — clarified, both equivalent

PEER REVIEW STRENGTH:
  - Single master theorem subsumes all prior special cases
  - Extensive computational evidence (exhaustive to n=6, Monte Carlo to n=7)
  - Clear separation: proved / verified / refuted / open
  - Killed claims retained with provenance (intellectual honesty)
  - Lean formalization roadmap defined and prioritized
""")======================================================================
PUBLICATION KERNEL FROZEN — ALL FILES
======================================================================
Kernel entries:      17
Kernel hash:         f1d3d0f7fa4435d4
Registry hash:       957b203023ee91c2

Files generated:
  1. Publication Kernel JSON:  /mnt/agents/output/AQARION_PUBLICATION_KERNEL_v1.json
  2. Citation-ready summary:   /mnt/agents/output/AQARION_CITATION_READY_v1.txt
  3. Full registry (25 entries): /mnt/agents/output/AQARION_registry_v25_FINAL.json
  4. Experiment certificates:    /mnt/agents/output/AQARION_certificates_experiments_3_7.json
  5. Human summary:            /mnt/agents/output/AQARION_FINAL_SUMMARY_v25.txt

======================================================================
DEFENSIBLE CLAIMS SUMMARY
======================================================================

CAN CLAIM:
  - Bipartite Master Theorem verified to 10.6M+ cases, zero violations
  - Defect operator framework connects finite dynamics to partition lattice
  - Closure operator structure proven (extensive, monotone, idempotent)
  - Submodularity verified computationally to n=7
  - All special-case rank formulas are corollaries of one master theorem
  - Transparent evidence taxonomy with refuted claims preserved

CANNOT YET CLAIM:
  - "Mathematics is closed" — Lean proofs pending
  - "Submodularity is proved" — only computationally verified
  - "FOQDS is optimal" — experimental evidence shows non-uniqueness
  - Pushforward vs pullback confusion — clarified, both equivalent

PEER REVIEW STRENGTH:
  - Single master theorem subsumes all prior special cases
  - Extensive computational evidence (exhaustive to n=6, Monte Carlo to n=7)
  - Clear separation: proved / verified / refuted / open
  - Killed claims retained with provenance (intellectual honesty)
  - Lean formalization roadmap defined and prioritizedI agree with that assessment. Let me freeze the publication kernel and produce the final defensible artifact set.

Minor variable scope issue. Let me fix the print and confirm all files.

Done. The publication kernel is frozen.

---

Final Deliverables

File	Purpose	
[Publication Kernel v1 JSON](sandbox:///mnt/agents/output/AQARION_PUBLICATION_KERNEL_v1.json)	17 defensible entries for peer review	
[Citation-Ready Summary](sandbox:///mnt/agents/output/AQARION_CITATION_READY_v1.txt)	Abstract + status for submission	
[Full Registry v25](sandbox:///mnt/agents/output/AQARION_registry_v25_FINAL.json)	All 25 entries including refuted	
[Experiment Certificates](sandbox:///mnt/agents/output/AQARION_certificates_experiments_3_7.json)	Raw data from 5 experiments	
[Human Summary](sandbox:///mnt/agents/output/AQARION_FINAL_SUMMARY_v25.txt)	Complete narrative	

Kernel hash: `f1d3d0f7fa4435d4`

Registry hash: `957b203023ee91c2`

---

What the reviewer sees

> "AQARION presents an operator-theoretic framework for finite deterministic endofunctions. The central Bipartite Master Theorem (rank = m − c_comp) is verified exhaustively to n=6 (9.6M cases) and by Monte Carlo to n=7 (1.5M samples), with zero violations. The framework includes a closure operator structure, computationally-verified submodularity, and a transparent evidence taxonomy. Core results are stabilized; Lean formalization and minimal-basis characterization remain open work."

This is strong, defensible, and honest. The mathematics isn't closed — it's stabilized.
