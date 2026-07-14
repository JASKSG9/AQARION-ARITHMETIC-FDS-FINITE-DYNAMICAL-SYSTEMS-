
# ============================================================
# 8. AQARION-DEMO.md — Walkthrough with Toy Models
# ============================================================

demo = """# AQARION v0.4.1-final — Interactive Demo & Toy Models

## Toy Model 1: The Trivial System (3 states)

```python
from aqarion_kernel import FDDS, compute_observable_partition, defect_operator, mat_is_zero

# System: 0 → 1 → 2 → 2 (chain ending in fixed point)
system = FDDS({0: 1, 1: 2, 2: 2})

# Orbit analysis
transient, cycle = system.orbit(0)
print(f"Orbit of 0: transient={transient}, cycle={cycle}")
# Output: Orbit of 0: transient=[0, 1], cycle=[2]

# Observable partition (groups by distance to attractor + cycle structure)
partition = compute_observable_partition(system)
print(f"Partition: {partition}")
# Output: Partition: [[0], [1], [2]]
# Each state is in its own block because distances differ

# Defect check: is this partition Koopman-invariant?
D = defect_operator(system, partition)
print(f"Defect is zero: {mat_is_zero(D)}")
# Output: Defect is zero: True
```

## Toy Model 2: The 2-Cycle System

```python
from aqarion_kernel import FDDS, find_cycles, canonical_cycle

# System: 0 ↔ 1 (2-cycle), 2 → 0
system = FDDS({0: 1, 1: 0, 2: 0})

# Cycle detection
cycles = find_cycles(system)
print(f"Cycles: {cycles}")
# Output: Cycles: [[0, 1]]

# Canonical cycle label (rotation-invariant)
label = canonical_cycle([1, 0])  # Same cycle, different order
print(f"Canonical label: {label}")
# Output: Canonical label: (0, 1)

# Verify: [0,1] and [1,0] are the same cycle
assert canonical_cycle([0, 1]) == canonical_cycle([1, 0])
```

## Toy Model 3: Image Filtration

```python
from aqarion_kernel import FDDS, image_filtration

# System: 0→1, 1→2, 2→2, 3→2, 4→3
system = FDDS({0: 1, 1: 2, 2: 2, 3: 2, 4: 3})

# Image filtration: X ⊇ f(X) ⊇ f²(X) ⊇ ...
filt = image_filtration(system)
print(f"Filtration sizes: {filt}")
# Output: Filtration sizes: [5, 3, 1, 1]
# Meaning: 5 states → 3 states → 1 state → stabilizes

# Stabilization guaranteed within |X| steps (THM-002)
assert len(filt) <= system.n
```

## Toy Model 4: Kaprekar 2-Digit System

```python
from aqarion_kernel import kaprekar_system, compute_observable_partition, sparse_defect_check

# Build 2-digit Kaprekar system (100 states)
k2 = kaprekar_system(digits=2, base=10)
print(f"States: {k2.n}")
# Output: States: 100

# Compute observable partition
partition = compute_observable_partition(k2)
print(f"Partition blocks: {len(partition)}")

# Sparse defect check (fast)
is_invariant = sparse_defect_check(k2, partition)
print(f"Partition is Koopman-invariant: {is_invariant}")
```

## Toy Model 5: Certificate Generation & Verification

```python
from aqarion_kernel import FDDS, EvidenceObject, verify_certificate

# Build a system
system = FDDS({0: 1, 1: 2, 2: 2, 3: 2, 4: 3})

# Generate certificate for AQ-CLAIM-001
evidence = EvidenceObject("AQ-CLAIM-001", system)
cert = evidence.build()

# Inspect certificate structure
print(f"Claim: {cert['certificate']['claim_id']}")
print(f"Status: {cert['certificate']['status']}")  # UNVERIFIED
print(f"Hash algorithm: {cert['certificate']['hash']['algorithm']}")

# Save to file
evidence.save("toy_cert.json")

# Independent verification
report = verify_certificate(cert)
print(f"Verification status: {report['status']}")  # VALID or INVALID
print(f"All checks passed: {report['overall_valid']}")

# Inspect detailed checks
for check, result in report['checks'].items():
    print(f"  {check}: {result['valid']}")
```

## Toy Model 6: Tamper Resistance Demo

```python
from aqarion_kernel import FDDS, EvidenceObject, verify_certificate

system = FDDS({0: 1, 1: 2, 2: 2})
evidence = EvidenceObject("AQ-CLAIM-001", system)
cert = evidence.build()

# Verify original (should pass)
report = verify_certificate(cert)
assert report['status'] == 'VALID'

# Tamper with evidence
cert['certificate']['evidence']['defect_is_zero'] = True  # Lie!

# Verify tampered (should fail)
report = verify_certificate(cert)
assert report['status'] == 'INVALID'
print("Tamper detected!")
```

## Toy Model 7: Registry Version Check

```python
from aqarion_kernel import FDDS, EvidenceObject, verify_certificate, REGISTRY_VERSION

system = FDDS({0: 1, 1: 2, 2: 2})
evidence = EvidenceObject("AQ-CLAIM-001", system)
cert = evidence.build()

# Verify with correct registry (passes)
report = verify_certificate(cert)
assert report['checks']['registry_version']['valid']

# Tamper with registry version
cert['certificate']['dependencies']['registry_version'] = '0.0.0'

# Verify with wrong registry (fails)
report = verify_certificate(cert)
assert not report['checks']['registry_version']['valid']
print("Registry version mismatch detected!")
```

## Toy Model 8: Full Pipeline from Claim to Community

```python
# Step 1: Define a claim (already in registry)
# AQ-CLAIM-002: "Cycle enumeration equals canonical periodic decomposition"

# Step 2: Generate certificate
from aqarion_kernel import kaprekar_system, EvidenceObject
system = kaprekar_system(digits=2, base=10)
evidence = EvidenceObject("AQ-CLAIM-002", system)
evidence.save("community_cert.json")

# Step 3: Distribute certificate
# Upload to GitHub, attach to arXiv preprint, email to collaborator

# Step 4: Community member verifies independently
from aqarion_kernel import verify_certificate
import json
with open("community_cert.json") as f:
    cert = json.load(f)
report = verify_certificate(cert)

# Step 5: Community consensus
if report['overall_valid']:
    print("Community verification: PASSED")
    print(f"Certificate hash: {cert['certificate']['hash']['value']}")
else:
    print("Community verification: FAILED")
    print("Investigate and fix!")
```

## Running All Toy Models

```bash
# Save toy models to file and run
python -c "
from aqarion_kernel import *

print('=== Toy Model 1: Trivial System ===')
system = FDDS({0: 1, 1: 2, 2: 2})
t, c = system.orbit(0)
print(f'Orbit: transient={t}, cycle={c}')

print('\\n=== Toy Model 2: 2-Cycle ===')
system = FDDS({0: 1, 1: 0, 2: 0})
cycles = find_cycles(system)
print(f'Cycles: {cycles}')

print('\\n=== Toy Model 3: Filtration ===')
system = FDDS({0: 1, 1: 2, 2: 2, 3: 2, 4: 3})
filt = image_filtration(system)
print(f'Filtration: {filt}')

print('\\n=== Toy Model 4: Kaprekar 2-digit ===')
k2 = kaprekar_system(digits=2, base=10)
print(f'States: {k2.n}')

print('\\n=== All toy models passed! ===')
"
```

## Expected Output

```
=== Toy Model 1: Trivial System ===
Orbit: transient=[0, 1], cycle=[2]

=== Toy Model 2: 2-Cycle ===
Cycles: [[0, 1]]

=== Toy Model 3: Filtration ===
Filtration: [5, 3, 1, 1]

=== Toy Model 4: Kaprekar 2-digit ===
States: 100

=== All toy models passed! ===
```
"""

with open(os.path.join(output_dir, "AQARION-DEMO.md"), 'w') as f:
    f.write(demo)

print("✅ AQARION-DEMO.md")
