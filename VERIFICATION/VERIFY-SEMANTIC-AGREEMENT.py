# verify_semantic_agreement.py
import subprocess, json, hashlib

def canonical_hash(output_json_path):
    with open(output_json_path, 'r', encoding='utf-8') as f:
        raw = f.read()
    # Enforce LF and no trailing whitespace
    normalized = raw.replace('\r\n', '\n').strip() + '\n'
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

# 1. Run Python certification
subprocess.run(["python", "-m", "certification.run", "--output", "cert_py.json"])
py_hash = canonical_hash("cert_py.json")

# 2. Run Lean certification (via `lake exec` or `lean --run`)
subprocess.run(["lake", "exec", "aqarion-cert", "--", "--output", "cert_lean.json"])
lean_hash = canonical_hash("cert_lean.json")

# 3. Compare and Assert
assert py_hash == lean_hash, f"Kernel disagreement! Py: {py_hash}, Lean: {lean_hash}"
print("✅ V21-001/008 PASS: Cross-kernel semantic agreement.")
