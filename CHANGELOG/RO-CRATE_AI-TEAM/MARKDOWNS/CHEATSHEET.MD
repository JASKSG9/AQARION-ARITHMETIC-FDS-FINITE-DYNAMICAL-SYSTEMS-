
# ============================================================
# 3. AQARION-CHEATSHEET.md — Developer Quick Reference
# ============================================================

cheatsheet = """# AQARION v0.4.1-final — Developer Cheatsheet

## One-Liners

```bash
# Run all tests
python -m unittest test_aqarion -v

# Generate certificate for a claim
python main.py generate AQ-CLAIM-001

# Verify a certificate independently
python verify_certificate.py AQ-CERT-AQ-CLAIM-001-001.json

# Show mathematical registry
python main.py registry

# Docker build and verify
docker build -t aqarion:0.4.1-final .
docker run aqarion:0.4.1-final
```

## Kernel API

### Exact Arithmetic
```python
from aqarion_kernel import ExactNumber
a = ExactNumber("1/3")
b = ExactNumber("2/3")
assert a + b == ExactNumber(1)
```

### FDDS (Finite Deterministic Dynamical System)
```python
from aqarion_kernel import FDDS
system = FDDS({0: 1, 1: 2, 2: 2})  # 0→1→2→2
transient, cycle = system.orbit(0)
# transient = [0, 1], cycle = [2]
```

### Kaprekar System
```python
from aqarion_kernel import kaprekar_system
k2 = kaprekar_system(digits=2, base=10)  # 100 states
k4 = kaprekar_system(digits=4, base=10)  # 10,000 states (v0.5.0)
```

### Observable Partition
```python
from aqarion_kernel import compute_observable_partition
partition = compute_observable_partition(system)
# Groups states by (distance_to_attractor, canonical_cycle)
```

### Defect Operator
```python
from aqarion_kernel import defect_operator, mat_is_zero
D = defect_operator(system, partition)
assert mat_is_zero(D)  # Partition is Koopman-invariant
```

### Sparse Check (O(|X|) vs O(|X|³))
```python
from aqarion_kernel import sparse_defect_check
assert sparse_defect_check(system, partition)  # Same result, faster
```

### Certificate Generation
```python
from aqarion_kernel import EvidenceObject
ev = EvidenceObject("AQ-CLAIM-001", system)
cert = ev.build()  # Returns dict
ev.save("cert.json")  # Writes file
```

### Independent Verification
```python
from aqarion_kernel import verify_certificate
report = verify_certificate(cert)
assert report["status"] == "VALID"
```

## Claim Registry

| Claim ID | Statement | Verification |
|----------|-----------|-------------|
| AQ-CLAIM-001 | Observable quotient partition satisfies (I-P)KP = 0 | Recompute partition + defect |
| AQ-CLAIM-002 | Cycle enumeration equals canonical periodic decomposition | Recompute cycles |
| AQ-CLAIM-003 | Image filtration stabilizes at |Per(f)| within |X| steps | Recompute filtration |
| AQ-CLAIM-004 | Transition hash matches system definition | Recompute hash |

## Certificate Schema v3.1

```json
{
  "aqarion_version": "0.4.1-final",
  "certificate_version": "3.1.0",
  "certificate": {
    "claim_id": "AQ-CLAIM-001",
    "claim_statement": "...",
    "status": "UNVERIFIED",
    "dependencies": {
      "registry_version": "0.4.1-final",
      "definitions": ["AQ-DEF-001", "AQ-DEF-007", "AQ-DEF-008"],
      "theorems": ["AQ-THM-003", "AQ-THM-004"]
    },
    "system": {"states": [...], "transition": {...}, "size": 100},
    "evidence": {"partition": [...], "defect_is_zero": false, "defect_norm_sq": "44/3"},
    "proof_obligation": {"method": "exact_fraction_arithmetic", "recomputable": true},
    "hash": {"algorithm": "SHA-256", "scope": "certificate", "value": "..."}
  },
  "audit": {"kernel_version": "0.4.1-final", "timestamp": "..."}
}
```

## Trust Model

| Layer | Component | Trust Basis |
|-------|-----------|-------------|
| 0 | Human statement | Mathematical rigor |
| 1 | Exact computation | Python Fractions (no float) |
| 2 | Independent reproduction | Docker, open source |
| 3 | Formal bridge | Future: Lean export |
| 4 | Community | Distributed verification |

## Versioning Rules

- Claim IDs never change meaning. New versions get new IDs.
- Registry version is frozen per release.
- Certificates are immutable once generated.
- Hash covers mathematical content only (not audit metadata).
"""

with open(os.path.join(output_dir, "AQARION-CHEATSHEET.md"), 'w') as f:
    f.write(cheatsheet)

print("✅ AQARION-CHEATSHEET.md")
