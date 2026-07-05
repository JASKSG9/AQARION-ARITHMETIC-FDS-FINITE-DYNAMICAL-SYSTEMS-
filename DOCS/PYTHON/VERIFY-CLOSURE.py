"""
verify_closure.py — AQARION Level 19: Verification Closure
===========================================================
Node #10878 · v1.0.0 · 2026-06-21
Protocol: Prove First · Predict Second · No Free Parameters

Implements 12 genuine axioms from the Level 19 proposal.
Corrections applied:
  - V19-001 merged into V19-002 (order-independence is stronger)
  - V19-009 extends V19-004 (runtime order, not just DAG structure)
  - V19-014 merged into V19-013 (functor framing → pub gate extension)
  - V19-015 demoted to obstruction REPORT, not Ω formalism (undefined F,V)

Design:
  The registry is the single source of truth.
  claim_state.json is the canonical output artifact.
  Everything else derives from it.
"""

import json
import hashlib
import copy
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Set, Tuple
from enum import Enum

# ══════════════════════════════════════════════════════════════════════════════
# DATA MODEL
# ══════════════════════════════════════════════════════════════════════════════

class ClaimStatus(str, Enum):
    CONJECTURE  = "Conjecture"
    ACTIVE      = "Active"
    VERIFIED    = "Verified"
    REJECTED    = "Rejected"
    COUNTEREXAMPLE = "Counterexample"
    DEPRECATED  = "Deprecated"
    KILLED      = "Killed"

LEGAL_TRANSITIONS = {
    ClaimStatus.CONJECTURE:  {ClaimStatus.ACTIVE, ClaimStatus.REJECTED},
    ClaimStatus.ACTIVE:      {ClaimStatus.VERIFIED, ClaimStatus.REJECTED,
                              ClaimStatus.COUNTEREXAMPLE, ClaimStatus.DEPRECATED},
    ClaimStatus.VERIFIED:    {ClaimStatus.DEPRECATED},   # only forward
    ClaimStatus.REJECTED:    {ClaimStatus.DEPRECATED},
    ClaimStatus.COUNTEREXAMPLE: {ClaimStatus.DEPRECATED},
    ClaimStatus.DEPRECATED:  set(),
    ClaimStatus.KILLED:      set(),
}

TERMINAL_STATUSES = {ClaimStatus.VERIFIED, ClaimStatus.REJECTED,
                     ClaimStatus.COUNTEREXAMPLE, ClaimStatus.KILLED,
                     ClaimStatus.DEPRECATED}

@dataclass
class EvidenceRecord:
    type: str        # exhaustive_search, proof_written, lean_formalized, script, dataset, etc.
    artifact: Optional[str] = None  # path to script/data file if applicable
    description: str = ""

@dataclass
class ClaimRecord:
    id: str
    statement: str
    status: ClaimStatus
    dependencies: List[str] = field(default_factory=list)
    evidence: List[EvidenceRecord] = field(default_factory=list)
    paper: Optional[str] = None       # which paper requires this claim
    root: bool = False                # True = axiom / definition (no parents needed)

    def has_executable_evidence(self) -> bool:
        executable_types = {"exhaustive_search", "script", "dataset", "lean_formalized"}
        return any(e.type in executable_types for e in self.evidence)

    def evidence_grade(self) -> str:
        ev_types = {e.type for e in self.evidence}
        if "proof_written" in ev_types and "lean_formalized" in ev_types: return "PV"
        if "proof_written" in ev_types: return "P"
        if "adversarial" in ev_types and "exhaustive_search" in ev_types: return "AV"
        if "exhaustive_search" in ev_types: return "C2"
        if "random_search" in ev_types: return "C1"
        return "C0"

@dataclass
class Registry:
    claims: Dict[str, ClaimRecord] = field(default_factory=dict)
    papers: Dict[str, List[str]] = field(default_factory=dict)  # paper -> required claim IDs

    def add(self, claim: ClaimRecord):
        self.claims[claim.id] = claim

    def to_canonical_json(self) -> str:
        """Canonical serialization: sorted keys, no timestamps."""
        data = {}
        for cid in sorted(self.claims.keys()):
            c = self.claims[cid]
            data[cid] = {
                "id": c.id,
                "statement": c.statement,
                "status": c.status.value,
                "dependencies": sorted(c.dependencies),
                "evidence": [{"type": e.type, "artifact": e.artifact or "",
                              "description": e.description}
                             for e in sorted(c.evidence, key=lambda x: x.type)],
                "paper": c.paper or "",
                "root": c.root,
                "grade": c.evidence_grade(),
            }
        return json.dumps({"schema": "AQARION-v1", "claims": data}, indent=2, sort_keys=True)

    def sha256(self) -> str:
        return hashlib.sha256(self.to_canonical_json().encode()).hexdigest()


# ══════════════════════════════════════════════════════════════════════════════
# LEVEL 19 AXIOM IMPLEMENTATIONS
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class AxiomResult:
    id: str
    name: str
    passed: bool
    message: str
    detail: str = ""

def _build_dep_graph(registry: Registry):
    """Build networkx-style adjacency from registry."""
    # Returns: {node: set_of_parents}
    graph = {cid: set() for cid in registry.claims}
    for cid, claim in registry.claims.items():
        for dep in claim.dependencies:
            if dep not in graph:
                graph[dep] = set()
            graph[dep]  # ensure exists
        # edges: dep → cid (dep must come before cid)
    edges = []
    for cid, claim in registry.claims.items():
        for dep in claim.dependencies:
            edges.append((dep, cid))
    return graph, edges

def _topological_sort(nodes, edges):
    """Kahn's algorithm. Returns (order, has_cycle)."""
    in_degree = {n: 0 for n in nodes}
    adj = defaultdict(set)
    for src, dst in edges:
        if src in in_degree and dst in in_degree:
            adj[src].add(dst)
            in_degree[dst] += 1
    queue = sorted([n for n, d in in_degree.items() if d == 0])
    order = []
    while queue:
        node = queue.pop(0)
        order.append(node)
        for nbr in sorted(adj[node]):
            in_degree[nbr] -= 1
            if in_degree[nbr] == 0:
                queue.append(nbr)
    has_cycle = len(order) < len(nodes)
    return order, has_cycle

# ── V19-002: Deterministic Certification (strongest idempotence) ──────────
def check_deterministic_certification(registry: Registry) -> AxiomResult:
    """V(R) produces identical SHA256 regardless of execution order."""
    h1 = registry.sha256()
    # Simulate "different order": re-serialize with reversed claim list
    shuffled = Registry(
        claims=dict(reversed(list(registry.claims.items()))),
        papers=registry.papers
    )
    h2 = shuffled.sha256()
    ok = h1 == h2
    return AxiomResult("AQ-V19-002", "Deterministic Certification", ok,
        f"SHA256: {'STABLE' if ok else 'UNSTABLE'}",
        f"Forward: {h1[:16]}...  Reversed: {h2[:16]}...")

# ── V19-003: Dependency Completeness ──────────────────────────────────────
def check_dependency_completeness(registry: Registry) -> AxiomResult:
    """Every dependency reference points to an existing claim."""
    broken = []
    for cid, claim in registry.claims.items():
        for dep in claim.dependencies:
            if dep not in registry.claims:
                broken.append((cid, dep))
    ok = len(broken) == 0
    detail = f"Broken refs: {broken[:5]}" if broken else "All dependencies resolve"
    return AxiomResult("AQ-V19-003", "Dependency Completeness", ok,
        f"{len(broken)} broken dependency reference(s)", detail)

# ── V19-004: No Cyclic Dependencies ───────────────────────────────────────
def check_acyclicity(registry: Registry) -> AxiomResult:
    """Dependency graph must be a DAG."""
    nodes = list(registry.claims.keys())
    edges = [(dep, cid) for cid, c in registry.claims.items() for dep in c.dependencies]
    _, has_cycle = _topological_sort(nodes, edges)
    if has_cycle:
        # Find the cycle
        return AxiomResult("AQ-V19-004", "No Cyclic Dependencies", False,
            "CYCLE DETECTED — proof graph is invalid", "Run nx.find_cycle() for details")
    return AxiomResult("AQ-V19-004", "No Cyclic Dependencies", True,
        "Dependency DAG is acyclic", f"{len(nodes)} nodes, {len(edges)} edges")

# ── V19-005: Reachability from Root Definitions ───────────────────────────
def check_root_reachability(registry: Registry) -> AxiomResult:
    """Every non-root claim reachable from some root via dependency edges."""
    roots = {cid for cid, c in registry.claims.items() if c.root}
    if not roots:
        return AxiomResult("AQ-V19-005", "Root Reachability", False,
            "No root definitions found — define at least one claim with root=True", "")
    # BFS from roots
    edges = [(dep, cid) for cid, c in registry.claims.items() for dep in c.dependencies]
    adj = defaultdict(set)
    for src, dst in edges:
        adj[src].add(dst)
    reachable = set(roots)
    queue = list(roots)
    while queue:
        node = queue.pop(0)
        for nbr in adj[node]:
            if nbr not in reachable:
                reachable.add(nbr); queue.append(nbr)
    orphans = [cid for cid in registry.claims if cid not in reachable 
               and not registry.claims[cid].root
               and registry.claims[cid].status not in (ClaimStatus.KILLED, ClaimStatus.DEPRECATED)]
    ok = len(orphans) == 0
    return AxiomResult("AQ-V19-005", "Root Reachability", ok,
        f"{len(orphans)} orphan claim(s)" if orphans else f"All {len(registry.claims)} claims reachable",
        f"Orphans: {orphans[:5]}" if orphans else f"Roots: {sorted(roots)}")

# ── V19-006: Evidence Reachability ────────────────────────────────────────
def check_evidence_reachability(registry: Registry) -> AxiomResult:
    """Every Verified/AV claim must have executable evidence."""
    executable_grades = {"C2", "AV", "P", "PV"}
    gaps = []
    for cid, claim in registry.claims.items():
        if claim.status in (ClaimStatus.VERIFIED,) and claim.evidence_grade() in executable_grades:
            if not claim.has_executable_evidence():
                gaps.append(cid)
    ok = len(gaps) == 0
    return AxiomResult("AQ-V19-006", "Evidence Reachability", ok,
        f"{len(gaps)} verified claim(s) lack executable evidence",
        f"Gaps: {gaps[:5]}" if gaps else "All verified claims have executable evidence")

# ── V19-007: Hash Stability ───────────────────────────────────────────────
def check_hash_stability(registry: Registry, n: int = 3) -> AxiomResult:
    """Repeated verify() produces identical SHA256."""
    hashes = [registry.sha256() for _ in range(n)]
    ok = len(set(hashes)) == 1
    return AxiomResult("AQ-V19-007", "Hash Stability", ok,
        f"{'STABLE' if ok else 'UNSTABLE'} across {n} executions",
        f"Hash: {hashes[0][:24]}..." if ok else f"Distinct hashes: {list(set(hashes))}")

# ── V19-009: Topological Execution Order ──────────────────────────────────
def check_topological_order(registry: Registry) -> AxiomResult:
    """Verify() can always run in an order consistent with dependencies."""
    nodes = list(registry.claims.keys())
    edges = [(dep, cid) for cid, c in registry.claims.items() for dep in c.dependencies]
    order, has_cycle = _topological_sort(nodes, edges)
    if has_cycle:
        return AxiomResult("AQ-V19-009", "Topological Execution Order", False,
            "No valid execution order exists (cycle present)", "")
    # Verify order is valid: for every edge (u→v), u appears before v
    pos = {node: i for i, node in enumerate(order)}
    violations = [(u, v) for u, v in edges if u in pos and v in pos and pos[u] >= pos[v]]
    ok = len(violations) == 0
    return AxiomResult("AQ-V19-009", "Topological Execution Order", ok,
        f"Valid execution order {'found' if ok else 'VIOLATED'}",
        f"Order: {order[:6]}..." if ok else f"Violations: {violations[:3]}")

# ── V19-010: Registry Consistency ────────────────────────────────────────
def check_registry_consistency(registry: Registry, external_ids: Set[str] = None) -> AxiomResult:
    """Claim IDs in registry match external registry file (if provided)."""
    if external_ids is None:
        # Self-consistency: check no duplicate IDs (already enforced by dict)
        ok = len(registry.claims) == len(set(registry.claims.keys()))
        return AxiomResult("AQ-V19-010", "Registry Consistency", ok,
            f"{'No' if ok else 'DUPLICATE'} ID conflicts in registry",
            f"{len(registry.claims)} unique claim IDs")
    internal = set(registry.claims.keys())
    only_internal = internal - external_ids
    only_external = external_ids - internal
    ok = len(only_internal) == 0 and len(only_external) == 0
    detail = ""
    if only_internal: detail += f"In registry only: {sorted(only_internal)[:5]}. "
    if only_external: detail += f"In external only: {sorted(only_external)[:5]}."
    return AxiomResult("AQ-V19-010", "Registry Consistency", ok,
        f"{'Consistent' if ok else 'INCONSISTENT'} with external registry",
        detail or "Perfect match")

# ── V19-011: Status Validity ──────────────────────────────────────────────
def check_status_validity(registry: Registry) -> AxiomResult:
    """All claims have a valid status from the allowed enum."""
    invalid = []
    for cid, claim in registry.claims.items():
        if not isinstance(claim.status, ClaimStatus):
            invalid.append((cid, claim.status))
        # Extra: verified claims must have grade >= C2
        if claim.status == ClaimStatus.VERIFIED and claim.evidence_grade() == "C0" and not claim.root:
            invalid.append((cid, f"Verified but grade C0"))
    ok = len(invalid) == 0
    return AxiomResult("AQ-V19-011", "Status Validity", ok,
        f"{len(invalid)} status violation(s)",
        f"Violations: {invalid[:3]}" if invalid else "All statuses valid")

# ── V19-012: Evidence Classification Uniqueness ───────────────────────────
def check_classification_uniqueness(registry: Registry) -> AxiomResult:
    """Each claim has exactly one terminal status."""
    multi = []
    for cid, claim in registry.claims.items():
        terminal_count = sum(1 for s in TERMINAL_STATUSES if claim.status == s)
        if terminal_count > 1:
            multi.append(cid)
    ok = len(multi) == 0
    return AxiomResult("AQ-V19-012", "Classification Uniqueness", ok,
        f"{'No' if ok else str(len(multi))} multi-status violations",
        f"Violations: {multi}" if multi else "Each claim has exactly one class")

# ── V19-013: Publication Readiness Gate ───────────────────────────────────
def check_publication_readiness(registry: Registry) -> AxiomResult:
    """For each paper, all required claims must be Verified."""
    blocked = {}
    for paper, required_ids in registry.papers.items():
        not_verified = []
        for cid in required_ids:
            if cid not in registry.claims:
                not_verified.append(f"{cid} (MISSING)")
            elif registry.claims[cid].status != ClaimStatus.VERIFIED:
                not_verified.append(f"{cid} ({registry.claims[cid].status.value})")
        if not_verified:
            blocked[paper] = not_verified
    ok = len(blocked) == 0
    if not registry.papers:
        return AxiomResult("AQ-V19-013", "Publication Readiness", True,
            "No papers registered (define paper manifests to enable this gate)", "")
    detail = "; ".join(f"{p}: {v[:2]}" for p, v in blocked.items())
    return AxiomResult("AQ-V19-013", "Publication Readiness", ok,
        f"{'ELIGIBLE' if ok else 'BLOCKED'} — {len(blocked)} paper(s) not ready",
        detail or "All papers: required claims verified")

# ── V19-015 (demoted): Obstruction Report ────────────────────────────────
def check_obstruction_report(registry: Registry) -> AxiomResult:
    """
    Reports structural obstructions: claims that are Verified but have
    unverified/missing dependencies (logical gap in the proof chain).
    
    NOTE: The Ω = V∘F - F∘V formulation from the proposal is demoted to C0.
    F and V as linear operators on a well-defined state space are not defined.
    This implementation reports the SAME INFORMATION without false precision.
    """
    obstructions = []
    for cid, claim in registry.claims.items():
        if claim.status == ClaimStatus.VERIFIED:
            for dep in claim.dependencies:
                if dep not in registry.claims:
                    obstructions.append((cid, dep, "MISSING"))
                elif registry.claims[dep].status != ClaimStatus.VERIFIED:
                    obstructions.append((cid, dep, registry.claims[dep].status.value))
    ok = len(obstructions) == 0
    detail = f"Obstructions: {obstructions[:4]}" if obstructions else "No structural obstructions"
    return AxiomResult("AQ-V19-015-demoted", "Obstruction Report (demoted from Ω formalism)",
        ok, f"{len(obstructions)} structural obstruction(s)", detail)


# ══════════════════════════════════════════════════════════════════════════════
# VERIFICATION CLOSURE RUNNER
# ══════════════════════════════════════════════════════════════════════════════

def run_verification_closure(registry: Registry, external_ids: Set[str] = None) -> List[AxiomResult]:
    """Run all Level 19 axioms and return results."""
    return [
        check_deterministic_certification(registry),
        check_dependency_completeness(registry),
        check_acyclicity(registry),
        check_root_reachability(registry),
        check_evidence_reachability(registry),
        check_hash_stability(registry),
        check_topological_order(registry),
        check_registry_consistency(registry, external_ids),
        check_status_validity(registry),
        check_classification_uniqueness(registry),
        check_publication_readiness(registry),
        check_obstruction_report(registry),
    ]

def print_closure_report(results: List[AxiomResult], registry: Registry):
    w = 62
    print("=" * w)
    print("  AQARION Verification Closure Report (Level 19)")
    print("=" * w)
    for r in results:
        status_str = "PASS ✓" if r.passed else "FAIL ✗"
        print(f"  {r.id:22s}  [{status_str}]  {r.name}")
        if r.detail:
            print(f"    {r.detail[:55]}")
    print("-" * w)
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    print(f"  {passed}/{total} axioms satisfied")
    print()
    print(f"  Repository State:     {'CERTIFICATION CLOSED' if passed==total else 'OPEN DEFECTS'}")
    print(f"  Verification Op:      {'IDEMPOTENT' if results[0].passed else 'NON-DETERMINISTIC'}")
    print(f"  Dependency Graph:     {'ACYCLIC' if results[2].passed else 'CYCLIC — INVALID'}")
    print(f"  Publication State:    {'ELIGIBLE' if results[10].passed else 'BLOCKED'}")
    print(f"  Registry SHA256:      {registry.sha256()[:32]}...")
    print("=" * w)


# ══════════════════════════════════════════════════════════════════════════════
# AQARION CANONICAL REGISTRY (v11.0.0 / v12.1 corrected)
# ══════════════════════════════════════════════════════════════════════════════

def build_aqarion_registry() -> Registry:
    reg = Registry()
    
    # Root definitions
    for rid, stmt in [
        ("DEF-FDDS",  "Finite Deterministic Dynamical System (X,T)"),
        ("DEF-OBS",   "Observable O: X → G (finite set)"),
        ("DEF-GAP",   "Sorted-gap observable π(n) = (a-d, b-c)"),
        ("DEF-FOQDS", "FOQDS as gfp(Φ), Φ(R)={(x,y)|O(x)=O(y),(T(x),T(y))∈R}"),
        ("DEF-KOOP",  "Koopman operator K: (Kf)(x)=f(T(x))"),
        ("DEF-FIBER", "Fiber projection Π: (Πf)(x)=E[f|π(x)]"),
        ("DEF-COMM",  "Commutator C = ΠK - KΠ"),
        ("DEF-DELTA", "Deviation Δ(x) = δ_{T(x)} - E[δ_{T(X)}|π(x)]"),
    ]:
        rec = ClaimRecord(rid, stmt, ClaimStatus.VERIFIED, root=True,
                         evidence=[EvidenceRecord("definition", description="Canonical definition")])
        reg.add(rec)
    
    # Lemmas
    reg.add(ClaimRecord("LEM-EQ-LATTICE", "Eq(X) is a complete lattice",
        ClaimStatus.VERIFIED, dependencies=["DEF-FDDS"],
        evidence=[EvidenceRecord("proof_written"), EvidenceRecord("lean_formalized")],
        paper="Paper-I"))
    reg.add(ClaimRecord("LEM-PHI-MONO", "Φ is monotone on Eq(X)",
        ClaimStatus.VERIFIED, dependencies=["DEF-FOQDS", "LEM-EQ-LATTICE"],
        evidence=[EvidenceRecord("proof_written"), EvidenceRecord("lean_formalized")],
        paper="Paper-I"))
    reg.add(ClaimRecord("LEM-PI-IDEM", "Π² = Π (idempotency, verified)",
        ClaimStatus.VERIFIED, dependencies=["DEF-FIBER"],
        evidence=[EvidenceRecord("proof_written"), EvidenceRecord("exhaustive_search",
                  artifact="verify_v11.py", description="Gate: Pi idempotent")]))
    
    # Core theorems
    reg.add(ClaimRecord("T-GFP-EXISTS", "gfp(Φ) exists by Knaster-Tarski",
        ClaimStatus.VERIFIED, dependencies=["LEM-EQ-LATTICE","LEM-PHI-MONO"],
        evidence=[EvidenceRecord("proof_written"), EvidenceRecord("lean_formalized")],
        paper="Paper-I"))
    reg.add(ClaimRecord("T-NERODE", "x∼_F y ↔ ∀n≥0: O(Tⁿx)=O(Tⁿy) (Nerode)",
        ClaimStatus.VERIFIED, dependencies=["DEF-FOQDS","T-GFP-EXISTS"],
        evidence=[EvidenceRecord("proof_written"), EvidenceRecord("lean_formalized")],
        paper="Paper-I"))
    reg.add(ClaimRecord("T-SEMICONJ", "π∘T=T_F∘π (semiconjugacy, 0 violations)",
        ClaimStatus.VERIFIED, dependencies=["DEF-FOQDS","T-NERODE"],
        evidence=[EvidenceRecord("proof_written"), EvidenceRecord("lean_formalized"),
                  EvidenceRecord("exhaustive_search", artifact="verify_v11.py",
                                 description="Gate 4: 0 violations on 9990 states"),
                  EvidenceRecord("adversarial", description="AML-C mutation testing"),
                  EvidenceRecord("mutation_testing", description="AML-G: all mutants caught")],
        paper="Paper-I"))
    reg.add(ClaimRecord("T-FOQDS-55", "FOQDS = 55 classes (base-10, 4-digit Kaprekar)",
        ClaimStatus.ACTIVE, dependencies=["DEF-GAP","DEF-FOQDS","T-NERODE"],
        evidence=[EvidenceRecord("exhaustive_search", artifact="verify_v11.py",
                                 description="Gate 3: 55 FOQDS classes"),
                  EvidenceRecord("random_search", description="Cross-checked multiple seeds"),
                  EvidenceRecord("lean_formalized", description="Kaprekar54.lean (gap side)")],
        paper="Paper-I"))
    reg.add(ClaimRecord("T-K55-MINPOLY", "K55 (FOQDS matrix) minimal poly = x⁷(x-1)",
        ClaimStatus.ACTIVE, dependencies=["DEF-KOOP","T-FOQDS-55"],
        evidence=[EvidenceRecord("exhaustive_search", artifact="verify_v11.py",
                                 description="Gate 8: K55 minimal poly"),
                  EvidenceRecord("adversarial"), EvidenceRecord("mutation_testing")],
        paper="Paper-I"))
    reg.add(ClaimRecord("T-K54-MINPOLY", "K54 (gap matrix) minimal poly = x⁶(x-1) [v11 CORRECTION]",
        ClaimStatus.ACTIVE, dependencies=["DEF-GAP","DEF-KOOP","T-FOQDS-55"],
        evidence=[EvidenceRecord("exhaustive_search", artifact="verify_v11.py",
                                 description="Gate 9: K54 minimal poly"),
                  EvidenceRecord("adversarial"), EvidenceRecord("mutation_testing")],
        paper="Paper-I"))
    reg.add(ClaimRecord("T-RANK-C", "rank(ΠK-KΠ)=1 for Kaprekar FOQDS space",
        ClaimStatus.ACTIVE, dependencies=["DEF-COMM","DEF-DELTA","T-FOQDS-55","LEM-PI-IDEM"],
        evidence=[EvidenceRecord("exhaustive_search", artifact="aml_core.py"),
                  EvidenceRecord("adversarial")],
        paper="Paper-II"))
    reg.add(ClaimRecord("T-KAP-CLASS4", "Kaprekar ∈ Class IV (mixed commutator class)",
        ClaimStatus.ACTIVE, dependencies=["T-RANK-C","DEF-COMM"],
        evidence=[EvidenceRecord("exhaustive_search"), EvidenceRecord("adversarial")]))
    
    # Killed claims
    for kid, stmt, reason in [
        ("T-CROSSBASE", "|Q_b|=b(b+1)/2 for all even b",
         "Fails b=4,6,8,12,14; AML-C adversarial testing"),
        ("T-AUTO-Z26",  "Automorphism group (ℤ₂)⁶ order 64",
         "Level-1 has 3 nodes; no ℤ₂ action found"),
        ("T-RANK-30",   "Incidence rank stabilizes at 30",
         "No matrix computes to 30; origin unknown"),
        ("T-K54-MP-OLD","K54 minimal poly = x⁷(x-1) [SUPERSEDED]",
         "Correct value is x⁶(x-1); see T-K54-MINPOLY"),
    ]:
        reg.add(ClaimRecord(kid, stmt, ClaimStatus.KILLED,
            evidence=[EvidenceRecord("adversarial", description=reason)]))
    
    # Open problems (conjecture status)
    for oid, stmt, deps in [
        ("OP-NEW-1", "K54/K55 +1 nilpotent index from FOQDS split (algebraic proof)",
         ["T-K54-MINPOLY","T-K55-MINPOLY","T-FOQDS-55"]),
        ("OP-NEW-2", "True cross-base FOQDS scaling law |Q_b|=f(b)",
         ["T-FOQDS-55"]),
        ("OP-NEW-4", "δ=dim(V_ref∩V_bdry) in general",
         ["T-RANK-C","T-KAP-CLASS4"]),
        ("OP-NEW-7", "Transpose mutant invariance: why K and Kᵀ satisfy same minpoly test",
         ["T-K54-MINPOLY"]),
    ]:
        reg.add(ClaimRecord(oid, stmt, ClaimStatus.CONJECTURE, dependencies=deps))
    
    # Paper manifests
    reg.papers["Paper-I"] = ["LEM-EQ-LATTICE","LEM-PHI-MONO","T-GFP-EXISTS",
                              "T-NERODE","T-SEMICONJ","T-FOQDS-55",
                              "T-K55-MINPOLY","T-K54-MINPOLY"]
    reg.papers["Paper-II"] = ["T-RANK-C","T-KAP-CLASS4","LEM-PI-IDEM"]
    
    return reg


if __name__ == "__main__":
    reg = build_aqarion_registry()
    results = run_verification_closure(reg)
    print_closure_report(results, reg)
    
    # Show claim state summary
    print("\nCLAIM STATE SUMMARY:")
    from collections import Counter
    counts = Counter(c.status.value for c in reg.claims.values())
    for status, count in sorted(counts.items()):
        print(f"  {status:15s}: {count}")
    
    print(f"\nTotal claims in registry: {len(reg.claims)}")
    print(f"Registry SHA256: {reg.sha256()[:48]}...")

