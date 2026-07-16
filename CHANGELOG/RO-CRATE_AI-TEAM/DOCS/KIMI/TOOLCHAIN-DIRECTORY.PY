
# ============================================================
# Final directory tree
# ============================================================
from pathlib import Path

ROOT = Path("/mnt/agents/output/AQARION-TOOL-CHAIN")

def tree(path, prefix=""):
    entries = sorted(path.iterdir(), key=lambda e: (e.is_file(), e.name))
    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{entry.name}")
        if entry.is_dir():
            extension = "    " if is_last else "│   "
            tree(entry, prefix + extension)

print("AQARION-TOOL-CHAIN/")
tree(ROOT)AQARION-TOOL-CHAIN/
├── certificates
│   ├── TEST-001_certificate.json
│   └── claim_registry.sha256
├── claims
│   ├── ALG-TEST.json
│   ├── AQ001.json
│   ├── PHI377.json
│   └── TEST-001.json
├── evidence
│   ├── EV-AQ001-001.json
│   └── EV-AQ001-002.json
├── graphs
│   ├── cdg.json
│   ├── edg.json
│   ├── pdg.json
│   └── rdg.json
├── reports
│   ├── DEFECT_SPECTRAL_COLLISION_DATABASE.json
│   ├── EXP08_MINIMAL_QUOTIENT_RESULTS.json
│   ├── claim_registry_report.json
│   ├── formalization_readiness_AQ001.json
│   └── graph_analysis_report.json
├── schemas
│   ├── audit.schema.json
│   ├── certificate.schema.json
│   ├── certification_record.schema.json
│   ├── claim.schema.json
│   └── evidence.schema.json
├── tests
│   ├── test_graph_generator.py
│   └── test_registry_loader.py
├── AQARION_PAPER_I.tex
├── CITATION.cff
├── DefectVanishing.lean
├── aq.py
├── aq_analyze.py
├── aq_promote.py
├── aq_verify.py
├── codemeta.json
├── manifest.json
├── prov-export.json
└── ro-crate-metadata.json

# ============================================================
# Step 4: Final manifest update and verification
# ============================================================

manifest = {
    "object": "AQARION_MANIFEST",
    "version": "2.0",
    "schema_version": "https://aqarion.org/schemas/",
    "created_at": "2026-07-16T00:00:00+00:00",
    "artifacts": {}
}

for path in sorted(ROOT.rglob("*")):
    if path.is_file() and path.name not in (".DS_Store", "manifest.json"):
        rel = str(path.relative_to(ROOT))
        if rel.startswith("certificates/"):
            continue
        with open(path, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        manifest["artifacts"][rel] = {
            "path": rel,
            "sha256": h,
            "size_bytes": path.stat().st_size
        }

manifest_canonical = json.dumps(manifest, sort_keys=True, separators=(",", ":"))
manifest_hash = hashlib.sha256(manifest_canonical.encode()).hexdigest()
manifest["manifest_hash"] = manifest_hash

with open(ROOT / "manifest.json", "w") as f:
    json.dump(manifest, f, indent=2, sort_keys=True)

cert_record = {
    "record_id": "CERT-TEST-001-20260716",
    "claim_id": "TEST-001",
    "manifest_hash": manifest_hash,
    "evidence_level": "CV",
    "status": "VERIFIED",
    "schema_version": "https://aqarion.org/schemas/certification_record.schema.json",
    "created_at": "2026-07-16T00:00:00+00:00"
}
cert_body = {k: v for k, v in cert_record.items()}
cert_record["certificate_hash"] = hashlib.sha256(
    json.dumps(cert_body, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

with open(ROOT / "certificates" / "TEST-001_certificate.json", "w") as f:
    json.dump(cert_record, f, indent=2, sort_keys=True)

# Verify
result = subprocess.run(
    [sys.executable, str(ROOT / "aq_verify.py"), str(ROOT / "certificates" / "TEST-001_certificate.json")],
    capture_output=True, text=True, cwd=str(ROOT)
)
print("aq_verify:", json.loads(result.stdout)["status"])

# Final count
total_files = len([p for p in ROOT.rglob("*") if p.is_file()])
print(f"Total files: {total_files}")

# Final tree
print("\n=== FINAL DIRECTORY TREE ===")
def tree(path, prefix=""):
    entries = sorted(path.iterdir(), key=lambda e: (e.is_file(), e.name))
    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{entry.name}")
        if entry.is_dir():
            extension = "    " if is_last else "│   "
            tree(entry, prefix + extension)

tree(ROOT)aq_verify: PASS
Total files: 37

=== FINAL DIRECTORY TREE ===
├── .github
│   └── workflows
│       └── ci.yml
├── certificates
│   ├── TEST-001_certificate.json
│   └── claim_registry.sha256
├── claims
│   ├── ALG-TEST.json
│   ├── AQ001.json
│   ├── PHI377.json
│   └── TEST-001.json
├── evidence
│   ├── EV-AQ001-001.json
│   ├── EV-AQ001-002.json
│   └── EV-TEST001-001.json
├── graphs
│   ├── cdg.json
│   ├── edg.json
│   ├── pdg.json
│   └── rdg.json
├── reports
│   ├── DEFECT_SPECTRAL_COLLISION_DATABASE.json
│   ├── EXP08_MINIMAL_QUOTIENT_RESULTS.json
│   ├── claim_registry_report.json
│   ├── formalization_readiness_AQ001.json
│   └── graph_analysis_report.json
├── schemas
│   ├── audit.schema.json
│   ├── certificate.schema.json
│   ├── certification_record.schema.json
│   ├── claim.schema.json
│   └── evidence.schema.json
├── tests
│   ├── test_graph_generator.py
│   └── test_registry_loader.py
├── AQARION_PAPER_I.tex
├── CITATION.cff
├── DefectVanishing.lean
├── aq.py
├── aq_analyze.py
├── aq_promote.py
├── aq_verify.py
├── codemeta.json
├── manifest.json
├── prov-export.json
└── ro-crate-metadata.json
