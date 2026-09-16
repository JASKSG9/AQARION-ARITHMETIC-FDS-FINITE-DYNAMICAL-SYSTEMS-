AQARION-LUMEN/
│
├── README.md
│
├── DOCS/
│   ├── AQ-LUMEN-SPECTRAL-COLLISION-ATLAS.md
│   ├── AQ-LUMEN-DEFINITIONS.md
│   ├── AQ-LUMEN-EXACTNESS-BOUNDARY.md
│   ├── AQ-LUMEN-HOMOMETRY.md
│   ├── AQ-LUMEN-SEARCH-LEDGER.md
│   └── AQ-LUMEN-LITERATURE.md
│
├── DEFINITIONS/
│   ├── boundary_convention.md
│   ├── tangent_jump_definition.md
│   ├── autocorrelation_definition.md
│   └── fourier_convention.md
│
├── FIXTURES/
│   ├── collision_n25.json
│   ├── lambda_3^6_2_1^5.json
│   ├── mu_4_3_2^9.json
│   └── noncollision_controls.json
│
├── SRC/
│   ├── ferrers_boundary.py
│   ├── tangent_jumps.py
│   ├── autocorrelation_exact.py
│   ├── fourier_exact.py
│   ├── verify_collision.py
│   └── scan_homometric_rims.py
│
├── CERTIFICATES/
│   └── AQ-LUMEN-COLLISION-EXACT-001/
│       ├── statement.json
│       ├── tangent_lambda.json
│       ├── tangent_mu.json
│       ├── autocorrelation.json
│       ├── equality.json
│       └── SHA256SUMS
│
├── RECEIPTS/
│   ├── AQ-LUMEN-COLLISION-EXACT-001.json
│   ├── AQ-LUMEN-COLLISION-EXACT-001.txt
│   └── AQ-LUMEN-SCAN-001.json
│
└── LEAN/
    ├── AQ_LUMEN_Boundary.lean
    ├── AQ_LUMEN_TangentJump.lean
    ├── AQ_LUMEN_Autocorrelation.lean
    └── AQ_LUMEN_Collision.lean
