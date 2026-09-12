CLAIMLOCK/
│
├── README.md
├── LICENSE
├── pyproject.toml
│
├── claimlock/
│   ├── scan.py
│   ├── replay.py
│   ├── provenance.py
│   ├── semantic.py
│   ├── dependency.py
│   ├── promotion.py
│   ├── explain.py
│   ├── policy.py          # NEW
│   ├── admissibility.py   # NEW
│   └── receipts.py        # NEW
│
├── schema/
│   ├── claim.schema.json
│   ├── evidence.schema.json
│   ├── receipt.schema.json
│   └── policy.schema.json # NEW
│
├── reason-codes/
│   └── codes.yaml
│
├── policies/
│   ├── research.yaml
│   ├── software.yaml
│   └── agent.yaml
│
├── verifiers/
│   ├── python_replay/
│   ├── matrix_dual_route/
│   ├── hash/
│   └── lean/
│
├── fixtures/
│   ├── aqarion-k2r-beta4/
│   ├── circular-proof/
│   ├── self-certified-json/
│   ├── stale-hash/
│   ├── wrong-scope-replay/      
│   ├── verifier-self-certifies/ 
│   └── dependency-cycle/        
│
├── benchmark/
│   └── ClaimLock-100/
│
└── docs/
    ├── THREAT_MODEL.md
    ├── TRUST_MODEL.md
    ├── CLAIM_LIFECYCLE.md
    ├── PROMOTION_SPEC.md        
    └── ADVERSARIAL_CASES.md     
