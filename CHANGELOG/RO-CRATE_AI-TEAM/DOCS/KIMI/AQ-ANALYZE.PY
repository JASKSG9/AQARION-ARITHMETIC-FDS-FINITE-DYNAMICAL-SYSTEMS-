
# ============================================================
# Update manifest with aq_analyze.py and graph analysis report
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

# Update certificate
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

# Print graph analysis report
with open(ROOT / "reports" / "graph_analysis_report.json") as f:
    analysis = json.load(f)

print("\n=== GRAPH ANALYSIS SUMMARY ===")
for name, data in analysis.items():
    print(f"\n{name.upper()}:")
    print(f"  Nodes: {data['nodes']}, Edges: {data['edges']}, Density: {data['density']:.4f}")
    print(f"  Cycles: {data['cycles_detected']}, Is DAG: {data['is_dag']}")
    print(f"  Max Depth: {data['max_depth']}")
    print(f"  Critical Path: {' -> '.join(data['critical_path'])}")
    print(f"  Components: {data['connected_components']} (sizes: {data['component_sizes']})")aq_verify: PASS

=== GRAPH ANALYSIS SUMMARY ===

CDG:
  Nodes: 4, Edges: 3, Density: 0.2500
  Cycles: 0, Is DAG: True
  Max Depth: 2
  Critical Path: PHI377 -> AQ001 -> TEST-001
  Components: 1 (sizes: [4])

EDG:
  Nodes: 6, Edges: 2, Density: 0.0667
  Cycles: 0, Is DAG: True
  Max Depth: 1
  Critical Path: AQ001 -> DefectVanishing.lean
  Components: 4 (sizes: [1, 2, 1, 2])

PDG:
  Nodes: 4, Edges: 3, Density: 0.2500
  Cycles: 0, Is DAG: True
  Max Depth: 2
  Critical Path: PHI377 -> AQ001 -> TEST-001
  Components: 1 (sizes: [4])

RDG:
  Nodes: 4, Edges: 0, Density: 0.0000
  Cycles: 0, Is DAG: True
  Max Depth: 0
  Critical Path: ALG-TEST
  Components: 4 (sizes: [1, 1, 1, 1])
