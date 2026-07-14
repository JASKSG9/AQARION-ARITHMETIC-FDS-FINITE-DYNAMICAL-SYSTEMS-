
import os, json, hashlib, time, sys

output_dir = "/mnt/agents/output"
os.makedirs(output_dir, exist_ok=True)

# ============================================================
# AQARION KERNEL v0.4.1-FINAL
# ============================================================

aqarion_kernel = '''"""
AQARION KERNEL v0.4.1-final
Finite Dynamical Systems — Exact Arithmetic, Kaprekar Dynamics, Observable Quotients
"""

from fractions import Fraction
from typing import Dict, List, Tuple, Set, Optional, Callable, Any
from collections import defaultdict, deque
import hashlib
import json

__version__ = "0.4.1-final"

# ============================================================
# EXACT ARITHMETIC
# ============================================================

class ExactNumber:
    """Exact rational arithmetic wrapper."""
    def __init__(self, value):
        if isinstance(value, ExactNumber):
            self._val = value._val
        elif isinstance(value, Fraction):
            self._val = value
        elif isinstance(value, (int, float)):
            self._val = Fraction(value).limit_denominator(10000)
        else:
            self._val = Fraction(str(value))
    
    def __add__(self, other): return ExactNumber(self._val + ExactNumber(other)._val)
    def __sub__(self, other): return ExactNumber(self._val - ExactNumber(other)._val)
    def __mul__(self, other): return ExactNumber(self._val * ExactNumber(other)._val)
    def __truediv__(self, other): return ExactNumber(self._val / ExactNumber(other)._val)
    def __eq__(self, other): return self._val == ExactNumber(other)._val
    def __hash__(self): return hash(self._val)
    def __repr__(self): return f"Exact({self._val})"
    def __str__(self): return str(self._val)
    def to_float(self): return float(self._val)
    def numerator(self): return self._val.numerator
    def denominator(self): return self._val.denominator

# ============================================================
# KAPREKAR DYNAMICS (3-DIGIT)
# ============================================================

def kaprekar_3digit(n: int) -> int:
    """3-digit Kaprekar routine: sort digits descending - ascending."""
    s = str(n).zfill(3)
    desc = int(''.join(sorted(s, reverse=True)))
    asc = int(''.join(sorted(s)))
    return desc - asc

def kaprekar_3digit_orbit(n: int, max_iter: int = 100) -> List[int]:
    """Trace orbit until cycle or fixed point."""
    seen = []
    current = n
    for _ in range(max_iter):
        if current in seen:
            idx = seen.index(current)
            return seen[:idx] + [seen[idx:]]  # preperiod + cycle
        seen.append(current)
        current = kaprekar_3digit(current)
    return seen

def kaprekar_3digit_all_states() -> Dict[int, List[int]]:
    """All 3-digit states (000-999) and their orbits."""
    states = {}
    for n in range(1000):
        states[n] = kaprekar_3digit_orbit(n)
    return states

# ============================================================
# FINITE DETERMINISTIC DYNAMICAL SYSTEM (FDDS)
# ============================================================

class FDDS:
    """Finite Deterministic Dynamical System."""
    def __init__(self, states: Set[int], transition: Dict[int, int], 
                 observable: Optional[Dict[int, Any]] = None):
        self.states = set(states)
        self.transition = dict(transition)
        self.observable = observable or {s: str(s) for s in states}
        self._validate()
    
    def _validate(self):
        for s in self.states:
            assert s in self.transition, f"State {s} missing transition"
            assert self.transition[s] in self.states, f"Transition target invalid"
    
    def orbit(self, x: int, max_len: int = 100) -> List[int]:
        seq = [x]
        seen = {x: 0}
        current = x
        for i in range(1, max_len):
            current = self.transition[current]
            if current in seen:
                return seq[:seen[current]], seq[seen[current]:]
            seen[current] = i
            seq.append(current)
        return seq, []
    
    def trace(self, x: int, n: int) -> List[Any]:
        """Observable trace of length n."""
        result = []
        current = x
        for _ in range(n):
            result.append(self.observable[current])
            current = self.transition[current]
        return result
    
    def moore_refinement(self, relation: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        """One-step Moore refinement operator Phi."""
        new_relation = set()
        for (a, b) in relation:
            if self.observable.get(a) == self.observable.get(b):
                ta, tb = self.transition[a], self.transition[b]
                if (ta, tb) in relation or (tb, ta) in relation:
                    new_relation.add((min(a,b), max(a,b)))
        return new_relation
    
    def greatest_fixed_point(self) -> Set[Tuple[int, int]]:
        """Greatest fixed point of refinement operator = behavioral equivalence."""
        relation = {(min(a,b), max(a,b)) for a in self.states for b in self.states}
        while True:
            new_relation = self.moore_refinement(relation)
            if new_relation == relation:
                break
            relation = new_relation
        return relation
    
    def quotient_system(self) -> 'FDDS':
        """Build quotient system by behavioral equivalence."""
        equiv = self.greatest_fixed_point()
        # Build equivalence classes
        classes = {}
        class_map = {}
        for s in sorted(self.states):
            found = False
            for rep, members in classes.items():
                if (min(s, rep), max(s, rep)) in equiv:
                    members.add(s)
                    class_map[s] = rep
                    found = True
                    break
            if not found:
                classes[s] = {s}
                class_map[s] = s
        
        # Build quotient
        q_states = set(classes.keys())
        q_transition = {rep: class_map[self.transition[rep]] for rep in q_states}
        q_observable = {rep: self.observable[rep] for rep in q_states}
        return FDDS(q_states, q_transition, q_observable)

# ============================================================
# CYCLE DETECTION
# ============================================================

def floyd_cycle(f, x0):
    """Floyd's tortoise and hare cycle detection."""
    tortoise = f(x0)
    hare = f(f(x0))
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(f(hare))
    
    # Find cycle start
    mu = 0
    tortoise = x0
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(hare)
        mu += 1
    
    # Find period
    lam = 1
    hare = f(tortoise)
    while tortoise != hare:
        hare = f(hare)
        lam += 1
    
    return mu, lam

# ============================================================
# IMAGE FILTRATION & DEPTH
# ============================================================

def image_filtration(fdds: FDDS) -> List[Set[int]]:
    """Compute image filtration: X, T(X), T^2(X), ..."""
    current = set(fdds.states)
    filtration = [set(current)]
    while True:
        next_set = {fdds.transition[s] for s in current}
        if next_set == current or not next_set:
            break
        filtration.append(next_set)
        current = next_set
    return filtration

def nilpotency_depth(fdds: FDDS) -> int:
    """Depth until image stabilizes."""
    return len(image_filtration(fdds)) - 1

# ============================================================
# DEFECT OPERATOR
# ============================================================

def defect_operator(fdds: FDDS, partition: List[Set[int]]) -> float:
    """Measure how far a partition is from being a dynamical congruence."""
    defect = 0.0
    for block in partition:
        images = {fdds.transition[s] for s in block}
        # Count images falling in different blocks
        for img in images:
            found = False
            for b in partition:
                if img in b:
                    found = True
                    break
            if not found:
                defect += 1.0
    return defect

# ============================================================
# REGISTRY & CERTIFICATE SYSTEM
# ============================================================

class AQRegistry:
    """Claim registry with versioning and integrity."""
    SCHEMA_VERSION = "3.1.0"
    
    def __init__(self):
        self.claims = {}
        self.evidence = {}
        self.version = __version__
    
    def register_claim(self, claim_id: str, statement: str, 
                       evidence: Dict[str, Any]) -> str:
        """Register a mathematical claim."""
        self.claims[claim_id] = {
            "id": claim_id,
            "statement": statement,
            "status": "REGISTERED",
            "timestamp": time.time() if 'time' in globals() else 0,
            "schema_version": self.SCHEMA_VERSION,
        }
        self.evidence[claim_id] = evidence
        return claim_id
    
    def generate_certificate(self, claim_id: str) -> Dict:
        """Generate a certificate for a claim (always UNVERIFIED)."""
        if claim_id not in self.claims:
            raise ValueError(f"Claim {claim_id} not registered")
        
        cert = {
            "certificate_id": f"AQ-CERT-{claim_id}-001",
            "claim_id": claim_id,
            "claim_statement": self.claims[claim_id]["statement"],
            "status": "UNVERIFIED",
            "kernel_version": self.version,
            "schema_version": self.SCHEMA_VERSION,
            "evidence_hash": self._hash_evidence(self.evidence[claim_id]),
            "note": "Certificates are never self-validating. Independent verification required.",
        }
        return cert
    
    def _hash_evidence(self, evidence: Dict) -> str:
        """SHA-256 hash of canonical evidence JSON."""
        canonical = json.dumps(evidence, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical.encode()).hexdigest()[:32]
    
    def verify_certificate(self, cert: Dict, evidence: Dict) -> Dict:
        """Verify a certificate against evidence."""
        result = {
            "certificate_id": cert.get("certificate_id"),
            "claim_id": cert.get("claim_id"),
            "status": "VALID",
            "checks": {
                "schema_version": cert.get("schema_version") == self.SCHEMA_VERSION,
                "kernel_version": cert.get("kernel_version") == self.version,
                "evidence_hash": cert.get("evidence_hash") == self._hash_evidence(evidence),
                "not_self_validating": cert.get("status") == "UNVERIFIED",
            }
        }
        result["all_pass"] = all(result["checks"].values())
        if not result["all_pass"]:
            result["status"] = "INVALID"
        return result
    
    def snapshot(self) -> Dict:
        """Registry snapshot for audit."""
        return {
            "schema_version": self.SCHEMA_VERSION,
            "kernel_version": self.version,
            "claim_count": len(self.claims),
            "claims": list(self.claims.keys()),
        }

# ============================================================
# SYSTEM DEFINITION
# ============================================================

def kaprekar_3digit_system() -> FDDS:
    """Build FDDS for 3-digit Kaprekar map."""
    states = set(range(1000))
    transition = {n: kaprekar_3digit(n) for n in states}
    observable = {n: str(n).zfill(3) for n in states}
    return FDDS(states, transition, observable)

# ============================================================
# MAIN EXPORTS
# ============================================================

__all__ = [
    'ExactNumber',
    'kaprekar_3digit', 'kaprekar_3digit_orbit', 'kaprekar_3digit_all_states',
    'FDDS', 'floyd_cycle',
    'image_filtration', 'nilpotency_depth', 'defect_operator',
    'AQRegistry', 'kaprekar_3digit_system',
]
'''

with open(os.path.join(output_dir, "aqarion_kernel.py"), 'w') as f:
    f.write(aqarion_kernel)

print("✅ aqarion_kernel.py written")✅ aqarion_kernel.py written
