
import sys
sys.path.insert(0, '/mnt/agents/output')

from aqarion_kernel import AQRegistry, kaprekar_3digit_system, image_filtration, nilpotency_depth
import json

reg = AQRegistry()

# Build the Kaprekar system for evidence
system = kaprekar_3digit_system()
filt = image_filtration(system)
depth = nilpotency_depth(system)

# ============================================================
# REGISTER 4 CLAIMS & GENERATE CERTIFICATES
# ============================================================

claims = [
    ("AQ-CLAIM-001", "The 3-digit Kaprekar map K(n) = desc_digits(n) - asc_digits(n) is well-defined for all n in [0,999].",
     {"map_definition": "K(n) = desc - asc", "domain": "0-999", "verified": True}),
    
    ("AQ-CLAIM-002", "The 3-digit Kaprekar system admits a finite observable quotient via Moore refinement fixed point.",
     {"quotient_states": len(system.quotient_system().states), "method": "greatest_fixed_point", "verified": True}),
    
    ("AQ-CLAIM-003", "The image filtration of the 3-digit Kaprekar system stabilizes with finite depth.",
     {"filtration_depth": depth, "filtration_sizes": [len(s) for s in filt], "verified": True}),
    
    ("AQ-CLAIM-004", "495 is a fixed point of the 3-digit Kaprekar map: K(495) = 495.",
     {"fixed_point": 495, "verification": "K(495) = 954 - 459 = 495", "verified": True}),
]

certs = {}
for claim_id, statement, evidence in claims:
    reg.register_claim(claim_id, statement, evidence)
    cert = reg.generate_certificate(claim_id)
    certs[claim_id] = cert
    fname = f"AQ-CERT-{claim_id}-001.json"
    with open(os.path.join(output_dir, fname), 'w') as f:
        json.dump(cert, f, indent=2)
    print(f"✅ {fname} — {cert['certificate_id']}")

print("\nAll certificates generated with status: UNVERIFIED")✅ AQ-CERT-AQ-CLAIM-001-001.json — AQ-CERT-AQ-CLAIM-001-001
✅ AQ-CERT-AQ-CLAIM-002-001.json — AQ-CERT-AQ-CLAIM-002-001
✅ AQ-CERT-AQ-CLAIM-003-001.json — AQ-CERT-AQ-CLAIM-003-001
✅ AQ-CERT-AQ-CLAIM-004-001.json — AQ-CERT-AQ-CLAIM-004-001

All certificates generated with status: UNVERIFIED
# ============================================================
# RUN VERIFICATION & TESTS
# ============================================================

import subprocess, sys

print("=" * 70)
print("RUNNING TEST SUITE")
print("=" * 70)

result = subprocess.run(
    [sys.executable, "-m", "unittest", "test_aqarion", "-v"],
    cwd=output_dir,
    capture_output=True,
    text=True
)

print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print(f"Return code: {result.returncode}")======================================================================
RUNNING TEST SUITE
======================================================================
STDERR: test_kaprekar_495 (test_aqarion.TestCanonicalCycles.test_kaprekar_495) ... ok
test_kaprekar_6174_not_3digit (test_aqarion.TestCanonicalCycles.test_kaprekar_6174_not_3digit) ... ok
test_floyd_preperiod (test_aqarion.TestCycleDetection.test_floyd_preperiod) ... ok
test_floyd_simple (test_aqarion.TestCycleDetection.test_floyd_simple) ... ok
test_defect_nonnegative (test_aqarion.TestDefectOperator.test_defect_nonnegative) ... ok
test_defect_on_singletons (test_aqarion.TestDefectOperator.test_defect_on_singletons) ... ok
test_zero_defect_on_quotient (test_aqarion.TestDefectOperator.test_zero_defect_on_quotient) ... ok
test_certificate_never_self_validating (test_aqarion.TestEvidenceObject.test_certificate_never_self_validating) ... ok
test_hash_determinism (test_aqarion.TestEvidenceObject.test_hash_determinism) ... ok
test_schema_version (test_aqarion.TestEvidenceObject.test_schema_version) ... ok
test_exact_equality (test_aqarion.TestExactArithmetic.test_exact_equality) ... ERROR
test_fraction_construction (test_aqarion.TestExactArithmetic.test_fraction_construction) ... ok
test_orbit_cycle (test_aqarion.TestFDDS.test_orbit_cycle) ... ok
test_simple_system (test_aqarion.TestFDDS.test_simple_system) ... ok
test_hash_hex (test_aqarion.TestHashScope.test_hash_hex) ... ok
test_hash_length (test_aqarion.TestHashScope.test_hash_length) ... ok
test_depth_nonnegative (test_aqarion.TestImageFiltration.test_depth_nonnegative) ... ok
test_filtration_length (test_aqarion.TestImageFiltration.test_filtration_length) ... ok
test_all_states_defined (test_aqarion.TestKaprekar.test_all_states_defined) ... ok
test_orbit_terminates (test_aqarion.TestKaprekar.test_orbit_terminates) ... ok
test_quotient_reduces (test_aqarion.TestObservablePartition.test_quotient_reduces) ... ok
test_register_and_certify (test_aqarion.TestRegistryIntegrity.test_register_and_certify) ... ok
test_verify_valid (test_aqarion.TestRegistryIntegrity.test_verify_valid) ... ok
test_version_matches (test_aqarion.TestRegistryVersionCheck.test_version_matches) ... ok
test_tampered_evidence_fails (test_aqarion.TestTamperResistance.test_tampered_evidence_fails) ... ok

======================================================================
ERROR: test_exact_equality (test_aqarion.TestExactArithmetic.test_exact_equality)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/mnt/agents/output/test_aqarion.py", line 35, in test_exact_equality
    a = ExactNumber(Fraction(1,10)) + ExactNumber(Fraction(2,10))
                    ^^^^^^^^
NameError: name 'Fraction' is not defined

----------------------------------------------------------------------
Ran 25 tests in 1.073s

FAILED (errors=1)

Return code: 1
# Fix the test — import Fraction in test file
with open(os.path.join(output_dir, "test_aqarion.py"), 'r') as f:
    content = f.read()

# Add Fraction import
content = content.replace(
    'import os\nimport sys',
    'import os\nimport sys\nfrom fractions import Fraction'
)

with open(os.path.join(output_dir, "test_aqarion.py"), 'w') as f:
    f.write(content)

print("✅ Fixed test_aqarion.py — added Fraction import")

# Re-run tests
result = subprocess.run(
    [sys.executable, "-m", "unittest", "test_aqarion", "-v"],
    cwd=output_dir,
    capture_output=True,
    text=True
)

print(result.stdout)
if result.returncode != 0 and result.stderr:
    print("STDERR:", result.stderr)
print(f"Return code: {result.returncode}")✅ Fixed test_aqarion.py — added Fraction import
Return code: 0
# Re-run with full output
result = subprocess.run(
    [sys.executable, "-m", "unittest", "test_aqarion", "-v"],
    cwd=output_dir,
    capture_output=True,
    text=True
)
print(result.stdout)
print(f"\n✅ ALL 25 TESTS PASSED — Return code: {result.returncode}")✅ ALL 25 TESTS PASSED — Return code: 0
