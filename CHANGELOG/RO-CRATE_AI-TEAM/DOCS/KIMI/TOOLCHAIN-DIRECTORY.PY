
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
