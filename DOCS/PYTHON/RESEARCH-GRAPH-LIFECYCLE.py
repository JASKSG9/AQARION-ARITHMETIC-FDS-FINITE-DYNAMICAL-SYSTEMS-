"""aqarion.research_graph.derived_lifecycle
Lifecycle states are DERIVED from evidence, not assigned.

State = f(evidence_synthesis, graph_structure)

The transition log remains for audit, but current state is recomputed.
"""

from typing import Dict, List, Optional
from enum import Enum, auto

import sys
sys.path.insert(0, "/mnt/agents/output/aqarion")
from evidence.object import EvidenceStatus, EvidenceKind, EvidenceFamily, get_evidence_synthesis

class DerivedLifecycleState(Enum):
    IDEA = "idea"
    CONJECTURE = "conjecture"
    DERIVATION = "derivation"
    IMPLEMENTATION = "implementation"
    VERIFIED = "verified"
    FORMALIZED = "formalized"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class DerivedLifecycle:
    """Lifecycle state computed from evidence, not assigned."""
    
    def __init__(self, graph):
        self.graph = graph
    
    def compute_state(self, node_id: str) -> DerivedLifecycleState:
        """Compute lifecycle state from evidence and graph structure."""
        node = self.graph.get_node(node_id)
        if not node:
            return DerivedLifecycleState.IDEA
        
        # Check if archived/superseded
        if node.superseded or node.deprecated:
            return DerivedLifecycleState.ARCHIVED
        
        # Check for publication
        pubs = [e for e in self.graph.edges 
                if e.target == node_id and e.source.startswith("pub_")]
        if pubs:
            return DerivedLifecycleState.PUBLISHED
        
        # Get evidence synthesis
        evidence = get_evidence_synthesis(node_id)
        
        # Formal proof?
        formal = [e for e in evidence if e.family == EvidenceFamily.FORMAL and e.is_valid()]
        if formal:
            return DerivedLifecycleState.FORMALIZED
        
        # Verified?
        if any(e.confidence > 0.7 for e in evidence if e.is_valid()):
            return DerivedLifecycleState.VERIFIED
        
        # Implementation?
        impls = [e for e in self.graph.edges 
                 if e.target == node_id and e.edge_type.value == "implements"]
        if impls:
            return DerivedLifecycleState.IMPLEMENTATION
        
        # Derivation?
        derivs = [e for e in self.graph.edges 
                  if e.target == node_id and e.edge_type.value == "proves"]
        if derivs:
            return DerivedLifecycleState.DERIVATION
        
        # Conjecture?
        if node.content and len(node.content) > 10:
            return DerivedLifecycleState.CONJECTURE
        
        return DerivedLifecycleState.IDEA
    
    def compute_all(self) -> Dict[str, DerivedLifecycleState]:
        """Compute lifecycle for all nodes."""
        return {
            nid: self.compute_state(nid)
            for nid in self.graph.nodes
        }
    
    def get_publication_ready(self) -> List[str]:
        """Nodes ready for publication (FORMALIZED)."""
        states = self.compute_all()
        return [
            nid for nid, state in states.items()
            if state == DerivedLifecycleState.FORMALIZED
        ]
    
    def get_exploratory(self) -> List[str]:
        """Nodes still exploratory (IDEA or CONJECTURE)."""
        states = self.compute_all()
        return [
            nid for nid, state in states.items()
            if state in {DerivedLifecycleState.IDEA, DerivedLifecycleState.CONJECTURE}
        ]
    
    def explain_state(self, node_id: str) -> Dict:
        """Explain why a node is in its current state."""
        state = self.compute_state(node_id)
        evidence = get_evidence_synthesis(node_id)
        
        return {
            "node": node_id,
            "computed_state": state.value,
            "evidence_count": len(evidence),
            "recommendation": "Collect evidence" if not evidence else "Continue verification",
        }

def get_derived_lifecycle(graph):
    return DerivedLifecycle(graph)
