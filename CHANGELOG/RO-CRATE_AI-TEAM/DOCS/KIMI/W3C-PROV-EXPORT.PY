
# ============================================================
# 3. W3C PROV Export
# ============================================================

prov_export = {
    "@context": {
        "prov": "http://www.w3.org/ns/prov#",
        "aq": "https://aqarion.org/ns/",
        "xsd": "http://www.w3.org/2001/XMLSchema#"
    },
    "@graph": [
        {
            "@id": "aq:agent_aqarion",
            "@type": "prov:Agent",
            "prov:type": "prov:SoftwareAgent",
            "prov:label": "AQARION Tool Chain v21.0"
        },
        {
            "@id": "aq:activity_registry_build",
            "@type": "prov:Activity",
            "prov:startedAtTime": "2026-07-16T00:00:00+00:00",
            "prov:endedAtTime": "2026-07-16T00:00:00+00:00",
            "prov:wasAssociatedWith": {"@id": "aq:agent_aqarion"},
            "prov:used": [
                {"@id": "aq:claim_test001"},
                {"@id": "aq:claim_aq001"},
                {"@id": "aq:claim_phi377"}
            ]
        },
        {
            "@id": "aq:entity_registry",
            "@type": "prov:Entity",
            "prov:type": "aq:ClaimRegistry",
            "prov:wasGeneratedBy": {"@id": "aq:activity_registry_build"},
            "prov:wasAttributedTo": {"@id": "aq:agent_aqarion"},
            "aq:hash": "9bf22540c65da58570a8759911646f1485f1070515cf91798fcf26606e542c8f"
        },
        {
            "@id": "aq:claim_test001",
            "@type": "prov:Entity",
            "prov:type": "aq:Claim",
            "aq:claim_id": "TEST-001",
            "aq:evidence_level": "CV",
            "aq:status": "VERIFIED"
        },
        {
            "@id": "aq:claim_aq001",
            "@type": "prov:Entity",
            "prov:type": "aq:Claim",
            "aq:claim_id": "AQ001",
            "aq:evidence_level": "FV",
            "aq:status": "PROVED",
            "prov:wasDerivedFrom": {"@id": "aq:claim_test001"}
        },
        {
            "@id": "aq:claim_phi377",
            "@type": "prov:Entity",
            "prov:type": "aq:Claim",
            "aq:claim_id": "PHI377",
            "aq:evidence_level": "OPEN",
            "aq:status": "OPEN",
            "prov:wasDerivedFrom": {"@id": "aq:claim_aq001"}
        }
    ]
}

with open(ROOT / "prov-export.json", "w") as f:
    json.dump(prov_export, f, indent=2, sort_keys=False)

print("prov-export.json written.")prov-export.json written.
