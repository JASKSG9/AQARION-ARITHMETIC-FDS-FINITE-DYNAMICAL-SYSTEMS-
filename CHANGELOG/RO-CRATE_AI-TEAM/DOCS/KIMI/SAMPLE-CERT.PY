
# ============================================================
# 5. Create a sample Certification Record for aq_verify testing
# ============================================================

# Load existing claim to compute its hash
with open(ROOT / "claims" / "TEST-001.json", "rb") as f:
    claim_hash = hashlib.sha256(f.read()).hexdigest()

# Build certification record
cert_record = {
    "record_id": "CERT-TEST-001-20260716",
    "claim_id": "TEST-001",
    "artifact_hash": claim_hash,
    "graphs": {
        "pdg": "0" * 64,  # placeholder — no graph files yet
        "cdg": "0" * 64,
        "edg": "0" * 64,
        "rdg": "0" * 64
    },
    "evidence_level": "CV",
    "status": "VERIFIED",
    "timestamp": "2026-07-16T00:00:00+00:00"
}

# Compute certificate_hash (hash of everything except certificate_hash itself)
cert_body = {k: v for k, v in cert_record.items()}
cert_record["certificate_hash"] = hashlib.sha256(
    json.dumps(cert_body, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

with open(ROOT / "certificates" / "TEST-001_certificate.json", "w") as f:
    json.dump(cert_record, f, indent=2, sort_keys=True)

print("TEST-001_certificate.json created.")
print(f"Claim hash: {claim_hash}")
print(f"Certificate hash: {cert_record['certificate_hash']}")TEST-001_certificate.json created.
Claim hash: e08bdf4b40919fe9beacd7a88756fa7a5b63e2df7d7d842d74570f0e43da678e
Certificate hash: d028d25a53b41acb98ab60aecac36196ac4315ba077115767aa16295a1c08dc1
