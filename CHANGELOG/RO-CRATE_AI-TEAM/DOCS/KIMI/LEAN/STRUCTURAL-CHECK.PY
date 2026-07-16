
# Check actual structure
with open(ROOT / "claims" / "AQ-THM-001.json", "r") as f:
    thm = json.load(f)
print("AQ-THM-001 keys:", list(thm.keys()))
print("metadata keys:", list(thm['metadata'].keys()))
print("lean_status:", thm['metadata'].get('lean_status', 'NOT FOUND'))

with open(ROOT / "certificates" / "CERT-AQ001-001.json", "r") as f:
    cert = json.load(f)
print("\nCERT keys:", list(cert.keys()))
print("metadata keys:", list(cert['metadata'].keys()))
print("results:", cert['metadata'].get('results', 'NOT FOUND'))AQ-THM-001 keys: ['certificate_id', 'created_at', 'dependencies', 'evidence_ids', 'metadata', 'object_id', 'object_type', 'specification_id', 'status', 'verification_method_ids', 'version']
metadata keys: ['description', 'lean_status', 'mathematical_statement', 'maturity', 'title']
lean_status: {'formalization_file': 'lean/Aqarion/FDDS.lean', 'mathlib_dependencies': ['Mathlib.LinearAlgebra.FiniteDimensional', 'Mathlib.LinearAlgebra.Matrix', 'Mathlib.Algebra.Module.Submodule', 'Mathlib.Data.Finset.Basic'], 'proof_completed': '2026-07-16', 'proof_obligations_remaining': 0, 'target_theorem': 'defect_vanishing_criterion', 'verification_method': 'symbolic_proof_in_lean4'}

CERT keys: ['created_at', 'dependencies', 'metadata', 'object_id', 'object_type', 'status', 'version']
metadata keys: ['artifact_hash', 'claim_id', 'description', 'evidence_ids', 'maturity', 'results', 'specification_id', 'title', 'verification_method_ids']
results: {'dependency_check': 'PASS', 'lean_proof': 'PASS', 'lean_proof_obligations': '0 remaining', 'lean_specification': 'PASS', 'schema_check': 'PASS', 'verification': 'PASS'}
