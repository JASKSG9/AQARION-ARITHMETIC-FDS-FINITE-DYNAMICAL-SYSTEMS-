aqarion-replay-lab/
├── README.md
├── LICENSE
├── SECURITY.md
├── GOVERNANCE.md
├── schemas/
│   ├── claim-contract.v0.1.schema.json
│   ├── receipt.v0.1.schema.json
│   ├── regression.v0.1.schema.json
│   ├── replay-diff.v0.1.schema.json
│   └── mutation-result.v0.1.schema.json
├── policy/
│   ├── semantic-firewall.v0.1.json
│   └── verdict-policy.v0.1.json
├── fixtures/
│   ├── spectral-defect/
│   │   ├── contract.json
│   │   ├── fixture-grid.json
│   │   ├── verifier.js
│   │   └── expected-controls.json
│   ├── semantic-drift/
│   │   ├── SDS-R005.json
│   │   ├── SDS-R009.json
│   │   ├── SDS-R013.json
│   │   └── CP-009.json
│   └── toy-even/
│       ├── contract.json
│       └── verify.py
├── engine/
│   ├── validateContract.ts
│   ├── evaluatePolicy.ts
│   ├── createReceipt.ts
│   ├── replayDiff.ts
│   ├── mutationCompiler.ts
│   └── canonicalize.dev.ts
├── web/
│   ├── index.html
│   ├── app.js
│   ├── styles.css
│   └── demos/
│       ├── spectral-defect.html
│       ├── regression-museum.html
│       └── toy-replay.html
├── tests/
│   ├── policy/
│   ├── contracts/
│   ├── mutations/
│   └── fixtures/
└── receipts/
    └── .gitkeep
