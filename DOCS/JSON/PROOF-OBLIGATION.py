
import sqlite3
import numpy as np
from datetime import datetime
from collections import defaultdict
import json, os

OUTPUT_DIR = "/mnt/agents/output"
AQARION_DIR = f"{OUTPUT_DIR}/aqarion_lab"

# ============================================================
# PHASE IV: PROOF-OBLIGATION ENGINE
# ============================================================

class ProofObligationEngine:
    """
    Automatically tracks what is missing for each theorem.
    No manually assigned percentages — everything derived from the graph.
    """
    
    OBLIGATION_TYPES = [
        "definition",           # All terms formally defined
        "assumptions",          # Hypotheses stated
        "proof",                # Mathematical proof exists
        "computational_verification",  # Code verifies claim
        "exhaustive_check",     # Finite cases checked
        "independent_impl",     # Second implementation
        "lean_formalization",   # Lean proof complete
        "constructive_witness", # Explicit example constructed
        "counterexample_search", # No counterexample found
        "literature_audit",     # Prior art checked
        "reproducibility",      # Deterministic replay
        "artifact_hashes",      # SHA256 for all outputs
    ]
    
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = f"{AQARION_DIR}/research_graph.db"
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
    
    def get_obligations(self, theorem_id):
        """
        Derive proof obligations automatically from the graph.
        Returns a dict: {obligation: status}
        """
        cursor = self.conn.cursor()
        
        # Get theorem node
        cursor.execute("SELECT * FROM nodes WHERE id = ?", (theorem_id,))
        theorem = cursor.fetchone()
        if not theorem:
            return {}
        
        theorem = dict(theorem)
        theorem['content'] = json.loads(theorem.get('content', '{}'))
        
        obligations = {}
        
        # 1. Definition: Does the theorem have a formal statement?
        obligations['definition'] = bool(theorem['content'].get('statement'))
        
        # 2. Assumptions: Are hypotheses recorded?
        obligations['assumptions'] = bool(theorem['content'].get('assumptions') or 
                                          theorem['content'].get('convention'))
        
        # 3. Proof: Is there a proof node pointing to this theorem?
        cursor.execute('''
            SELECT COUNT(*) FROM edges 
            WHERE target_id = ? AND edge_type = 'PROVES'
        ''', (theorem_id,))
        obligations['proof'] = cursor.fetchone()[0] > 0
        
        # 4. Computational verification: Are there experiments that generate this theorem?
        cursor.execute('''
            SELECT COUNT(*) FROM edges 
            WHERE target_id = ? AND edge_type = 'GENERATED_BY'
        ''', (theorem_id,))
        obligations['computational_verification'] = cursor.fetchone()[0] > 0
        
        # 5. Exhaustive check: Does content mention exhaustive verification?
        obligations['exhaustive_check'] = 'exhaustive' in str(theorem['content']).lower()
        
        # 6. Independent implementation: Multiple experiments?
        cursor.execute('''
            SELECT COUNT(*) FROM edges 
            WHERE target_id = ? AND edge_type = 'GENERATED_BY'
        ''', (theorem_id,))
        gen_count = cursor.fetchone()[0]
        obligations['independent_impl'] = gen_count >= 2
        
        # 7. Lean formalization: Is there a Lean object certifying this?
        cursor.execute('''
            SELECT COUNT(*) FROM edges 
            WHERE target_id = ? AND edge_type = 'CERTIFIED_BY'
        ''', (theorem_id,))
        lean_count = cursor.fetchone()[0]
        obligations['lean_formalization'] = lean_count > 0
        
        # 8. Constructive witness: For sharpness claims, is there a witness?
        obligations['constructive_witness'] = 'witness' in str(theorem['content']).lower() or \
                                               'constructive' in str(theorem['content']).lower()
        
        # 9. Counterexample search: Is there a counterexample node that was superseded?
        cursor.execute('''
            SELECT COUNT(*) FROM edges 
            WHERE target_id = ? AND edge_type = 'SUPERSEDES'
        ''', (theorem_id,))
        obligations['counterexample_search'] = cursor.fetchone()[0] > 0
        
        # 10. Literature audit: Is citation needed mentioned?
        obligations['literature_audit'] = not theorem['content'].get('citation_needed')
        
        # 11. Reproducibility: Are there artifacts with hashes?
        cursor.execute('''
            SELECT COUNT(*) FROM artifacts 
            WHERE node_id = ? AND sha256 != 'computed'
        ''', (theorem_id,))
        obligations['reproducibility'] = cursor.fetchone()[0] > 0
        
        # 12. Artifact hashes: Same as reproducibility
        obligations['artifact_hashes'] = obligations['reproducibility']
        
        return obligations
    
    def obligation_report(self, theorem_id):
        """Generate a human-readable obligation report."""
        obligations = self.get_obligations(theorem_id)
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM nodes WHERE id = ?", (theorem_id,))
        theorem = dict(cursor.fetchone())
        theorem['content'] = json.loads(theorem.get('content', '{}'))
        
        report = {
            "theorem_id": theorem_id,
            "title": theorem['title'],
            "status": theorem['status'],
            "obligations": obligations,
            "satisfied": sum(obligations.values()),
            "total": len(obligations),
            "completion": sum(obligations.values()) / len(obligations) if obligations else 0,
            "missing": [k for k, v in obligations.items() if not v]
        }
        return report
    
    def all_theorems_report(self):
        """Generate obligation reports for all theorems."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM nodes WHERE type = 'theorem'")
        theorems = [r[0] for r in cursor.fetchall()]
        
        reports = {}
        for tid in theorems:
            reports[tid] = self.obligation_report(tid)
        
        return reports
    
    def build_command(self, theorem_id):
        """
        Generate the sequence of commands to build a theorem package.
        """
        obligations = self.get_obligations(theorem_id)
        
        steps = []
        
        if not obligations.get('definition'):
            steps.append("aq define " + theorem_id)
        
        if not obligations.get('assumptions'):
            steps.append("aq assumptions " + theorem_id)
        
        if not obligations.get('proof'):
            steps.append("aq prove " + theorem_id)
        
        if not obligations.get('computational_verification'):
            steps.append("aq verify " + theorem_id)
        
        if not obligations.get('lean_formalization'):
            steps.append("aq lean " + theorem_id)
        
        if not obligations.get('reproducibility'):
            steps.append("aq hash " + theorem_id)
        
        return steps


# ============================================================
# RUN THE PROOF-OBLIGATION ENGINE
# ============================================================

print("=" * 70)
print("PHASE IV: PROOF-OBLIGATION ENGINE")
print("=" * 70)

engine = ProofObligationEngine()

# Generate reports for all theorems
reports = engine.all_theorems_report()

print("\n📋 PROOF OBLIGATION REPORTS")
print("=" * 70)

for tid, report in reports.items():
    print(f"\n📐 {tid}: {report['title']}")
    print(f"   Status: {report['status']} | Completion: {report['completion']*100:.0f}%")
    print(f"   Satisfied: {report['satisfied']}/{report['total']}")
    
    if report['missing']:
        print(f"   Missing obligations:")
        for miss in report['missing']:
            print(f"      □ {miss}")
    else:
        print(f"   ✅ All obligations satisfied")
    
    # Build steps
    steps = engine.build_command(tid)
    if steps:
        print(f"   Build steps:")
        for step in steps:
            print(f"      $ {step}")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

total_obligations = sum(r['total'] for r in reports.values())
total_satisfied = sum(r['satisfied'] for r in reports.values())
print(f"\nTotal obligations: {total_satisfied}/{total_obligations} ({100*total_satisfied/total_obligations:.0f}%)")

for tid, report in reports.items():
    bar = "█" * int(report['completion'] * 20) + "░" * (20 - int(report['completion'] * 20))
    print(f"   {tid:25s} {bar} {report['completion']*100:.0f}%")

# Save obligation registry
obligation_registry = {
    "generated_at": datetime.now().isoformat(),
    "engine_version": "1.0",
    "obligation_types": engine.OBLIGATION_TYPES,
    "theorems": reports
}

registry_path = f"{AQARION_DIR}/obligation_registry.json"
with open(registry_path, 'w') as f:
    json.dump(obligation_registry, f, indent=2)
print(f"\n📄 Obligation registry saved: {registry_path}")

engine.conn.close()======================================================================
PHASE IV: PROOF-OBLIGATION ENGINE
======================================================================

📋 PROOF OBLIGATION REPORTS
======================================================================

📐 AQ-THM-DR: Defect Rank Theorem: rank(D_Π) ≤ m-1
   Status: verified | Completion: 50%
   Satisfied: 6/12
   Missing obligations:
      □ computational_verification
      □ exhaustive_check
      □ independent_impl
      □ lean_formalization
      □ constructive_witness
      □ literature_audit
   Build steps:
      $ aq verify AQ-THM-DR
      $ aq lean AQ-THM-DR

📐 AQ-THM-DR-SHARP: Sharpness: Generic K achieves rank m-1
   Status: conjecture | Completion: 17%
   Satisfied: 2/12
   Missing obligations:
      □ assumptions
      □ proof
      □ computational_verification
      □ exhaustive_check
      □ independent_impl
      □ lean_formalization
      □ constructive_witness
      □ counterexample_search
      □ reproducibility
      □ artifact_hashes
   Build steps:
      $ aq assumptions AQ-THM-DR-SHARP
      $ aq prove AQ-THM-DR-SHARP
      $ aq verify AQ-THM-DR-SHARP
      $ aq lean AQ-THM-DR-SHARP
      $ aq hash AQ-THM-DR-SHARP

📐 AQ-THM-AFFINE: Kaprekar Affine Lift Identity
   Status: verified | Completion: 42%
   Satisfied: 5/12
   Missing obligations:
      □ assumptions
      □ computational_verification
      □ exhaustive_check
      □ independent_impl
      □ lean_formalization
      □ constructive_witness
      □ counterexample_search
   Build steps:
      $ aq assumptions AQ-THM-AFFINE
      $ aq verify AQ-THM-AFFINE
      $ aq lean AQ-THM-AFFINE

📐 AQ-THM-DEPTH: Depth Reduction: ν(X) - ν(G) = 1
   Status: conjecture | Completion: 17%
   Satisfied: 2/12
   Missing obligations:
      □ assumptions
      □ proof
      □ computational_verification
      □ exhaustive_check
      □ independent_impl
      □ lean_formalization
      □ constructive_witness
      □ counterexample_search
      □ reproducibility
      □ artifact_hashes
   Build steps:
      $ aq assumptions AQ-THM-DEPTH
      $ aq prove AQ-THM-DEPTH
      $ aq verify AQ-THM-DEPTH
      $ aq lean AQ-THM-DEPTH
      $ aq hash AQ-THM-DEPTH

📐 AQ-THM-EXACT: Exact Quotient Criterion: D_Π = 0 ⟺ forward invariant
   Status: proven | Completion: 42%
   Satisfied: 5/12
   Missing obligations:
      □ assumptions
      □ computational_verification
      □ exhaustive_check
      □ independent_impl
      □ lean_formalization
      □ constructive_witness
      □ counterexample_search
   Build steps:
      $ aq assumptions AQ-THM-EXACT
      $ aq verify AQ-THM-EXACT
      $ aq lean AQ-THM-EXACT

======================================================================
SUMMARY
======================================================================

Total obligations: 20/60 (33%)
   AQ-THM-DR                 ██████████░░░░░░░░░░ 50%
   AQ-THM-DR-SHARP           ███░░░░░░░░░░░░░░░░░ 17%
   AQ-THM-AFFINE             ████████░░░░░░░░░░░░ 42%
   AQ-THM-DEPTH              ███░░░░░░░░░░░░░░░░░ 17%
   AQ-THM-EXACT              ████████░░░░░░░░░░░░ 42%

📄 Obligation registry saved: /mnt/agents/output/aqarion_lab/obligation_registry.json
