
import subprocess
import sys

# Rebuild manifest
result = subprocess.run(
    [sys.executable, str(ROOT / "aq_manifest.py")],
    capture_output=True, text=True, cwd=str(ROOT)
)
print(result.stdout, end="")
if result.stderr:
    print(result.stderr, end="")

# Rebuild release
result = subprocess.run(
    [sys.executable, str(ROOT / "aq_release.py")],
    capture_output=True, text=True, cwd=str(ROOT)
)
print(result.stdout, end="")
if result.stderr:
    print(result.stderr, end="")

# Show final state
print("\n=== Final AQARION v1.0 State ===\n")

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
print(f"Lean Status: {thm['metadata']['lean_status']['proof_status']}")

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

print("\n=== AQARION v1.0: COMPLETE ===")Manifest: /mnt/agents/output/AQARION-TOOL-CHAIN/manifest.json
Artifacts: 17
Manifest Hash: eed9e15151092eb7bba2af38ef6177315897bbb42ac59779031758fd80a26b99
Self-Verify: PASS
Release bundle: /mnt/agents/output/AQARION-TOOL-CHAIN/release
Files: 6
  certificates/CERT-AQ001-001.json
  environment.json
  manifest.json
  registry_snapshot.json
  release_manifest.json
  verification_report.json

=== Final AQARION v1.0 State ===

Manifest Hash: eed9e15151092eb7bba2af38ef6177315897bbb42ac59779031758fd80a26b99
Artifacts: 17
Graph Nodes: 10
Graph Edges: 14
Graph Cycles: 0

AQ-THM-001 Status: VERIFIED
Assurance: FORMALLY_VERIFIED
Error:
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
Cell In[5], line 40
     38 print(f"\nAQ-THM-001 Status: {thm['status']}")
     39 print(f"Assurance: {thm['metadata']['maturity']['assurance']}")
---> 40 print(f"Lean Status: {thm['metadata']['lean_status']['proof_status']}")
     42 with open(ROOT / "certificates" / "CERT-AQ001-001.json", "r") as f:
     43     cert = json.load(f)

KeyError: 'proof_status'
