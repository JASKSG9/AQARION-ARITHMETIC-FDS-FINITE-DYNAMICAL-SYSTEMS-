import { useState } from "react";

// ══════════════════════════════════════════════════════════════════════════════
// AQARION — LEVEL 19: VERIFICATION CLOSURE & DEPENDENCY INTEGRITY
// Node #10878 · 2026-06-21
// Prove First · Predict Second · No Free Parameters
// ══════════════════════════════════════════════════════════════════════════════

const C = {
  bg: "#070a10", panel: "#0c1018", panel2: "#101520",
  border: "#182030", accent: "#38bdf8", gold: "#f59e0b",
  green: "#34d399", red: "#f87171", orange: "#fb923c",
  purple: "#a78bfa", cyan: "#22d3ee", muted: "#475569",
  text: "#e2e8f0", textDim: "#64748b",
};

// ── REAL RUN RESULTS (from actual execution) ───────────────
const AXIOM_RESULTS = [
  { id:"AQ-V19-002", name:"Deterministic Certification",
    passed:true, msg:"SHA256 identical regardless of claim processing order",
    detail:"Forward: 17d2d453b0f68ccd...  Reversed: 17d2d453b0f68ccd...",
    note:"Order-independence is stronger than idempotence. Catches hidden state bugs." },
  { id:"AQ-V19-003", name:"Dependency Completeness",
    passed:true, msg:"All 31 dependency references resolve to existing claims",
    detail:"27 nodes, 31 edges",
    note:"Every claim referenced as a dependency exists in the registry." },
  { id:"AQ-V19-004", name:"No Cyclic Dependencies",
    passed:true, msg:"Dependency graph is acyclic — no circular proofs",
    detail:"Kahn topological sort completes successfully",
    note:"A cycle would invalidate everything downstream. Most critical axiom." },
  { id:"AQ-V19-005", name:"Root Reachability",
    passed:true, msg:"All active/verified claims reachable from root definitions",
    detail:"Roots: DEF-COMM, DEF-DELTA, DEF-FDDS, DEF-FIBER, DEF-FOQDS, DEF-GAP, DEF-KOOP, DEF-OBS",
    note:"Killed claims exempt: they are anti-theorems, not theorems. Design insight from failure." },
  { id:"AQ-V19-006", name:"Evidence Reachability",
    passed:true, msg:"All verified claims have executable evidence artifacts",
    detail:"verify_v11.py and aml_core.py listed as artifacts in evidence chains",
    note:"Prevents 'verified by computation' claims with no actual script." },
  { id:"AQ-V19-007", name:"Hash Stability",
    passed:true, msg:"SHA256(claim_state.json) stable across 3 executions",
    detail:"17d2d453b0f68ccd8307c0cd... (no timestamps, UUIDs, or random seeds in output)",
    note:"Ensure canonical serialization: sorted keys, no execution-time metadata." },
  { id:"AQ-V19-009", name:"Topological Execution Order",
    passed:true, msg:"Valid execution order exists and is consistent",
    detail:"DEF-* → LEM-* → T-SEMICONJ → T-FOQDS-55 → T-K55-MINPOLY ...",
    note:"Tests the runtime scheduler, not just graph structure. Distinct from V19-004." },
  { id:"AQ-V19-010", name:"Registry Consistency",
    passed:true, msg:"27 unique claim IDs, no duplicates",
    detail:"Machine registry (claim_state.json) consistent with human registry",
    note:"Catches documentation drift between CHECKPOINT.md and code." },
  { id:"AQ-V19-011", name:"Status Validity",
    passed:true, msg:"All statuses valid after root-definition exemption applied",
    detail:"Root definitions (root=True) exempt from grade≥C2 requirement",
    note:"Design insight: axioms ≠ theorems. Definitions are verified by definition, not computation." },
  { id:"AQ-V19-012", name:"Classification Uniqueness",
    passed:true, msg:"Each claim has exactly one status class",
    detail:"No claim has multiple conflicting statuses",
    note:"Statuses: Conjecture|Active|Verified|Rejected|Counterexample|Deprecated|Killed" },
  { id:"AQ-V19-013", name:"Publication Readiness Gate",
    passed:false, msg:"Paper I BLOCKED — 3 required claims not yet Verified",
    detail:"T-FOQDS-55 (Active/C2), T-K55-MINPOLY (Active/AV), T-K54-MINPOLY (Active/AV)",
    note:"This failure is CORRECT and should NOT be fixed with a workaround. Paper I needs algebraic proofs." },
  { id:"AQ-V19-015", name:"Obstruction Report (demoted from Ω formalism)",
    passed:true, msg:"No structural obstructions: no verified claim has unverified parents",
    detail:"Ω = V∘F − F∘V formulation demoted: F undefined as linear operator",
    note:"Same information delivered without false mathematical precision." },
];

const CLAIM_REGISTRY = [
  // Roots
  {id:"DEF-FDDS",  stmt:"Finite Deterministic Dynamical System (X,T)", status:"Verified", grade:"DEF", root:true, paper:null},
  {id:"DEF-OBS",   stmt:"Observable O: X → G", status:"Verified", grade:"DEF", root:true, paper:null},
  {id:"DEF-GAP",   stmt:"Sorted-gap observable π(n) = (a−d, b−c)", status:"Verified", grade:"DEF", root:true, paper:null},
  {id:"DEF-FOQDS", stmt:"FOQDS as gfp(Φ)", status:"Verified", grade:"DEF", root:true, paper:null},
  {id:"DEF-KOOP",  stmt:"Koopman operator K", status:"Verified", grade:"DEF", root:true, paper:null},
  {id:"DEF-FIBER", stmt:"Fiber projection Π", status:"Verified", grade:"DEF", root:true, paper:null},
  {id:"DEF-COMM",  stmt:"Commutator C = ΠK − KΠ", status:"Verified", grade:"DEF", root:true, paper:null},
  {id:"DEF-DELTA", stmt:"Deviation Δ(x) = δ_T(x) − E[δ_T(X)|π(x)]", status:"Verified", grade:"DEF", root:true, paper:null},
  // Lemmas
  {id:"LEM-EQ-LATTICE",stmt:"Eq(X) is a complete lattice", status:"Verified", grade:"PV", root:false, paper:"Paper-I"},
  {id:"LEM-PHI-MONO",  stmt:"Φ is monotone on Eq(X)", status:"Verified", grade:"PV", root:false, paper:"Paper-I"},
  {id:"LEM-PI-IDEM",   stmt:"Π² = Π (idempotency)", status:"Verified", grade:"P+C2", root:false, paper:"Paper-II"},
  // Theorems
  {id:"T-GFP-EXISTS",stmt:"gfp(Φ) exists by Knaster-Tarski", status:"Verified", grade:"PV", root:false, paper:"Paper-I"},
  {id:"T-NERODE",    stmt:"Nerode characterization of ∼_F", status:"Verified", grade:"PV", root:false, paper:"Paper-I"},
  {id:"T-SEMICONJ",  stmt:"Semiconjugacy π∘T=T_F∘π (0 violations)", status:"Verified", grade:"PV", root:false, paper:"Paper-I"},
  {id:"T-FOQDS-55",  stmt:"FOQDS = 55 classes (Kaprekar)", status:"Active", grade:"C2", root:false, paper:"Paper-I"},
  {id:"T-K55-MINPOLY",stmt:"K55 minimal poly = x⁷(x−1)", status:"Active", grade:"AV", root:false, paper:"Paper-I"},
  {id:"T-K54-MINPOLY",stmt:"K54 minimal poly = x⁶(x−1) [v11]", status:"Active", grade:"AV", root:false, paper:"Paper-I"},
  {id:"T-RANK-C",    stmt:"rank(ΠK−KΠ) = 1 for Kaprekar", status:"Active", grade:"AV", root:false, paper:"Paper-II"},
  {id:"T-KAP-CLASS4",stmt:"Kaprekar ∈ Class IV (mixed)", status:"Active", grade:"AV", root:false, paper:"Paper-II"},
  // Killed
  {id:"T-CROSSBASE", stmt:"|Q_b|=b(b+1)/2 — ALL EVEN BASES", status:"Killed", grade:"—", root:false, paper:null},
  {id:"T-AUTO-Z26",  stmt:"Automorphism group (ℤ₂)⁶ order 64", status:"Killed", grade:"—", root:false, paper:null},
  {id:"T-RANK-30",   stmt:"Incidence rank stabilizes at 30", status:"Killed", grade:"—", root:false, paper:null},
  {id:"T-K54-MP-OLD",stmt:"K54 minimal poly = x⁷(x−1) [SUPERSEDED]", status:"Killed", grade:"—", root:false, paper:null},
  // Conjectures
  {id:"OP-NEW-1",    stmt:"K54/K55 +1 nilpotent index (algebraic proof)", status:"Conjecture", grade:"C0", root:false, paper:null},
  {id:"OP-NEW-2",    stmt:"True cross-base scaling law |Q_b|=f(b)", status:"Conjecture", grade:"C0", root:false, paper:null},
  {id:"OP-NEW-4",    stmt:"δ=dim(V_ref∩V_bdry) in general", status:"Conjecture", grade:"C0", root:false, paper:null},
  {id:"OP-NEW-7",    stmt:"Transpose mutant invariance mechanism", status:"Conjecture", grade:"C0", root:false, paper:null},
];

const DEP_GRAPH = [
  ["DEF-FDDS","LEM-EQ-LATTICE"],["DEF-FOQDS","LEM-PHI-MONO"],["LEM-EQ-LATTICE","LEM-PHI-MONO"],
  ["LEM-EQ-LATTICE","T-GFP-EXISTS"],["LEM-PHI-MONO","T-GFP-EXISTS"],
  ["DEF-FOQDS","T-NERODE"],["T-GFP-EXISTS","T-NERODE"],
  ["DEF-FOQDS","T-SEMICONJ"],["T-NERODE","T-SEMICONJ"],
  ["DEF-GAP","T-FOQDS-55"],["DEF-FOQDS","T-FOQDS-55"],["T-NERODE","T-FOQDS-55"],
  ["DEF-KOOP","T-K55-MINPOLY"],["T-FOQDS-55","T-K55-MINPOLY"],
  ["DEF-GAP","T-K54-MINPOLY"],["DEF-KOOP","T-K54-MINPOLY"],["T-FOQDS-55","T-K54-MINPOLY"],
  ["DEF-COMM","T-RANK-C"],["DEF-DELTA","T-RANK-C"],["T-FOQDS-55","T-RANK-C"],["LEM-PI-IDEM","T-RANK-C"],
  ["T-RANK-C","T-KAP-CLASS4"],["DEF-COMM","T-KAP-CLASS4"],
  ["T-K54-MINPOLY","OP-NEW-1"],["T-K55-MINPOLY","OP-NEW-1"],["T-FOQDS-55","OP-NEW-1"],
  ["T-FOQDS-55","OP-NEW-2"],["T-RANK-C","OP-NEW-4"],["T-KAP-CLASS4","OP-NEW-4"],
  ["T-K54-MINPOLY","OP-NEW-7"],
];

const PAPER_MANIFESTS = {
  "Paper-I": {
    required: ["LEM-EQ-LATTICE","LEM-PHI-MONO","T-GFP-EXISTS","T-NERODE","T-SEMICONJ",
               "T-FOQDS-55","T-K55-MINPOLY","T-K54-MINPOLY"],
    status: "BLOCKED",
    blocking: ["T-FOQDS-55 (Active/C2)","T-K55-MINPOLY (Active/AV)","T-K54-MINPOLY (Active/AV)"],
    path_to_eligible: "Prove T-FOQDS-55 algebraically via DFA minimization, and T-K55/K54-MINPOLY from graph structure."
  },
  "Paper-II": {
    required: ["T-RANK-C","T-KAP-CLASS4","LEM-PI-IDEM"],
    status: "BLOCKED",
    blocking: ["T-RANK-C (Active/AV)","T-KAP-CLASS4 (Active/AV)"],
    path_to_eligible: "Prove rank(C)=1 algebraically (coupling term δ proof). Prove Kaprekar ∈ Class IV formally."
  }
};

const DESIGN_INSIGHTS = [
  {
    id:"INS-1",
    title:"Killed claims are anti-theorems",
    finding:"V19-005 originally failed because killed claims had no root ancestry. Fix: exempt KILLED/DEPRECATED from reachability. Design insight: the registry needs two spaces — theorem space (DAG-governed) and anti-theorem space (adversarially terminated).",
    impact:"HIGH",
  },
  {
    id:"INS-2",
    title:"Definitions ≠ Theorems in evidence requirements",
    finding:"V19-011 failed because DEF-* claims are Verified but grade=C0. Fix: root=True exempts from grade check. Axioms are verified by stipulation, not computation. This is a real type distinction the system needs.",
    impact:"HIGH",
  },
  {
    id:"INS-3",
    title:"Paper I is blocked — this is the governance system working correctly",
    finding:"T-FOQDS-55, T-K55-MINPOLY, T-K54-MINPOLY are Active (C2/AV), not Verified. Paper I requires Verified claims. DO NOT workaround. Either prove them or submit as 'computational investigation' with explicit claim status labels.",
    impact:"CRITICAL",
  },
  {
    id:"INS-4",
    title:"Ω = V∘F − F∘V formulation is C0, not a theorem",
    finding:"V19-015 claimed an obstruction operator Ω. F is not defined as a linear operator on any specified state space. The actual property (verified claims with unverified parents) is real and implementable without the Ω notation. Demoted to 'Obstruction Report'.",
    impact:"MEDIUM",
  },
];

// ── COMPONENTS ─────────────────────────────────────────────

function Badge({color, children, size}) {
  const p = {green:["#0d2e1e","#34d399"],red:["#2e0d0d","#f87171"],
    gold:["#2e1e0d","#f59e0b"],blue:["#0d1e2e","#38bdf8"],
    orange:["#2e180d","#fb923c"],purple:["#1a0d2e","#a78bfa"],
    cyan:["#0d2428","#22d3ee"],gray:["#1a1a2e","#64748b"]};
  const [bg,fg] = p[color]||p.blue;
  return <span style={{background:bg,border:`1px solid ${fg}`,color:fg,
    borderRadius:4,padding:`2px ${size==="lg"?"12":"8"}px`,
    fontSize:size==="lg"?12:10,fontWeight:700,letterSpacing:"0.06em",fontFamily:"monospace"}}>
    {children}</span>;
}

function StatusBadge({status, grade}) {
  const cfg = {
    Verified:   {color:"green"},  Active:     {color:"blue"},
    Conjecture: {color:"purple"}, Killed:     {color:"red"},
    BLOCKED:    {color:"red"},    ELIGIBLE:   {color:"green"},
    DEF:        {color:"cyan"},
  };
  const c = cfg[status]||cfg.Active;
  return <Badge color={c.color}>{grade || status}</Badge>;
}

function Card({children, highlight, style}) {
  return <div style={{background:C.panel,border:`1px solid ${highlight||C.border}`,
    borderRadius:10,padding:"16px 20px",marginBottom:12,...(style||{})}}>{children}</div>;
}

// ── AXIOM RESULT ROW ──────────────────────────────────────
function AxiomRow({result, expanded, onToggle}) {
  return (
    <div style={{marginBottom:8}}>
      <div onClick={onToggle} style={{cursor:"pointer",background:C.panel2,
        border:`1px solid ${result.passed?C.green+"44":C.red+"66"}`,
        borderRadius:8,padding:"12px 16px",display:"flex",alignItems:"center",gap:12}}>
        <div style={{width:28,height:28,borderRadius:"50%",display:"flex",
          alignItems:"center",justifyContent:"center",flexShrink:0,
          background:`${result.passed?C.green:C.red}22`,
          border:`2px solid ${result.passed?C.green:C.red}`,
          color:result.passed?C.green:C.red,fontSize:14,fontWeight:900}}>
          {result.passed?"✓":"✗"}
        </div>
        <div style={{flex:1}}>
          <div style={{display:"flex",gap:8,alignItems:"center",flexWrap:"wrap"}}>
            <span style={{fontFamily:"monospace",color:C.textDim,fontSize:11}}>{result.id}</span>
            <span style={{color:C.text,fontWeight:700,fontSize:13}}>{result.name}</span>
            {!result.passed && <Badge color="red">BLOCKED</Badge>}
          </div>
          <div style={{color:result.passed?C.textDim:C.red,fontSize:12,marginTop:2}}>
            {result.msg}
          </div>
        </div>
        <div style={{color:C.muted,fontSize:12}}>{expanded?"▲":"▼"}</div>
      </div>
      {expanded && (
        <div style={{background:C.panel,border:`1px solid ${C.border}`,
          borderRadius:"0 0 8px 8px",padding:"12px 16px",marginTop:-4}}>
          <div style={{fontFamily:"monospace",fontSize:12,color:C.accent,marginBottom:8}}>
            {result.detail}
          </div>
          <div style={{color:C.textDim,fontSize:12,borderLeft:`3px solid ${C.gold}`,paddingLeft:10}}>
            {result.note}
          </div>
        </div>
      )}
    </div>
  );
}

// ── REGISTRY TABLE ────────────────────────────────────────
function RegistryTable({filter}) {
  const filtered = filter ? CLAIM_REGISTRY.filter(c =>
    c.status === filter || (filter === "root" && c.root)) : CLAIM_REGISTRY;
  const statusColors = {Verified:C.green,Active:C.accent,Conjecture:C.purple,Killed:C.red};

  return (
    <div style={{fontFamily:"monospace",fontSize:11,maxHeight:420,overflowY:"auto"}}>
      <div style={{display:"grid",gridTemplateColumns:"130px 60px 60px 80px 1fr",
        gap:"0 8px",color:C.textDim,borderBottom:`1px solid ${C.border}`,
        paddingBottom:6,marginBottom:6,position:"sticky",top:0,background:C.panel}}>
        <span>ID</span><span>Status</span><span>Grade</span><span>Paper</span><span>Statement</span>
      </div>
      {filtered.map(c => (
        <div key={c.id} style={{display:"grid",
          gridTemplateColumns:"130px 60px 60px 80px 1fr",
          gap:"0 8px",marginBottom:4,opacity:c.status==="Killed"?0.5:1}}>
          <span style={{color:c.root?C.cyan:C.text,
            textDecoration:c.status==="Killed"?"line-through":"none",
            fontSize:10}}>{c.id}</span>
          <span style={{color:statusColors[c.status]||C.textDim,fontSize:10,fontWeight:700}}>
            {c.status.slice(0,7)}</span>
          <span style={{color:c.grade==="DEF"?C.cyan:c.grade==="PV"?C.green:
            c.grade==="AV"?C.orange:c.grade==="C2"?C.accent:C.textDim,fontSize:10}}>
            {c.grade}</span>
          <span style={{color:C.textDim,fontSize:9}}>{c.paper||"—"}</span>
          <span style={{color:C.textDim,overflow:"hidden",textOverflow:"ellipsis",
            whiteSpace:"nowrap",fontSize:10}}>{c.stmt}</span>
        </div>
      ))}
      <div style={{color:C.textDim,fontSize:10,marginTop:8,borderTop:`1px solid ${C.border}`,paddingTop:6}}>
        Showing {filtered.length} of {CLAIM_REGISTRY.length} claims
      </div>
    </div>
  );
}

// ── DEP GRAPH MINI VIZ ────────────────────────────────────
function DepGraphViz() {
  const levels = [
    {y:20,  nodes:["DEF-FDDS","DEF-OBS","DEF-GAP","DEF-FOQDS","DEF-KOOP","DEF-FIBER","DEF-COMM","DEF-DELTA"], c:C.cyan},
    {y:90,  nodes:["LEM-EQ-LATTICE","LEM-PHI-MONO","LEM-PI-IDEM"], c:C.purple},
    {y:160, nodes:["T-GFP-EXISTS","T-NERODE","T-SEMICONJ"], c:C.green},
    {y:230, nodes:["T-FOQDS-55","T-K55-MINPOLY","T-K54-MINPOLY"], c:C.accent},
    {y:300, nodes:["T-RANK-C","T-KAP-CLASS4"], c:C.gold},
    {y:370, nodes:["OP-NEW-1","OP-NEW-2","OP-NEW-4","OP-NEW-7"], c:C.purple},
  ];

  const W = 500;
  const nodePos = {};
  levels.forEach(lv => {
    const n = lv.nodes.length;
    lv.nodes.forEach((id, i) => {
      nodePos[id] = { x: (i+1) * W / (n+1), y: lv.y + 18 };
    });
  });

  const killed = ["T-CROSSBASE","T-AUTO-Z26","T-RANK-30","T-K54-MP-OLD"];

  return (
    <div style={{overflowX:"auto"}}>
      <svg viewBox={`0 0 ${W} 420`} style={{width:"100%",display:"block",maxWidth:W}}>
        {/* Edges */}
        {DEP_GRAPH.slice(0, 20).map(([src,dst], i) => {
          const s = nodePos[src], d = nodePos[dst];
          if (!s || !d) return null;
          return <line key={i} x1={s.x} y1={s.y} x2={d.x} y2={d.y}
            stroke={C.border} strokeWidth={1} opacity={0.6} />;
        })}
        {/* Nodes by level */}
        {levels.map((lv, li) => (
          lv.nodes.map((id, ni) => {
            const pos = nodePos[id];
            if (!pos) return null;
            const label = id.replace("DEF-","").replace("LEM-","").replace("T-","").replace("OP-","");
            return (
              <g key={id}>
                <circle cx={pos.x} cy={pos.y} r={16} fill={C.panel}
                  stroke={lv.c} strokeWidth={1.5} />
                <text x={pos.x} y={pos.y+4} fill={lv.c} fontSize={7}
                  textAnchor="middle" fontFamily="monospace">{label.slice(0,8)}</text>
              </g>
            );
          })
        ))}
        {/* Level labels */}
        {levels.map((lv, i) => (
          <text key={i} x={10} y={lv.y+22} fill={C.muted} fontSize={8}
            fontFamily="monospace">L{i}</text>
        ))}
        {/* Killed cluster */}
        <rect x={5} y={380} width={W-10} height={30} fill="rgba(248,113,113,0.05)"
          stroke={C.red+"44"} strokeWidth={1} rx={4} />
        <text x={W/2} y={398} fill={C.red} fontSize={8} textAnchor="middle"
          fontFamily="monospace">KILLED: T-CROSSBASE · T-AUTO-Z26 · T-RANK-30 · T-K54-MP-OLD</text>
      </svg>
    </div>
  );
}

// ── MAIN APP ──────────────────────────────────────────────
export default function App() {
  const [tab, setTab] = useState("report");
  const [expandedAxiom, setExpandedAxiom] = useState(null);
  const [regFilter, setRegFilter] = useState(null);

  const tabs = [
    {id:"report",   label:"Closure Report"},
    {id:"insights", label:"Design Insights"},
    {id:"registry", label:"Claim Registry"},
    {id:"depgraph", label:"Dep Graph"},
    {id:"papers",   label:"Paper Status"},
  ];

  const passed = AXIOM_RESULTS.filter(r=>r.passed).length;
  const total = AXIOM_RESULTS.length;

  return (
    <div style={{background:C.bg,minHeight:"100vh",color:C.text,
      fontFamily:"'Inter',system-ui,sans-serif",
      maxWidth:920,margin:"0 auto",padding:"28px 20px"}}>

      {/* HEADER */}
      <div style={{marginBottom:28}}>
        <div style={{display:"flex",gap:14,alignItems:"flex-start",marginBottom:14}}>
          <div style={{width:6,height:52,background:`linear-gradient(180deg,${C.green},${C.cyan})`,
            borderRadius:3,flexShrink:0}} />
          <div style={{flex:1}}>
            <div style={{color:C.green,fontSize:10,fontWeight:700,letterSpacing:"0.2em",
              textTransform:"uppercase",marginBottom:4}}>LEVEL 19 · VERIFICATION CLOSURE</div>
            <h1 style={{color:C.text,fontSize:24,fontWeight:900,margin:"0 0 4px",
              letterSpacing:"-0.03em"}}>Dependency Integrity & Governance</h1>
            <p style={{color:C.textDim,fontSize:12,margin:0}}>
              The verification infrastructure itself as an auditable mathematical object.
              11/12 axioms pass. Paper I blocked — correctly.
            </p>
          </div>
          <div style={{display:"flex",flexDirection:"column",gap:6,flexShrink:0}}>
            <Badge color="green" size="lg">11/12 PASS</Badge>
            <Badge color="orange" size="lg">1 BLOCKED</Badge>
            <Badge color="blue" size="lg">SHA256 STABLE</Badge>
          </div>
        </div>

        {/* Summary strip */}
        <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(130px,1fr))",gap:8}}>
          {[
            {l:"Claims total",   v:"27",          c:C.accent},
            {l:"Verified",       v:"14",           c:C.green},
            {l:"Active (C2/AV)", v:"5",            c:C.gold},
            {l:"Killed",         v:"4",            c:C.red},
            {l:"DAG acyclic",    v:"27N · 31E",    c:C.purple},
            {l:"SHA256",         v:"17d2d453…",    c:C.cyan},
          ].map(x=>(
            <div key={x.l} style={{background:C.panel,border:`1px solid ${x.c}33`,
              borderRadius:8,padding:"10px 12px",textAlign:"center"}}>
              <div style={{color:x.c,fontSize:x.v.length>6?14:20,fontWeight:900,
                fontFamily:"monospace"}}>{x.v}</div>
              <div style={{color:C.textDim,fontSize:9,textTransform:"uppercase",
                letterSpacing:"0.1em"}}>{x.l}</div>
            </div>
          ))}
        </div>
      </div>

      {/* NAV */}
      <div style={{display:"flex",gap:4,flexWrap:"wrap",marginBottom:24,
        borderBottom:`1px solid ${C.border}`}}>
        {tabs.map(t=>(
          <button key={t.id} onClick={()=>setTab(t.id)} style={{
            background:tab===t.id?`linear-gradient(135deg,${C.green},${C.cyan})`:"transparent",
            color:tab===t.id?C.bg:C.textDim,border:"none",
            borderRadius:"6px 6px 0 0",padding:"8px 16px",
            fontSize:12,fontWeight:700,cursor:"pointer"}}>
            {t.label}
          </button>
        ))}
      </div>

      {/* ── CLOSURE REPORT ── */}
      {tab === "report" && (
        <div>
          <div style={{color:C.textDim,fontSize:12,marginBottom:16}}>
            Click any axiom to expand. 12 axioms implemented from the Level 19 proposal
            (15 proposed, 2 merged as redundant, 1 demoted from Ω formalism).
          </div>
          {AXIOM_RESULTS.map(r => (
            <AxiomRow key={r.id} result={r}
              expanded={expandedAxiom===r.id}
              onToggle={()=>setExpandedAxiom(expandedAxiom===r.id ? null : r.id)} />
          ))}
          <Card highlight={C.green} style={{marginTop:20}}>
            <div style={{fontFamily:"monospace",fontSize:13,lineHeight:1.8}}>
              <div style={{color:C.green,fontWeight:700,marginBottom:8}}>
                === AQARION Verification Closure Report (Level 19) ===
              </div>
              <div><span style={{color:C.textDim,width:220,display:"inline-block"}}>Repository State:</span>
                <span style={{color:C.text}}>OPEN DEFECTS (Paper I blocked)</span></div>
              <div><span style={{color:C.textDim,width:220,display:"inline-block"}}>Verification Op:</span>
                <span style={{color:C.green}}>IDEMPOTENT</span></div>
              <div><span style={{color:C.textDim,width:220,display:"inline-block"}}>Dependency Graph:</span>
                <span style={{color:C.green}}>ACYCLIC (27 nodes, 31 edges)</span></div>
              <div><span style={{color:C.textDim,width:220,display:"inline-block"}}>Publication State:</span>
                <span style={{color:C.red}}>BLOCKED (3 claims need proof)</span></div>
              <div><span style={{color:C.textDim,width:220,display:"inline-block"}}>Registry SHA256:</span>
                <span style={{color:C.accent}}>17d2d453b0f68ccd8307c0cdd4bb1e10...</span></div>
              <div><span style={{color:C.textDim,width:220,display:"inline-block"}}>Axioms satisfied:</span>
                <span style={{color:C.gold}}>11/12</span></div>
            </div>
          </Card>
        </div>
      )}

      {/* ── DESIGN INSIGHTS ── */}
      {tab === "insights" && (
        <div>
          <div style={{color:C.textDim,fontSize:12,marginBottom:16}}>
            Running Level 19 on the actual registry revealed three design insights
            and one philosophical correction. These are improvements to the governance
            system itself, not to the mathematics.
          </div>
          {DESIGN_INSIGHTS.map(ins => (
            <div key={ins.id} style={{background:C.panel,
              border:`1px solid ${ins.impact==="CRITICAL"?C.red:ins.impact==="HIGH"?C.orange:C.border}33`,
              borderRadius:10,padding:"16px 20px",marginBottom:12}}>
              <div style={{display:"flex",gap:8,alignItems:"center",flexWrap:"wrap",marginBottom:8}}>
                <span style={{fontFamily:"monospace",color:C.accent,fontSize:11}}>{ins.id}</span>
                <Badge color={ins.impact==="CRITICAL"?"red":ins.impact==="HIGH"?"orange":"blue"}>
                  {ins.impact}
                </Badge>
              </div>
              <div style={{color:C.text,fontWeight:700,marginBottom:8}}>{ins.title}</div>
              <div style={{color:C.textDim,fontSize:13,lineHeight:1.7}}>{ins.finding}</div>
            </div>
          ))}
          <Card highlight={C.purple}>
            <div style={{color:C.purple,fontWeight:700,marginBottom:8}}>
              What Level 19 proves about the system:
            </div>
            <div style={{color:C.text,fontSize:13,lineHeight:1.7}}>
              Verification closure converts AQARION from "a collection of scripts that
              produce results" into "a deterministic certification operator over repository
              states." The SHA256 of claim_state.json is a complete fingerprint of the
              research program's epistemic state at any moment.
              <br/><br/>
              <span style={{color:C.textDim}}>
                Most importantly: the governance system caught a real problem. Paper I
                has three claims at C2/AV level. Under the governance rules, it cannot
                be submitted. That is not a bug — it is the system working.
              </span>
            </div>
          </Card>
        </div>
      )}

      {/* ── REGISTRY ── */}
      {tab === "registry" && (
        <div>
          <div style={{display:"flex",gap:8,flexWrap:"wrap",marginBottom:16}}>
            {[null,"Verified","Active","Conjecture","Killed","root"].map(f => (
              <button key={String(f)} onClick={()=>setRegFilter(f)} style={{
                background:regFilter===f?C.accent:"transparent",
                color:regFilter===f?C.bg:C.textDim,
                border:`1px solid ${C.border}`,borderRadius:6,
                padding:"4px 12px",fontSize:11,cursor:"pointer",fontFamily:"monospace"}}>
                {f||"All"}
              </button>
            ))}
          </div>
          <Card><RegistryTable filter={regFilter} /></Card>
        </div>
      )}

      {/* ── DEP GRAPH ── */}
      {tab === "depgraph" && (
        <div>
          <div style={{color:C.textDim,fontSize:12,marginBottom:12}}>
            Dependency DAG: 27 nodes, 31 edges. Topological order verified (L0=roots, L5=conjectures).
            Killed claims shown as separate cluster — anti-theorems, not theorems.
          </div>
          <Card><DepGraphViz /></Card>
          <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(160px,1fr))",gap:8,marginTop:12}}>
            {[
              {l:"Roots (L0)",    c:C.cyan,   v:"8 definitions"},
              {l:"Lemmas (L1)",   c:C.purple, v:"3 lemmas"},
              {l:"Core thms (L2)",c:C.green,  v:"3 theorems"},
              {l:"Kaprekar (L3)", c:C.accent, v:"3 theorems"},
              {l:"Commutator (L4)",c:C.gold,  v:"2 theorems"},
              {l:"Open (L5)",     c:C.purple, v:"4 conjectures"},
            ].map(x=>(
              <div key={x.l} style={{background:C.panel2,border:`1px solid ${x.c}33`,
                borderRadius:8,padding:"8px 12px"}}>
                <div style={{color:x.c,fontSize:11,fontWeight:700}}>{x.l}</div>
                <div style={{color:C.textDim,fontSize:11}}>{x.v}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── PAPERS ── */}
      {tab === "papers" && (
        <div>
          {Object.entries(PAPER_MANIFESTS).map(([paper, info]) => (
            <div key={paper} style={{background:C.panel,
              border:`2px solid ${info.status==="ELIGIBLE"?C.green:C.red}`,
              borderRadius:10,padding:"20px",marginBottom:16}}>
              <div style={{display:"flex",gap:12,alignItems:"center",marginBottom:12}}>
                <h3 style={{color:C.text,fontSize:18,fontWeight:800,margin:0}}>{paper}</h3>
                <Badge color={info.status==="ELIGIBLE"?"green":"red"} size="lg">
                  {info.status}
                </Badge>
              </div>
              <div style={{marginBottom:10}}>
                <div style={{color:C.textDim,fontSize:11,marginBottom:6,textTransform:"uppercase",
                  letterSpacing:"0.1em"}}>Required claims</div>
                <div style={{display:"flex",flexWrap:"wrap",gap:6}}>
                  {info.required.map(id => {
                    const c = CLAIM_REGISTRY.find(x=>x.id===id);
                    const isBlocked = info.blocking.some(b=>b.startsWith(id));
                    return (
                      <div key={id} style={{background:isBlocked?`${C.red}11`:`${C.green}11`,
                        border:`1px solid ${isBlocked?C.red:C.green}44`,
                        borderRadius:6,padding:"3px 10px",fontSize:11,fontFamily:"monospace",
                        color:isBlocked?C.red:C.green}}>
                        {id} {c?`(${c.grade})`:""}
                      </div>
                    );
                  })}
                </div>
              </div>
              {info.blocking.length > 0 && (
                <div style={{background:`${C.red}08`,border:`1px solid ${C.red}33`,
                  borderRadius:8,padding:"12px 14px",marginBottom:10}}>
                  <div style={{color:C.red,fontWeight:700,fontSize:12,marginBottom:6}}>
                    Blocking claims (not yet Verified):
                  </div>
                  {info.blocking.map(b=>(
                    <div key={b} style={{color:C.textDim,fontSize:12,padding:"2px 0"}}>⊘ {b}</div>
                  ))}
                </div>
              )}
              <div style={{color:C.gold,fontSize:13,borderLeft:`3px solid ${C.gold}`,paddingLeft:10}}>
                Path to eligible: {info.path_to_eligible}
              </div>
            </div>
          ))}
          <Card>
            <div style={{color:C.purple,fontWeight:700,marginBottom:8}}>
              Option: Define COMPUTATIONAL_PAPER manifest type
            </div>
            <div style={{color:C.text,fontSize:13,lineHeight:1.7}}>
              If Integers or Experimental Mathematics accepts papers with explicitly labeled C2/AV claims
              (computational results, not proofs), define a separate manifest type with a lower bar:
              AV-sufficient, with claims clearly marked as "computationally verified, proof pending."
              <br/><br/>
              <span style={{color:C.textDim}}>
                This is not a workaround — it is an honest description of the epistemic status.
                Many journals accept this, especially in experimental mathematics.
              </span>
            </div>
          </Card>
        </div>
      )}

      <div style={{borderTop:`1px solid ${C.border}`,marginTop:36,paddingTop:14,
        display:"flex",justifyContent:"space-between",flexWrap:"wrap",gap:8,
        fontSize:10,color:C.textDim}}>
        <span>AQARION Node #10878 · Level 19 · 2026-06-21 · SHA256: 17d2d453...</span>
        <span style={{color:C.green}}>Prove First · Predict Second · No Free Parameters</span>
      </div>
    </div>
  );
}
