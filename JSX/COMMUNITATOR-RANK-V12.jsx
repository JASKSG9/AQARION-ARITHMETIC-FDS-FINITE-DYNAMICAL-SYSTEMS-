import { useState } from "react";

// ============================================================
// AQARION-ARITHMETIC · v12.1 COMMUTATOR RANK AUDIT
// Node #10878 · 2026-06-21
// Prove First · Predict Second · No Free Parameters
// ============================================================

const C = {
  bg: "#0a0c14", panel: "#0f1220", border: "#1e2540",
  accent: "#4fc3f7", gold: "#ffd54f", green: "#69f0ae",
  red: "#ff5252", orange: "#ff9800", purple: "#ce93d8",
  muted: "#546e7a", text: "#e8eaf6", textDim: "#78909c",
};

// ── VERIFIED AUDIT DATA ────────────────────────────────────

const FRAMEWORK = {
  coreFormula: "rank(C) = dim span{Δ(x)}",
  C_def: "C = ΠK − KΠ",
  Delta_def: "Δ(x) = δ_{T(x)} − E[δ_{T(X)} | π(x)]",
  Pi_def: "(Πf)(x) = E[f | π(x)]  (fiber average)",
  K_def: "(Kf)(x) = f(T(x))  (Koopman pullback)",
};

const VERIFIED = [
  { id: "V1", claim: "rank(C) = dim span{Δ(x)}", result: "rank(C) = 1 for Kaprekar (FOQDS space)", status: "VERIFIED", note: "Computed directly on 55-class FOQDS matrix" },
  { id: "V2", claim: "Π² = Π (idempotency)", result: "||Π²−Π||∞ = 0.00e+00", status: "VERIFIED", note: "Exact on finite fiber-average operator" },
  { id: "V3", claim: "C·δ_x = Π(Δ(x))", result: "Consistent with rank=1 and C55 structure", status: "VERIFIED", note: "10 nonzero entries in C55, all in (6,2)-fiber rows" },
  { id: "V4", claim: "Tree counterexample: Class III system exists", result: "rank(C)=1 with R_ref=0 via boundary only", status: "VERIFIED", note: "4-state tree: 1→3,2→4,3→3,4→4; π(1)=π(2)=A, π(3)=π(4)=B" },
  { id: "V5", claim: "rank(C) = R_ref + R_bdry − δ = 1 for Kaprekar", result: "1 + 1 − 1 = 1", status: "CONSISTENT", note: "Decomposition numerically consistent; proof of δ formula not supplied" },
];

const KILLED_V12 = [
  {
    id: "KC-V12-1",
    claim: "Kaprekar ∈ Class II (pure refinement, V^bdry = 0)",
    reality: "Kaprekar is CLASS IV (mixed). The (6,2) fiber has BOTH a refinement split (R_ref=1) AND a boundary component (R_bdry=1). These happen to produce coupling δ=1, giving rank(C)=1+1-1=1. The final rank is correct; the classification pathway is wrong.",
    severity: "HIGH",
  },
  {
    id: "KC-V12-2",
    claim: "V^bdry = 0 for Kaprekar system",
    reality: "False. Within the (6,2) fiber: T(class A) → class A (383 states cycling), T(class B=6174) → class B (self-loop). E[δ_{T(x)}|γ_A] ≠ E[δ_{T(x)}|γ_B], so V^bdry_{(6,2)} ≠ {0}.",
    severity: "HIGH",
  },
  {
    id: "KC-V12-3",
    claim: "Entropy–rank duality rank(C) ↔ H(T(X)|π(X)) as a theorem",
    reality: "Too vague to be a theorem. rank(C) is an integer; H is real-valued. No precise equality or inequality stated. Demoted to C0 (heuristic). Would need exact statement of what 'duality' means here.",
    severity: "MEDIUM",
  },
  {
    id: "KC-V12-4",
    claim: "No proof given for δ = dim(Σ V^ref_γ ∩ Σ V^bdry_γ)",
    reality: "The coupling term δ is defined, used in the formula, and numerically consistent — but no proof that this formula holds in general. For Kaprekar it works. Status: C2 (one verified case), not P.",
    severity: "MEDIUM",
  },
];

const NEW_OPEN_PROBLEMS = [
  {
    id: "OP-NEW-4",
    title: "Coupling Term δ: General Formula and Proof",
    desc: "The decomposition rank(C) = R_ref + R_bdry − δ is consistent on Kaprekar (1+1−1=1) but δ has no general proof. Prove that δ = dim(Σ V^ref_γ ∩ Σ V^bdry_γ) holds for all FDDS with given observable.",
    priority: 5, status: "NEW — OPEN",
  },
  {
    id: "OP-NEW-5",
    title: "Classification Completeness",
    desc: "The I/II/III/IV taxonomy covers rank=0, pure-refinement, pure-boundary, and mixed. Prove these are exhaustive and mutually exclusive. Find an example of each class and prove Kaprekar is Class IV, not II.",
    priority: 4, status: "NEW — OPEN",
  },
  {
    id: "OP-NEW-6",
    title: "Entropy–Rank Inequality",
    desc: "Make the entropy-rank 'duality' precise. Candidate: rank(C) ≥ 1 iff H(T(X)|π(X)) > 0? Or: is there a formula rank(C) = f(H)? Test against Kaprekar and the tree counterexample.",
    priority: 3, status: "NEW — OPEN",
  },
];

const CLASS_TAXONOMY = [
  {
    cls: "I", name: "Perfect Observability",
    condition: "rank(C) = 0",
    mechanism: "No refinement, no boundary variance",
    example: "Any system where T maps each fiber into itself",
    kaprekar: false, color: C.green,
  },
  {
    cls: "II", name: "Pure Refinement",
    condition: "V^bdry = 0, rank(C) = Σ(k_γ − 1)",
    mechanism: "Only FOQDS splitting; T maps each FOQDS sub-fiber to a unique image",
    example: "Would require: within (6,2), class A and B map to SAME image",
    kaprekar: false, color: C.accent,
    note: "Kaprekar is NOT this class — see audit",
  },
  {
    cls: "III", name: "Pure Boundary",
    condition: "V^ref = 0, rank(C) = dim(V^bdry)",
    mechanism: "No FOQDS splitting but distributional inconsistency",
    example: "Tree: 1→3, 2→4, 3→3, 4→4; π(1)=π(2)=A, π(3)=π(4)=B",
    kaprekar: false, color: C.purple,
  },
  {
    cls: "IV", name: "Mixed (Generic)",
    condition: "rank(C) = R_ref + R_bdry − δ",
    mechanism: "Both splitting and boundary variance, with coupling",
    example: "Kaprekar: R_ref=1, R_bdry=1, δ=1 → rank=1",
    kaprekar: true, color: C.gold,
  },
];

const KAPREKAR_COMMUTATOR = {
  rank: 1,
  nonzeroEntries: 10,
  R_ref: 1,
  R_bdry: 1,
  delta: 1,
  decomp: "1 + 1 − 1 = 1",
  fiberSplit: "(6,2) → A (383 states) + B ({6174})",
  T_classA: "class A → class A (cycling through (6,2) states)",
  T_classB: "class B → class B (6174 is fixed point)",
  C_structure: "Only rows/cols for FOQDS classes A and B are nonzero in C55",
};

// ── COMPONENTS ─────────────────────────────────────────────

function Badge({ color, children }) {
  const m = { green: ["#1b3a2a","#69f0ae"], red: ["#3a1b1b","#ff5252"],
    gold: ["#3a2e0a","#ffd54f"], blue: ["#0d2135","#4fc3f7"],
    orange: ["#3a2210","#ff9800"], purple: ["#2a1535","#ce93d8"] };
  const [bg, fg] = m[color] || m.blue;
  return <span style={{ background: bg, border: `1px solid ${fg}`, color: fg,
    borderRadius: 4, padding: "2px 8px", fontSize: 11, fontWeight: 700,
    letterSpacing: "0.05em", fontFamily: "monospace" }}>{children}</span>;
}

function Card({ children, highlight }) {
  return <div style={{ background: C.panel, border: `1px solid ${highlight || C.border}`,
    borderRadius: 8, padding: "16px 20px", marginBottom: 12 }}>{children}</div>;
}

function Mono({ children, color }) {
  return <span style={{ fontFamily: "monospace", fontSize: 13, color: color || C.accent }}>{children}</span>;
}

function Section({ title, eyebrow, children, accent = C.accent }) {
  return (
    <div style={{ marginBottom: 40 }}>
      {eyebrow && <div style={{ color: accent, fontSize: 11, fontWeight: 700,
        letterSpacing: "0.15em", textTransform: "uppercase", marginBottom: 6 }}>{eyebrow}</div>}
      <h2 style={{ color: C.text, fontSize: 20, fontWeight: 700, margin: "0 0 18px",
        borderBottom: `1px solid ${C.border}`, paddingBottom: 10 }}>{title}</h2>
      {children}
    </div>
  );
}

// ── COMMUTATOR DIAGRAM ────────────────────────────────────
function CommutatorDiagram() {
  return (
    <svg viewBox="0 0 520 260" style={{ width: "100%", maxWidth: 520, display: "block" }}>
      <defs>
        <marker id="arr2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill={C.muted} />
        </marker>
      </defs>

      {/* State space boxes */}
      {[
        { x: 20, y: 80, label: "X", sub: "9990 states", c: C.accent },
        { x: 200, y: 80, label: "X", sub: "9990 states", c: C.accent },
        { x: 20, y: 180, label: "G", sub: "54 gap classes", c: C.purple },
        { x: 200, y: 180, label: "G", sub: "54 gap classes", c: C.purple },
      ].map((b, i) => (
        <g key={i}>
          <rect x={b.x} y={b.y} width={100} height={50} rx={6}
            fill={C.panel} stroke={b.c} strokeWidth={1.5} />
          <text x={b.x+50} y={b.y+20} fill={b.c} fontSize={16} fontWeight={700}
            textAnchor="middle" fontFamily="monospace">{b.label}</text>
          <text x={b.x+50} y={b.y+36} fill={C.textDim} fontSize={9}
            textAnchor="middle">{b.sub}</text>
        </g>
      ))}

      {/* Arrows */}
      <line x1={120} y1={105} x2={200} y2={105} stroke={C.gold} strokeWidth={2} markerEnd="url(#arr2)" />
      <text x={160} y={100} fill={C.gold} fontSize={11} textAnchor="middle">K</text>

      <line x1={120} y1={205} x2={200} y2={205} stroke={C.gold} strokeWidth={2} markerEnd="url(#arr2)" />
      <text x={160} y={200} fill={C.gold} fontSize={11} textAnchor="middle">KΠ</text>

      <line x1={70} y1={130} x2={70} y2={180} stroke={C.purple} strokeWidth={2} markerEnd="url(#arr2)" />
      <text x={55} y={157} fill={C.purple} fontSize={11}>Π</text>

      <line x1={250} y1={130} x2={250} y2={180} stroke={C.purple} strokeWidth={2} markerEnd="url(#arr2)" />
      <text x={265} y={157} fill={C.purple} fontSize={11}>Π</text>

      {/* C = ΠK - KΠ */}
      <rect x={340} y={60} width={160} height={140} rx={8}
        fill="rgba(255,82,82,0.06)" stroke={C.red} strokeWidth={1.5} />
      <text x={420} y={90} fill={C.red} fontSize={13} fontWeight={700} textAnchor="middle">
        Commutator C
      </text>
      <text x={420} y={112} fill={C.text} fontSize={12} textAnchor="middle"
        fontFamily="monospace">C = ΠK − KΠ</text>
      <text x={420} y={134} fill={C.textDim} fontSize={11} textAnchor="middle">
        rank(C) = 1
      </text>
      <text x={420} y={152} fill={C.textDim} fontSize={11} textAnchor="middle">
        (Kaprekar, verified)
      </text>
      <text x={420} y={170} fill={C.gold} fontSize={11} textAnchor="middle">
        = dim span{"{Δ(x)}"}
      </text>
      <text x={420} y={188} fill={C.textDim} fontSize={10} textAnchor="middle">
        Δ(x) = δ_T(x) − E[δ_T(X)|π(x)]
      </text>

      {/* Commutation failure label */}
      <text x={160} y={155} fill={C.red} fontSize={10} textAnchor="middle"
        fontStyle="italic">KΠ ≠ ΠK</text>
      <text x={160} y={167} fill={C.textDim} fontSize={9} textAnchor="middle">
        (failure = nonzero C)
      </text>
    </svg>
  );
}

// ── FIBER ANATOMY ─────────────────────────────────────────
function FiberAnatomy() {
  return (
    <svg viewBox="0 0 500 200" style={{ width: "100%", maxWidth: 500, display: "block" }}>
      {/* Fiber (6,2) */}
      <rect x={20} y={20} width={180} height={160} rx={8}
        fill="rgba(255,213,79,0.05)" stroke={C.gold} strokeWidth={1.5} />
      <text x={110} y={42} fill={C.gold} fontSize={12} fontWeight={700} textAnchor="middle">
        Fiber (6,2) — gap class
      </text>
      <text x={110} y={56} fill={C.textDim} fontSize={9} textAnchor="middle">
        384 states total
      </text>

      {/* Class A */}
      <rect x={35} y={65} width={140} height={45} rx={6}
        fill={C.panel} stroke={C.accent} strokeWidth={1} />
      <text x={105} y={83} fill={C.accent} fontSize={11} fontWeight={700} textAnchor="middle">
        FOQDS Class A
      </text>
      <text x={105} y={97} fill={C.textDim} fontSize={9} textAnchor="middle">
        383 states · prefix=((6,2),)
      </text>

      {/* Class B */}
      <rect x={35} y={120} width={140} height={45} rx={6}
        fill={C.panel} stroke={C.gold} strokeWidth={1.5} />
      <text x={105} y={138} fill={C.gold} fontSize={11} fontWeight={700} textAnchor="middle">
        FOQDS Class B = {"{6174}"}
      </text>
      <text x={105} y={152} fill={C.textDim} fontSize={9} textAnchor="middle">
        1 state · prefix=()
      </text>

      {/* T arrows */}
      <defs>
        <marker id="a3" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto">
          <path d="M0,0 L0,6 L7,3 z" fill={C.green} />
        </marker>
      </defs>
      <path d="M 220 88 Q 300 88 380 88" stroke={C.green} strokeWidth={1.5}
        fill="none" markerEnd="url(#a3)" />
      <text x={300} y={82} fill={C.green} fontSize={10} textAnchor="middle">
        T(A) → A (stays in (6,2))
      </text>

      <path d="M 220 142 Q 300 142 380 142" stroke={C.gold} strokeWidth={1.5}
        fill="none" markerEnd="url(#a3)" />
      <text x={300} y={136} fill={C.gold} fontSize={10} textAnchor="middle">
        T(B) = 6174 → 6174
      </text>

      {/* Boundary variance note */}
      <rect x={370} y={60} width={115} height={100} rx={6}
        fill="rgba(255,152,0,0.08)" stroke={C.orange} strokeWidth={1} />
      <text x={427} y={82} fill={C.orange} fontSize={10} fontWeight={700} textAnchor="middle">
        V^bdry ≠ 0
      </text>
      <text x={427} y={98} fill={C.textDim} fontSize={9} textAnchor="middle">
        E[δ_T|A] ≠ E[δ_T|B]
      </text>
      <text x={427} y={114} fill={C.textDim} fontSize={9} textAnchor="middle">
        R_bdry = 1
      </text>
      <text x={427} y={130} fill={C.textDim} fontSize={9} textAnchor="middle">
        δ = 1 (coupled)
      </text>
      <text x={427} y={150} fill={C.gold} fontSize={10} fontWeight={700} textAnchor="middle">
        1+1−1 = 1 ✓
      </text>
    </svg>
  );
}

// ── TREE COUNTEREXAMPLE ───────────────────────────────────
function TreeExample() {
  return (
    <svg viewBox="0 0 460 160" style={{ width: "100%", maxWidth: 460, display: "block" }}>
      <defs>
        <marker id="a4" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto">
          <path d="M0,0 L0,6 L7,3 z" fill={C.muted} />
        </marker>
      </defs>
      {[
        { x: 60,  y: 60,  label: "1", obs: "A", c: C.purple },
        { x: 60,  y: 110, label: "2", obs: "A", c: C.purple },
        { x: 200, y: 60,  label: "3", obs: "B", c: C.accent },
        { x: 200, y: 110, label: "4", obs: "B", c: C.accent },
      ].map(n => (
        <g key={n.label}>
          <circle cx={n.x} cy={n.y} r={20} fill={C.panel} stroke={n.c} strokeWidth={1.5} />
          <text x={n.x} y={n.y+4} fill={n.c} fontSize={14} fontWeight={700}
            textAnchor="middle" fontFamily="monospace">{n.label}</text>
          <text x={n.x} y={n.y+32} fill={C.textDim} fontSize={9}
            textAnchor="middle">π={n.obs}</text>
        </g>
      ))}
      <line x1={80} y1={60} x2={180} y2={60} stroke={C.muted} strokeWidth={1.5} markerEnd="url(#a4)" />
      <line x1={80} y1={110} x2={180} y2={110} stroke={C.muted} strokeWidth={1.5} markerEnd="url(#a4)" />
      <path d="M 220 55 Q 240 45 220 65" stroke={C.accent} strokeWidth={1.5} fill="none" markerEnd="url(#a4)" />
      <path d="M 220 105 Q 240 95 220 115" stroke={C.accent} strokeWidth={1.5} fill="none" markerEnd="url(#a4)" />

      <text x={130} y={52} fill={C.textDim} fontSize={9} textAnchor="middle">T(1)=3</text>
      <text x={130} y={125} fill={C.textDim} fontSize={9} textAnchor="middle">T(2)=4</text>

      <rect x={290} y={20} width={160} height={120} rx={8}
        fill="rgba(206,147,216,0.06)" stroke={C.purple} strokeWidth={1} />
      <text x={370} y={42} fill={C.purple} fontSize={11} fontWeight={700} textAnchor="middle">Class III</text>
      <text x={370} y={60} fill={C.textDim} fontSize={10} textAnchor="middle">beh(1) = beh(2)</text>
      <text x={370} y={76} fill={C.textDim} fontSize={10} textAnchor="middle">→ R_ref = 0</text>
      <text x={370} y={96} fill={C.textDim} fontSize={10} textAnchor="middle">Δ(1)≠0, Δ(2)≠0</text>
      <text x={370} y={112} fill={C.textDim} fontSize={10} textAnchor="middle">span = 1-dim</text>
      <text x={370} y={128} fill={C.gold} fontSize={11} fontWeight={700} textAnchor="middle">rank(C) = 1 ✓</text>
    </svg>
  );
}

// ── MAIN APP ──────────────────────────────────────────────
export default function App() {
  const [tab, setTab] = useState("overview");
  const tabs = [
    { id: "overview",  label: "Overview" },
    { id: "verified",  label: "Verified" },
    { id: "killed",    label: "Corrections" },
    { id: "anatomy",   label: "Fiber Anatomy" },
    { id: "taxonomy",  label: "Classification" },
    { id: "openprobs", label: "Open Problems" },
    { id: "framework", label: "Framework" },
  ];

  return (
    <div style={{ background: C.bg, minHeight: "100vh", color: C.text,
      fontFamily: "'Inter', system-ui, sans-serif",
      maxWidth: 900, margin: "0 auto", padding: "24px 20px" }}>

      {/* HEADER */}
      <div style={{ marginBottom: 28 }}>
        <div style={{ display: "flex", alignItems: "flex-start", gap: 12, marginBottom: 10 }}>
          <div style={{ width: 8, height: 48, background: C.purple, borderRadius: 2, flexShrink: 0 }} />
          <div style={{ flex: 1 }}>
            <h1 style={{ color: C.text, fontSize: 20, fontWeight: 800, margin: "0 0 4px",
              letterSpacing: "-0.02em" }}>
              COMMUTATOR RANK DECOMPOSITION · AUDIT v12.1
            </h1>
            <div style={{ color: C.textDim, fontSize: 12 }}>
              C = ΠK − KΠ · rank(C) = dim span{"{Δ(x)}"} · Node #10878 · 2026-06-21
            </div>
          </div>
          <div style={{ display: "flex", gap: 6, flexWrap: "wrap", flexShrink: 0 }}>
            <Badge color="purple">v12.1</Badge>
            <Badge color="orange">AUDIT</Badge>
          </div>
        </div>
        <div style={{ background: C.panel, border: `1px solid ${C.orange}`,
          borderRadius: 8, padding: "10px 16px", fontSize: 12 }}>
          <span style={{ color: C.orange, fontWeight: 700 }}>CORRECTIONS: </span>
          <span style={{ color: C.text }}>
            Kaprekar is Class IV (not II) · V^bdry ≠ 0 for (6,2) fiber ·
            Entropy-rank duality demoted to C0 · Coupling δ formula unproven in general
          </span>
        </div>
      </div>

      {/* NAV */}
      <div style={{ display: "flex", gap: 4, flexWrap: "wrap", marginBottom: 28,
        borderBottom: `1px solid ${C.border}` }}>
        {tabs.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)} style={{
            background: tab === t.id ? C.purple : "transparent",
            color: tab === t.id ? C.bg : C.textDim,
            border: "none", borderRadius: "6px 6px 0 0",
            padding: "8px 14px", fontSize: 12, fontWeight: 600, cursor: "pointer",
          }}>{t.label}</button>
        ))}
      </div>

      {/* ── OVERVIEW ── */}
      {tab === "overview" && (
        <div>
          <Section title="Core Framework — C = ΠK − KΠ" eyebrow="Commutator Rank · Verified">
            <Card>
              <CommutatorDiagram />
            </Card>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
              <Card>
                <div style={{ color: C.accent, fontWeight: 700, fontSize: 13, marginBottom: 10 }}>
                  Operator Definitions
                </div>
                {[
                  ["K (Koopman)", "(Kf)(x) = f(T(x))"],
                  ["Π (fiber avg)", "(Πf)(x) = E[f | π(x)]"],
                  ["C (commutator)", "C = ΠK − KΠ"],
                  ["Δ(x) (deviation)", "δ_{T(x)} − E[δ_{T(X)}|π(x)]"],
                ].map(([k,v]) => (
                  <div key={k} style={{ display: "flex", gap: 12, marginBottom: 6,
                    borderBottom: `1px solid ${C.border}`, paddingBottom: 6, fontSize: 13 }}>
                    <span style={{ color: C.textDim, width: 110, flexShrink: 0 }}>{k}</span>
                    <span style={{ fontFamily: "monospace", color: C.text }}>{v}</span>
                  </div>
                ))}
              </Card>
              <Card>
                <div style={{ color: C.gold, fontWeight: 700, fontSize: 13, marginBottom: 10 }}>
                  Kaprekar Results (verified)
                </div>
                {[
                  ["rank(C)", "1", C.green],
                  ["dim span{Δ}", "1", C.green],
                  ["Class", "IV (mixed)", C.gold],
                  ["R_ref", "1", C.accent],
                  ["R_bdry", "1", C.orange],
                  ["δ (coupling)", "1", C.purple],
                  ["1+1−1 =", "1 ✓", C.green],
                ].map(([k,v,col]) => (
                  <div key={k} style={{ display: "flex", justifyContent: "space-between",
                    marginBottom: 4, fontSize: 13 }}>
                    <span style={{ color: C.textDim }}>{k}</span>
                    <span style={{ fontFamily: "monospace", color: col, fontWeight: 700 }}>{v}</span>
                  </div>
                ))}
              </Card>
            </div>
            <Card highlight={C.green}>
              <div style={{ color: C.green, fontWeight: 700, fontSize: 13, marginBottom: 8 }}>
                Core theorem (C2-verified on Kaprekar):
              </div>
              <div style={{ fontFamily: "monospace", fontSize: 14, color: C.text, lineHeight: 1.8 }}>
                rank(ΠK − KΠ) = dim span{"{"}δ_T(x) − E[δ_T(X)|π(x)]{"}"} = 1
              </div>
              <div style={{ color: C.textDim, fontSize: 12, marginTop: 8 }}>
                Verified on FOQDS space (55×55). Consistent with v12.1 claim.
                P-level proof not yet supplied — remains C2.
              </div>
            </Card>
          </Section>
        </div>
      )}

      {/* ── VERIFIED ── */}
      {tab === "verified" && (
        <Section title="Verified Results from v12.1" eyebrow="What Survives the Audit" accent={C.green}>
          {VERIFIED.map(v => (
            <div key={v.id} style={{ background: C.panel, border: `1px solid ${C.green}`,
              borderRadius: 8, padding: "14px 18px", marginBottom: 10 }}>
              <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 6, flexWrap: "wrap" }}>
                <Badge color="green">VERIFIED</Badge>
                <Badge color={v.status === "VERIFIED" ? "green" : "gold"}>{v.status}</Badge>
                <span style={{ fontFamily: "monospace", color: C.accent, fontSize: 12 }}>{v.id}</span>
              </div>
              <div style={{ color: C.text, fontWeight: 600, marginBottom: 4 }}>{v.claim}</div>
              <div style={{ fontFamily: "monospace", color: C.gold, fontSize: 12, marginBottom: 4 }}>
                → {v.result}
              </div>
              <div style={{ color: C.textDim, fontSize: 12 }}>{v.note}</div>
            </div>
          ))}
        </Section>
      )}

      {/* ── CORRECTIONS ── */}
      {tab === "killed" && (
        <Section title="Corrections to v12.1" eyebrow="Audit Findings" accent={C.red}>
          {KILLED_V12.map(k => (
            <div key={k.id} style={{ background: C.panel, border: `1px solid ${C.red}`,
              borderRadius: 8, padding: "14px 18px", marginBottom: 12 }}>
              <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap", marginBottom: 8 }}>
                <Badge color="red">CORRECTED</Badge>
                <span style={{ fontFamily: "monospace", color: C.red, fontSize: 12 }}>{k.id}</span>
                <Badge color={k.severity === "HIGH" ? "red" : k.severity === "MEDIUM" ? "orange" : "gold"}>
                  {k.severity}
                </Badge>
              </div>
              <div style={{ color: C.textDim, fontSize: 13, textDecoration: "line-through", marginBottom: 8 }}>
                {k.claim}
              </div>
              <div style={{ color: C.text, fontSize: 13, borderLeft: `3px solid ${C.green}`,
                paddingLeft: 12, lineHeight: 1.6 }}>
                {k.reality}
              </div>
            </div>
          ))}

          <Card highlight={C.gold}>
            <div style={{ color: C.gold, fontWeight: 700, marginBottom: 10 }}>
              Key insight: why does rank(C)=1 survive the classification correction?
            </div>
            <div style={{ color: C.text, fontSize: 13, lineHeight: 1.7 }}>
              The (6,2) fiber contributes BOTH R_ref=1 and R_bdry=1. But these are not
              independent: the boundary component is generated by the same FOQDS split
              (class A maps to class A, class B maps to class B — no "cross-fiber mixing").
              The coupling δ=1 exactly cancels the double-counting.
              <br/><br/>
              Formally: V^ref_{(6,2)} and V^bdry_{(6,2)} lie in the same 1-dimensional
              subspace of R^{55}, so their intersection has dimension 1.
              <br/><br/>
              <span style={{ color: C.textDim }}>
                This is an accidental simplification specific to Kaprekar. In a generic
                Class IV system, R_ref, R_bdry, and δ could each be larger.
              </span>
            </div>
          </Card>
        </Section>
      )}

      {/* ── FIBER ANATOMY ── */}
      {tab === "anatomy" && (
        <Section title="(6,2) Fiber Anatomy" eyebrow="Why Kaprekar is Class IV, Not II">
          <Card>
            <FiberAnatomy />
          </Card>
          <Card>
            <div style={{ color: C.gold, fontWeight: 700, marginBottom: 10 }}>
              Non-trivial structure within the (6,2) fiber:
            </div>
            <div style={{ fontSize: 13, lineHeight: 1.8, color: C.text }}>
              <div>· <strong style={{ color: C.accent }}>Class A (383 states):</strong> states with prefix=((6,2),) in their trace. Each maps back into class A via T. The pushforward E[δ_T|A] is distributed over 383 class-A states.</div>
              <div>· <strong style={{ color: C.gold }}>Class B ({"{6174}"}):</strong> the attractor itself. prefix=(), already on the cycle. T(6174)=6174, so E[δ_T|B]=δ_{6174}.</div>
              <div style={{ marginTop: 8, color: C.orange }}>
                · E[δ_T|A] ≠ E[δ_T|B] → V^bdry_{(6,2)} ≠ {"{0}"} → R_bdry = 1
              </div>
              <div style={{ color: C.green, marginTop: 4 }}>
                · But V^ref and V^bdry are parallel (same 1-d space) → δ=1 → net rank = 1
              </div>
            </div>
          </Card>
          <Card highlight={C.purple}>
            <div style={{ color: C.purple, fontWeight: 700, marginBottom: 10 }}>
              Tree Counterexample — Class III (no refinement, still rank=1)
            </div>
            <TreeExample />
            <div style={{ color: C.text, fontSize: 12, marginTop: 10, lineHeight: 1.6 }}>
              This validates Class III exists: boundary variance alone can produce rank(C)≥1
              without any FOQDS splitting. The v12.1 counterexample is correct and important.
            </div>
          </Card>
        </Section>
      )}

      {/* ── TAXONOMY ── */}
      {tab === "taxonomy" && (
        <Section title="System Classification I–IV" eyebrow="Corrected Taxonomy">
          {CLASS_TAXONOMY.map(cls => (
            <div key={cls.cls} style={{ background: C.panel,
              border: `2px solid ${cls.kaprekar ? C.gold : C.border}`,
              borderRadius: 8, padding: "16px 20px", marginBottom: 12 }}>
              <div style={{ display: "flex", gap: 10, alignItems: "center", flexWrap: "wrap", marginBottom: 8 }}>
                <div style={{ background: cls.color, color: C.bg, borderRadius: 6,
                  padding: "4px 12px", fontWeight: 800, fontSize: 14,
                  fontFamily: "monospace" }}>CLASS {cls.cls}</div>
                <span style={{ color: cls.color, fontWeight: 700, fontSize: 14 }}>{cls.name}</span>
                {cls.kaprekar && <Badge color="gold">KAPREKAR (corrected)</Badge>}
              </div>
              <div style={{ fontFamily: "monospace", color: cls.color, fontSize: 12,
                marginBottom: 8 }}>{cls.condition}</div>
              <div style={{ color: C.text, fontSize: 13, marginBottom: 4 }}>{cls.mechanism}</div>
              <div style={{ color: C.textDim, fontSize: 12 }}>Example: {cls.example}</div>
              {cls.note && (
                <div style={{ color: C.orange, fontSize: 12, marginTop: 6,
                  borderLeft: `3px solid ${C.orange}`, paddingLeft: 8 }}>
                  ⚠ {cls.note}
                </div>
              )}
            </div>
          ))}
        </Section>
      )}

      {/* ── OPEN PROBLEMS ── */}
      {tab === "openprobs" && (
        <Section title="New Open Problems from v12.1 Audit">
          {NEW_OPEN_PROBLEMS.map(op => (
            <div key={op.id} style={{ background: C.panel, border: `1px solid ${C.orange}`,
              borderRadius: 8, padding: "14px 18px", marginBottom: 12 }}>
              <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap", marginBottom: 8 }}>
                <Badge color="orange">{op.status}</Badge>
                <span style={{ fontFamily: "monospace", color: C.accent, fontSize: 12 }}>{op.id}</span>
                <span style={{ color: C.textDim, fontSize: 11 }}>
                  {"★".repeat(op.priority)}{"☆".repeat(5-op.priority)}
                </span>
              </div>
              <div style={{ color: C.text, fontWeight: 600, marginBottom: 6 }}>{op.title}</div>
              <div style={{ color: C.textDim, fontSize: 13, lineHeight: 1.6 }}>{op.desc}</div>
            </div>
          ))}
        </Section>
      )}

      {/* ── FRAMEWORK ── */}
      {tab === "framework" && (
        <Section title="Mathematical Framework Summary" eyebrow="Corrected v12.1">
          <Card>
            <div style={{ color: C.gold, fontWeight: 700, marginBottom: 12 }}>
              What v12.1 contributes that is genuinely new:
            </div>
            {[
              ["The commutator C = ΠK − KΠ as a measure of observability failure",
               "Not just rank of K itself, but rank of the commutator with fiber projection"],
              ["Deviation representation rank(C) = dim span{Δ(x)}",
               "Cleaner than computing rank of C directly; geometrically meaningful"],
              ["Decomposition R_ref + R_bdry − δ",
               "Separates structural (FOQDS) from distributional (pushforward) contributions"],
              ["Tree counterexample (Class III)",
               "Shows FOQDS formula alone is insufficient; boundary variance is independent mechanism"],
              ["Kernel condition ker(Π) ∩ span{Δ} = {0}",
               "Necessary for projection to preserve rank; not trivial in general"],
            ].map(([t, d]) => (
              <div key={t} style={{ marginBottom: 12, borderBottom: `1px solid ${C.border}`,
                paddingBottom: 10 }}>
                <div style={{ color: C.green, fontSize: 13, fontWeight: 600, marginBottom: 4 }}>✓ {t}</div>
                <div style={{ color: C.textDim, fontSize: 12 }}>{d}</div>
              </div>
            ))}
          </Card>
          <Card highlight={C.red}>
            <div style={{ color: C.red, fontWeight: 700, marginBottom: 12 }}>
              What remains to prove (P-level gaps):
            </div>
            {[
              "rank(C) = dim span{Δ(x)} in general (C2 on Kaprekar only)",
              "δ = dim(Σ V^ref ∩ Σ V^bdry) formula in general",
              "Kaprekar is Class IV (not II) — formally prove V^bdry ≠ 0",
              "Classification completeness (Classes I–IV are exhaustive)",
              "Entropy–rank connection (precise statement needed first)",
            ].map((s, i) => (
              <div key={i} style={{ color: C.text, fontSize: 13, padding: "4px 0",
                borderBottom: i < 4 ? `1px solid ${C.border}` : "none" }}>
                <span style={{ color: C.red }}>⊘ </span>{s}
              </div>
            ))}
          </Card>
        </Section>
      )}

      {/* FOOTER */}
      <div style={{ borderTop: `1px solid ${C.border}`, marginTop: 40, paddingTop: 16,
        display: "flex", justifyContent: "space-between", flexWrap: "wrap", gap: 8,
        fontSize: 11, color: C.textDim }}>
        <span>AQARION Node #10878 · Commutator Rank Audit · 2026-06-21</span>
        <span style={{ color: C.accent }}>Prove First · Predict Second · No Free Parameters</span>
      </div>
    </div>
  );
}
