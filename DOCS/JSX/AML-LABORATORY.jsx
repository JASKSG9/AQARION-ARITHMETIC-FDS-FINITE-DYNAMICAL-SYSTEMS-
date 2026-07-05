import { useState, useEffect } from "react";

// ══════════════════════════════════════════════════════════════════════════════
// AQARION — ADVERSARIAL MATHEMATICS LABORATORY (AML)
// Version 1.0.0 · Node #10878 · 2026-06-21
// Prove First · Predict Second · No Free Parameters
// ══════════════════════════════════════════════════════════════════════════════

const C = {
  bg:      "#080b12",
  panel:   "#0d1121",
  panel2:  "#111828",
  border:  "#1a2340",
  accent:  "#38bdf8",
  gold:    "#f59e0b",
  green:   "#34d399",
  red:     "#f87171",
  orange:  "#fb923c",
  purple:  "#a78bfa",
  cyan:    "#22d3ee",
  muted:   "#475569",
  text:    "#e2e8f0",
  textDim: "#64748b",
};

// ── REAL COMPUTED DATA ────────────────────────────────────

const EVIDENCE_WEIGHTS = {
  exhaustive_search: 3, random_search: 2, adversarial: 3,
  mutation_testing: 2, independent_impl: 2, literature: 1,
  proof_written: 4, lean_formalized: 3,
};
const MAX_PRESSURE = Object.values(EVIDENCE_WEIGHTS).reduce((a,b)=>a+b,0); // 20

const CLAIMS_REGISTRY = [
  { id:"T-SEMICONJ",   stmt:"Semiconjugacy π∘T=T_F∘π (0 violations)",
    ev:{exhaustive_search:1,random_search:1,adversarial:1,mutation_testing:1,independent_impl:1,proof_written:1,lean_formalized:1},
    killed:false },
  { id:"T-FOQDS-55",   stmt:"FOQDS = 55 classes (base-10, 4-digit)",
    ev:{exhaustive_search:1,random_search:1,independent_impl:1,lean_formalized:1},
    killed:false },
  { id:"T-K55-MP",     stmt:"K55 minimal poly = x⁷(x−1)",
    ev:{exhaustive_search:1,random_search:1,adversarial:1,mutation_testing:1},
    killed:false },
  { id:"T-K54-MP",     stmt:"K54 minimal poly = x⁶(x−1)  [v11 correction]",
    ev:{exhaustive_search:1,random_search:1,adversarial:1,mutation_testing:1},
    killed:false },
  { id:"T-RANK-C=1",   stmt:"rank(ΠK−KΠ) = 1 for Kaprekar FOQDS",
    ev:{exhaustive_search:1,adversarial:1},
    killed:false },
  { id:"T-KAP-CLASS4", stmt:"Kaprekar ∈ Class IV (mixed commutator class)",
    ev:{exhaustive_search:1,adversarial:1},
    killed:false },
  { id:"T-COUPLING",   stmt:"δ = dim(V_ref ∩ V_bdry)  — general formula",
    ev:{exhaustive_search:1},
    killed:false },
  { id:"T-CROSSBASE",  stmt:"|Q_b| = b(b+1)/2 for all even b",
    ev:{adversarial:1},
    killed:true, killReason:"Fails b=4,6,8,12,14 (all computed)" },
  { id:"T-AUTO-Z26",   stmt:"Automorphism group (ℤ₂)⁶ order 64",
    ev:{},
    killed:true, killReason:"Level-1 has 3 nodes; no ℤ₂ action found" },
  { id:"T-RANK-30",    stmt:"Incidence rank stabilizes at 30",
    ev:{},
    killed:true, killReason:"No matrix computes to 30; origin unknown" },
];

function pressureScore(ev) {
  return Object.entries(ev).reduce((s,[k,v]) => s + (v ? (EVIDENCE_WEIGHTS[k]||1) : 0), 0);
}
function gradeFromEv(ev, killed) {
  if (killed) return "KILLED";
  if (ev.proof_written && ev.lean_formalized) return "PV";
  if (ev.proof_written) return "P";
  if (ev.adversarial && ev.exhaustive_search) return "AV";
  if (ev.exhaustive_search) return "C2";
  if (ev.random_search) return "C1";
  return "C0";
}

const AML_MODULES = [
  { id:"A", name:"FDDS Family Generator",
    desc:"Generate 13 canonical FDDS families (Kaprekar, random, nilpotent, trees, affine, DFA…) as standardized inputs for every theorem benchmark.",
    status:"IMPLEMENTED", color:C.accent },
  { id:"B", name:"Executable Property Language",
    desc:"Define theorems as machine-checkable properties: SemiConjugacy, Π²=Π, AttractorReachable, FOQDSRefinesObs, rank(C)=dim span{Δ}. Every claim becomes a test.",
    status:"IMPLEMENTED", color:C.green },
  { id:"C", name:"Adversarial Generator",
    desc:"Mutation operators: merge_fixed_points, reroute_transient, inject_symmetry, collapse_obs. Each generates boundary cases designed to expose failures.",
    status:"IMPLEMENTED", color:C.gold },
  { id:"D", name:"Counterexample Minimizer",
    desc:"Delta-debugging on FDDS state sets. Given a failing system, iteratively remove states while preserving failure → minimal witness certificate.",
    status:"IMPLEMENTED", color:C.purple },
  { id:"E", name:"Collision Atlas",
    desc:"Hash FDDS systems by observable signature. Collisions = systems that look identical under the invariant. Archive as first-class research objects.",
    status:"IMPLEMENTED", color:C.cyan },
  { id:"F", name:"Invariant Competition",
    desc:"Benchmark FOQDS against: WL refinement, canonical graph labeling, degree sequences, spectral invariants, exact lumpability. Where does each separate or merge?",
    status:"PLANNED", color:C.orange },
  { id:"G", name:"Implementation Mutation Testing",
    desc:"Mutate implementations (transpose K, off-by-one k, scale, wrong norm) and verify the test suite catches every mutant. Currently: 2 survivors found (transpose_K, k+1).",
    status:"IMPLEMENTED", color:C.red },
  { id:"H", name:"Structured Proof Templates",
    desc:"Goal → Definitions → Assumptions → Dependencies → Steps+Justifications → Edge Cases → Conclusion. Enforces Alethfeld-style proof structure for Lean translation.",
    status:"PLANNED", color:C.accent },
  { id:"I", name:"Proof Pressure Index",
    desc:"Multi-dimensional evidence accumulation: exhaustive/random/adversarial/mutation/independent/literature/proof/lean. Grade = {C0,C1,C2,AV,P,PV}.",
    status:"IMPLEMENTED", color:C.green },
  { id:"J", name:"Autonomous Observatory",
    desc:"Generate → Analyze → Detect anomalies → Cluster → Rank surprises → Human review → Conjecture. Discovery engine, not just a reporter.",
    status:"PLANNED", color:C.purple },
];

const MUTATION_RESULTS = [
  { mutant:"transpose_K",    caught:false, note:"K^T has same minimal poly structure — detector blind to it" },
  { mutant:"add_identity",   caught:true,  note:"K+I shifts eigenvalues; poly test correctly fails" },
  { mutant:"scale_2",        caught:true,  note:"2K not stochastic; nilpotent test fails" },
  { mutant:"off-by-one k+1", caught:false, note:"k=7 also passes test since K^7(K-I)=0 too (x⁷ still annihilates)" },
  { mutant:"off-by-one k−1", caught:true,  note:"k=5: K^5(K-I)≠0, correctly detected" },
];

const COLLISION_STATS = {
  systems: 200, domain: "random 10-state, mod-3 obs",
  distinctSigs: 94, collidingSigs: 49, maxBucket: 10,
  example: "Seeds {0,2,68,...} → 7 distinct systems, same observable signature",
};

const CROSS_BASE = [
  {b:4,  foqds:12,  formula:10,  match:false},
  {b:6,  foqds:26,  formula:21,  match:false},
  {b:8,  foqds:43,  formula:36,  match:false},
  {b:10, foqds:55,  formula:55,  match:true },
  {b:12, foqds:587, formula:78,  match:false},
  {b:14, foqds:1232,formula:105, match:false},
];

const OPEN_PROBLEMS = [
  {id:"OP-NEW-1", title:"K54/K55 Minimal Poly +1 Difference",
   desc:"Prove algebraically that FOQDS splitting of {6174} adds exactly 1 to the nilpotent index. K54: x⁶(x−1), K55: x⁷(x−1).", priority:5, status:"OPEN"},
  {id:"OP-NEW-2", title:"True Cross-Base FOQDS Scaling Law",
   desc:"b(b+1)/2 holds only for b=10. Determine |Q_b| as a function of b. Connect to attractor structure per base.", priority:5, status:"OPEN"},
  {id:"OP-NEW-3", title:"Base-12 Anomaly",
   desc:"|Q₁₂| = 587 vs |Q₈| = 43 and |Q₁₄| = 1232. Verify computation and understand structural cause.", priority:4, status:"RECHECK"},
  {id:"OP-NEW-4", title:"Coupling Term δ: General Proof",
   desc:"Prove δ = dim(Σ V_ref_γ ∩ Σ V_bdry_γ) for all FDDS. Currently C2 on Kaprekar only.", priority:5, status:"OPEN"},
  {id:"OP-NEW-5", title:"Classification Completeness",
   desc:"Prove Classes I–IV are exhaustive and mutually exclusive. Formally prove Kaprekar ∈ Class IV.", priority:4, status:"OPEN"},
  {id:"OP-NEW-6", title:"Entropy–Rank Inequality",
   desc:"State precisely: rank(C) ≥ 1 iff H(T(X)|π(X)) > 0? Test on Kaprekar and Class III tree.", priority:3, status:"OPEN"},
  {id:"OP-NEW-7", title:"Transpose Mutant Invariance",
   desc:"K and Kᵀ satisfy the same minimal polynomial test. Determine whether this reveals a structural symmetry or a gap in the detector.", priority:3, status:"NEW"},
];

// ── COMPONENTS ─────────────────────────────────────────────

function Badge({color, children}) {
  const palettes = {
    green:  ["#0d2e1e","#34d399"], red:   ["#2e0d0d","#f87171"],
    gold:   ["#2e1e0d","#f59e0b"], blue:  ["#0d1e2e","#38bdf8"],
    orange: ["#2e180d","#fb923c"], purple:["#1a0d2e","#a78bfa"],
    cyan:   ["#0d2428","#22d3ee"],
  };
  const [bg, fg] = palettes[color] || palettes.blue;
  return <span style={{background:bg,border:`1px solid ${fg}`,color:fg,
    borderRadius:4,padding:"2px 8px",fontSize:10,fontWeight:700,
    letterSpacing:"0.06em",fontFamily:"monospace"}}>{children}</span>;
}

function PressureBar({score, max, color}) {
  const pct = score / max;
  return (
    <div style={{display:"flex",alignItems:"center",gap:8}}>
      <div style={{flex:1,height:6,background:C.border,borderRadius:3,overflow:"hidden"}}>
        <div style={{height:"100%",width:`${pct*100}%`,
          background:`linear-gradient(90deg,${color}88,${color})`,borderRadius:3,
          transition:"width 0.4s ease"}} />
      </div>
      <span style={{color:C.textDim,fontSize:10,fontFamily:"monospace",width:40}}>
        {score}/{max}
      </span>
    </div>
  );
}

function Pill({text, color}) {
  return <span style={{background:`${color}22`,border:`1px solid ${color}55`,
    color,borderRadius:20,padding:"2px 10px",fontSize:11,fontFamily:"monospace"}}>{text}</span>;
}

function Card({children, highlight, style}) {
  return <div style={{background:C.panel,border:`1px solid ${highlight||C.border}`,
    borderRadius:10,padding:"16px 20px",marginBottom:12,...(style||{})}}>{children}</div>;
}

function SectionHeader({eyebrow, title, accent}) {
  return (
    <div style={{marginBottom:20}}>
      {eyebrow && <div style={{color:accent||C.accent,fontSize:10,fontWeight:700,
        letterSpacing:"0.2em",textTransform:"uppercase",marginBottom:6}}>{eyebrow}</div>}
      <h2 style={{color:C.text,fontSize:20,fontWeight:800,margin:0,
        borderBottom:`1px solid ${C.border}`,paddingBottom:10}}>{title}</h2>
    </div>
  );
}

// ── PIPELINE DIAGRAM ──────────────────────────────────────
function PipelineDiagram() {
  const steps = [
    {label:"Idea",          sub:"C0",   c:C.textDim},
    {label:"Definition",    sub:"C0",   c:C.textDim},
    {label:"Executable\nSpec", sub:"C1", c:C.accent},
    {label:"Adversarial\nGen", sub:"C2", c:C.gold},
    {label:"Counterex.\nSearch",sub:"AV",c:C.orange},
    {label:"Indep.\nImpl",  sub:"AV",   c:C.orange},
    {label:"Proof",         sub:"P",    c:C.purple},
    {label:"Lean\nVerify",  sub:"PV",   c:C.green},
    {label:"Publication",   sub:"PV",   c:C.green},
  ];

  return (
    <div style={{overflowX:"auto",paddingBottom:8}}>
      <div style={{display:"flex",alignItems:"center",gap:0,minWidth:700}}>
        {steps.map((s,i) => (
          <div key={i} style={{display:"flex",alignItems:"center"}}>
            <div style={{display:"flex",flexDirection:"column",alignItems:"center",
              background:C.panel2,border:`1px solid ${s.c}44`,borderRadius:8,
              padding:"10px 14px",minWidth:80,textAlign:"center"}}>
              <div style={{color:s.c,fontSize:11,fontWeight:700,lineHeight:1.3,
                whiteSpace:"pre-line"}}>{s.label}</div>
              <div style={{background:`${s.c}22`,color:s.c,borderRadius:4,
                padding:"1px 6px",fontSize:10,fontWeight:800,marginTop:4,
                fontFamily:"monospace"}}>{s.sub}</div>
            </div>
            {i < steps.length-1 && (
              <div style={{color:C.muted,fontSize:18,padding:"0 4px"}}>→</div>
            )}
          </div>
        ))}
      </div>
      <div style={{color:C.red,fontSize:12,marginTop:12,fontStyle:"italic",paddingLeft:4}}>
        ↑ Key shift: proof is no longer the first serious verification step
      </div>
    </div>
  );
}

// ── PPI TABLE ─────────────────────────────────────────────
function PPITable() {
  const gradeColor = {PV:C.green,P:C.purple,AV:C.orange,C2:C.accent,C1:C.textDim,C0:C.textDim,KILLED:C.red};
  return (
    <div style={{fontFamily:"monospace",fontSize:12}}>
      <div style={{display:"grid",gridTemplateColumns:"140px 50px 1fr 200px",
        gap:"0 12px",color:C.textDim,borderBottom:`1px solid ${C.border}`,
        paddingBottom:6,marginBottom:6,fontSize:11}}>
        <span>Claim ID</span><span>Grade</span><span>Pressure</span><span>Statement</span>
      </div>
      {CLAIMS_REGISTRY.map(c => {
        const sc = pressureScore(c.ev);
        const g = gradeFromEv(c.ev, c.killed);
        const col = gradeColor[g] || C.textDim;
        return (
          <div key={c.id} style={{display:"grid",
            gridTemplateColumns:"140px 50px 1fr 200px",
            gap:"0 12px",marginBottom:8,opacity:c.killed?0.5:1}}>
            <span style={{color:c.killed?C.red:C.text,
              textDecoration:c.killed?"line-through":"none"}}>{c.id}</span>
            <span style={{color:col,fontWeight:700}}>{g}</span>
            <PressureBar score={sc} max={MAX_PRESSURE} color={col} />
            <span style={{color:C.textDim,fontSize:11,overflow:"hidden",
              textOverflow:"ellipsis",whiteSpace:"nowrap"}}>{c.stmt}</span>
          </div>
        );
      })}
      <div style={{color:C.textDim,fontSize:11,marginTop:8,borderTop:`1px solid ${C.border}`,paddingTop:6}}>
        MAX_PRESSURE = {MAX_PRESSURE} | Grades: C0→C1→C2→AV→P→PV | AV = Adversarially Verified
      </div>
    </div>
  );
}

// ── MUTATION TEST TABLE ───────────────────────────────────
function MutationTable() {
  return (
    <div>
      {MUTATION_RESULTS.map((m,i) => (
        <div key={i} style={{display:"flex",gap:12,alignItems:"flex-start",
          padding:"8px 0",borderBottom:`1px solid ${C.border}`,fontSize:13}}>
          <div style={{width:20,flexShrink:0,
            color:m.caught?C.green:C.red,fontWeight:700,fontSize:16}}>
            {m.caught ? "✓" : "⚠"}
          </div>
          <div style={{flex:1}}>
            <div style={{fontFamily:"monospace",color:m.caught?C.text:C.red,
              fontWeight:m.caught?400:700}}>{m.mutant}</div>
            <div style={{color:C.textDim,fontSize:12}}>{m.note}</div>
          </div>
          <Badge color={m.caught?"green":"red"}>{m.caught?"CAUGHT":"SURVIVED"}</Badge>
        </div>
      ))}
      <div style={{color:C.orange,fontSize:13,marginTop:10,
        borderLeft:`3px solid ${C.orange}`,paddingLeft:10}}>
        2 mutants survive: detector must be strengthened.
        Fix: check that k is minimal (k−1 test) AND that K is not symmetric/self-adjoint.
      </div>
    </div>
  );
}

// ── COLLISION ATLAS DISPLAY ───────────────────────────────
function CollisionDisplay() {
  const { systems, domain, distinctSigs, collidingSigs, maxBucket, example } = COLLISION_STATS;
  const coverage = distinctSigs / systems;
  return (
    <div>
      <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(140px,1fr))",gap:10,marginBottom:16}}>
        {[
          {l:"Systems tested",  v:systems,     c:C.accent},
          {l:"Distinct sigs",   v:distinctSigs, c:C.green},
          {l:"Colliding sigs",  v:collidingSigs,c:C.orange},
          {l:"Max bucket",      v:maxBucket,    c:C.red},
        ].map(x=>(
          <div key={x.l} style={{background:C.panel2,border:`1px solid ${x.c}44`,
            borderRadius:8,padding:"12px 14px"}}>
            <div style={{color:C.textDim,fontSize:10,textTransform:"uppercase",
              letterSpacing:"0.1em",marginBottom:4}}>{x.l}</div>
            <div style={{color:x.c,fontSize:24,fontWeight:800,fontFamily:"monospace"}}>{x.v}</div>
          </div>
        ))}
      </div>
      <Card>
        <div style={{color:C.textDim,fontSize:12,marginBottom:6}}>Domain: {domain}</div>
        <div style={{color:C.text,fontSize:13,marginBottom:4}}>
          <strong style={{color:C.orange}}>{collidingSigs}</strong> of {distinctSigs} signatures
          have collisions — {Math.round(collidingSigs/distinctSigs*100)}% of the signature space
          is degenerate under this observable.
        </div>
        <div style={{color:C.textDim,fontSize:12}}>Example: {example}</div>
        <div style={{color:C.accent,fontSize:12,marginTop:8}}>
          Each collision is a permanent research object: store minimal witness + reproduction script + affected theorem version.
        </div>
      </Card>
    </div>
  );
}

// ── MODULE GRID ───────────────────────────────────────────
function ModuleGrid() {
  return (
    <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(260px,1fr))",gap:12}}>
      {AML_MODULES.map(m => (
        <div key={m.id} style={{background:C.panel2,
          border:`1px solid ${m.status==="IMPLEMENTED"?m.color+"44":C.border}`,
          borderRadius:10,padding:"14px 16px"}}>
          <div style={{display:"flex",alignItems:"center",gap:8,marginBottom:8}}>
            <div style={{background:`${m.color}22`,color:m.color,
              borderRadius:6,padding:"4px 10px",fontWeight:800,fontSize:13,
              fontFamily:"monospace"}}>AML-{m.id}</div>
            <Badge color={m.status==="IMPLEMENTED"?"green":"orange"}>
              {m.status}
            </Badge>
          </div>
          <div style={{color:m.color,fontWeight:700,fontSize:13,marginBottom:6}}>
            {m.name}
          </div>
          <div style={{color:C.textDim,fontSize:12,lineHeight:1.6}}>{m.desc}</div>
        </div>
      ))}
    </div>
  );
}

// ── OPEN PROBLEMS ─────────────────────────────────────────
function OpenProblems() {
  const statusColor = {OPEN:C.accent,RECHECK:C.orange,NEW:C.purple};
  return (
    <div>
      {OPEN_PROBLEMS.map(op => (
        <div key={op.id} style={{background:C.panel,
          border:`1px solid ${statusColor[op.status]||C.border}33`,
          borderRadius:10,padding:"14px 18px",marginBottom:10}}>
          <div style={{display:"flex",gap:8,alignItems:"center",flexWrap:"wrap",marginBottom:6}}>
            <span style={{fontFamily:"monospace",color:C.accent,fontSize:12}}>{op.id}</span>
            <Pill text={op.status} color={statusColor[op.status]||C.accent} />
            <span style={{color:C.gold,fontSize:12}}>{"★".repeat(op.priority)}{"☆".repeat(5-op.priority)}</span>
          </div>
          <div style={{color:C.text,fontWeight:600,marginBottom:4}}>{op.title}</div>
          <div style={{color:C.textDim,fontSize:13,lineHeight:1.6}}>{op.desc}</div>
        </div>
      ))}
    </div>
  );
}

// ── CROSS-BASE TABLE ──────────────────────────────────────
function CrossBaseTable() {
  return (
    <div>
      <div style={{fontFamily:"monospace",fontSize:12}}>
        <div style={{display:"grid",gridTemplateColumns:"60px 80px 100px 80px 80px",
          gap:"0 12px",color:C.textDim,borderBottom:`1px solid ${C.border}`,
          paddingBottom:6,marginBottom:6}}>
          <span>Base</span><span>FOQDS</span><span>b(b+1)/2</span><span>Ratio</span><span>Match</span>
        </div>
        {CROSS_BASE.map(d => (
          <div key={d.b} style={{display:"grid",
            gridTemplateColumns:"60px 80px 100px 80px 80px",
            gap:"0 12px",marginBottom:4}}>
            <span style={{color:C.text}}>b={d.b}</span>
            <span style={{color:d.match?C.green:C.orange,fontWeight:d.b===12?700:400}}>
              {d.foqds.toLocaleString()}
            </span>
            <span style={{color:C.muted}}>{d.formula}</span>
            <span style={{color:C.text}}>{(d.foqds/d.formula).toFixed(2)}×</span>
            <span style={{color:d.match?C.green:C.red,fontWeight:700}}>
              {d.match?"YES ✓":"NO ✗"}
            </span>
          </div>
        ))}
      </div>
      <div style={{background:`${C.red}11`,border:`1px solid ${C.red}44`,
        borderRadius:8,padding:"10px 14px",marginTop:12}}>
        <div style={{color:C.red,fontWeight:700,fontSize:12,marginBottom:4}}>KILLED: b(b+1)/2 as universal law</div>
        <div style={{color:C.textDim,fontSize:12}}>
          Base 10 is a coincidence. b=12 (587) is anomalously large — suspect computation bug or multi-attractor regime.
          AML-C adversarial testing falsified this claim across 5 bases.
        </div>
      </div>
    </div>
  );
}

// ── MAIN APP ──────────────────────────────────────────────
export default function App() {
  const [tab, setTab] = useState("pipeline");
  const tabs = [
    {id:"pipeline",   label:"AML Pipeline"},
    {id:"modules",    label:"Modules"},
    {id:"ppi",        label:"Pressure Index"},
    {id:"mutations",  label:"Mutation Test"},
    {id:"collisions", label:"Collision Atlas"},
    {id:"crossbase",  label:"Cross-Base"},
    {id:"openprobs",  label:"Open Problems"},
  ];

  return (
    <div style={{background:C.bg,minHeight:"100vh",color:C.text,
      fontFamily:"'Inter',system-ui,sans-serif",
      maxWidth:960,margin:"0 auto",padding:"28px 20px"}}>

      {/* HEADER */}
      <div style={{marginBottom:32}}>
        <div style={{display:"flex",alignItems:"flex-start",gap:16,marginBottom:14}}>
          <div style={{flexShrink:0}}>
            <div style={{width:5,height:56,background:`linear-gradient(180deg,${C.accent},${C.purple})`,
              borderRadius:3}} />
          </div>
          <div style={{flex:1}}>
            <div style={{color:C.accent,fontSize:11,fontWeight:700,letterSpacing:"0.2em",
              textTransform:"uppercase",marginBottom:6}}>
              AQARION RESEARCH · NODE #10878
            </div>
            <h1 style={{color:C.text,fontSize:26,fontWeight:900,margin:"0 0 6px",
              letterSpacing:"-0.03em"}}>
              Adversarial Mathematics Laboratory
            </h1>
            <p style={{color:C.textDim,fontSize:13,margin:0,maxWidth:600}}>
              Every theorem enters the same pressure-testing pipeline. Proof is not the first serious verification step.
              Adversarial testing, counterexample search, independent implementation, and formal verification are each orthogonal evidence types.
            </p>
          </div>
          <div style={{display:"flex",flexDirection:"column",gap:6,flexShrink:0}}>
            <Badge color="blue">v1.0.0</Badge>
            <Badge color="green">AML ACTIVE</Badge>
            <Badge color="purple">10 MODULES</Badge>
          </div>
        </div>

        {/* Key metric strip */}
        <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(140px,1fr))",
          gap:8}}>
          {[
            {l:"Claims tracked",  v:"10",  c:C.accent},
            {l:"Claims killed",   v:"3",   c:C.red},
            {l:"AV or better",    v:"5",   c:C.orange},
            {l:"PV certified",    v:"1",   c:C.green},
            {l:"Mutants tested",  v:"5",   c:C.purple},
            {l:"Survivors (⚠)",  v:"2",   c:C.red},
          ].map(x=>(
            <div key={x.l} style={{background:C.panel,border:`1px solid ${x.c}33`,
              borderRadius:8,padding:"10px 14px",textAlign:"center"}}>
              <div style={{color:x.c,fontSize:22,fontWeight:900,fontFamily:"monospace"}}>{x.v}</div>
              <div style={{color:C.textDim,fontSize:10,textTransform:"uppercase",
                letterSpacing:"0.1em"}}>{x.l}</div>
            </div>
          ))}
        </div>
      </div>

      {/* NAV */}
      <div style={{display:"flex",gap:4,flexWrap:"wrap",marginBottom:28,
        borderBottom:`1px solid ${C.border}`}}>
        {tabs.map(t => (
          <button key={t.id} onClick={()=>setTab(t.id)} style={{
            background:tab===t.id ? `linear-gradient(135deg,${C.accent},${C.purple})` : "transparent",
            color:tab===t.id ? C.bg : C.textDim,
            border:"none",borderRadius:"6px 6px 0 0",
            padding:"8px 16px",fontSize:12,fontWeight:700,cursor:"pointer"}}>
            {t.label}
          </button>
        ))}
      </div>

      {/* CONTENT */}

      {tab === "pipeline" && (
        <div>
          <SectionHeader eyebrow="Core Innovation" title="The AML Verification Pipeline"
            accent={C.accent} />
          <Card>
            <div style={{color:C.textDim,fontSize:12,marginBottom:12}}>
              The pipeline treats every claim as adversarial until it survives systematic pressure:
            </div>
            <PipelineDiagram />
          </Card>
          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12}}>
            <Card highlight={C.green}>
              <div style={{color:C.green,fontWeight:700,marginBottom:10,fontSize:13}}>
                What this adds over traditional math:
              </div>
              {[
                "Executable properties — theorems become test contracts",
                "Adversarial generation — test cases built to break claims",
                "Mutation testing — implementation correctness verified",
                "Counterexample minimization — minimal witnesses, not just failures",
                "Collision atlas — invariant completeness is permanently tracked",
                "Proof Pressure Index — evidence accumulates, grade is earned",
              ].map((s,i)=>(
                <div key={i} style={{color:C.text,fontSize:12,padding:"3px 0",
                  borderBottom:i<5?`1px solid ${C.border}`:"none"}}>
                  <span style={{color:C.green}}>+ </span>{s}
                </div>
              ))}
            </Card>
            <Card highlight={C.red}>
              <div style={{color:C.red,fontWeight:700,marginBottom:10,fontSize:13}}>
                Key caution (from v16 proposal):
              </div>
              <div style={{color:C.text,fontSize:13,lineHeight:1.7}}>
                Adversarial testing, exhaustive computation, and formal verification strengthen
                confidence in <em>different</em> ways. None substitute for a general mathematical
                proof when a universal theorem is claimed.
                <br/><br/>
                <span style={{color:C.textDim}}>
                  AV (adversarially verified) is a grade between C2 and P — not a synonym for P.
                  Keep evidence types orthogonal. The PPI enforces this.
                </span>
              </div>
            </Card>
          </div>

          <Card>
            <div style={{color:C.gold,fontWeight:700,marginBottom:10,fontSize:13}}>
              New evidence grade: AV (Adversarially Verified)
            </div>
            <div style={{display:"grid",gridTemplateColumns:"repeat(7,1fr)",gap:6}}>
              {[
                {g:"C0", desc:"Concept only",     c:C.textDim},
                {g:"C1", desc:"Model defined",     c:C.textDim},
                {g:"C2", desc:"Exhaustive search", c:C.accent},
                {g:"AV", desc:"+ adversarial",     c:C.orange},
                {g:"P",  desc:"Math proof",        c:C.purple},
                {g:"PV", desc:"Proof + Lean",      c:C.green},
                {g:"✗",  desc:"KILLED",            c:C.red},
              ].map(x=>(
                <div key={x.g} style={{background:C.panel2,border:`1px solid ${x.c}44`,
                  borderRadius:8,padding:"10px",textAlign:"center"}}>
                  <div style={{color:x.c,fontSize:16,fontWeight:900,fontFamily:"monospace"}}>{x.g}</div>
                  <div style={{color:C.textDim,fontSize:9,marginTop:4}}>{x.desc}</div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}

      {tab === "modules" && (
        <div>
          <SectionHeader eyebrow="Laboratory Infrastructure" title="AML Modules A–J"
            accent={C.cyan} />
          <ModuleGrid />
        </div>
      )}

      {tab === "ppi" && (
        <div>
          <SectionHeader eyebrow="Proof Pressure Index" title="Evidence Registry — All Active Claims"
            accent={C.purple} />
          <Card>
            <PPITable />
          </Card>
          <Card>
            <div style={{color:C.gold,fontWeight:700,marginBottom:10,fontSize:13}}>
              Evidence weight system (MAX = {MAX_PRESSURE}):
            </div>
            <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(180px,1fr))",gap:8}}>
              {Object.entries(EVIDENCE_WEIGHTS).map(([k,w])=>(
                <div key={k} style={{display:"flex",justifyContent:"space-between",
                  padding:"4px 8px",background:C.panel2,borderRadius:6,fontSize:12}}>
                  <span style={{color:C.textDim}}>{k.replace(/_/g," ")}</span>
                  <span style={{color:C.gold,fontFamily:"monospace",fontWeight:700}}>+{w}</span>
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}

      {tab === "mutations" && (
        <div>
          <SectionHeader eyebrow="AML-G · Implementation Mutation Testing"
            title="Detector vs Mutants — Kaprekar K54 (k=6)"
            accent={C.red} />
          <Card>
            <div style={{color:C.textDim,fontSize:12,marginBottom:12}}>
              Testing minimal polynomial detector against known implementation errors.
              A correctly-written test suite should catch ALL mutants.
            </div>
            <MutationTable />
          </Card>
          <Card highlight={C.orange}>
            <div style={{color:C.orange,fontWeight:700,marginBottom:10,fontSize:13}}>
              Required fixes to eliminate survivors:
            </div>
            <div style={{fontSize:13,lineHeight:1.8,color:C.text}}>
              <div>
                <strong style={{color:C.accent}}>Transpose survivor:</strong> Add test that K ≠ Kᵀ
                (stochastic matrices are not symmetric). Or test that the right eigenvectors differ.
              </div>
              <div style={{marginTop:8}}>
                <strong style={{color:C.accent}}>Off-by-one k+1 survivor:</strong> Minimal polynomial
                means the SMALLEST k such that K^k(K−I) = 0. Add a check that K^(k−1)(K−I) ≠ 0.
                This is already in the definition — the detector was incomplete.
              </div>
            </div>
          </Card>
        </div>
      )}

      {tab === "collisions" && (
        <div>
          <SectionHeader eyebrow="AML-E · Collision Atlas"
            title="Observable Signature Collisions"
            accent={C.cyan} />
          <CollisionDisplay />
          <Card>
            <div style={{color:C.purple,fontWeight:700,marginBottom:10,fontSize:13}}>
              Why collisions matter (borrowing from WL in graph isomorphism):
            </div>
            <div style={{color:C.text,fontSize:13,lineHeight:1.7}}>
              A collision = two distinct FDDS systems with the same observable signature.
              These are the <em>indistinguishable pairs</em> under the current invariant.
              In WL theory, these became canonical benchmarks for testing GNN completeness.
              <br/><br/>
              For AQARION: each collision bucket is a permanent research object.
              Store: minimal witness, reproduction script, affected theorem, version discovered.
              <br/><br/>
              <span style={{color:C.textDim}}>
                49/94 signature types (52%) have collisions under mod-3 observable on 10-state systems.
                This means the mod-3 observable is highly degenerate — useful for stress-testing
                theorems that claim to separate systems.
              </span>
            </div>
          </Card>
        </div>
      )}

      {tab === "crossbase" && (
        <div>
          <SectionHeader eyebrow="Cross-Base Audit · AML-C Result"
            title="FOQDS Counts vs b(b+1)/2"
            accent={C.orange} />
          <CrossBaseTable />
        </div>
      )}

      {tab === "openprobs" && (
        <div>
          <SectionHeader eyebrow="Active Research Frontier"
            title="Open Problems — v11+v12.1+AML Audit"
            accent={C.gold} />
          <OpenProblems />
        </div>
      )}

      {/* FOOTER */}
      <div style={{borderTop:`1px solid ${C.border}`,marginTop:40,paddingTop:16,
        display:"flex",justifyContent:"space-between",flexWrap:"wrap",gap:8,
        fontSize:11,color:C.textDim}}>
        <span>AQARION Research Node #10878 · AML v1.0.0 · 2026-06-21</span>
        <span style={{color:C.accent}}>Prove First · Predict Second · No Free Parameters</span>
        <span>MIT (code) / CC-BY-4.0 (docs) · Open Source</span>
      </div>
    </div>
  );
}
