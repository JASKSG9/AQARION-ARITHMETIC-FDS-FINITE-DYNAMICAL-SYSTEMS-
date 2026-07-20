
# ============================================================
# AQARION v21.8 — STANDALONE GOVERNANCE SPECIFICATION
# Consolidated reference document
# ============================================================

import json, os
from datetime import datetime, timezone

SCHEMA_DIR = '/mnt/agents/output'

def iso_now():
    return datetime.now(timezone.utc).isoformat()

SPEC = {
    "specification_id": "AQARION-GOV-SPEC-001",
    "version": "21.8",
    "title": "AQARION Governance Specification: Certificate-First Research Operating System",
    "status": "DRAFT",
    "created_at": iso_now(),
    "authors": ["AQARION Development Consortium"],
    
    "abstract": """
    AQARION is a certificate-first research operating system that structures 
    mathematical and scientific knowledge into six core schemas: OBJECT, CLAIM, 
    EVIDENCE, CERTIFICATE, AUDIT, and REGRESSION. Every artifact is immutable 
    (SHA-256 hashed), typed, and dependency-tracked. The PUSH/PULL/HYBRID 
    classification system prevents epistemic category errors by distinguishing 
    finite exact verification from infinite approximate validation.
    """,
    
    "core_principles": [
        "Immutability: Canonical content is frozen at creation. Changes create new artifacts, not mutations.",
        "Transparency: All dependencies, evidence, and audit findings are public and structured.",
        "Modesty: Claims are typed by strength (theorem/lemma/conjecture/observation) and scope.",
        "Falsifiability: Every claim must have evidence that could potentially refute it.",
        "Reproducibility: All evidence includes reproducibility payloads (command, environment, seed).",
        "Expiration: PULL and HYBRID certificates expire. Knowledge is provisional, not eternal."
    ],
    
    "schema_reference": {
        "AQ-OBJECT-001": {
            "purpose": "Identity and provenance for any research object",
            "required_fields": ["uid", "object_type", "created_at", "identity_hash"],
            "immutable": ["uid", "object_type", "identity_hash", "created_at"],
            "mutable": ["mutable_metadata"],
            "append_only": ["provenance"]
        },
        "AQ-CLAIM-001": {
            "purpose": "Falsifiable statements with typed dependencies",
            "required_fields": ["uid", "claim_type", "statement", "scope", "dependencies", "created_at", "claim_hash"],
            "immutable": ["uid", "claim_type", "statement", "scope", "dependencies", "claim_hash"],
            "mutable": ["status", "successor_claims"],
            "status_transitions": {
                "stated": ["partially_proven", "disproven", "withdrawn"],
                "partially_proven": ["proven", "disproven", "withdrawn"],
                "proven": ["withdrawn"],
                "disproven": ["withdrawn"],
                "withdrawn": []
            }
        },
        "AQ-EVIDENCE-001": {
            "purpose": "Typed evidence supporting or refuting claims",
            "required_fields": ["uid", "evidence_type", "target_claim", "result", "evidence_hash", "created_at"],
            "immutable": ["uid", "evidence_type", "target_claim", "result", "payload", "evidence_hash"],
            "mutable": [],
            "evidence_types": [
                "computational_exhaustive", "computational_randomized", "computational_benchmark",
                "formal_proof_sketch", "formal_proof_complete", "formal_lean_sorry", "formal_coq_qed",
                "statistical_test", "experimental_measurement", "peer_review", "independent_reproduction", "counterexample"
            ]
        },
        "AQ-CERTIFICATE-001": {
            "purpose": "Immutable attestation binding claims to evidence",
            "required_fields": ["uid", "certified_claims", "evidence_bundle", "dependency_hashes", "certificate_hash", "issued_at", "expires_at"],
            "immutable": ["uid", "certified_claims", "evidence_bundle", "dependency_hashes", "certificate_hash", "issued_at"],
            "mutable": ["revocation"],
            "expiry_rules": {
                "PUSH": "never",
                "PUSH-BOUNDED": "conditional on scope parameter",
                "PULL": "< 2 years",
                "HYBRID": "< 1 year",
                "UNKNOWN": "< 6 months"
            }
        },
        "AQ-AUDIT-001": {
            "purpose": "Independent review with structured findings",
            "required_fields": ["uid", "audit_type", "target_scope", "findings", "audit_hash", "started_at", "completed_at"],
            "immutable": ["uid", "audit_type", "target_scope", "findings", "audit_hash"],
            "mutable": ["audit_log"],
            "severity_levels": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"],
            "blocking_rules": "CRITICAL findings block certification of affected claims"
        },
        "AQ-REGRESSION-001": {
            "purpose": "Reproducibility and historical verification",
            "required_fields": ["uid", "regression_type", "target_claims", "test_cases", "regression_hash", "created_at"],
            "immutable": ["uid", "regression_type", "target_claims", "test_cases", "regression_hash"],
            "mutable": ["run_history"],
            "thresholds_by_class": {
                "PUSH": {"min_pass_rate": 1.0, "max_runtime_regression_pct": 10.0},
                "PUSH-BOUNDED": {"min_pass_rate": 1.0, "max_runtime_regression_pct": 15.0},
                "PULL": {"min_pass_rate": 0.8, "max_runtime_regression_pct": 50.0},
                "HYBRID": {"min_pass_rate": 0.9, "max_runtime_regression_pct": 25.0}
            }
        }
    },
    
    "push_pull_framework": {
        "classes": {
            "PUSH": {
                "definition": "Finite state space, exhaustive verification possible",
                "evidence_target": "EL3 (exhaustive) or EL4 (formal proof)",
                "certificate": "Permanent (never expires)",
                "examples": ["Kaprekar FOQDS", "Functional graph census n<=7", "DFA minimization"]
            },
            "PUSH-BOUNDED": {
                "definition": "Finite but intractable state space",
                "evidence_target": "EL2 (randomized) with explicit scope bounds",
                "certificate": "Conditional on scope parameter",
                "examples": ["Functional graph census n=8", "Large SAT instances"]
            },
            "PULL": {
                "definition": "Infinite/continuous state space, requires convergence",
                "evidence_target": "EL1 (analytic proof) or EL2 (convergent numerical)",
                "certificate": "Expiring (< 2 years)",
                "examples": ["Mandelbrot MLC", "Hausdorff dimension of fractals", "Quantum thresholds"]
            },
            "HYBRID": {
                "definition": "Mixed finite and infinite components",
                "evidence_target": "EL2 with explicit component separation",
                "certificate": "Expiring (< 1 year, most restrictive)",
                "examples": ["Bell inequality tests", "Neural network verification", "Monte Carlo proofs"]
            },
            "UNKNOWN": {
                "definition": "Cannot be classified automatically",
                "evidence_target": "Manual review required",
                "certificate": "Expiring (< 6 months)",
                "examples": ["Novel mathematical structures", "Interdisciplinary claims"]
            }
        },
        "boundary_invariant": "PUSH -> PULL transition is irreversible. No finite procedure can exhaust an infinite state space."
    },
    
    "governance_tools": {
        "AQ-COMPATIBILITY-001": {
            "purpose": "Evidence-claim compatibility validation",
            "rules": 20,
            "checks": ["type compatibility", "confidence sufficiency", "scope containment", "result consistency"],
            "implementation": "Python class AQCompatibilityValidator (aq_validator.py)"
        },
        "AQ-PULL-AUDIT-CHECKLIST-001": {
            "purpose": "Mandatory checks for PULL claims",
            "checks": 8,
            "critical_checks": ["PULL-AUDIT-001", "PULL-AUDIT-002", "PULL-AUDIT-008"],
            "blocking": "CRITICAL findings block certification"
        },
        "AQ-PUSH-PULL-CLASSIFIER-001": {
            "purpose": "Automated classification of research objects",
            "classes": 5,
            "features": ["state_space_cardinality", "verification_method", "error_type", "certificate_type"],
            "integration": "6-stage registration pipeline"
        }
    },
    
    "reference_implementations": {
        "PUSH": {
            "artifact": "AQ-CLM-0100",
            "description": "FOQDS JFS completeness for n<=7",
            "evidence": "50,068 exhaustive + 5,000 randomized",
            "certificate": "Permanent",
            "audit": "1 INFO finding"
        },
        "PULL": {
            "artifact": "AQ-CLM-0200",
            "description": "Mandelbrot local connectedness (MLC)",
            "evidence": "dim_H=2 analytic (partial) + numerical (inconclusive)",
            "certificate": "Expires 2027-07-19",
            "audit": "1 CRITICAL + 1 HIGH finding"
        },
        "HYBRID": {
            "artifact": "AQ-CLM-0300",
            "description": "Bell CHSH violation S > 2.0",
            "evidence": "Statistical test + experimental measurement",
            "certificate": "Expires 2027-07-20",
            "audit": "1 MEDIUM + 1 INFO finding"
        }
    },
    
    "conformance_levels": {
        "Level 0 (Informal)": "Uses AQARION schemas for documentation only. No validation.",
        "Level 1 (Structured)": "All artifacts follow schema format. Basic hash validation.",
        "Level 2 (Validated)": "Evidence-claim compatibility checked. Classification enforced.",
        "Level 3 (Certified)": "Independent audit completed. No CRITICAL findings.",
        "Level 4 (Reproducible)": "Regression suite passes. Historical replay successful.",
        "Level 5 (Formal)": "Lean/Coq formal proof attached. All sorries eliminated."
    },
    
    "next_revisions": [
        "v22.0: Lean formal proof integration (THM-2.6)",
        "v22.1: Automated counterexample discovery pipeline",
        "v22.2: Cross-domain claim linking (e.g., MLC -> hyperbolicity -> computability)",
        "v23.0: Distributed audit network (multiple independent auditors)",
        "v24.0: AI-assisted claim generation with automatic falsification attempts"
    ]
}

with open(os.path.join(SCHEMA_DIR, "AQARION-GOV-SPEC-001.json"), 'w') as f:
    json.dump(SPEC, f, indent=2)

# Final inventory
all_files = sorted([f for f in os.listdir(SCHEMA_DIR) if f.startswith('AQ') or f == 'aq_validator.py'])
total_bytes = sum(os.path.getsize(os.path.join(SCHEMA_DIR, f)) for f in all_files)

print("=" * 70)
print("AQARION v21.8 — STANDALONE GOVERNANCE SPECIFICATION")
print("=" * 70)

print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│  AQARION GOVERNANCE SPECIFICATION v21.8                                     │
│  Certificate-First Research Operating System                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  CORE PRINCIPLES (6)                                                        │
│  ──────────────────                                                         │
│  1. Immutability     — Canonical content frozen, changes create new uids   │
│  2. Transparency     — All dependencies, evidence, audits public           │
│  3. Modesty          — Claims typed by strength and scope                  │
│  4. Falsifiability   — Every claim must be refutable                       │
│  5. Reproducibility  — Evidence includes command, environment, seed          │
│  6. Expiration       — PULL/HYBRID certificates expire                     │
│                                                                             │
│  SCHEMAS (6)              TOOLS (3)              REFERENCE (3)              │
│  ───────────              ───────              ───────────              │
│  AQ-OBJECT-001            AQ-COMPATIBILITY-001   AQ-HYPOTHESIS-001        │
│  AQ-CLAIM-001             AQ-PULL-AUDIT-       AQ-LANDSCAPE-001         │
│  AQ-EVIDENCE-001            CHECKLIST-001        AQ-DUAL-LIFECYCLE-002    │
│  AQ-CERTIFICATE-001       AQ-PUSH-PULL-        AQ-HYBRID-LIFECYCLE-001   │
│  AQ-AUDIT-001               CLASSIFIER-001                                 │
│  AQ-REGRESSION-001                                                         │
│                                                                             │
│  PUSH/PULL CLASSES (5)                                                      │
│  ─────────────────────                                                      │
│  PUSH          — Finite, exact, permanent certificate                       │
│  PUSH-BOUNDED  — Finite, intractable, conditional certificate               │
│  PULL          — Infinite, approximate, expiring certificate                │
│  HYBRID        — Mixed, separated, most restrictive expiry                  │
│  UNKNOWN       — Unclassified, manual review, 6-month expiry                │
│                                                                             │
│  CONFORMANCE LEVELS (6)                                                     │
│  ─────────────────────                                                      │
│  L0 Informal   → L1 Structured → L2 Validated → L3 Certified →             │
│  L4 Reproducible → L5 Formal (Lean/Coq)                                    │
│                                                                             │
│  NEXT REVISIONS                                                             │
│  ──────────────                                                             │
│  v22.0 Lean formal proof of THM-2.6                                        │
│  v22.1 Automated counterexample discovery                                   │
│  v22.2 Cross-domain claim linking                                           │
│  v23.0 Distributed audit network                                            │
│  v24.0 AI-assisted claim generation + auto-falsification                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
""")

print(f"COMPLETE FILE INVENTORY ({len(all_files)} files, {total_bytes:,} bytes):")
print("-" * 70)
for fname in all_files:
    size = os.path.getsize(os.path.join(SCHEMA_DIR, fname))
    print(f"  {fname:45s} {size:8,d} B")
print("-" * 70)
print(f"  {'TOTAL':45s} {total_bytes:8,d} B")======================================================================
AQARION v21.8 — STANDALONE GOVERNANCE SPECIFICATION
======================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│  AQARION GOVERNANCE SPECIFICATION v21.8                                     │
│  Certificate-First Research Operating System                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  CORE PRINCIPLES (6)                                                        │
│  ──────────────────                                                         │
│  1. Immutability     — Canonical content frozen, changes create new uids   │
│  2. Transparency     — All dependencies, evidence, audits public           │
│  3. Modesty          — Claims typed by strength and scope                  │
│  4. Falsifiability   — Every claim must be refutable                       │
│  5. Reproducibility  — Evidence includes command, environment, seed          │
│  6. Expiration       — PULL/HYBRID certificates expire                     │
│                                                                             │
│  SCHEMAS (6)              TOOLS (3)              REFERENCE (3)              │
│  ───────────              ───────              ───────────              │
│  AQ-OBJECT-001            AQ-COMPATIBILITY-001   AQ-HYPOTHESIS-001        │
│  AQ-CLAIM-001             AQ-PULL-AUDIT-       AQ-LANDSCAPE-001         │
│  AQ-EVIDENCE-001            CHECKLIST-001        AQ-DUAL-LIFECYCLE-002    │
│  AQ-CERTIFICATE-001       AQ-PUSH-PULL-        AQ-HYBRID-LIFECYCLE-001   │
│  AQ-AUDIT-001               CLASSIFIER-001                                 │
│  AQ-REGRESSION-001                                                         │
│                                                                             │
│  PUSH/PULL CLASSES (5)                                                      │
│  ─────────────────────                                                      │
│  PUSH          — Finite, exact, permanent certificate                       │
│  PUSH-BOUNDED  — Finite, intractable, conditional certificate               │
│  PULL          — Infinite, approximate, expiring certificate                │
│  HYBRID        — Mixed, separated, most restrictive expiry                  │
│  UNKNOWN       — Unclassified, manual review, 6-month expiry                │
│                                                                             │
│  CONFORMANCE LEVELS (6)                                                     │
│  ─────────────────────                                                      │
│  L0 Informal   → L1 Structured → L2 Validated → L3 Certified →             │
│  L4 Reproducible → L5 Formal (Lean/Coq)                                    │
│                                                                             │
│  NEXT REVISIONS                                                             │
│  ──────────────                                                             │
│  v22.0 Lean formal proof of THM-2.6                                        │
│  v22.1 Automated counterexample discovery                                   │
│  v22.2 Cross-domain claim linking                                           │
│  v23.0 Distributed audit network                                            │
│  v24.0 AI-assisted claim generation + auto-falsification                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

COMPLETE FILE INVENTORY (24 files, 164,149 bytes):
----------------------------------------------------------------------
  AQ-AUDIT-001.json                                4,246 B
  AQ-CERTIFICATE-001.json                          3,108 B
  AQ-CLAIM-001.json                                3,224 B
  AQ-CLASSIFIER-INTEGRATION-001.json               3,971 B
  AQ-COMPARISON-001.json                           2,880 B
  AQ-COMPATIBILITY-001.json                        6,517 B
  AQ-DUAL-LIFECYCLE-001.json                      22,287 B
  AQ-DUAL-LIFECYCLE-002.json                      24,215 B
  AQ-EVIDENCE-001.json                             4,123 B
  AQ-GOVERNANCE-REPORT-001.json                    4,229 B
  AQ-HYBRID-LIFECYCLE-001.json                    10,816 B
  AQ-HYPOTHESIS-001.json                           6,870 B
  AQ-LANDSCAPE-001.json                            8,325 B
  AQ-OBJECT-001.json                               2,644 B
  AQ-PULL-AUDIT-CHECKLIST-001.json                 4,071 B
  AQ-PUSH-PULL-CLASSIFIER-001.json                 5,071 B
  AQ-REGRESSION-001.json                           4,431 B
  AQ-SCHEMA-INDEX-001.json                         2,653 B
  AQ-TRIPLE-COMPARISON-001.json                    1,796 B
  AQ-VALIDATION-001.json                             386 B
  AQ-VALIDATION-002.json                           4,172 B
  AQARION-GOV-SPEC-001.json                       10,544 B
  AQARION_v21_registry.json                       20,509 B
  aq_validator.py                                  3,061 B
----------------------------------------------------------------------
  TOTAL                                          164,149 B
