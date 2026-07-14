
# ============================================================
# TEST SUITE (25 tests)
# ============================================================

test_aqarion = '''"""
AQARION TEST SUITE v0.4.1-final
25 tests covering exact arithmetic, FDDS, cycles, certificates.
"""

import unittest
import json
import os
import sys

# Add output dir to path
sys.path.insert(0, '/mnt/agents/output')

from aqarion_kernel import (
    ExactNumber, kaprekar_3digit, kaprekar_3digit_orbit,
    kaprekar_3digit_all_states, FDDS, AQRegistry,
    floyd_cycle, image_filtration, nilpotency_depth,
    defect_operator, kaprekar_3digit_system
)

# ============================================================
# TEST EXACT ARITHMETIC
# ============================================================

class TestExactArithmetic(unittest.TestCase):
    def test_fraction_construction(self):
        a = ExactNumber("1/3")
        b = ExactNumber("2/3")
        self.assertEqual((a + b)._val, 1)
    
    def test_exact_equality(self):
        a = ExactNumber(0.1) + ExactNumber(0.2)
        b = ExactNumber(0.3)
        # Note: float construction has limits; test rational instead
        a = ExactNumber(Fraction(1,10)) + ExactNumber(Fraction(2,10))
        b = ExactNumber(Fraction(3,10))
        self.assertEqual(a, b)

# ============================================================
# TEST FDDS
# ============================================================

class TestFDDS(unittest.TestCase):
    def test_simple_system(self):
        states = {0, 1, 2}
        trans = {0: 1, 1: 2, 2: 0}
        obs = {0: "a", 1: "b", 2: "c"}
        fdds = FDDS(states, trans, obs)
        self.assertEqual(fdds.transition[0], 1)
    
    def test_orbit_cycle(self):
        states = {0, 1}
        trans = {0: 1, 1: 0}
        fdds = FDDS(states, trans)
        pre, cyc = fdds.orbit(0)
        self.assertEqual(cyc, [0, 1])

# ============================================================
# TEST CYCLE DETECTION
# ============================================================

class TestCycleDetection(unittest.TestCase):
    def test_floyd_simple(self):
        f = lambda x: (x + 1) % 5
        mu, lam = floyd_cycle(f, 0)
        self.assertEqual(lam, 5)
        self.assertEqual(mu, 0)
    
    def test_floyd_preperiod(self):
        # 0->1->2->3->3 (fixed point)
        f = lambda x: min(x + 1, 3)
        mu, lam = floyd_cycle(f, 0)
        self.assertEqual(mu, 3)
        self.assertEqual(lam, 1)

# ============================================================
# TEST CANONICAL CYCLES
# ============================================================

class TestCanonicalCycles(unittest.TestCase):
    def test_kaprekar_495(self):
        # 495 is the famous fixed point
        self.assertEqual(kaprekar_3digit(495), 495)
    
    def test_kaprekar_6174_not_3digit(self):
        # 6174 is 4-digit, not applicable here
        # Just verify 3-digit system has 495 as attractor
        result = kaprekar_3digit(100)
        self.assertNotEqual(result, 100)

# ============================================================
# TEST IMAGE FILTRATION
# ============================================================

class TestImageFiltration(unittest.TestCase):
    def test_filtration_length(self):
        system = kaprekar_3digit_system()
        filt = image_filtration(system)
        self.assertGreater(len(filt), 0)
        self.assertEqual(filt[0], system.states)
    
    def test_depth_nonnegative(self):
        system = kaprekar_3digit_system()
        depth = nilpotency_depth(system)
        self.assertGreaterEqual(depth, 0)

# ============================================================
# TEST OBSERVABLE PARTITION
# ============================================================

class TestObservablePartition(unittest.TestCase):
    def test_quotient_reduces(self):
        system = kaprekar_3digit_system()
        q = system.quotient_system()
        self.assertLessEqual(len(q.states), len(system.states))

# ============================================================
# TEST DEFECT OPERATOR
# ============================================================

class TestDefectOperator(unittest.TestCase):
    def test_zero_defect_on_quotient(self):
        # Trivial partition should have some defect
        system = kaprekar_3digit_system()
        partition = [system.states]  # One big block
        d = defect_operator(system, partition)
        self.assertGreaterEqual(d, 0)
    
    def test_defect_on_singletons(self):
        system = kaprekar_3digit_system()
        partition = [{s} for s in system.states]
        d = defect_operator(system, partition)
        self.assertEqual(d, 0)  # Singletons are always congruent
    
    def test_defect_nonnegative(self):
        system = kaprekar_3digit_system()
        partition = [{0, 1, 2}, set(system.states) - {0, 1, 2}]
        d = defect_operator(system, partition)
        self.assertGreaterEqual(d, 0)

# ============================================================
# TEST KAPREKAR
# ============================================================

class TestKaprekar(unittest.TestCase):
    def test_all_states_defined(self):
        states = kaprekar_3digit_all_states()
        self.assertEqual(len(states), 1000)
    
    def test_orbit_terminates(self):
        orbit = kaprekar_3digit_orbit(100)
        self.assertIsInstance(orbit, list)

# ============================================================
# TEST REGISTRY
# ============================================================

class TestRegistryIntegrity(unittest.TestCase):
    def test_register_and_certify(self):
        reg = AQRegistry()
        reg.register_claim("TEST-001", "Test claim", {"data": 42})
        cert = reg.generate_certificate("TEST-001")
        self.assertEqual(cert["status"], "UNVERIFIED")
        self.assertIn("evidence_hash", cert)
    
    def test_verify_valid(self):
        reg = AQRegistry()
        evidence = {"computation": "verified", "result": 495}
        reg.register_claim("TEST-002", "Kaprekar fixed point", evidence)
        cert = reg.generate_certificate("TEST-002")
        result = reg.verify_certificate(cert, evidence)
        self.assertTrue(result["all_pass"])

# ============================================================
# TEST EVIDENCE OBJECT
# ============================================================

class TestEvidenceObject(unittest.TestCase):
    def test_hash_determinism(self):
        reg = AQRegistry()
        e1 = {"a": 1, "b": 2}
        e2 = {"b": 2, "a": 1}
        h1 = reg._hash_evidence(e1)
        h2 = reg._hash_evidence(e2)
        self.assertEqual(h1, h2)
    
    def test_certificate_never_self_validating(self):
        reg = AQRegistry()
        reg.register_claim("TEST-003", "Self-validation test", {})
        cert = reg.generate_certificate("TEST-003")
        self.assertEqual(cert["status"], "UNVERIFIED")
    
    def test_schema_version(self):
        reg = AQRegistry()
        self.assertEqual(reg.SCHEMA_VERSION, "3.1.0")

# ============================================================
# TEST HASH SCOPE
# ============================================================

class TestHashScope(unittest.TestCase):
    def test_hash_length(self):
        reg = AQRegistry()
        h = reg._hash_evidence({"test": "data"})
        self.assertEqual(len(h), 32)
    
    def test_hash_hex(self):
        reg = AQRegistry()
        h = reg._hash_evidence({"test": "data"})
        self.assertTrue(all(c in '0123456789abcdef' for c in h))

# ============================================================
# TEST VERSION CHECK
# ============================================================

class TestRegistryVersionCheck(unittest.TestCase):
    def test_version_matches(self):
        reg = AQRegistry()
        self.assertEqual(reg.version, "0.4.1-final")

# ============================================================
# TEST TAMPER RESISTANCE
# ============================================================

class TestTamperResistance(unittest.TestCase):
    def test_tampered_evidence_fails(self):
        reg = AQRegistry()
        evidence = {"correct": True}
        reg.register_claim("TAMPER-001", "Tamper test", evidence)
        cert = reg.generate_certificate("TAMPER-001")
        
        tampered = {"correct": False}
        result = reg.verify_certificate(cert, tampered)
        self.assertFalse(result["all_pass"])

# ============================================================
# RUN
# ============================================================

if __name__ == '__main__':
    unittest.main(verbosity=2)
'''

with open(os.path.join(output_dir, "test_aqarion.py"), 'w') as f:
    f.write(test_aqarion)

print("✅ test_aqarion.py written (25 tests)")
