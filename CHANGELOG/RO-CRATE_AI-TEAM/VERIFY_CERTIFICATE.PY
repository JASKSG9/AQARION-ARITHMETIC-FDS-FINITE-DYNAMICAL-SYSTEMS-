
# ============================================================
# VERIFY CERTIFICATE
# ============================================================

verify_certificate = '''"""
AQARION CERTIFICATE VERIFIER v0.4.1-final
Independent verification — certificates are never self-validating.
"""

import json
import sys
import os

__version__ = "0.4.1-final"

def load_certificate(path: str) -> dict:
    with open(path, 'r') as f:
        return json.load(f)

def verify_certificate(cert: dict, evidence: dict = None) -> dict:
    """Verify a certificate independently."""
    from aqarion_kernel import AQRegistry
    
    registry = AQRegistry()
    
    # If no evidence provided, use minimal check
    if evidence is None:
        evidence = {"note": "Evidence not provided — structural check only"}
    
    result = registry.verify_certificate(cert, evidence)
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_certificate.py <certificate.json>")
        sys.exit(1)
    
    cert_path = sys.argv[1]
    cert = load_certificate(cert_path)
    result = verify_certificate(cert)
    
    print(f"Certificate: {result['certificate_id']}")
    print(f"Claim:       {result['claim_id']}")
    print(f"Status:      {result['status']}")
    print(f"All checks:  {result['all_pass']}")
    for check, passed in result['checks'].items():
        print(f"  {check}: {'PASS' if passed else 'FAIL'}")
    
    return 0 if result['all_pass'] else 1

if __name__ == "__main__":
    sys.exit(main())
'''

with open(os.path.join(output_dir, "verify_certificate.py"), 'w') as f:
    f.write(verify_certificate)

# ============================================================
# MAIN CLI
# ============================================================

main_py = '''"""
AQARION CLI v0.4.1-final
Command-line interface for kernel operations.
"""

import sys
import json
from aqarion_kernel import (
    kaprekar_3digit, kaprekar_3digit_orbit, kaprekar_3digit_system,
    FDDS, AQRegistry, ExactNumber, floyd_cycle, image_filtration,
    nilpotency_depth, defect_operator
)

__version__ = "0.4.1-final"

def cmd_kaprekar(n: str):
    try:
        val = int(n)
        result = kaprekar_3digit(val)
        orbit = kaprekar_3digit_orbit(val)
        print(f"K({val:03d}) = {result:03d}")
        print(f"Orbit: {orbit}")
    except ValueError:
        print(f"Invalid number: {n}")

def cmd_system():
    system = kaprekar_3digit_system()
    print(f"States: {len(system.states)}")
    print(f"Sample transitions:")
    for n in [0, 100, 495, 617]:
        print(f"  {n:03d} -> {system.transition[n]:03d}")
    
    # Quotient
    q = system.quotient_system()
    print(f"\nQuotient states: {len(q.states)}")
    
    # Filtration
    filt = image_filtration(system)
    print(f"Image filtration depth: {len(filt)-1}")
    
    # Fixed point 495
    mu, lam = floyd_cycle(kaprekar_3digit, 100)
    print(f"Cycle detection from 100: preperiod={mu}, period={lam}")

def cmd_version():
    print(f"AQARION v{__version__}")

def main():
    if len(sys.argv) < 2:
        cmd_version()
        print("\nUsage:")
        print("  python main.py kaprekar <n>    — Compute Kaprekar routine")
        print("  python main.py system          — Analyze Kaprekar system")
        print("  python main.py version         — Show version")
        return
    
    cmd = sys.argv[1]
    if cmd == "kaprekar" and len(sys.argv) > 2:
        cmd_kaprekar(sys.argv[2])
    elif cmd == "system":
        cmd_system()
    elif cmd == "version":
        cmd_version()
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
'''

with open(os.path.join(output_dir, "main.py"), 'w') as f:
    f.write(main_py)

print("✅ verify_certificate.py written")
print("✅ main.py written")
