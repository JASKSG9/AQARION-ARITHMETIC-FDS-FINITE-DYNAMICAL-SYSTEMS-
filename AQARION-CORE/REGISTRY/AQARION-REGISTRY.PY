
import os
import json
import hashlib

os.makedirs('/mnt/agents/output/benchmarks/kaprekar_gap', exist_ok=True)

# ============================================================
# 1. registry.json
# ============================================================

registry = {
    "system": "four_digit_kaprekar_gap_base10",
    "registry_version": "AQ-001-POST-PHI377",
    "created": "2026-07-15",
    "objects": {
        "1_raw_system": {
            "name": "Raw Kaprekar System",
            "description": "Complete 4-digit Kaprekar routine state space",
            "cardinality": 9990,
            "status": "VERIFIED_COMPUTATION",
            "boundary": "computation_only"
        },
        "2_gap_observation": {
            "name": "Gap Observation",
            "description": "Projection π: X → G where g = (d_max - d_min, d_2nd_max - d_2nd_min)",
            "status": "VERIFIED_COMPUTATION",
            "boundary": "observation_map"
        },
        "3_active_gap_system": {
            "name": "Active Gap System G*",
            "cardinality": 54,
            "root": "(6,2)",
            "depth": 6,
            "status": "CERTIFIED",
            "boundary": "dynamical_system"
        },
        "4_exact_quotient": {
            "name": "Exact Observation Quotient",
            "defect_rank": 0,
            "defect_norm": 0.0,
            "violations": 0,
            "status": "CERTIFIED",
            "boundary": "exact_quotient",
            "theorem_dependency": "AQ-001"
        },
        "5_image_filtration": {
            "name": "Image Filtration",
            "chain": [54, 20, 14, 10, 7, 4, 1],
            "stabilization_depth": 6,
            "terminal": "(6,2)",
            "status": "CERTIFIED",
            "boundary": "filtration",
            "label": "finite observed collapse depth"
        },
        "6_tree_geometry": {
            "name": "Undirected Symmetrization",
            "vertices": 54,
            "edges": 53,
            "connected": True,
            "acyclic": True,
            "tree_test": True,
            "status": "CERTIFIED",
            "boundary": "geometric_structure"
        },
        "7_spectral_geometry": {
            "name": "Normalized Laplacian Spectrum",
            "spectral_gap": 0.01140178938892764,
            "status": "EMPIRICAL_GEOMETRIC_SIGNATURE",
            "boundary": "spectral",
            "label": "empirical"
        },
        "8_curvature_geometry": {
            "name": "Ollivier-Ricci Curvature",
            "mean_curvature": -0.3596436059,
            "negative_edges": 19,
            "zero_edges": 34,
            "positive_edges": 0,
            "status": "EMPIRICAL_GEOMETRIC_SIGNATURE",
            "boundary": "curvature",
            "label": "empirical"
        }
    },
    "object_boundaries": {
        "image_ne_quotient": True,
        "benchmark_ne_theorem": True,
        "geometry_ne_dynamics": True,
        "proof_ne_computation": True
    },
    "pipeline": {
        "core": ["1_raw_system", "2_gap_observation"],
        "certification": ["3_active_gap_system", "4_exact_quotient", "5_image_filtration"],
        "benchmark": ["6_tree_geometry"],
        "application": ["7_spectral_geometry", "8_curvature_geometry"]
    }
}

with open('/mnt/agents/output/benchmarks/kaprekar_gap/registry.json', 'w') as f:
    json.dump(registry, f, indent=2, sort_keys=True)

print("registry.json created")registry.json created
