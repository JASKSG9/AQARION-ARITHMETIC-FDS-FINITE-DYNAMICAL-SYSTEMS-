
import os, json, hashlib

output_dir = "/mnt/agents/output"

# Generate SHA256SUM manifest
manifest_lines = []
for fname in sorted(os.listdir(output_dir)):
    fpath = os.path.join(output_dir, fname)
    if os.path.isfile(fpath):
        with open(fpath, 'rb') as f:
            h = hashlib.sha256(f.read()).hexdigest()
        size = os.path.getsize(fpath)
        manifest_lines.append(f"{h}  {fname}")

manifest = "\n".join(manifest_lines)
with open(os.path.join(output_dir, "SHA256SUM"), 'w') as f:
    f.write(manifest + "\n")

# VERSION.txt
with open(os.path.join(output_dir, "VERSION.txt"), 'w') as f:
    f.write("AQARION v0.4.1-final\nFrozen: 2026-07-13\nSchema: 3.1.0\n")

# Print final summary
print("=" * 70)
print("AQARION v0.4.1-FINAL — JULY13 COMPLETE DELIVERABLES")
print("=" * 70)
print(f"\nDirectory: {output_dir}")
print("-" * 70)

total_size = 0
for fname in sorted(os.listdir(output_dir)):
    fpath = os.path.join(output_dir, fname)
    if os.path.isfile(fpath):
        size = os.path.getsize(fpath)
        total_size += size
        print(f"  {fname:50s} {size:>10,} bytes")

print("-" * 70)
print(f"  {'TOTAL':50s} {total_size:>10,} bytes")
print("=" * 70)======================================================================
AQARION v0.4.1-FINAL — JULY13 COMPLETE DELIVERABLES
======================================================================

Directory: /mnt/agents/output
----------------------------------------------------------------------
  AQ-CERT-AQ-CLAIM-001-001.json                             438 bytes
  AQ-CERT-AQ-CLAIM-002-001.json                             435 bytes
  AQ-CERT-AQ-CLAIM-003-001.json                             419 bytes
  AQ-CERT-AQ-CLAIM-004-001.json                             401 bytes
  AQARION-ABSTRACT.txt                                    4,227 bytes
  AQARION-ASCII-ATLAS.txt                                12,598 bytes
  AQARION-AUDIT.md                                        5,778 bytes
  AQARION-CHEATSHEET.md                                   3,780 bytes
  AQARION-DEMO.md                                         6,551 bytes
  AQARION-FLOW.md                                         7,049 bytes
  AQARION-KOOPMAN-FORMALIZATION.txt                      25,556 bytes
  AQARION-MERMAID.md                                      5,945 bytes
  AQARION-OVERVIEW.md                                    10,593 bytes
  AQARION-QA.md                                           4,733 bytes
  AQARION-TOC.md                                          2,833 bytes
  AQARION-TOY-MODELS.py                                   6,734 bytes
  Dockerfile                                                152 bytes
  README.md                                                 688 bytes
  SHA256SUM                                               1,980 bytes
  VERSION.txt                                                54 bytes
  aqarion_kernel.py                                      11,649 bytes
  main.py                                                 1,854 bytes
  requirements.txt                                           14 bytes
  test_aqarion.py                                         8,420 bytes
  verify_certificate.py                                   1,335 bytes
----------------------------------------------------------------------
  TOTAL                                                 124,216 bytes
======================================================================
