QUICKSTART-AQARION-RIP/
├── DOCS
│ └── MARKDOWNS
│ └── AQ-S16-SKILL.md
├── ENGINES
│ ├── AQ-S16-SAT-001.py ← exact Q-rank saturation (n=1..5, 0 mismatches)
│ ├── AQ-S9-SOURCE-DRIFT-DEMO.py ← S9 drift residual rJU - rJT
│ ├── AQ-S9-SOURCE-DRIFT.yml
│ ├── Circulant_intertwiner.py ← += fix for m=2
│ ├── domain-firewall.py ← L2 vs K2 exact charpoly
│ ├── forest-acrylic.py ← typo kept from screenshot + fixed copy below
│ └── forest-acyclic.py ← DSU exact
├── SCHEMAS
│ └── RECEIPTS
│ ├── AQ-RPL-001.json ← RPL-001 fixed: direct returncode, FAILED⇒RECEIPT
│ └── AQ-S16-V001.json ← saturation V001 PASS 6/21/55/120/231
├── SCRIPTS
│ ├── JSON
│ │ └── AQ-S9-MANIFEST.json ← variable=rJU
│ ├── LEAN
│ │ └── SaturationRank.lean ← OPEN sketch
│ ├── PYTHON
│ │ ├── AQ-REPLAY.py ← aqreplay CLI (init/capture/verify/closure/diff)
│ │ ├── AQ-S16-CAPTURE.py ← capture.py RPL-001 fixed
│ │ ├── AQ-S9-DRIFT.py
│ │ ├── AQ-S9-SOURCE-CLEAN.py ← variable="rJU"
│ │ └── AQ-S9-SOURCE-DRIFT.py ← variable="rJT"
│ ├── YAML
│ │ └── AQ-S16-SAT-001.yml ← claim λ_max=1⇔rank<3
│ └── CAPTURE-RUN.sh ← FIXED: PIPESTATUS[0] + set +e/-e
├── TESTS
│ └── AQ-RP-1001.py ← test_success + test_failure still writes receipt
├── init-aqarion-replay-lab-20260915.sh
└── README.md
