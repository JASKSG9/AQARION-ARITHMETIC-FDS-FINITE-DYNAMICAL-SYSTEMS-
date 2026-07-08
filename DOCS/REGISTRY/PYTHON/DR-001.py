
import numpy as np
import json
from datetime import datetime

# ============================================================
# DR-001 REGISTRY — IMMUTABLE DEFINITIONS & OBSERVATIONS
# Version: 2026-07-08-0513
# ============================================================

REGISTRY = {
    "registry_id": "DR-001-REGISTRY-v20260708-0513",
    "timestamp": "2026-07-08T05:13:00Z",
    "status": "FROZEN — No mutable fields below this line",
    
    # ========================================================
    # PRIORITY 0: IMMUTABLE DEFINITIONS
    # ========================================================
    "definitions": {
        "state_space": {
            "primary": "1D expanding map (doubling map T(x) = 2x mod 1 on [0,1])",
            "secondary": "2D baker map (x,y) -> (2x mod 1, (y + floor(2x))/2)",
            "note": "These are DISTINCT objects. Claims for one do not transfer to the other without explicit proof."
        },
        
        "evolution_operators": {
            "Koopman_U": {
                "definition": "(Uf)(x) = f(T(x))",
                "discretization": "Ulam: n cells, K_{ij} = 1 if T(cell_j) intersects cell_i, else 0 (point evaluation at cell representative)",
                "matrix_form": "K_{i,T(i)} = 1 for T(i) = 2i mod n"
            },
            "Perron_Frobenius_L": {
                "definition": "(Lρ)(x) = sum_{y: T(y)=x} ρ(y) / |T'(y)|",
                "discretization": "Ulam: L_{ij} = measure(T^{-1}(cell_i) ∩ cell_j) / measure(cell_j)",
                "note": "For doubling map, L = K^T / 2 (up to scaling)"
            },
            "Ulam_approximation": {
                "definition": "Piecewise constant approximation on partition cells",
                "note": "This is the NUMERICAL object actually computed, distinct from the analytical operator"
            }
        },
        
        "partition": {
            "type": "uniform_equipartition",
            "description": "n cells of equal length 1/n on [0,1]",
            "coarse_graining": "Partition Π groups cells into k blocks of m cells each (n = k·m)",
            "example": "n=4, k=2, m=2: G_0={0,1}, G_1={2,3}",
            "projector_P": "P_Π f = block average: (P_Π f)(i) = (1/|G_j|) sum_{l in G_j} f(l) for i in G_j"
        },
        
        "defect_operator": {
            "definition": "D = (I - P_Π) K P_Π",
            "domain_codomain": "D: V_Π -> V_Π^⊥ where V_Π = image(P_Π), V_Π^⊥ = ker(P_Π)",
            "note": "V_Π^0 (zero-sum subspace) is a subspace of V_Π^⊥; for uniform partitions they coincide"
        }
    },
    
    # ========================================================
    # PRIORITY 1: PROVEN PROPOSITIONS (Immutable)
    # ========================================================
    "proven_propositions": {
        "PROP-DR-001-001": {
            "statement": "D = (I-P)KP maps V_Π to V_Π^⊥",
            "proof_status": "PROVEN",
            "proof_sketch": "For any f, P_Π f ∈ V_Π. Then K P_Π f is some vector. (I-P_Π) projects to the orthogonal complement. Thus D f ∈ V_Π^⊥."
        },
        "PROP-DR-001-002": {
            "statement": "rank(D) ≤ min(dim V_Π, dim V_Π^⊥) = min(k, n-k)",
            "proof_status": "PROVEN",
            "proof_sketch": "rank(D) ≤ rank(P_Π) = dim V_Π = k. Also D maps into V_Π^⊥ so rank(D) ≤ dim V_Π^⊥ = n-k. Standard rank inequality."
        },
        "PROP-DR-001-003": {
            "statement": "For n=4, k=2, m=2: rank(D) ≤ 2",
            "proof_status": "FOLLOWS FROM PROP-DR-001-002",
            "note": "min(2, 2) = 2"
        }
    },
    
    # ========================================================
    # PRIORITY 2: COMPUTATIONAL OBSERVATIONS (Verified, not generalized)
    # ========================================================
    "computational_observations": {
        "OBS-DR-001-001": {
            "description": "Doubling map discretizations (Koopman, PF, coarse Baker) on n=4, k=2, m=2",
            "systems_tested": ["Koopman doubling", "Perron-Frobenius doubling", "2D Baker (coarse x-strip)"],
            "rank_D": 1,
            "nullity_D": 3,
            "singular_values": "[0.5, 0, 0, 0] (one nonzero singular value = 0.5)",
            "ratio_to_bound": 1/2,
            "operator_property": "All three matrices produce IDENTICAL D (up to scaling)",
            "why_rank_1": "T(0)=T(2)=0 and T(1)=T(3)=2 causes K·e_G0 and K·e_G1 to project to parallel vectors in V_Π^⊥",
            "status": "VERIFIED COMPUTATION — DO NOT GENERALIZE BEYOND TESTED SYSTEMS"
        },
        "OBS-DR-001-002": {
            "description": "Block-preserving operators on n=4, k=2, m=2",
            "systems_tested": ["Cyclic block map", "Shift on Z_k × Z_m"],
            "rank_D": 0,
            "nullity_D": 4,
            "singular_values": "[0, 0, 0, 0]",
            "ratio_to_bound": 0,
            "operator_property": "K(V_Π) ⊆ V_Π, so (I-P)KP = 0 identically",
            "status": "VERIFIED COMPUTATION — DO NOT GENERALIZE BEYOND TESTED SYSTEMS"
        },
        "OBS-DR-001-003": {
            "description": "Constructed operator achieving rank=2 on n=4, k=2, m=2",
            "systems_tested": ["Asymmetric within-block operator"],
            "rank_D": 2,
            "nullity_D": 2,
            "singular_values": "[0.707, 0.707, 0, 0]",
            "ratio_to_bound": 1.0,
            "operator_property": "K e_G0 and K e_G1 project to LINEARLY INDEPENDENT vectors in V_Π^⊥",
            "status": "VERIFIED COMPUTATION — EXISTENCE PROOF ONLY"
        }
    },
    
    # ========================================================
    # PRIORITY 3: RETIRED CLAIMS (Moved to conjectures)
    # ========================================================
    "retired_claims": {
        "FORMER-THM-rank-formula": {
            "original_claim": "rank(D) = m(k-1)",
            "status": "RETIRED — Insufficient evidence",
            "reason": "Only verified for one constructed example (OBS-DR-001-003). Counter-evidence: OBS-DR-001-001 shows rank=1 when formula predicts 2. OBS-DR-001-002 shows rank=0 when formula predicts 2.",
            "new_location": "See conjectures section below"
        }
    },
    
    # ========================================================
    # PRIORITY 4: OPEN CONJECTURES
    # ========================================================
    "conjectures": {
        "CONJ-DR-001-001": {
            "statement": "For 'generic' expanding maps with uniform partition, rank(D) = min(k, m(k-1)) with high probability",
            "evidence": "OBS-DR-001-003 (constructed example achieves bound)",
            "status": "OPEN — Needs systematic testing over random map ensembles",
            "blockers": ["Define 'generic' precisely", "Test for n > 4", "Test non-uniform partitions"]
        },
        "CONJ-DR-001-002": {
            "statement": "The doubling map's algebraic structure T(j) = 2j mod n causes systematic rank collapse when n = 2^m",
            "evidence": "OBS-DR-001-001 (T(0)=T(2), T(1)=T(3) for n=4)",
            "status": "OPEN — Test n=8, 16 to see if pattern persists",
            "testable_prediction": "For n=8, k=2, m=4: T(0)=T(4)=0, T(1)=T(5)=2, T(2)=T(6)=4, T(3)=T(7)=6. Rank may still be 1."
        },
        "CONJ-DR-001-003": {
            "statement": "Perron-Frobenius and Koopman operators for the same map produce the same rank(D) for uniform partitions",
            "evidence": "OBS-DR-001-001 (both give rank=1)",
            "status": "OPEN — Test with non-uniform partitions and other maps"
        }
    },
    
    # ========================================================
    # PRIORITY 5: DECISIVE EXPERIMENT SUITE (Planned)
    # ========================================================
    "planned_experiments": {
        "EXP-DR-001-001": {
            "description": "Scale n while varying k, m independently",
            "parameters": [
                "n=8: (k=2,m=4), (k=4,m=2), (k=8,m=1)",
                "n=16: (k=2,m=8), (k=4,m=4), (k=8,m=2), (k=16,m=1)",
                "n=32: selected combinations"
            ],
            "operators": ["Koopman doubling", "Perron-Frobenius doubling", "Full 2D Baker"],
            "metrics": ["rank(D)", "nullity(D)", "singular values", "ratio rank/bound"],
            "purpose": "Determine if rank pattern is systematic or map-dependent"
        },
        "EXP-DR-001-002": {
            "description": "Partition alignment tests",
            "parameters": [
                "Aligned: partition boundaries match map discontinuities",
                "Misaligned: partition boundaries shifted by 1/2 cell",
                "Random: non-uniform block sizes"
            ],
            "purpose": "Test if rank collapse in OBS-DR-001-001 is due to alignment with map structure"
        },
        "EXP-DR-001-003": {
            "description": "Random map ensemble",
            "parameters": [
                "Generate random piecewise linear expanding maps",
                "Compute rank(D) for each",
                "Compare distribution to deterministic maps"
            ],
            "purpose": "Test CONJ-DR-001-001 (generic behavior)"
        }
    }
}

# Save registry
output_path = "/mnt/agents/output/DR-001-REGISTRY-v20260708-0513.json"
with open(output_path, 'w') as f:
    json.dump(REGISTRY, f, indent=2)

print("="*80)
print("DR-001 REGISTRY FROZEN")
print("="*80)
print(f"Registry ID: {REGISTRY['registry_id']}")
print(f"Timestamp: {REGISTRY['timestamp']}")
print(f"Status: {REGISTRY['status']}")
print()
print("IMMUTABLE DEFINITIONS:")
print(f"  State space: {REGISTRY['definitions']['state_space']['primary']}")
print(f"  Partition: {REGISTRY['definitions']['partition']['type']}")
print(f"  Defect operator: {REGISTRY['definitions']['defect_operator']['definition']}")
print()
print("PROVEN PROPOSITIONS:")
for key, prop in REGISTRY['proven_propositions'].items():
    print(f"  {key}: {prop['statement']}")
    print(f"    Status: {prop['proof_status']}")
print()
print("COMPUTATIONAL OBSERVATIONS:")
for key, obs in REGISTRY['computational_observations'].items():
    print(f"  {key}: rank(D) = {obs['rank_D']} (tested: {', '.join(obs['systems_tested'])})")
    print(f"    Ratio to bound: {obs['ratio_to_bound']}")
print()
print("RETIRED CLAIMS:")
for key, claim in REGISTRY['retired_claims'].items():
    print(f"  {key}: '{claim['original_claim']}' → {claim['status']}")
print()
print("OPEN CONJECTURES:")
for key, conj in REGISTRY['conjectures'].items():
    print(f"  {key}: {conj['status']}")
    print(f"    Blockers: {', '.join(conj['blockers']) if conj.get('blockers') else 'None listed'}")
print()
print("PLANNED EXPERIMENTS:")
for key, exp in REGISTRY['planned_experiments'].items():
    print(f"  {key}: {exp['description']}")
print()
print(f"Registry saved to: {output_path}")
print("="*80)================================================================================
DR-001 REGISTRY FROZEN
================================================================================
Registry ID: DR-001-REGISTRY-v20260708-0513
Timestamp: 2026-07-08T05:13:00Z
Status: FROZEN — No mutable fields below this line

IMMUTABLE DEFINITIONS:
  State space: 1D expanding map (doubling map T(x) = 2x mod 1 on [0,1])
  Partition: uniform_equipartition
  Defect operator: D = (I - P_Π) K P_Π

PROVEN PROPOSITIONS:
  PROP-DR-001-001: D = (I-P)KP maps V_Π to V_Π^⊥
    Status: PROVEN
  PROP-DR-001-002: rank(D) ≤ min(dim V_Π, dim V_Π^⊥) = min(k, n-k)
    Status: PROVEN
  PROP-DR-001-003: For n=4, k=2, m=2: rank(D) ≤ 2
    Status: FOLLOWS FROM PROP-DR-001-002

COMPUTATIONAL OBSERVATIONS:
  OBS-DR-001-001: rank(D) = 1 (tested: Koopman doubling, Perron-Frobenius doubling, 2D Baker (coarse x-strip))
    Ratio to bound: 0.5
  OBS-DR-001-002: rank(D) = 0 (tested: Cyclic block map, Shift on Z_k × Z_m)
    Ratio to bound: 0
  OBS-DR-001-003: rank(D) = 2 (tested: Asymmetric within-block operator)
    Ratio to bound: 1.0

RETIRED CLAIMS:
  FORMER-THM-rank-formula: 'rank(D) = m(k-1)' → RETIRED — Insufficient evidence

OPEN CONJECTURES:
  CONJ-DR-001-001: OPEN — Needs systematic testing over random map ensembles
    Blockers: Define 'generic' precisely, Test for n > 4, Test non-uniform partitions
  CONJ-DR-001-002: OPEN — Test n=8, 16 to see if pattern persists
    Blockers: None listed
  CONJ-DR-001-003: OPEN — Test with non-uniform partitions and other maps
    Blockers: None listed

PLANNED EXPERIMENTS:
  EXP-DR-001-001: Scale n while varying k, m independently
  EXP-DR-001-002: Partition alignment tests
  EXP-DR-001-003: Random map ensemble

Registry saved to: /mnt/agents/output/DR-001-REGISTRY-v20260708-0513.json
================================================================================
