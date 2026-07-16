
from pathlib import Path
import json
import hashlib

ROOT = Path("/mnt/agents/output/AQARION-TOOL-CHAIN")
SCHEMAS_DIR = ROOT / "schemas"
SCHEMAS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 1. JSON Schemas (frozen)
# ============================================================

claim_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://aqarion.org/schemas/claim.schema.json",
    "title": "AQARION Claim",
    "description": "A single mathematical or computational claim.",
    "type": "object",
    "required": ["claim_id", "description", "evidence_level", "status", "dependencies", "artifacts"],
    "properties": {
        "claim_id": {"type": "string", "pattern": "^[A-Z0-9-]+$"},
        "description": {"type": "string", "minLength": 1},
        "evidence_level": {"type": "string", "enum": ["ALG", "CV", "FV", "OPEN"]},
        "status": {"type": "string", "enum": ["OPEN", "VERIFIED", "PROVED", "DISPROVED", "KILLED"]},
        "dependencies": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
        "artifacts": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
        "provenance": {"type": "object"}
    },
    "additionalProperties": False
}

evidence_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://aqarion.org/schemas/evidence.schema.json",
    "title": "AQARION Evidence",
    "description": "Evidence artifact supporting a claim.",
    "type": "object",
    "required": ["evidence_id", "claim_id", "evidence_type", "artifact_path", "checksum"],
    "properties": {
        "evidence_id": {"type": "string"},
        "claim_id": {"type": "string"},
        "evidence_type": {"type": "string", "enum": ["computation", "proof", "formalization", "citation", "data"]},
        "artifact_path": {"type": "string"},
        "checksum": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "timestamp": {"type": "string", "format": "date-time"}
    },
    "additionalProperties": False
}

certificate_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://aqarion.org/schemas/certificate.schema.json",
    "title": "AQARION Certificate",
    "description": "Cryptographic attestation of claim status.",
    "type": "object",
    "required": ["record_id", "claim_id", "artifact_hash", "graphs", "evidence_level", "status", "timestamp", "certificate_hash"],
    "properties": {
        "record_id": {"type": "string"},
        "claim_id": {"type": "string"},
        "artifact_hash": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "graphs": {
            "type": "object",
            "properties": {
                "pdg": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
                "cdg": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
                "edg": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
                "rdg": {"type": "string", "pattern": "^[a-f0-9]{64}$"}
            },
            "required": ["pdg", "cdg", "edg", "rdg"]
        },
        "evidence_level": {"type": "string", "enum": ["ALG", "CV", "FV", "OPEN"]},
        "status": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "certificate_hash": {"type": "string", "pattern": "^[a-f0-9]{64}$"}
    },
    "additionalProperties": False
}

certification_record_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://aqarion.org/schemas/certification_record.schema.json",
    "title": "AQARION Certification Record",
    "description": "Canonical record for a certified claim.",
    "type": "object",
    "required": ["record_id", "claim_id", "artifact_hash", "graphs", "evidence_level", "status", "timestamp", "certificate_hash"],
    "properties": {
        "record_id": {"type": "string"},
        "claim_id": {"type": "string"},
        "artifact_hash": {"type": "string"},
        "graphs": {
            "type": "object",
            "properties": {
                "pdg": {"type": "string"},
                "cdg": {"type": "string"},
                "edg": {"type": "string"},
                "rdg": {"type": "string"}
            },
            "required": ["pdg", "cdg", "edg", "rdg"]
        },
        "evidence_level": {"type": "string"},
        "status": {"type": "string"},
        "timestamp": {"type": "string"},
        "certificate_hash": {"type": "string"}
    },
    "additionalProperties": False
}

audit_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://aqarion.org/schemas/audit.schema.json",
    "title": "AQARION Audit Report",
    "description": "Machine-readable audit of a claim registry.",
    "type": "object",
    "required": ["status", "claims_loaded", "duplicates", "claims", "hash", "timestamp"],
    "properties": {
        "status": {"type": "string", "enum": ["PASS", "FAIL"]},
        "claims_loaded": {"type": "integer", "minimum": 0},
        "duplicates": {"type": "integer", "minimum": 0},
        "schema_errors": {"type": "integer", "minimum": 0},
        "claims": {"type": "array", "items": {"type": "string"}},
        "duplicate_ids": {"type": "array", "items": {"type": "string"}},
        "schema_error_messages": {"type": "array", "items": {"type": "string"}},
        "hash": {"type": "string"},
        "timestamp": {"type": "string"}
    },
    "additionalProperties": False
}

schemas = {
    "claim.schema.json": claim_schema,
    "evidence.schema.json": evidence_schema,
    "certificate.schema.json": certificate_schema,
    "certification_record.schema.json": certification_record_schema,
    "audit.schema.json": audit_schema,
}

for fname, schema in schemas.items():
    with open(SCHEMAS_DIR / fname, "w") as f:
        json.dump(schema, f, indent=2, sort_keys=True)

print("Schemas written:")
for f in sorted(SCHEMAS_DIR.glob("*.json")):
    print(f"  {f.name}")Schemas written:
  audit.schema.json
  certificate.schema.json
  certification_record.schema.json
  claim.schema.json
  evidence.schema.json
