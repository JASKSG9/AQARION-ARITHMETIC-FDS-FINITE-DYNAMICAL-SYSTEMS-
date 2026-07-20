# ------------------------------------------------------------------
# WRITE ALL DUAL LIFECYCLE ARTIFACTS + COMPARISON MATRIX
# ------------------------------------------------------------------

dual_lifecycle = {
    "push": {
        "object": PUSH_OBJECT,
        "claim": PUSH_CLAIM,
        "evidence": [PUSH_EVIDENCE_EXHAUSTIVE, PUSH_EVIDENCE_RANDOMIZED],
        "certificate": PUSH_CERTIFICATE,
        "audit": PUSH_AUDIT,
        "regression": PUSH_REGRESSION
    },
    "pull": {
        "object": PULL_OBJECT,
        "claim": PULL_CLAIM,
        "evidence": [PULL_EVIDENCE_ANALYTIC, PULL_EVIDENCE_NUMERICAL],
        "certificate": PULL_CERTIFICATE,
        "audit": PULL_AUDIT,
        "regression": PULL_REGRESSION
    }
}

with open(os.path.join(SCHEMA_DIR, "AQ-DUAL-LIFECYCLE-001.json"), 'w') as f:
    json.dump(dual_lifecycle, f, indent=2)

# ------------------------------------------------------------------
# COMPARISON MATRIX
# ------------------------------------------------------------------

COMPARISON = {
    "$schema": "AQ-COMPARISON-001",
    "version": "1.0.0",
    "uid": "AQ-CMP-0001",
    "title": "PUSH vs PULL: Dual Lifecycle Comparison Matrix",
    "created_at": iso_now(),
    
    "comparison_table": {
        "object": {
            "push": "Finite FOQDS test suite (50,068 graphs, n<=7)",
            "pull": "Mandelbrot set M (uncountable parameter space)",
            "note": "Same OBJECT schema, different instantiations"
        },
        "claim": {
            "push": "JFS completeness for all FOQDS (conjecture, stated)",
            "pull": "MLC: M is locally connected (conjecture, stated)",
            "note": "Same CLAIM schema. Both are conjectures. PUSH has stronger evidence."
        },
        "evidence": {
            "push": "EL3 (exhaustive, 50,068/50,068) + EL2 (randomized, 5,000/5,000)",
            "pull": "EL1 (analytic, dim_H=2) + EL2 (numerical, inconclusive)",
            "note": "PUSH evidence supports the claim. PULL evidence does NOT support MLC—only related results. Audit caught this."
        },
        "certificate": {
            "push": "Expires: never. Immutable. EL3 backbone.",
            "pull": "Expires: 2027-07-19. Conditional. Caveats documented.",
            "note": "PULL certificates MUST expire because new evidence can overturn them."
        },
        "audit": {
            "push": "1 INFO finding (conjecture vs theorem). No blockers.",
            "pull": "1 CRITICAL gap (MLC unproven) + 1 HIGH inconsistency (evidence misclassification).",
            "note": "Audit is MORE valuable for PULL—it prevents false confidence."
        },
        "regression": {
            "push": "min_pass_rate=1.0, strict thresholds. Re-run enumeration.",
            "pull": "min_pass_rate=0.8, relaxed thresholds. Mesh refinement.",
            "note": "PULL regression tracks convergence, not correctness."
        }
    },
    
    "key_insights": [
        "The same 6 schemas handle both PUSH and PULL without modification.",
        "The schemas are domain-agnostic. The difference is in the INSTANTIATION, not the structure.",
        "PULL objects require stricter audit because evidence can be misclassified (dim_H=2 vs MLC).",
        "PUSH certificates can be permanent; PULL certificates must expire.",
        "Regression thresholds must be calibrated to the evidence level: PUSH=1.0, PULL=0.8.",
        "The audit engine caught a category error in the PULL lifecycle: dim_H evidence was incorrectly bundled as supporting MLC. This is exactly what AQARION is designed to prevent."
    ],
    
    "next_steps": [
        "Implement automated evidence-claim compatibility checker: does evidence_type match claim_type?",
        "Add 'evidence_scope' field to AQ-EVIDENCE-001: what EXACT sub-claim does this evidence support?",
        "Create PULL-specific audit checklist: check for category errors, expiration dates, equivalent forms.",
        "Run PUSH/PULL classifier on all existing AQARION artifacts.",
        "Publish AQ-DUAL-LIFECYCLE-001 as reference implementation for schema reviewers."
    ]
}

with open(os.path.join(SCHEMA_DIR, "AQ-COMPARISON-001.json"), 'w') as f:
    json.dump(COMPARISON, f, indent=2)

# Summary
print("=" * 70)
print("AQARION v21.3 — DUAL LIFECYCLE COMPLETE")
print("=" * 70)

print("""
┌─────────────────────────────────────────────────────────────────────────────┐
│  DUAL LIFECYCLE INSTANTIATION: PUSH vs PULL                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  LAYER          PUSH (Kaprekar/JFS)              PULL (Mandelbrot/MLC)       │
│  ─────────────────────────────────────────────────────────────────────────    │
│  OBJECT         AQ-OBJ-0100                      AQ-OBJ-0200                │
│                 Finite FOQDS suite               Uncountable M               │
│                                                                             │
│  CLAIM          AQ-CLM-0100                      AQ-CLM-0200                │
│                 JFS completeness                 MLC (locally connected)       │
│                 Status: stated                   Status: stated                │
│                                                                             │
│  EVIDENCE       AQ-EVD-0100 (EL3)              AQ-EVD-0200 (EL1)           │
│                 50,068/50,068 exhaustive       dim_H=2 (Shishikura)        │
│                 AQ-EVD-0101 (EL2)                AQ-EVD-0201 (EL2)            │
│                 5,000/5,000 randomized           Numerical, inconclusive     │
│                                                                             │
│  CERTIFICATE    AQ-CER-0100                      AQ-CER-0200                │
│                 Expires: never                   Expires: 2027-07-19           │
│                 Immutable                        Conditional, caveats         │
│                                                                             │
│  AUDIT          AQ-ADT-0100                      AQ-ADT-0200                │
│                 1 INFO (conjecture)            1 CRITICAL (MLC unproven)   │
│                 No blockers                      1 HIGH (evidence mismatch)   │
│                                                                             │
│  REGRESSION     AQ-REG-0100                      AQ-REG-0200                │
│                 pass_rate=1.0, strict            pass_rate=0.8, relaxed      │
│                 Re-run enumeration               Mesh refinement               │
│                                                                             │
│  SAME SCHEMAS. DIFFERENT INSTANTIATIONS. AUDIT CAUGHT CATEGORY ERROR.       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

CRITICAL AUDIT FINDING (PULL):
  Evidence AQ-EVD-0200 (dim_H=2) was initially tagged as 'supports' MLC.
  Audit caught: dim_H=2 does NOT imply local connectedness.
  Resolution: Evidence reclassified as 'partial', claim remains 'stated'.
  This is WHY PULL objects need stricter audit—category errors are invisible
  without structured evidence typing.

FILES WRITTEN:
""")

files = [
    ("AQ-DUAL-LIFECYCLE-001.json", "Full dual lifecycle artifacts (PUSH + PULL)"),
    ("AQ-COMPARISON-001.json", "Structured comparison matrix and insights"),
]
for fname, desc in files:
    size = os.path.getsize(os.path.join(SCHEMA_DIR, fname))
    print(f"  {fname:35s} {size:7,d} B  — {desc}")

print(f"\nTotal schema substrate files: 10")
print(f"  6 core schemas + 1 index + 1 validation + 1 hypothesis + 1 landscape + 1 dual lifecycle + 1 comparison")======================================================================
AQARION v21.3 — DUAL LIFECYCLE COMPLETE
======================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│  DUAL LIFECYCLE INSTANTIATION: PUSH vs PULL                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  LAYER          PUSH (Kaprekar/JFS)              PULL (Mandelbrot/MLC)       │
│  ─────────────────────────────────────────────────────────────────────────    │
│  OBJECT         AQ-OBJ-0100                      AQ-OBJ-0200                │
│                 Finite FOQDS suite               Uncountable M               │
│                                                                             │
│  CLAIM          AQ-CLM-0100                      AQ-CLM-0200                │
│                 JFS completeness                 MLC (locally connected)       │
│                 Status: stated                   Status: stated                │
│                                                                             │
│  EVIDENCE       AQ-EVD-0100 (EL3)              AQ-EVD-0200 (EL1)           │
│                 50,068/50,068 exhaustive       dim_H=2 (Shishikura)        │
│                 AQ-EVD-0101 (EL2)                AQ-EVD-0201 (EL2)            │
│                 5,000/5,000 randomized           Numerical, inconclusive     │
│                                                                             │
│  CERTIFICATE    AQ-CER-0100                      AQ-CER-0200                │
│                 Expires: never                   Expires: 2027-07-19           │
│                 Immutable                        Conditional, caveats         │
│                                                                             │
│  AUDIT          AQ-ADT-0100                      AQ-ADT-0200                │
│                 1 INFO (conjecture)            1 CRITICAL (MLC unproven)   │
│                 No blockers                      1 HIGH (evidence mismatch)   │
│                                                                             │
│  REGRESSION     AQ-REG-0100                      AQ-REG-0200                │
│                 pass_rate=1.0, strict            pass_rate=0.8, relaxed      │
│                 Re-run enumeration               Mesh refinement               │
│                                                                             │
│  SAME SCHEMAS. DIFFERENT INSTANTIATIONS. AUDIT CAUGHT CATEGORY ERROR.       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

CRITICAL AUDIT FINDING (PULL):
  Evidence AQ-EVD-0200 (dim_H=2) was initially tagged as 'supports' MLC.
  Audit caught: dim_H=2 does NOT imply local connectedness.
  Resolution: Evidence reclassified as 'partial', claim remains 'stated'.
  This is WHY PULL objects need stricter audit—category errors are invisible
  without structured evidence typing.

FILES WRITTEN:

  AQ-DUAL-LIFECYCLE-001.json           22,287 B  — Full dual lifecycle artifacts (PUSH + PULL)
  AQ-COMPARISON-001.json                2,880 B  — Structured comparison matrix and insights

Total schema substrate files: 10
  6 core schemas + 1 index + 1 validation + 1 hypothesis + 1 landscape + 1 dual lifecycle + 1 comparison
