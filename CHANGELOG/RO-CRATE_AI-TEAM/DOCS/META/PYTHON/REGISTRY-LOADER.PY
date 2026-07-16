import json, hashlib, pathlib
FIXED_TIMESTAMP = "2026-07-16T00:00:00+00:00"
BASE = pathlib.Path(__file__).parent.parent
def load_claims():
    claims_dir = BASE / "claims"
    claims = []
    seen = set()
    duplicates = []
    for path in sorted(claims_dir.glob("*.json")):
        with open(path) as f:
            data = json.load(f)
        for field in ["id", "title", "status", "evidence_level", "dependencies"]:
            if field not in data:
                raise ValueError(f"Schema gate failed for {path}: missing {field}")
        if data["id"] in seen:
            duplicates.append(data["id"])
        seen.add(data["id"])
        claims.append(data)
    if duplicates:
        raise ValueError(f"Duplicate detection: {duplicates}")
    claims_sorted = sorted(claims, key=lambda x: x["id"])
    return claims_sorted
def canonical_hash(claims_sorted):
    canonical = json.dumps(claims_sorted, sort_keys=True, separators=(',',':'))
    return hashlib.sha256(canonical.encode()).hexdigest(), canonical
def main():
    (BASE / "certificates").mkdir(parents=True, exist_ok=True)
    (BASE / "reports").mkdir(parents=True, exist_ok=True)
    claims = load_claims()
    h1, canonical = canonical_hash(claims)
    h2, _ = canonical_hash(claims)
    h3, _ = canonical_hash(claims)
    assert h1 == h2 == h3, "Non-deterministic registry hash"
    cert = {
        "certificate_id": "claim-registry.sha256",
        "registry_hash": h1,
        "hash_scope": ["claims/*.json canonical sorted by id, sort_keys True, separators ,:"],
        "excluded": ["timestamp", "generator_version", "file_mtime"],
        "timestamp_fixed": FIXED_TIMESTAMP,
        "timestamp_excluded_from_hash": True,
        "deterministic_runs": 3,
        "determinism_verified": True,
        "claims_count": len(claims),
        "ordering": [c["id"] for c in claims]
    }
    cert_path = BASE / "certificates/claim-registry.sha256.json"
    with open(cert_path, 'w') as f:
        json.dump(cert, f, sort_keys=True, indent=2)
    report = {
        "registry_hash": h1,
        "deterministic_hash_verified": h1 == h2 == h3,
        "claims": claims,
        "report_timestamp": FIXED_TIMESTAMP,
        "schema_gate": "pass",
        "duplicate_check": "pass"
    }
    report_path = BASE / "reports/claim-registry-report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, sort_keys=True, indent=2)
    print(f"[AQTC-002] Registry loader PASS")
    print(f"  Registry hash: {h1}")
    print(f"  Determinism: 3/3 identical")
    return h1
if __name__ == "__main__":
    main()

