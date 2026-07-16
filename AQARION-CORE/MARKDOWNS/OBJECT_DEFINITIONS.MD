
# ============================================================
# 2. object_definitions.md
# ============================================================

object_defs = '''# AQ-001 Object Definitions — Kaprekar Gap Benchmark

## Object Boundary Policy

The following objects are tracked **separately**. No object may be substituted for another.

| Object | Type | Status | Boundary |
|--------|------|--------|----------|
| Raw system | Computation | VERIFIED_COMPUTATION | computation_only |
| Gap observation | Map | VERIFIED_COMPUTATION | observation_map |
| Active gap system | Dynamical system | CERTIFIED | dynamical_system |
| Exact quotient | Theorem instance | CERTIFIED | exact_quotient |
| Image filtration | Sequence | CERTIFIED | filtration |
| Tree geometry | Graph structure | CERTIFIED | geometric_structure |
| Spectral geometry | Spectrum | EMPIRICAL_GEOMETRIC_SIGNATURE | spectral |
| Curvature geometry | Edge metric | EMPIRICAL_GEOMETRIC_SIGNATURE | curvature |

---

## Object 1: Raw System

**Name:** four_digit_kaprekar_base10

**Definition:**
- State space: 4-digit numbers with at least 2 distinct digits
- Cardinality: 9990
- Transition: Kaprekar routine (desc - asc)

**Status:** VERIFIED_COMPUTATION
**Boundary:** computation_only
**Theorem dependency:** None

---

## Object 2: Gap Observation

**Name:** gap_projection

**Definition:**
- For 4-digit number with digits d1 >= d2 >= d3 >= d4:
- π(n) = (d1 - d4, d2 - d3)

**Status:** VERIFIED_COMPUTATION
**Boundary:** observation_map
**Theorem dependency:** None

---

## Object 3: Active Gap System

**Name:** G*

**Definition:**
- States: 54 unique gap values
- Transition: T_G(g) = gap(Kaprekar(n)) for any n with gap(n) = g
- Fixed point: (6,2)
- Maximum depth: 6

**Status:** CERTIFIED
**Boundary:** dynamical_system
**Theorem dependency:** None

---

## Object 4: Exact Quotient

**Name:** identity_observation_quotient

**Definition:**
- Partition: identity on G* (54 blocks)
- Defect operator: D_Π = (I - P) K P
- Measured: rank(D_Π) = 0, ||D_Π||_F = 0

**Status:** CERTIFIED
**Boundary:** exact_quotient
**Theorem dependency:** AQ-001

**Firewall:** This is a computational certificate of exactness, not a universal theorem.

---

## Object 5: Image Filtration

**Name:** image_chain

**Definition:**
- E_0 = G* (54 states)
- E_{k+1} = T(E_k)
- Chain: 54 → 20 → 14 → 10 → 7 → 4 → 1

**Status:** CERTIFIED
**Boundary:** filtration
**Label:** finite observed collapse depth

**Firewall:** NOT a nilpotency theorem. This is a finite observed sequence.

---

## Object 6: Tree Geometry

**Name:** undirected_symmetrization

**Definition:**
- Vertices: 54 (gap states)
- Edges: 53 (symmetrized directed edges)
- Properties: connected, acyclic
- Tree test: edges = vertices - 1

**Status:** CERTIFIED
**Boundary:** geometric_structure

---

## Object 7: Spectral Geometry

**Name:** normalized_laplacian_spectrum

**Definition:**
- L = I - D^{-1/2} A D^{-1/2}
- μ1 (Fiedler value): 0.01140178938892764

**Status:** EMPIRICAL_GEOMETRIC_SIGNATURE
**Boundary:** spectral
**Label:** empirical

**Firewall:** This is a computed spectrum, not a spectral theorem.

---

## Object 8: Curvature Geometry

**Name:** ollivier_ricci_curvature

**Definition:**
- κ(x,y) for each undirected edge
- Mean: -0.3596436059
- Negative edges: 19/53
- Zero edges: 34/53
- Positive edges: 0/53

**Status:** EMPIRICAL_GEOMETRIC_SIGNATURE
**Boundary:** curvature
**Label:** empirical

**Firewall:** This is an empirical geometric signature, not a curvature theorem.

---

## Boundary Enforcement

The following substitutions are **PROHIBITED**:

1. image (filtration) → quotient (exactness)
2. benchmark (tree) → theorem (AQ-001)
3. geometry (spectral) → dynamics (Koopman)
4. proof (Lean) → computation (Python)

---

## Pipeline

```
CORE
  ↓
1. Raw system (9990 states)
2. Gap observation (π: X → G)
  ↓
CERTIFICATION
  ↓
3. Active gap system (54 states, depth 6)
4. Exact quotient (D = 0)
5. Image filtration (54→20→14→10→7→4→1)
  ↓
BENCHMARK
  ↓
6. Tree geometry (54V, 53E, tree)
  ↓
APPLICATION
  ↓
7. Spectral geometry (μ1 = 0.0114)
8. Curvature geometry (mean κ = -0.36)
```
'''

with open('/mnt/agents/output/benchmarks/kaprekar_gap/object_definitions.md', 'w') as f:
    f.write(object_defs)

print("object_definitions.md created")object_definitions.md created
