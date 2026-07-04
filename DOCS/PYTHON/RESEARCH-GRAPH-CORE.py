"""aqarion.research_graph.core
Canonical Research Graph — Single source of truth.

Nodes and edges are the primary objects. Everything else (lifecycle, trust, debt, readiness) is derived.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple, Any
from enum import Enum, auto
from datetime import datetime, timezone
import hashlib
import json

class NodeType(Enum):
    DEFINITION = "definition"
    THEOREM = "theorem"
    LEMMA = "lemma"
    CONJECTURE = "conjecture"
    EXPERIMENT = "experiment"
    IMPLEMENTATION = "implementation"
    EVIDENCE = "evidence"
    WITNESS = "witness"
    ORACLE_RUN = "oracle_run"
    LEAN_PROOF = "lean_proof"
    PUBLICATION = "publication"
    RELEASE = "release"
    ASSUMPTION = "assumption"
    COUNTEREXAMPLE = "counterexample"

class EdgeType(Enum):
    DEPENDS_ON = "depends_on"
    PROVES = "proves"
    IMPLEMENTS = "implements"
    VERIFIES = "verifies"
    SUPPORTS = "supports"
    REPRODUCES = "reproduces"
    PUBLISHES = "publishes"
    REFUTES = "refutes"
    SUPERSEDES = "supersedes"

@dataclass
class ResearchNode:
    id: str
    node_type: NodeType
    title: str
    content: str = ""
    certified: bool = False
    deprecated: bool = False
    superseded: bool = False
    metadata: Dict = field(default_factory=dict)
    created: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class ResearchEdge:
    id: str
    source: str
    target: str
    edge_type: EdgeType
    created: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ResearchGraph:
    """Canonical Research Graph — single source of truth."""
    
    def __init__(self):
        self.nodes: Dict[str, ResearchNode] = {}
        self.edges: List[ResearchEdge] = []
        self.evidence_map: Dict[str, List[str]] = {}  # claim_id -> evidence_ids
    
    def add_node(self, node: ResearchNode):
        self.nodes[node.id] = node
    
    def add_edge(self, edge: ResearchEdge):
        self.edges.append(edge)
    
    def get_node(self, node_id: str) -> Optional[ResearchNode]:
        return self.nodes.get(node_id)
    
    def get_dependencies(self, node_id: str) -> List[str]:
        return [e.source for e in self.edges if e.target == node_id]
    
    def get_evidence(self, claim_id: str) -> List[str]:
        return self.evidence_map.get(claim_id, [])
    
    def to_dict(self) -> Dict:
        return {
            "nodes": {nid: {
                "id": n.id,
                "type": n.node_type.value,
                "title": n.title,
                "certified": n.certified,
                "deprecated": n.deprecated,
                "superseded": n.superseded,
            } for nid, n in self.nodes.items()},
            "edges": [{
                "id": e.id,
                "source": e.source,
                "target": e.target,
                "type": e.edge_type.value,
            } for e in self.edges],
        }
    
    def save(self, path: str):
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

# Global graph instance
_GRAPH = ResearchGraph()

def get_graph() -> ResearchGraph:
    """Singleton access to the Research Graph."""
    return _GRAPH

# Bootstrap some core nodes
def bootstrap_graph():
    g = get_graph()
    
    # Core definitions
    g.add_node(ResearchNode("D1", NodeType.DEFINITION, "Finite State Space", "X finite", True))
    g.add_node(ResearchNode("D2", NodeType.DEFINITION, "Transition Function", "T: X → X deterministic", True))
    g.add_node(ResearchNode("D3", NodeType.DEFINITION, "Observable", "O: X → Σ", True))
    g.add_node(ResearchNode("D4", NodeType.DEFINITION, "Partition", "Π of X into blocks", True))
    
    # Theorems
    g.add_node(ResearchNode("T1", NodeType.THEOREM, "Nilpotent Obstruction Law", "𝓘² = 0", True))
    g.add_node(ResearchNode("T2", NodeType.THEOREM, "Invariant Equivalence", "D_Π = 0 ⇔ invariant partition", True))
    g.add_node(ResearchNode("T3", NodeType.THEOREM, "Kernel-Image Identity", "ker(𝓘) = Im(P)", False))
    
    # Edges
    g.add_edge(ResearchEdge("E1", "D1", "T1", EdgeType.DEPENDS_ON))
    g.add_edge(ResearchEdge("E2", "D2", "T1", EdgeType.DEPENDS_ON))
    g.add_edge(ResearchEdge("E3", "T1", "T2", EdgeType.PROVES))
    
    print("Research Graph bootstrapped with core nodes and edges.")

bootstrap_graph()
