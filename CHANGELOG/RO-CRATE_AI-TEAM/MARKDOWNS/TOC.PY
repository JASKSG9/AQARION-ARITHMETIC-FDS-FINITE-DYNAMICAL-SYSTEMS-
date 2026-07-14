
import os, json, hashlib, subprocess, sys

output_dir = "/mnt/agents/output"
os.makedirs(output_dir, exist_ok=True)

# ============================================================
# 1. TABLE OF CONTENTS (TOC)
# ============================================================

toc = """# AQARION v0.4.1-FINAL — Table of Contents

**Frozen Release:** July 13, 2026  
**Status:** REFERENCE ARTIFACT READY  
**Schema:** 3.1.0  
**Kernel:** 0.4.1-final

---

## Source Files

| File | Purpose | Lines | Tests |
|------|---------|-------|-------|
| `aqarion_kernel.py` | Core kernel: exact arithmetic, FDDS, Kaprekar, registry, certificates | ~500 | 13 |
| `verify_certificate.py` | Independent verifier: dependency-aware, claimed/recomputed separation | ~80 | 4 |
| `main.py` | CLI: generate, verify, test, registry commands | ~120 | 0 |
| `test_aqarion.py` | Unit test suite: 25 tests, 13 classes | ~300 | 25 |
| `Dockerfile` | Container build: Python 3.11-slim | ~10 | 0 |
| `requirements.txt` | Dependencies: none (stdlib only) | ~3 | 0 |
| `README.md` | Quick start guide | ~40 | 0 |

## Certificates (Status: UNVERIFIED)

| Certificate | Claim | Evidence | Hash |
|-------------|-------|----------|------|
| `AQ-CERT-AQ-CLAIM-001-001.json` | Observable quotient partition satisfies (I-P)KP = 0 | Partition, defect zero check | SHA-256 |
| `AQ-CERT-AQ-CLAIM-002-001.json` | Cycle enumeration equals canonical periodic decomposition | Cycles, canonical labels | SHA-256 |
| `AQ-CERT-AQ-CLAIM-003-001.json` | Image filtration stabilizes at |Per(f)| within |X| steps | Filtration sequence, depth | SHA-256 |
| `AQ-CERT-AQ-CLAIM-004-001.json` | Transition hash matches system definition | Hash recomputation | SHA-256 |

## Reference Artifacts

| File | Purpose |
|------|---------|
| `registry_snapshot.json` | Frozen claim registry state |
| `system_definition.json` | 3-digit Kaprekar system specification |
| `VERIFY_OUTPUT.txt` | Verification run log |
| `VERSION.txt` | Version stamp |
| `SHA256SUM` | Cryptographic manifest |

## Documentation

| File | Audience | Purpose |
|------|----------|---------|
| `AQARION-ABSTRACT.txt` | All | Identity document: what AQARION is |
| `AQARION-CHEATSHEET.md` | Developers | Quick reference for all APIs |
| `AQARION-QA.md` | Users | Frequently asked questions |
| `AQARION-OVERVIEW.md` | Reviewers | Architecture and design philosophy |
| `AQARION-ASCII-ATLAS.txt` | Visual learners | ASCII art system diagrams |
| `AQARION-MERMAID.md` | Diagram users | Mermaid flowcharts |
| `AQARION-DEMO.md` | New users | Walkthrough with toy models |
| `AQARION-TOY-MODELS.py` | Learners | Self-contained educational examples |
| `AQARION-FLOW.md` | Contributors | Development and release workflow |
| `AQARION-AUDIT.md` | Auditors | Complete audit trail |

## External Links

- GitHub: `https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-`
- HuggingFace: `https://huggingface.co/Quantarion9`
- Replit: `https://aqarion-kernel--jamesaqarion.replit.app/`

---

**Navigation:** Start with `AQARION-ABSTRACT.txt` → `AQARION-DEMO.md` → `AQARION-CHEATSHEET.md`
"""

with open(os.path.join(output_dir, "AQARION-TOC.md"), 'w') as f:
    f.write(toc)

print("✅ AQARION-TOC.md")
