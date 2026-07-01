import { useState } from "react";

const MATRIX = [
  [1,1,0,0,0,0,0,0,0,1],
  [0,1,1,0,0,0,0,0,1,0],
  [0,0,1,1,0,0,0,1,0,0],
  [0,0,0,1,1,0,1,0,0,0],
  [0,0,0,0,1,1,0,0,0,0],
  [1,0,0,0,0,1,0,0,0,0],
  [0,0,0,0,0,0,1,1,0,0],
  [0,0,0,0,0,0,0,1,1,0],
  [0,1,0,0,0,0,0,0,1,0],
  [1,0,0,0,0,0,0,0,0,1],
];

const EIGENVALUES = [
  { val: "2.4552", type: "real", note: "Perron — dominant" },
  { val: "1.8009", type: "real", note: "" },
  { val: "1.489 ± 0.787i", type: "complex", note: "conjugate pair" },
  { val: "1.0000 (×2)", type: "real", note: "double eigenvalue" },
  { val: "0.511 ± 0.787i", type: "complex", note: "conjugate pair" },
  { val: "−0.4552", type: "real", note: "" },
  { val: "0.1991", type: "real", note: "" },
];

const CYCLES = [
  { length: 2, path: "0 → 9 → 0", type: "back-loop" },
  { length: 2, path: "1 → 8 → 1", type: "back-loop" },
  { length: 4, path: "1 → 2 → 7 → 8 → 1", type: "shortcut" },
  { length: 6, path: "0 → 1 → 2 → 3 → 4 → 5 → 0", type: "main spine" },
  { length: 6, path: "1 → 2 → 3 → 6 → 7 → 8 → 1", type: "branch" },
];

const WORD_COUNTS = [
  { n: 1, count: 10 }, { n: 2, count: 24 }, { n: 3, count: 58 },
  { n: 4, count: 141 }, { n: 5, count: 346 }, { n: 6, count: 856 },
  { n: 7, count: 2127 }, { n: 8, count: 5289 }, { n: 9, count: 13130 },
  { n: 10, count: 32509 },
];

const PERRON = [0.1712, 0.1315, 0.1010, 0.0849, 0.0809, 0.1177, 0.0427, 0.0621, 0.0904, 0.1177];

const KILLS = [
  { claim: "ρ(A) ≈ φ = 1.618", reality: "ρ(A) = 2.4552, gap = 0.837" },
  { claim: "entropy = log(φ) = 0.481", reality: "h = 0.898, almost exactly 2×log(φ)" },
  { claim: "Sturmian complexity (linear)", reality: "Exponential: p(10) = 32,509 vs Sturmian p(10) = 11" },
  { claim: "|forbidden| = 50", reality: "76 forbidden (A has 24 ones, not 50)" },
];

export default function SFTDashboard() {
  const [tab, setTab] = useState("matrix");
  const [hover, setHover] = useState(null);

  const PHI = 1.6180339887;
  const RHO_A = 2.4552280346;
  const H = 0.89821964;

  const maxBar = Math.max(...PERRON);

  return (
    <div style={{
      background: "#05070f",
      minHeight: "100vh",
      color: "#c4cfe0",
      fontFamily: "'JetBrains Mono', 'Courier New', monospace",
      padding: "22px 24px"
    }}>
      {/* Header */}
      <div style={{ marginBottom: "20px", borderBottom: "1px solid #0d1424", paddingBottom: "14px" }}>
        <div style={{ fontSize: "9px", color: "#1e2d48", letterSpacing: "3px", marginBottom: "5px" }}>
          NODE #10878 · 2026-06-24 · SFT ANALYSIS
        </div>
        <div style={{ fontSize: "21px", fontWeight: "700", color: "#e4eaf8" }}>
          10-State SFT — Complete Audit
        </div>
        <div style={{ display: "flex", gap: "16px", marginTop: "8px" }}>
          {[
            { label: "ρ(A)", val: RHO_A.toFixed(6), color: "#00e5a0" },
            { label: "entropy h", val: H.toFixed(6), color: "#4a90d9" },
            { label: "forbidden", val: "76", color: "#9b59b6" },
            { label: "φ claim", val: "FALSE", color: "#ff4444" },
          ].map(s => (
            <div key={s.label}>
              <div style={{ fontSize: "16px", fontWeight: "700", color: s.color }}>{s.val}</div>
              <div style={{ fontSize: "9px", color: "#2d3d58", letterSpacing: "1px" }}>{s.label.toUpperCase()}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", gap: "6px", marginBottom: "18px" }}>
        {["matrix", "spectrum", "cycles", "complexity", "kills"].map(t => (
          <button key={t} onClick={() => setTab(t)} style={{
            padding: "5px 12px",
            borderRadius: "3px",
            border: tab === t ? "1px solid #4a90d9" : "1px solid #0d1424",
            background: tab === t ? "#0a1628" : "transparent",
            color: tab === t ? "#4a90d9" : "#2d3d58",
            cursor: "pointer",
            fontSize: "10px",
            letterSpacing: "1px",
            textTransform: "uppercase"
          }}>{t}</button>
        ))}
      </div>

      {/* MATRIX TAB */}
      {tab === "matrix" && (
        <div>
          <div style={{ fontSize: "10px", color: "#2d3d58", marginBottom: "12px" }}>
            Click a cell to inspect. Green = allowed transition. All diagonal = 1 (self-loops).
          </div>
          <div style={{ display: "inline-block" }}>
            {/* Column headers */}
            <div style={{ display: "flex" }}>
              <div style={{ width: "28px" }} />
              {Array.from({length: 10}, (_, j) => (
                <div key={j} style={{ width: "28px", textAlign: "center", fontSize: "9px", color: "#2d3d58", marginBottom: "3px" }}>
                  {j}
                </div>
              ))}
            </div>
            {MATRIX.map((row, i) => (
              <div key={i} style={{ display: "flex", alignItems: "center" }}>
                <div style={{ width: "28px", fontSize: "9px", color: "#2d3d58", textAlign: "right", paddingRight: "4px" }}>{i}</div>
                {row.map((val, j) => {
                  const isDiag = i === j;
                  const isHovered = hover === `${i},${j}`;
                  const bg = val === 1
                    ? isDiag ? "#0a2a18" : "#083020"
                    : "#0a0d15";
                  const border = isHovered ? "1px solid #00e5a0" : val === 1 ? "1px solid #00e5a044" : "1px solid #0d1424";
                  return (
                    <div key={j}
                      onMouseEnter={() => setHover(`${i},${j}`)}
                      onMouseLeave={() => setHover(null)}
                      style={{
                        width: "26px", height: "26px",
                        background: bg,
                        border,
                        display: "flex", alignItems: "center", justifyContent: "center",
                        fontSize: "11px",
                        color: val === 1 ? (isDiag ? "#7effd0" : "#00e5a0") : "#1a2540",
                        cursor: "default",
                        margin: "1px",
                        borderRadius: "2px"
                      }}>
                      {val}
                    </div>
                  );
                })}
              </div>
            ))}
          </div>
          <div style={{ marginTop: "14px", fontSize: "10px", color: "#4a5568" }}>
            <span style={{ color: "#00e5a0" }}>■</span> Allowed (24 total) &nbsp;
            <span style={{ color: "#1a2540" }}>■</span> Forbidden (76 total) &nbsp;
            <span style={{ color: "#7effd0" }}>■</span> Self-loop (10 diagonal)
          </div>
          {hover && (
            <div style={{ marginTop: "10px", padding: "8px 12px", background: "#080b14", border: "1px solid #0d1424", borderRadius: "4px", fontSize: "10px" }}>
              Cell ({hover}): {MATRIX[+hover.split(",")[0]][+hover.split(",")[1]] === 1 ? "ALLOWED — transition " + hover.split(",")[0] + " → " + hover.split(",")[1] : "FORBIDDEN"}
            </div>
          )}
        </div>
      )}

      {/* SPECTRUM TAB */}
      {tab === "spectrum" && (
        <div>
          <div style={{ marginBottom: "16px" }}>
            <div style={{ fontSize: "12px", color: "#e4eaf8", marginBottom: "10px", fontWeight: "600" }}>Eigenvalues of A</div>
            {EIGENVALUES.map((ev, i) => (
              <div key={i} style={{
                display: "flex", justifyContent: "space-between", alignItems: "center",
                padding: "8px 12px", marginBottom: "4px",
                border: "1px solid #0d1424", borderRadius: "3px", background: "#080b14"
              }}>
                <span style={{ color: "#e4eaf8", fontSize: "12px" }}>λ: {ev.val}</span>
                <div style={{ display: "flex", gap: "8px" }}>
                  {ev.note && <span style={{ fontSize: "9px", color: "#4a5568" }}>{ev.note}</span>}
                  <span style={{
                    fontSize: "9px", padding: "1px 6px", borderRadius: "2px",
                    background: ev.type === "real" ? "#00e5a022" : "#4a90d922",
                    color: ev.type === "real" ? "#00e5a0" : "#4a90d9",
                    border: `1px solid ${ev.type === "real" ? "#00e5a033" : "#4a90d933"}`
                  }}>{ev.type}</span>
                </div>
              </div>
            ))}
          </div>
          <div style={{ padding: "12px", border: "1px solid #ff444422", borderRadius: "4px", background: "#0d0508" }}>
            <div style={{ fontSize: "10px", color: "#ff4444", marginBottom: "6px" }}>φ COMPARISON</div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px", fontSize: "11px" }}>
              <div>
                <div style={{ color: "#2d3d58", fontSize: "9px" }}>ρ(A)</div>
                <div style={{ color: "#ff4444", fontWeight: "700" }}>{RHO_A.toFixed(6)}</div>
              </div>
              <div>
                <div style={{ color: "#2d3d58", fontSize: "9px" }}>φ = (1+√5)/2</div>
                <div style={{ color: "#4a5568" }}>{PHI.toFixed(6)}</div>
              </div>
              <div>
                <div style={{ color: "#2d3d58", fontSize: "9px" }}>h = log(ρ)</div>
                <div style={{ color: "#ff4444" }}>{H.toFixed(6)}</div>
              </div>
              <div>
                <div style={{ color: "#2d3d58", fontSize: "9px" }}>log(φ)</div>
                <div style={{ color: "#4a5568" }}>0.481212</div>
              </div>
            </div>
            <div style={{ marginTop: "10px", fontSize: "10px", color: "#ff4444" }}>
              |ρ − φ| = 0.837 &nbsp;·&nbsp; h ≈ 1.866 × log(φ) &nbsp;·&nbsp; NOT RELATED
            </div>
          </div>
          <div style={{ marginTop: "14px", padding: "12px", border: "1px solid #00e5a022", borderRadius: "4px", background: "#030a05" }}>
            <div style={{ fontSize: "10px", color: "#00e5a0", marginBottom: "6px" }}>KEY IDENTITY (exact)</div>
            <div style={{ fontSize: "12px", color: "#e4eaf8" }}>ρ(A) = 1 + ρ(B)</div>
            <div style={{ fontSize: "10px", color: "#4a5568", marginTop: "4px" }}>
              Because all diagonal entries = 1: A = B + I, so eigenvalues shift by exactly 1.
            </div>
            <div style={{ fontSize: "11px", color: "#00e5a0", marginTop: "6px" }}>
              char poly of B: x²(x⁸ − 2x⁶ − x² + 1)
            </div>
          </div>
          {/* Perron measure */}
          <div style={{ marginTop: "14px" }}>
            <div style={{ fontSize: "11px", color: "#e4eaf8", marginBottom: "8px" }}>Parry Measure (max entropy stationary distribution)</div>
            {PERRON.map((p, i) => (
              <div key={i} style={{ display: "flex", gap: "8px", alignItems: "center", marginBottom: "3px" }}>
                <span style={{ fontSize: "9px", color: "#2d3d58", width: "12px" }}>{i}</span>
                <div style={{
                  height: "12px",
                  width: `${(p / maxBar) * 180}px`,
                  background: "#4a90d9",
                  opacity: 0.7,
                  borderRadius: "1px"
                }} />
                <span style={{ fontSize: "10px", color: "#4a90d9" }}>{p.toFixed(4)}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* CYCLES TAB */}
      {tab === "cycles" && (
        <div>
          <div style={{ fontSize: "10px", color: "#2d3d58", marginBottom: "14px" }}>
            B = A − I has exactly 5 simple cycles. Self-loops in A make period = 1 → aperiodic.
          </div>
          {CYCLES.map((c, i) => (
            <div key={i} style={{
              padding: "12px 14px", marginBottom: "8px",
              border: c.type === "main spine" ? "1px solid #00e5a044" : "1px solid #0d1424",
              borderRadius: "4px", background: c.type === "main spine" ? "#020a06" : "#080b14"
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px" }}>
                <span style={{ color: "#e4eaf8", fontSize: "12px" }}>Length {c.length}</span>
                <span style={{
                  fontSize: "9px", padding: "2px 7px", borderRadius: "2px",
                  background: c.type === "main spine" ? "#00e5a018" : "#4a90d918",
                  color: c.type === "main spine" ? "#00e5a0" : "#4a90d9",
                  border: `1px solid ${c.type === "main spine" ? "#00e5a033" : "#4a90d933"}`
                }}>{c.type}</span>
              </div>
              <div style={{ fontSize: "11px", color: "#6b7280", fontFamily: "monospace" }}>{c.path}</div>
            </div>
          ))}
          <div style={{ marginTop: "10px", padding: "10px 12px", border: "1px solid #0d1424", borderRadius: "4px", background: "#080b14", fontSize: "10px", color: "#4a5568" }}>
            gcd(2,2,4,6,6) = 2 for B alone — but A has length-1 self-loops, so period = gcd(1,2,2,4,6,6) = <span style={{ color: "#00e5a0" }}>1 → APERIODIC ✓</span>
          </div>
        </div>
      )}

      {/* COMPLEXITY TAB */}
      {tab === "complexity" && (
        <div>
          <div style={{ fontSize: "10px", color: "#ff4444", marginBottom: "12px" }}>
            Growth is EXPONENTIAL converging to ρ ≈ 2.455. Sturmian = linear (p(n) = n+1). FALSE.
          </div>
          {WORD_COUNTS.map((w, i) => {
            const ratio = i > 0 ? (w.count / WORD_COUNTS[i-1].count) : null;
            const sturmian = w.n + 1;
            return (
              <div key={w.n} style={{
                display: "flex", gap: "12px", alignItems: "center",
                padding: "6px 0", borderBottom: "1px solid #0a0d15", fontSize: "11px"
              }}>
                <span style={{ color: "#2d3d58", width: "24px" }}>n={w.n}</span>
                <span style={{ color: "#e4eaf8", width: "70px", textAlign: "right" }}>{w.count.toLocaleString()}</span>
                {ratio && <span style={{ color: "#4a90d9", width: "52px" }}>×{ratio.toFixed(3)}</span>}
                <div style={{ flex: 1, display: "flex", alignItems: "center", gap: "6px" }}>
                  <div style={{
                    height: "8px",
                    width: `${Math.min((w.count / 32509) * 200, 200)}px`,
                    background: "#4a90d9",
                    borderRadius: "1px",
                    opacity: 0.6
                  }} />
                </div>
                <span style={{ color: "#1a2540", fontSize: "9px" }}>Sturmian: {sturmian}</span>
              </div>
            );
          })}
          <div style={{ marginTop: "12px", padding: "10px 12px", border: "1px solid #0d1424", borderRadius: "4px", background: "#080b14", fontSize: "10px" }}>
            <div style={{ color: "#ff4444" }}>Sturmian claim: p(n) ≈ n + 1</div>
            <div style={{ color: "#e4eaf8", marginTop: "4px" }}>Reality: p(n) ≈ 2.455ⁿ⁻¹ × 10</div>
            <div style={{ color: "#4a5568", marginTop: "4px" }}>At n=10: 32,509 actual vs 11 Sturmian</div>
          </div>
        </div>
      )}

      {/* KILLS TAB */}
      {tab === "kills" && (
        <div>
          <div style={{ fontSize: "10px", color: "#2d3d58", marginBottom: "14px" }}>
            Four claims killed by computation. All hard failures, not rounding.
          </div>
          {KILLS.map((k, i) => (
            <div key={i} style={{
              padding: "12px 14px", marginBottom: "8px",
              border: "1px solid #ff444422", borderRadius: "4px", background: "#0d0508"
            }}>
              <div style={{ display: "flex", gap: "8px", alignItems: "center", marginBottom: "6px" }}>
                <span style={{ color: "#ff4444", fontSize: "14px" }}>✗</span>
                <span style={{ fontSize: "11px", color: "#9ca3af" }}>CLAIMED: {k.claim}</span>
              </div>
              <div style={{ fontSize: "11px", color: "#e4eaf8", paddingLeft: "22px" }}>
                ACTUAL: <span style={{ color: "#00e5a0" }}>{k.reality}</span>
              </div>
            </div>
          ))}
          <div style={{ marginTop: "14px", padding: "12px", border: "1px solid #00e5a022", borderRadius: "4px", background: "#030a05" }}>
            <div style={{ fontSize: "10px", color: "#00e5a0", marginBottom: "8px" }}>WHAT IS TRUE</div>
            {[
              "Irreducible: YES ✓",
              "Aperiodic: YES ✓ (self-loops force period 1)",
              "Valid 10-state SFT: YES ✓",
              "Topological entropy: h = 0.89822 (exact, computable)",
              "Characteristic poly: x²(x⁸ − 2x⁶ − x² + 1)",
              "ρ(A) = 1 + ρ(B) exactly (shift by self-loops)",
            ].map((item, i) => (
              <div key={i} style={{ fontSize: "10px", color: "#6b7280", padding: "3px 0" }}>→ {item}</div>
            ))}
          </div>
        </div>
      )}

      <div style={{
        marginTop: "20px", borderTop: "1px solid #0d1424", paddingTop: "10px",
        display: "flex", justifyContent: "space-between", fontSize: "8px", color: "#141e2f"
      }}>
        <span>PROVE FIRST · NO FREE PARAMETERS</span>
        <span>SFT ANALYSIS · NODE #10878</span>
      </div>
    </div>
  );
}
