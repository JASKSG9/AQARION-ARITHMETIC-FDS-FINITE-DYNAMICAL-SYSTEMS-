
# ============================================================
# 2. RO-Crate metadata.json
# ============================================================

ro_crate = {
    "@context": "https://w3id.org/ro/crate/1.1/context",
    "@graph": [
        {
            "@type": "CreativeWork",
            "@id": "ro-crate-metadata.json",
            "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"},
            "about": {"@id": "./"},
            "datePublished": "2026-07-16T00:00:00+00:00",
            "description": "AQARION Tool Chain — Deterministic certification layer for computational and mathematical research artifacts.",
            "name": "AQARION-TOOL-CHAIN",
            "creator": {"@id": "https://aqarion.org"}
        },
        {
            "@id": "./",
            "@type": "Dataset",
            "hasPart": [
                {"@id": "claims/TEST-001.json"},
                {"@id": "claims/AQ001.json"},
                {"@id": "claims/PHI377.json"},
                {"@id": "certificates/claim_registry.sha256"},
                {"@id": "reports/claim_registry_report.json"},
                {"@id": "aq.py"},
                {"@id": "tests/test_registry_loader.py"}
            ],
            "name": "AQARION Tool Chain",
            "description": "Deterministic claim registry, certification, and audit infrastructure.",
            "datePublished": "2026-07-16T00:00:00+00:00",
            "license": "MIT"
        },
        {
            "@id": "claims/TEST-001.json",
            "@type": "Entity",
            "name": "TEST-001",
            "description": "Minimal deterministic certification test claim",
            "evidence_level": "CV",
            "status": "VERIFIED"
        },
        {
            "@id": "claims/AQ001.json",
            "@type": "Entity",
            "name": "AQ001",
            "description": "Observable defect operator D_Pi is well-defined for finite partitions",
            "evidence_level": "FV",
            "status": "PROVED"
        },
        {
            "@id": "claims/PHI377.json",
            "@type": "Entity",
            "name": "PHI377",
            "description": "Philosophical claim about mathematical truth certification",
            "evidence_level": "OPEN",
            "status": "OPEN"
        },
        {
            "@id": "certificates/claim_registry.sha256",
            "@type": "CreativeWork",
            "name": "Claim Registry Certificate",
            "description": "SHA-256 cryptographic attestation of registry integrity.",
            "encodingFormat": "text/plain"
        },
        {
            "@id": "reports/claim_registry_report.json",
            "@type": "Entity",
            "name": "Claim Registry Audit Report",
            "description": "Machine-readable audit of claim registry validation."
        },
        {
            "@id": "aq.py",
            "@type": "SoftwareSourceCode",
            "name": "AQARION Tool Chain Entry Point",
            "programmingLanguage": "Python",
            "description": "Main command-line interface for registry and certification operations."
        },
        {
            "@id": "tests/test_registry_loader.py",
            "@type": "SoftwareSourceCode",
            "name": "AQTC-002 Test Suite",
            "programmingLanguage": "Python",
            "description": "Deterministic hash verification for claim registry loader."
        }
    ]
}

with open(ROOT / "ro-crate-metadata.json", "w") as f:
    json.dump(ro_crate, f, indent=2, sort_keys=False)

print("ro-crate-metadata.json written.")ro-crate-metadata.json written.
