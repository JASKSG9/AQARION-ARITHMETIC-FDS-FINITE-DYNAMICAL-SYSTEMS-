CLAIMLOCK/
│
├── README.md
├── LICENSE
├── pyproject.toml
│
├── claimlock/
│   ├── claim.py
│   ├── state.py
│   ├── transition.py
│   ├── policy.py
│   ├── evidence.py
│   ├── provenance.py
│   ├── dependency.py
│   ├── replay.py
│   ├── receipt.py
│   ├── witness.py
│   ├── obligation.py
│   ├── cemetery.py
│   └── explain.py
│
├── schema/
│   ├── claim.schema.json
│   ├── evidence.schema.json
│   ├── receipt.schema.json
│   ├── transition.schema.json
│   └── policy.schema.json
│
├── policy/
│   ├── POLICY-001.yaml
│   └── TRANSITIONS-001.yaml
│
├── fixtures/
│   ├── refuted/
│   │   └── AQ-C3-O1/
│   ├── replay/
│   │   └── K2R-BETA4/
│   └── provenance/
│
├── examples/
│   ├── exact-refutation/
│   ├── computational-agreement/
│   ├── circular-provenance/
│   └── blocked-promotion/
│
├── tests/
│   ├── test_transition_legality.py
│   ├── test_circularity.py
│   ├── test_replay.py
│   └── test_policy.py
│
└── docs/
    ├── STATUS-MODEL.md
    ├── RECEIPT-SPEC.md
    ├── TRANSITION-SPEC.md
    └── FAILURE-MODES.md
