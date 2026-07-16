
# Final state display
print("=== Final AQARION v1.0 State ===\n")

with open(ROOT / "manifest.json", "r") as f:
    m = json.load(f)
print(f"Manifest Hash: {m['manifest_hash']}")
print(f"Artifacts: {len(m['artifacts'])}")

with open(ROOT / "graphs" / "dependency_graph.json", "r") as f:
    g = json.load(f)
print(f"Graph Nodes: {g['statistics']['node_count']}")
print(f"Graph Edges: {g['statistics']['edge_count']}")
print(f"Graph Cycles: {g['statistics']['cycles']}")

with open(ROOT / "claims" / "AQ-THM-001.json", "r") as f:
    thm = json.load(f)
print(f"\nAQ-THM-001 Status: {thm['status']}")
print(f"Assurance: {thm['metadata']['maturity']['assurance']}")
ls = thm['metadata']['lean_status']
print(f"Lean Proof: {ls.get('proof_obligations_remaining', 'N/A')} obligations remaining")
print(f"Completed: {ls.get('proof_completed', 'N/A')}")

with open(ROOT / "certificates" / "CERT-AQ001-001.json", "r") as f:
    cert = json.load(f)
print(f"\nCERT-AQ001-001 Status: {cert['status']}")
print(f"Assurance: {cert['metadata']['maturity']['assurance']}")
print(f"Results: {cert['metadata']['results']}")

print("\n=== Lean 4 Files ===")
for f in sorted(LEAN_DIR.rglob("*")):
    if f.is_file():
        rel = f.relative_to(LEAN_DIR)
        print(f"  {rel} ({f.stat().st_size} bytes)")

print("\n=== AQARION v1.0: COMPLETE ===")=== Final AQARION v1.0 State ===

Manifest Hash: eed9e15151092eb7bba2af38ef6177315897bbb42ac59779031758fd80a26b99
Artifacts: 17
Graph Nodes: 10
Graph Edges: 14
Graph Cycles: 0

AQ-THM-001 Status: VERIFIED
Assurance: FORMALLY_VERIFIED
Lean Proof: 0 obligations remaining
Completed: 2026-07-16

CERT-AQ001-001 Status: PROMOTED
Assurance: FORMALLY_VERIFIED
Results: {'dependency_check': 'PASS', 'lean_proof': 'PASS', 'lean_proof_obligations': '0 remaining', 'lean_specification': 'PASS', 'schema_check': 'PASS', 'verification': 'PASS'}

=== Lean 4 Files ===
  AQ-THM-001-bridge.json (1021 bytes)
  Aqarion/FDDS.lean (10040 bytes)
  Aqarion/FDDSExec.lean (2248 bytes)
  Aqarion/Kaprekar.lean (1882 bytes)
  MATHLIB_CAPABILITY_MAPPING.md (8238 bytes)
  PROOF_SKETCH.md (3312 bytes)
  lakefile.toml (180 bytes)

=== AQARION v1.0: COMPLETE ===
