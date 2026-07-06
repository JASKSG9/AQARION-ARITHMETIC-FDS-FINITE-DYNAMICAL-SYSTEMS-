import { useState } from "react";

// ─── Design tokens ────────────────────────────────────────────────────────────
// Subject: formal mathematics research platform. Audience: AQARION (JASKSG9),
// open-source peers, potential referees. Job: show the full architecture of
// everything produced, as a single navigable reference.
//
// Palette: deep-space navy + cold electric indigo + proof-green + evidence-amber
// Typography: monospace-forward (research artifact identity), no serifs (rigor)
// Signature element: animated "evidence flow" lines on the AROS layer diagram

const C = {
  bg:       "#080d1a",
  surface:  "#0d1528",
  panel:    "#111e35",
  border:   "#1c3054",
  indigo:   "#4f7ef8",
  violet:   "#7c5af8",
  green:    "#2de08b",
  amber:    "#f5a623",
  red:      "#f75a5a",
  grey:     "#4a6080",
  text:     "#c8d8f0",
  textDim:  "#5d7a9a",
  white:    "#e8f0ff",
};

const LAYERS = [
  {
    id:"L0", label:"L0 — MATHEMATICS", color: C.violet,
    desc:"The raw primitives: definitions, axioms, observables, operators, conjectures. Nothing computed, nothing verified — pure formal vocabulary.",
    items:["D1–D16: all definitions (DEFINITIONS.md)", "Gap observable π(n)=(a-d,b-c)", "Kaprekar map K(n)=desc-asc", "T_G quotient map", "Fiber-constant & transition congruence", "Proposed FNDS objects D13–D16"]
  },
  {
    id:"L1", label:"L1 — RESEARCH GRAPH (KERNEL)", color: C.indigo,
    desc:"Nodes are mathematical objects; edges are dependency/derivation relationships. Every claim lives here with its exact evidence label.",
    items:["T0–T4 + L1: proven theorem chain [P+CV]", "OP0a borrow split [P] — NEW", "OP0b chamber boxes [CV] — NEW", "T12-suff fiber independence [P] — NEW", "T12-app AQARION instance [P] — NEW", "T12-ce counterexample [P+CV-toy] — NEW", "C1–C6: certified computations [CV]", "Minimality Theorem via injectivity [P] — NEW"]
  },
  {
    id:"L2", label:"L2 — IMMUTABLE EVIDENCE STORE", color: C.green,
    desc:"Every artifact is content-addressed. Re-running verify.py must reproduce the same hash. No manual editing of evidence.",
    items:["verify_report.json (sha256: e5c7ba…)", "715 affine-lift exhaustive checks", "158 semiconjugacy fiber checks", "54-state full functional graph traversal", "10-chamber inequality system check (54/54 exact)", "T12 toy counterexample: 4-state exhaustive enum", "CLAIMS_REGISTER.md — single source of truth"]
  },
  {
    id:"L2.5", label:"L2.5 — EVIDENCE SYNTHESIS", color: C.amber,
    desc:"Contradictions flagged, scope gaps noted, no claim assumed from a prior session. Every check labeled with what it does and does NOT cover.",
    items:["0 contradictions across all reproducible checks", "C5 full-Koopman flagged out-of-scope (not refuted)", "Chamber method bug: caught, logged in AUDIT_REPORT.md", "Referee patch: chamber atlas ≠ transition congruence [CV]", "3-element congruence chain proved strict [P+CV]", "Old hash updated after referee-response checks added"]
  },
  {
    id:"L3", label:"L3 — GOVERNANCE ENGINE", color: C.indigo,
    desc:"Evidence labels ARE the policy output: [P] / [CV] / [P+CV] / [O] / [undefined]. No manual 'verified' stamps — status is derived from what's in L2.",
    items:["Evidence policy table (README.md)", "|G|=54 upgraded [CV]→[P+CV] (structural proof added)", "T12 upgraded [undefined]→[P] for AQARION case", "T13/T14: status [undefined] (DEFINITIONS.md flags pending)", "Chamber atlas: status corrected (not a Cong element)", "Spectral/Koopman: demoted to Corollary 4 (non-novel per referee)"]
  },
  {
    id:"L4", label:"L4 — DERIVED COMPUTATIONS", color: C.green,
    desc:"Trust, readiness, and debt computed from the graph — not claimed from memory.",
    items:["Paper A: submission-ready (T0–T4, L1, Minimality all [P+CV])", "Paper B: strong computation + OP0 partial [CV] contribution", "Paper C: T12 resolved for project case; general [O] sharpened", "Depth-quotient: 7-state valid congruence, strictly coarser than gap", "Affine lift: proven injective over G (injectivity certifies minimality)", "Technical debt: C5 out-of-scope; T13/T14 definitions pending"]
  },
  {
    id:"L5", label:"L5 — PROJECTIONS (DELIVERABLES)", color: C.violet,
    desc:"Every file below is a deterministic output of the research graph, not a manually curated document.",
    items:["README.md", "DEFINITIONS.md", "CLAIMS_REGISTER.md", "PROOFS.md", "OP0_CHAMBER_THEOREM.md", "REFEREE_RESPONSE_PATCHSET.md", "AUDIT_REPORT.md", "DEPENDENCY_GRAPH.mmd", "CHEATSHEET.md", "verify.py + verify_report.json + .sha256", "chamber_heatmap.png"]
  },
];

const THEOREM_CHAIN = [
  { id:"T0", label:"T0", desc:"Exact Quotient Criterion", badge:"P", dep:[] },
  { id:"D1", label:"D1-D2", desc:"K(n) & Gap π", badge:"D", dep:[] },
  { id:"T1", label:"T1", desc:"Affine Lift K=999g₁+90g₂", badge:"P+CV", dep:["D1"] },
  { id:"T2", label:"T2", desc:"Gap Projection Congruence", badge:"P", dep:["T1","D1"] },
  { id:"T3", label:"T3", desc:"Semiconjugacy π∘K=T_G∘π", badge:"P+CV", dep:["T0","T2"] },
  { id:"T4", label:"T4", desc:"(G,T_G) Deterministic, Closed", badge:"P+CV", dep:["T3"] },
  { id:"L1", label:"L1", desc:"ν(N)=D Nilpotency-Depth", badge:"P", dep:[] },
  { id:"C1", label:"C1", desc:"|G|=54 (structural + enum)", badge:"P+CV", dep:["T4"] },
  { id:"C4", label:"C4", desc:"Filtration 54→…→1", badge:"CV", dep:["T4"] },
  { id:"C6", label:"C6", desc:"Quotient Koopman ν_G=6", badge:"CV", dep:["T4","L1"] },
  { id:"FP", label:"FP", desc:"Unique Fixed Pt (6,2)↔6174", badge:"CV", dep:["T4"] },
  { id:"OP0a", label:"OP0a", desc:"Borrow Split g₂=0 axis", badge:"P★", dep:["T1"] },
  { id:"OP0b", label:"OP0b", desc:"10-chamber box inequalities", badge:"CV★", dep:["C1","C3"] },
  { id:"T12s", label:"T12-suff", desc:"Constant-on-fibers ⟹ product", badge:"P★", dep:["T0"] },
  { id:"T12c", label:"T12-ce", desc:"Counterexample: non-constant fails", badge:"P+CV★", dep:["T12s"] },
  { id:"T12a", label:"T12-app", desc:"AQARION's π satisfies T12-suff", badge:"P★", dep:["T12s","T1"] },
  { id:"MIN", label:"MIN", desc:"Minimality Theorem (injectivity)", badge:"P★", dep:["T1","T4"] },
  { id:"CHAIN", label:"CHAIN", desc:"3-element congruence chain proof", badge:"P+CV★", dep:["T4","L1"] },
];

const BADGE_STYLE = {
  "P":    { bg:"#162e45", color:C.indigo,  text:"P" },
  "P+CV": { bg:"#0e2e1e", color:C.green,   text:"P+CV" },
  "CV":   { bg:"#2a1f06", color:C.amber,   text:"CV" },
  "D":    { bg:"#201535", color:C.violet,  text:"D" },
  "P★":   { bg:"#162040", color:"#7ef0ff", text:"P ★NEW" },
  "CV★":  { bg:"#2a1f06", color:"#f5c842", text:"CV ★NEW" },
  "P+CV★":{ bg:"#0e2e1e", color:"#4ff0a0", text:"P+CV ★NEW" },
};

const REFEREE_FIXES = [
  {
    num:"R1", title:"Why 54? — structural proof", risk:"Rejection risk B", status:"Fixed",
    summary:"|G|=55-1=54 via closed-form triangular count C(11,2)-1. Pure [P], not enumeration.",
    before:"[CV] only — compute and report",
    after:"[P+CV] — C(n+2,2)-1 with n=9, corroborated by verify.py",
  },
  {
    num:"R2", title:"Observable equivalence formalized", risk:"Rejection risk A+B", status:"Fixed",
    summary:"D17: Cong(X,f) lattice defined. 3-element strict chain proved. Chamber atlas shown ≠ Cong element.",
    before:"Informal 'non-equivalent observables'",
    after:"[P+CV] explicit chain triv ≤ depth(7) ≤ gap(54), each strict",
  },
  {
    num:"R3", title:"Minimality via injectivity", risk:"Rejection risk A §5", status:"Fixed",
    summary:"Affine lift injective on G (verified, 0 collisions). Gap ∼ is unique coarsest fiber-constant congruence.",
    before:"'LPITC optimality' — undefined",
    after:"[P] Minimality Theorem in REFEREE_RESPONSE_PATCHSET.md §Fix3",
  },
  {
    num:"R4", title:"Spectral claims demoted", risk:"Rejection risk B §4", status:"Resolved",
    summary:"Koopman/Jordan reframed as Corollary 4 (generic fact, non-novel per Referee B). Not removed, scoped correctly.",
    before:"Presented as a theorem-level spectral result",
    after:"Corollary 4: 'standard consequence of unique fixed point, no cycles'",
  },
  {
    num:"R5", title:"Single Main Theorem + Corollaries", risk:"Referee C — strict", status:"Restructured",
    summary:"Factorization Theorem (main) + 4 Corollaries. OP0 explicitly separated to Paper B.",
    before:"T0–T4 bundle with mixed evidence layers",
    after:"Main Theorem → Cor1(54) → Cor2(Minimality) → Cor3(chain) → Cor4(Koopman remark)",
  },
];

const LIFECYCLE_STEPS = [
  { s:"IDEA", c:C.textDim },
  { s:"CONJECTURE", c:C.violet },
  { s:"DERIVATION", c:C.indigo },
  { s:"IMPLEMENTATION", c:C.indigo },
  { s:"COMPUTATIONAL VERIFICATION", c:C.green },
  { s:"INDEPENDENT ORACLE", c:C.green },
  { s:"FORMALIZATION", c:C.amber },
  { s:"EVIDENCE SYNTHESIS", c:C.amber },
  { s:"PUBLISHABLE", c:"#2de08b" },
  { s:"PUBLISHED", c:"#2de08b" },
  { s:"SUPERSEDED / ARCHIVED", c:C.grey },
];

// ─── Component ───────────────────────────────────────────────────────────────
export default function AROs() {
  const [activeLayer, setActiveLayer] = useState(null);
  const [activeNode, setActiveNode] = useState(null);
  const [tab, setTab] = useState("layers");

  const layer = activeLayer !== null ? LAYERS[activeLayer] : null;

  return (
    <div style={{ background:C.bg, color:C.text, fontFamily:"'Courier New', monospace", minHeight:"100vh", padding:"0 0 60px" }}>

      {/* ── Header ── */}
      <div style={{ background:`linear-gradient(135deg,#0a112b 0%,#101f40 100%)`, borderBottom:`1px solid ${C.border}`, padding:"28px 32px 20px" }}>
        <div style={{ display:"flex", alignItems:"baseline", gap:14 }}>
          <span style={{ fontSize:11, letterSpacing:4, color:C.indigo, textTransform:"uppercase" }}>AQARION-ARITHMETIC · JASKSG9 · Node #10878</span>
        </div>
        <h1 style={{ margin:"8px 0 4px", fontSize:26, fontWeight:700, color:C.white, letterSpacing:1 }}>
          AROS — Research Operating System
        </h1>
        <p style={{ margin:0, fontSize:12, color:C.textDim, maxWidth:680 }}>
          Complete visual workflow of all session deliverables · Framework Freeze v2.0.0 + Referee-Proof Patch Set
          · sha256 <span style={{ color:C.green }}>e5c7ba…</span>
        </p>

        {/* tabs */}
        <div style={{ display:"flex", gap:4, marginTop:18 }}>
          {[["layers","AROS Layers"],["theorems","Theorem Graph"],["referee","Referee Fixes"],["files","All Deliverables"],["lifecycle","Object Lifecycle"]].map(([k,v])=>(
            <button key={k} onClick={()=>setTab(k)} style={{
              background: tab===k ? C.indigo : "transparent",
              color: tab===k ? C.white : C.textDim,
              border:`1px solid ${tab===k ? C.indigo : C.border}`,
              borderRadius:4, padding:"5px 14px", fontSize:11, letterSpacing:1,
              textTransform:"uppercase", cursor:"pointer"
            }}>{v}</button>
          ))}
        </div>
      </div>

      <div style={{ padding:"24px 32px", maxWidth:1100 }}>

        {/* ═══════════════════════════════════════ LAYERS ══════════════════ */}
        {tab==="layers" && (
          <div>
            <p style={{ fontSize:11, color:C.textDim, marginBottom:20 }}>
              Click any layer to expand its contents. Every property of the repository (trust, readiness, publication status) is a deterministic computation over the Research Graph — nothing is manually labeled.
            </p>

            <div style={{ display:"flex", flexDirection:"column", gap:4 }}>
              {LAYERS.map((layer, i) => {
                const open = activeLayer === i;
                return (
                  <div key={layer.id}>
                    <div onClick={() => setActiveLayer(open ? null : i)} style={{
                      background: open ? C.panel : C.surface,
                      border:`1px solid ${open ? layer.color : C.border}`,
                      borderRadius:6, padding:"14px 20px", cursor:"pointer",
                      display:"flex", alignItems:"center", gap:14,
                      transition:"all 0.15s"
                    }}>
                      <span style={{ fontSize:11, fontWeight:700, color:layer.color, minWidth:40 }}>{layer.id}</span>
                      <span style={{ flex:1, fontSize:13, color:C.white, fontWeight:600 }}>{layer.label}</span>
                      <span style={{ fontSize:10, color:C.textDim }}>{open?"▲":"▼"}</span>
                    </div>

                    {open && (
                      <div style={{ background:C.panel, border:`1px solid ${layer.color}`, borderTop:"none", borderRadius:"0 0 6px 6px", padding:"16px 20px", display:"flex", gap:24 }}>
                        <div style={{ flex:1 }}>
                          <p style={{ margin:"0 0 14px", fontSize:12, color:C.textDim, lineHeight:1.6 }}>{layer.desc}</p>
                          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:6 }}>
                            {layer.items.map((item,j)=>(
                              <div key={j} style={{ display:"flex", gap:8, alignItems:"flex-start" }}>
                                <span style={{ color:layer.color, fontSize:10, marginTop:2 }}>◆</span>
                                <span style={{ fontSize:11, color:C.text, lineHeight:1.5 }}>{item}</span>
                              </div>
                            ))}
                          </div>
                        </div>

                        {/* flow arrow to next layer */}
                        {i < LAYERS.length - 1 && (
                          <div style={{ display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", minWidth:48 }}>
                            <div style={{ width:1, flex:1, background:`linear-gradient(to bottom,${layer.color},${LAYERS[i+1].color})`, opacity:0.4 }}/>
                            <span style={{ fontSize:18, color:LAYERS[i+1].color }}>↓</span>
                          </div>
                        )}
                      </div>
                    )}

                    {/* connector line between layers */}
                    {!open && i < LAYERS.length-1 && (
                      <div style={{ width:2, height:8, background:C.border, margin:"0 auto" }}/>
                    )}
                  </div>
                );
              })}
            </div>

            {/* Dependency shockwave diagram */}
            <div style={{ marginTop:32, background:C.surface, border:`1px solid ${C.border}`, borderRadius:8, padding:24 }}>
              <div style={{ fontSize:11, color:C.indigo, letterSpacing:3, textTransform:"uppercase", marginBottom:12 }}>Dependency Shockwave — If T1 changes…</div>
              <pre style={{ fontSize:11, color:C.textDim, lineHeight:1.7, margin:0 }}>{`            D1─────D2
             │
             T1   ← change here
           ╱    ╲
         T2      (affine lift used in T12-app, MIN, OP0a, OP0b)
          │
         T3 ────────────────────┐
          │                     │
         T4          every downstream CV/P+CV check reruns
       ╱  │  ╲                  │
     C1  C4  FP           CLAIMS_REGISTER.md updates
      │         ╲          AUDIT_REPORT.md updates
    OP0b        T12-app         │
                MIN          sha256 certificate regenerates
                              └─── Paper A/B/C readiness recomputed`}</pre>
            </div>
          </div>
        )}

        {/* ═══════════════════════════════════════ THEOREMS ════════════════ */}
        {tab==="theorems" && (
          <div>
            <p style={{ fontSize:11, color:C.textDim, marginBottom:20 }}>
              Click a node for details. ★NEW = proved or verified this session for the first time.
            </p>
            <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fill,minmax(200px,1fr))", gap:10 }}>
              {THEOREM_CHAIN.map(node => {
                const bs = BADGE_STYLE[node.badge] || BADGE_STYLE["P"];
                const isActive = activeNode === node.id;
                return (
                  <div key={node.id} onClick={()=>setActiveNode(isActive ? null : node.id)} style={{
                    background: isActive ? C.panel : C.surface,
                    border:`1px solid ${isActive ? bs.color : C.border}`,
                    borderRadius:6, padding:"12px 14px", cursor:"pointer"
                  }}>
                    <div style={{ display:"flex", justifyContent:"space-between", alignItems:"flex-start", marginBottom:6 }}>
                      <span style={{ fontSize:12, fontWeight:700, color:C.white }}>{node.label}</span>
                      <span style={{ fontSize:9, padding:"2px 6px", borderRadius:3, background:bs.bg, color:bs.color, whiteSpace:"nowrap" }}>{bs.text}</span>
                    </div>
                    <p style={{ margin:0, fontSize:11, color:C.text, lineHeight:1.4 }}>{node.desc}</p>
                    {node.dep.length > 0 && (
                      <div style={{ marginTop:8, display:"flex", flexWrap:"wrap", gap:4 }}>
                        {node.dep.map(d=>(
                          <span key={d} style={{ fontSize:9, color:C.textDim, background:C.bg, padding:"1px 5px", borderRadius:2 }}>← {d}</span>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {/* Legend */}
            <div style={{ marginTop:24, background:C.surface, border:`1px solid ${C.border}`, borderRadius:6, padding:16, display:"flex", flexWrap:"wrap", gap:16 }}>
              {Object.entries(BADGE_STYLE).map(([k,v])=>(
                <div key={k} style={{ display:"flex", alignItems:"center", gap:6 }}>
                  <span style={{ fontSize:9, padding:"2px 6px", borderRadius:3, background:v.bg, color:v.color }}>{v.text}</span>
                  <span style={{ fontSize:10, color:C.textDim }}>
                    {k==="P"?"Proved by direct algebra":
                     k==="P+CV"?"Proved + exhaustively verified":
                     k==="CV"?"Exhaustively verified (entire domain)":
                     k==="D"?"Definition":
                     k==="P★"?"Proved this session (new)":
                     k==="CV★"?"Verified this session (new)":
                     "Proved + verified this session"}
                  </span>
                </div>
              ))}
            </div>

            {/* ASCII dependency flowchart */}
            <div style={{ marginTop:20, background:C.surface, border:`1px solid ${C.border}`, borderRadius:8, padding:20 }}>
              <div style={{ fontSize:11, color:C.indigo, letterSpacing:3, textTransform:"uppercase", marginBottom:10 }}>Core proof chain (ASCII)</div>
              <pre style={{ fontSize:10, color:C.text, lineHeight:1.7, margin:0 }}>{`D1 ──────────────────┐
D2 ──────────────────┤
                     ▼
                    T1 [P+CV] ──────────────────────┐
                   / │                              │
                  ▼  ▼                              │
            T2[P] T0[P]                         OP0a[P★]   MIN[P★]
             │   ╲  /                               │         │
             │   T3[P+CV]                         OP0b[CV★]   │
             │    │                                 │         │
             └────┤                                 └────── Paper B
                  T4[P+CV]
               ╱  │  │  ╲
           C1[P+CV] C4 FP  C6[CV]    T12-suff[P★]
           │            │              │
         OP0b          L1           T12-ce[P+CV★]
                                       │
                                    T12-app[P★] ◀── T1
                                       │
                                    CHAIN[P+CV★]
                                       │
                                   Paper A (ready) + Paper C (emerging)`}</pre>
            </div>
          </div>
        )}

        {/* ═══════════════════════════════════════ REFEREE ═════════════════ */}
        {tab==="referee" && (
          <div>
            <p style={{ fontSize:11, color:C.textDim, marginBottom:20 }}>
              Three-referee simulation run against Paper I. Five rejection risks identified.
              All five resolved or restructured below — each backed by a new proof or exhaustive check.
            </p>
            <div style={{ display:"flex", flexDirection:"column", gap:12 }}>
              {REFEREE_FIXES.map(rf => {
                const statusColor = rf.status==="Fixed" ? C.green : rf.status==="Resolved" ? C.amber : C.indigo;
                return (
                  <div key={rf.num} style={{ background:C.surface, border:`1px solid ${C.border}`, borderRadius:8, padding:20 }}>
                    <div style={{ display:"flex", alignItems:"center", gap:12, marginBottom:10 }}>
                      <span style={{ fontSize:12, fontWeight:700, color:C.white, background:C.panel, padding:"3px 10px", borderRadius:4 }}>{rf.num}</span>
                      <span style={{ fontSize:13, fontWeight:700, color:C.white, flex:1 }}>{rf.title}</span>
                      <span style={{ fontSize:9, padding:"3px 8px", borderRadius:4, background:`${statusColor}22`, color:statusColor, border:`1px solid ${statusColor}44` }}>{rf.status.toUpperCase()}</span>
                      <span style={{ fontSize:10, color:C.red, background:"#2a0a0a", padding:"3px 8px", borderRadius:4 }}>{rf.risk}</span>
                    </div>
                    <p style={{ margin:"0 0 12px", fontSize:12, color:C.text, lineHeight:1.6 }}>{rf.summary}</p>
                    <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:10 }}>
                      <div style={{ background:C.bg, borderRadius:4, padding:"10px 14px", borderLeft:`3px solid ${C.red}` }}>
                        <div style={{ fontSize:9, color:C.red, letterSpacing:2, marginBottom:5 }}>BEFORE</div>
                        <div style={{ fontSize:11, color:C.textDim }}>{rf.before}</div>
                      </div>
                      <div style={{ background:C.bg, borderRadius:4, padding:"10px 14px", borderLeft:`3px solid ${C.green}` }}>
                        <div style={{ fontSize:9, color:C.green, letterSpacing:2, marginBottom:5 }}>AFTER</div>
                        <div style={{ fontSize:11, color:C.text }}>{rf.after}</div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Consensus table */}
            <div style={{ marginTop:24, background:C.surface, border:`1px solid ${C.border}`, borderRadius:8, padding:20 }}>
              <div style={{ fontSize:11, color:C.indigo, letterSpacing:3, textTransform:"uppercase", marginBottom:14 }}>Referee consensus — post-patch</div>
              {[
                ["✔ Accepted", C.green, ["Kaprekar admits finite quotient system","Factor map exists (semiconjugacy)","Quotient structure well-defined","Multiple observable-induced partitions exist (interesting)","Why 54? — structural triangular-number proof","Minimality — unique coarsest fiber-constant congruence","3-element congruence chain, strict at each step"]],
                ["⚠ Monitor", C.amber, ["OP0b chamber boxes: [CV] not [P] — symbolic derivation still needed for chambers 2–5,7,9","T13/T14: DEFINITIONS.md PROPOSED tags must be confirmed before evidence labels","C5 full-Koopman: out-of-scope, must be addressed in Paper B"]],
                ["✖ Resolved", C.grey, ["Spectral overstatement — demoted to Corollary 4 (remark)","Chamber atlas conflated with quotient — explicitly separated (chamber ≠ Cong element)","Multiple-theorem diffusion — restructured to 1 Main Theorem + 4 Corollaries","OP0 embedded in core narrative — moved to Paper B cleanly"]],
              ].map(([title, color, items]) => (
                <div key={title} style={{ marginBottom:16 }}>
                  <div style={{ fontSize:11, color, fontWeight:700, marginBottom:8 }}>{title}</div>
                  <div style={{ display:"flex", flexWrap:"wrap", gap:6 }}>
                    {items.map((item,i)=>(
                      <span key={i} style={{ fontSize:10, color:C.text, background:C.panel, padding:"4px 10px", borderRadius:4, border:`1px solid ${C.border}` }}>{item}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ═══════════════════════════════════════ FILES ═══════════════════ */}
        {tab==="files" && (
          <div>
            <p style={{ fontSize:11, color:C.textDim, marginBottom:20 }}>
              Complete deliverable manifest. Every file is a deterministic output — nothing manually curated post-proof.
            </p>
            <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fill,minmax(280px,1fr))", gap:10 }}>
              {[
                { file:"README.md", type:"ENTRY POINT", color:C.indigo, desc:"Package overview, manifest, evidence policy, one-line headline result", new:false },
                { file:"DEFINITIONS.md", type:"VOCABULARY", color:C.violet, desc:"D1–D16 incl. [PROPOSED] FNDS objects D13–D16. Authoritative. Frozen before PROOFS.md.", new:false },
                { file:"CLAIMS_REGISTER.md", type:"TRUTH TABLE", color:C.green, desc:"Every claim → evidence label, single source. 4 new results, 0 contradictions, 1 flagged out-of-scope.", new:false },
                { file:"PROOFS.md", type:"SYMBOLIC PROOFS", color:C.green, desc:"T0–T4, L1, OP0a, OP0b, T12-suff, T12-ce, T12-app. Algebra only — no numbers from memory.", new:false },
                { file:"OP0_CHAMBER_THEOREM.md", type:"NEW RESULT", color:"#7ef0ff", desc:"All 10 chambers as exact 4-inequality boxes. Full table + geometric interpretation + what remains open.", new:true },
                { file:"REFEREE_RESPONSE_PATCHSET.md", type:"PATCH SET", color:C.amber, desc:"3 rejection risks fixed: |G| structural proof, observable equivalence D17, minimality via injectivity.", new:true },
                { file:"AUDIT_REPORT.md", type:"AUDIT", color:C.amber, desc:"Line-by-line: every checkpoint claim vs independent re-derivation. Method bug logged. Hash updated.", new:false },
                { file:"DEPENDENCY_GRAPH.mmd", type:"MERMAID", color:C.violet, desc:"Paste into mermaid.live or GitHub .md. Colour-coded: [P]=blue, [CV]=green, ★=yellow, [O]=red dashed.", new:false },
                { file:"CHEATSHEET.md", type:"REFERENCE", color:C.indigo, desc:"One-screen reference: K(n) formula, |G|=54, ASCII chamber grid (programmatically verified), filemap.", new:false },
                { file:"verify.py", type:"ENGINE", color:C.green, desc:"From-scratch re-derivation. T1 exhaustive (715 checks), T3 fibers (158), all referee-response checks.", new:false },
                { file:"verify_report.json", type:"EVIDENCE STORE", color:C.green, desc:"Machine-readable output of all checks. sha256=e5c7ba…  Regenerate anytime with python3 verify.py.", new:false },
                { file:"verify_report.sha256", type:"CERTIFICATE", color:C.green, desc:"SHA-256 of verify_report.json. Certifies exact reproducibility of the run environment.", new:false },
                { file:"chamber_heatmap.png", type:"VISUAL", color:C.violet, desc:"Left: chamber id per (g1,g2), fixed pt (6,2) ringed. Right: det(M_k) heatmap in {-4,0,+4}.", new:false },
              ].map(f => (
                <div key={f.file} style={{ background:C.surface, border:`1px solid ${f.new ? f.color : C.border}`, borderRadius:6, padding:"14px 16px", position:"relative" }}>
                  {f.new && <div style={{ position:"absolute", top:8, right:8, fontSize:8, color:f.color, background:`${f.color}22`, padding:"2px 6px", borderRadius:3 }}>★ NEW</div>}
                  <div style={{ fontSize:9, color:f.color, letterSpacing:2, marginBottom:5 }}>{f.type}</div>
                  <div style={{ fontSize:12, fontWeight:700, color:C.white, marginBottom:6, wordBreak:"break-all" }}>{f.file}</div>
                  <div style={{ fontSize:10, color:C.textDim, lineHeight:1.5 }}>{f.desc}</div>
                </div>
              ))}
            </div>

            {/* hash display */}
            <div style={{ marginTop:20, background:C.surface, border:`1px solid ${C.green}22`, borderRadius:6, padding:16, display:"flex", gap:16, alignItems:"center" }}>
              <span style={{ fontSize:9, color:C.green, letterSpacing:2 }}>CERTIFICATE</span>
              <code style={{ fontSize:11, color:C.green, flex:1, wordBreak:"break-all" }}>sha256: e5c7badb93ebc4ad96773050fac01433ddd4b8540f5c62935c101a32e3d133bf</code>
              <span style={{ fontSize:9, color:C.textDim }}>verify_report.json</span>
            </div>
          </div>
        )}

        {/* ═══════════════════════════════════════ LIFECYCLE ═══════════════ */}
        {tab==="lifecycle" && (
          <div>
            <p style={{ fontSize:11, color:C.textDim, marginBottom:20 }}>
              Research object lifecycle per AROS architecture. Counterexamples and negative evidence are retained as first-class objects — never deleted.
            </p>
            <div style={{ display:"flex", gap:32 }}>
              {/* Lifecycle vertical */}
              <div style={{ display:"flex", flexDirection:"column", alignItems:"center", minWidth:200 }}>
                {LIFECYCLE_STEPS.map((step,i) => (
                  <div key={step.s} style={{ display:"flex", flexDirection:"column", alignItems:"center" }}>
                    <div style={{ background:C.surface, border:`1px solid ${step.c}`, borderRadius:6, padding:"8px 16px", fontSize:11, color:step.c, fontWeight:700, textAlign:"center", minWidth:180 }}>
                      {step.s}
                    </div>
                    {i < LIFECYCLE_STEPS.length-1 && (
                      <div style={{ width:2, height:16, background:`linear-gradient(to bottom,${step.c},${LIFECYCLE_STEPS[i+1].c})`, opacity:0.5 }}/>
                    )}
                  </div>
                ))}
              </div>

              {/* Where each result sits */}
              <div style={{ flex:1, display:"flex", flexDirection:"column", gap:10 }}>
                <div style={{ fontSize:11, color:C.indigo, letterSpacing:3, textTransform:"uppercase", marginBottom:4 }}>Current status of key results</div>
                {[
                  { item:"T0–T4, L1 (core theorem chain)", stage:"PUBLISHED (in repository)", note:"Submission-ready for Paper A" },
                  { item:"|G|=54 structural proof", stage:"PUBLISHABLE", note:"Added Fix 1 — closes Referee B's cardinality objection" },
                  { item:"D17 + congruence chain", stage:"PUBLISHABLE", note:"Added Fix 2 — closes Referee A+B's equivalence objection" },
                  { item:"Minimality Theorem", stage:"PUBLISHABLE", note:"Added Fix 3 — closes Referee A §5 LPITC objection" },
                  { item:"OP0a borrow-split proof", stage:"FORMALIZATION", note:"[P] proved here; not yet in LaTeX — next step" },
                  { item:"OP0b chamber box inequalities", stage:"COMPUTATIONAL VERIFICATION", note:"[CV] all 10 chambers; symbolic derivation for ch.2–9 remains open" },
                  { item:"T12-suff / T12-app", stage:"PUBLISHABLE", note:"General FNDS theorem + AQARION instance both proved [P]" },
                  { item:"T12 general FNDS (min hypothesis)", stage:"CONJECTURE → DERIVATION", note:"Sharpened — counterexample establishes non-trivial boundary" },
                  { item:"T13 / T14", stage:"IDEA", note:"Requires DEFINITIONS.md D13–D16 author confirmation first" },
                  { item:"C5 full-Koopman ν=7", stage:"INDEPENDENT ORACLE pending", note:"Out of scope this session — needed for Paper B" },
                  { item:"T12-counterexample (4-state system)", stage:"PUBLISHED", note:"First-class negative evidence, kept in PROOFS.md §T12-ce" },
                ].map(row => (
                  <div key={row.item} style={{ background:C.surface, border:`1px solid ${C.border}`, borderRadius:5, padding:"10px 14px" }}>
                    <div style={{ display:"flex", gap:10, alignItems:"baseline" }}>
                      <span style={{ fontSize:11, color:C.white, flex:1 }}>{row.item}</span>
                      <span style={{ fontSize:9, color:C.amber, whiteSpace:"nowrap" }}>{row.stage}</span>
                    </div>
                    <div style={{ fontSize:10, color:C.textDim, marginTop:3 }}>{row.note}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Repository Minimality Principle */}
            <div style={{ marginTop:28, background:`linear-gradient(135deg,#0e1e38,#121830)`, border:`1px solid ${C.indigo}44`, borderRadius:8, padding:22 }}>
              <div style={{ fontSize:9, color:C.indigo, letterSpacing:4, textTransform:"uppercase", marginBottom:10 }}>AROS Foundational Axiom</div>
              <p style={{ margin:0, fontSize:13, color:C.white, lineHeight:1.7, fontStyle:"italic" }}>
                "The repository stores only primitive facts — definitions, dependencies, evidence, policies, and provenance.
                Every other property (trust, maturity, publication readiness, dashboards, certification, documentation,
                release status, and metrics) is a <strong>deterministic computation</strong> over the Research Graph."
              </p>
              <p style={{ margin:"12px 0 0", fontSize:10, color:C.textDim }}>
                — Repository Minimality Principle · AROS Architecture Document
              </p>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
