
# ============================================================
# 9. AQARION-TOY-MODELS.py — Self-Contained Educational Examples
# ============================================================

toy_models = '''#!/usr/bin/env python3
"""
AQARION v0.4.1-final — Toy Models
Self-contained educational examples. No dependencies beyond stdlib.
Run: python AQARION-TOY-MODELS.py
"""

from fractions import Fraction
import json

# ============================================================
# TOY MODEL 1: The Trivial System
# ============================================================

def toy_trivial_system():
    print("=" * 60)
    print("TOY MODEL 1: Trivial System (0→1→2→2)")
    print("=" * 60)
    
    system = {0: 1, 1: 2, 2: 2}
    
    # Orbit
    def orbit(x):
        seen = {}
        path = []
        current = x
        while current not in seen:
            seen[current] = len(path)
            path.append(current)
            current = system[current]
        return path[:seen[current]], path[seen[current]:]
    
    t, c = orbit(0)
    print(f"Orbit of 0: transient={t}, cycle={c}")
    
    # Image filtration
    current = set(system.keys())
    filt = []
    while True:
        filt.append(len(current))
        if not current:
            break
        nxt = {system[x] for x in current}
        if nxt == current:
            break
        current = nxt
    print(f"Image filtration: {filt}")
    print()

# ============================================================
# TOY MODEL 2: The 2-Cycle
# ============================================================

def toy_two_cycle():
    print("=" * 60)
    print("TOY MODEL 2: 2-Cycle System (0↔1, 2→0)")
    print("=" * 60)
    
    system = {0: 1, 1: 0, 2: 0}
    
    # Find cycles
    visited = set()
    cycles = []
    for start in system:
        if start in visited:
            continue
        path = []
        seen = {}
        x = start
        while x not in seen:
            if x in visited and x not in seen:
                break
            seen[x] = len(path)
            path.append(x)
            x = system[x]
        if x in seen:
            cycle = path[seen[x]:]
            cycles.append(cycle)
            visited.update(path)
        else:
            visited.update(path)
    
    print(f"Cycles found: {cycles}")
    
    # Canonical cycle label
    def canonical(cycle):
        t = tuple(cycle)
        return min(t[i:] + t[:i] for i in range(len(t)))
    
    print(f"Canonical label of [0,1]: {canonical([0,1])}")
    print(f"Canonical label of [1,0]: {canonical([1,0])}")
    print(f"Same cycle? {canonical([0,1]) == canonical([1,0])}")
    print()

# ============================================================
# TOY MODEL 3: Kaprekar 2-Digit
# ============================================================

def toy_kaprekar_2digit():
    print("=" * 60)
    print("TOY MODEL 3: Kaprekar 2-Digit System")
    print("=" * 60)
    
    def kaprekar_step(n):
        s = str(n).zfill(2)
        desc = int("".join(sorted(s, reverse=True)))
        asc = int("".join(sorted(s)))
        return desc - asc
    
    # Build system
    system = {i: kaprekar_step(i) for i in range(100)}
    print(f"States: {len(system)}")
    
    # Sample orbits
    for start in [10, 27, 45]:
        path = [start]
        current = start
        seen = {start}
        for _ in range(20):
            current = system[current]
            if current in seen:
                break
            seen.add(current)
            path.append(current)
        print(f"Orbit of {start:02d}: {path}")
    
    print()

# ============================================================
# TOY MODEL 4: Exact Arithmetic
# ============================================================

def toy_exact_arithmetic():
    print("=" * 60)
    print("TOY MODEL 4: Exact Arithmetic with Fractions")
    print("=" * 60)
    
    a = Fraction(1, 3)
    b = Fraction(2, 3)
    c = a + b
    print(f"1/3 + 2/3 = {c} (exact)")
    
    # Matrix multiplication
    def mat_mult(A, B):
        n, m, p = len(A), len(B[0]), len(B)
        C = [[Fraction(0) for _ in range(m)] for _ in range(n)]
        for i in range(n):
            for j in range(m):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    I = [[Fraction(1,1) if i==j else Fraction(0) for j in range(2)] for i in range(2)]
    A = [[Fraction(1,2), Fraction(0)], [Fraction(0), Fraction(1,3)]]
    result = mat_mult(I, A)
    print(f"I × A = {result}")
    print()

# ============================================================
# TOY MODEL 5: Certificate Structure
# ============================================================

def toy_certificate():
    print("=" * 60)
    print("TOY MODEL 5: Certificate Structure (v3.1)")
    print("=" * 60)
    
    import hashlib
    
    cert = {
        "claim_id": "TOY-CLAIM-001",
        "claim_statement": "2-digit Kaprekar system has finite image filtration",
        "status": "UNVERIFIED",
        "dependencies": {
            "registry_version": "0.4.1-final",
            "definitions": ["AQ-DEF-001", "AQ-DEF-004"],
            "theorems": ["AQ-THM-002"]
        },
        "system": {"states": 100, "type": "kaprekar_2digit"},
        "evidence": {"filtration_depth": 5, "stabilizes": True},
        "proof_obligation": {"method": "exact_fraction_arithmetic", "recomputable": True}
    }
    
    canonical = json.dumps(cert, sort_keys=True, separators=(',', ':'))
    cert["hash"] = {
        "algorithm": "SHA-256",
        "scope": "certificate",
        "value": hashlib.sha256(canonical.encode()).hexdigest()
    }
    
    print(json.dumps(cert, indent=2))
    print()

# ============================================================
# TOY MODEL 6: Defect Operator (Conceptual)
# ============================================================

def toy_defect_concept():
    print("=" * 60)
    print("TOY MODEL 6: Defect Operator Concept")
    print("=" * 60)
    
    # System: 0→1, 1→2, 2→2, 3→2, 4→3
    system = {0: 1, 1: 2, 2: 2, 3: 2, 4: 3}
    
    # Partition: {{0}, {1}, {2,3,4}} — check if f maps each block into one block
    partition = [{0}, {1}, {2, 3, 4}]
    block_of = {}
    for i, block in enumerate(partition):
        for state in block:
            block_of[state] = i
    
    print(f"Partition: {partition}")
    for block in partition:
        targets = {block_of[system[s]] for s in block}
        status = "✓ INVARIANT" if len(targets) == 1 else "✗ DEFECT"
        print(f"  Block {block} -> targets {targets}: {status}")
    
    print()

# ============================================================
# RUN ALL
# ============================================================

if __name__ == "__main__":
    toy_trivial_system()
    toy_two_cycle()
    toy_kaprekar_2digit()
    toy_exact_arithmetic()
    toy_certificate()
    toy_defect_concept()
    
    print("=" * 60)
    print("ALL TOY MODELS COMPLETED SUCCESSFULLY")
    print("=" * 60)
'''

with open(os.path.join(output_dir, "AQARION-TOY-MODELS.py"), 'w') as f:
    f.write(toy_models)

# Run the toy models to verify
result = subprocess.run(
    [sys.executable, "AQARION-TOY-MODELS.py"],
    cwd=output_dir,
    capture_output=True,
    text=True
)
print(result.stdout)
if result.returncode != 0:
    print("STDERR:", result.stderr)
else:
    print("✅ AQARION-TOY-MODELS.py (all demos passed)")============================================================
TOY MODEL 1: Trivial System (0→1→2→2)
============================================================
Orbit of 0: transient=[0, 1], cycle=[2]
Image filtration: [3, 2, 1]

============================================================
TOY MODEL 2: 2-Cycle System (0↔1, 2→0)
============================================================
Cycles found: [[0, 1]]
Canonical label of [0,1]: (0, 1)
Canonical label of [1,0]: (0, 1)
Same cycle? True

============================================================
TOY MODEL 3: Kaprekar 2-Digit System
============================================================
States: 100
Orbit of 10: [10, 9, 81, 63, 27, 45]
Orbit of 27: [27, 45, 9, 81, 63]
Orbit of 45: [45, 9, 81, 63, 27]

============================================================
TOY MODEL 4: Exact Arithmetic with Fractions
============================================================
1/3 + 2/3 = 1 (exact)
I × A = [[Fraction(1, 2), Fraction(0, 1)], [Fraction(0, 1), Fraction(1, 3)]]

============================================================
TOY MODEL 5: Certificate Structure (v3.1)
============================================================
{
  "claim_id": "TOY-CLAIM-001",
  "claim_statement": "2-digit Kaprekar system has finite image filtration",
  "status": "UNVERIFIED",
  "dependencies": {
    "registry_version": "0.4.1-final",
    "definitions": [
      "AQ-DEF-001",
      "AQ-DEF-004"
    ],
    "theorems": [
      "AQ-THM-002"
    ]
  },
  "system": {
    "states": 100,
    "type": "kaprekar_2digit"
  },
  "evidence": {
    "filtration_depth": 5,
    "stabilizes": true
  },
  "proof_obligation": {
    "method": "exact_fraction_arithmetic",
    "recomputable": true
  },
  "hash": {
    "algorithm": "SHA-256",
    "scope": "certificate",
    "value": "755f107741351dd7900923980d78d2c16a3951ea6832a502c63533482e293799"
  }
}

============================================================
TOY MODEL 6: Defect Operator Concept
============================================================
Partition: [{0}, {1}, {2, 3, 4}]
  Block {0} -> targets {1}: ✓ INVARIANT
  Block {1} -> targets {2}: ✓ INVARIANT
  Block {2, 3, 4} -> targets {2}: ✓ INVARIANT

============================================================
ALL TOY MODELS COMPLETED SUCCESSFULLY
============================================================

✅ AQARION-TOY-MODELS.py (all demos passed)
