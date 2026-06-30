// Dashboard.jsx
// AQARION Observatory Dashboard — v2.7.0 snapshot
// Replace static data with live API calls as your infrastructure matures.

import React from 'react';

// ──────────────────────────────────────────────
// Sample Data (mirrors the 2026-06-29 Observatory)
// ──────────────────────────────────────────────
const OBSERVATORY_DATA = {
  summary: {
    questions: 147,
    openConjectures: 38,
    verifiedTheorems: 91,
    independentReproductions: 22,
    researchObjects: 624,
    evidenceObjects: 2418,
    leanCompletion: 78, // percent
    datasets: 34,
    interactiveApps: 12,
    communityContributions: 281,
  },
  genome: [
    { label: 'Definitions', value: 100 },
    { label: 'Experiments', value: 85 },
    { label: 'Lean Formalization', value: 78 },
    { label: 'Benchmarks', value: 90 },
    { label: 'Audits', value: 80 },
    { label: 'Visualizations', value: 60 },
    { label: 'Independent Reproductions', value: 40 },
    { label: 'Publications', value: 50 },
  ],
  trustGraph: [
    {
      id: 'OB',
      name: 'Positive Obstruction Bound',
      supportedBy: ['Proof', 'Enumeration'],
      confidence: 'high',
    },
    {
      id: 'T3',
      name: 'Fundamental Semiconjugacy',
      supportedBy: ['Symbolic Proof', 'Exhaustive Verification'],
      confidence: 'high',
    },
    {
      id: 'LC3',
      name: 'Rank Inequality (Critical Path)',
      supportedBy: ['Lean Proof (partial)'],
      confidence: 'medium',
    },
  ],
  recentActivity: [
    { date: '2026-06-29', action: 'Architecture stabilization (v2.7.0)' },
    { date: '2026-06-28', action: 'LC4 ObstructionBound.lean scaffold complete' },
    { date: '2026-06-26', action: 'Defect Operator Census benchmark validated' },
    { date: '2026-06-22', action: 'Frontier 2 cross-base universality verified' },
    { date: '2026-06-17', action: 'Independent reproduction of 55-class certificate (Python)' },
  ],
};

// ──────────────────────────────────────────────
// Helper Components
// ──────────────────────────────────────────────

const StatCard = ({ label, value, color = '#3b82f6' }) => (
  <div style={styles.statCard}>
    <div style={styles.statValue} color={color}>
      {value.toLocaleString()}
    </div>
    <div style={styles.statLabel}>{label}</div>
  </div>
);

const ProgressBar = ({ label, percent, color = '#22c55e' }) => (
  <div style={styles.genomeRow}>
    <span style={styles.genomeLabel}>{label}</span>
    <div style={styles.progressTrack}>
      <div
        style={{
          ...styles.progressFill,
          width: `${percent}%`,
          backgroundColor: color,
        }}
      />
    </div>
    <span style={styles.percentText}>{percent}%</span>
  </div>
);

const TrustNode = ({ node }) => {
  const badgeColor = node.confidence === 'high' ? '#22c55e' : '#f59e0b';
  return (
    <div style={styles.trustNode}>
      <span style={styles.trustName}>{node.name}</span>
      <span style={{ ...styles.confidenceBadge, backgroundColor: badgeColor }}>
        {node.confidence}
      </span>
      <div style={styles.trustSupports}>
        {node.supportedBy.map((s, i) => (
          <span key={i} style={styles.supportTag}>
            {s}
          </span>
        ))}
      </div>
    </div>
  );
};

const ActivityItem = ({ date, action }) => (
  <div style={styles.activityItem}>
    <span style={styles.activityDate}>{date}</span>
    <span style={styles.activityAction}>{action}</span>
  </div>
);

// ──────────────────────────────────────────────
// Main Dashboard Component
// ──────────────────────────────────────────────
const Dashboard = () => {
  const { summary, genome, trustGraph, recentActivity } = OBSERVATORY_DATA;

  return (
    <div style={styles.container}>
      {/* Header */}
      <header style={styles.header}>
        <h1 style={styles.title}>AQARION OBSERVATORY</h1>
        <p style={styles.subtitle}>2026-06-29 · v2.7.0 · Architecture Stabilization</p>
        <p style={styles.tagline}>
          “Every scientific statement in AQARION should be traceable to its motivating question,
          supporting evidence, computational artifacts, formal reasoning, revision history,
          and current confidence.”
        </p>
      </header>

      {/* Summary Cards */}
      <section style={styles.section}>
        <h2 style={styles.sectionTitle}>Project Pulse</h2>
        <div style={styles.cardGrid}>
          <StatCard label="Questions" value={summary.questions} />
          <StatCard label="Open Conjectures" value={summary.openConjectures} />
          <StatCard label="Verified Theorems" value={summary.verifiedTheorems} />
          <StatCard label="Independent Reproductions" value={summary.independentReproductions} />
          <StatCard label="Research Objects" value={summary.researchObjects} />
          <StatCard label="Evidence Objects" value={summary.evidenceObjects} />
          <StatCard label="Datasets" value={summary.datasets} />
          <StatCard label="Interactive Apps" value={summary.interactiveApps} />
          <StatCard label="Community Contributions" value={summary.communityContributions} />
        </div>
        {/* Lean Completion */}
        <div style={styles.leanBox}>
          <div style={styles.leanHeader}>
            <span>Lean Completion</span>
            <strong>{summary.leanCompletion}%</strong>
          </div>
          <div style={styles.leanTrack}>
            <div
              style={{
                ...styles.leanFill,
                width: `${summary.leanCompletion}%`,
              }}
            />
          </div>
        </div>
      </section>

      {/* Research Genome */}
      <section style={styles.section}>
        <h2 style={styles.sectionTitle}>Research Genome</h2>
        {genome.map((g) => (
          <ProgressBar
            key={g.label}
            label={g.label}
            percent={g.value}
            color={g.value > 80 ? '#22c55e' : g.value > 50 ? '#eab308' : '#ef4444'}
          />
        ))}
      </section>

      {/* Trust Graph */}
      <section style={styles.section}>
        <h2 style={styles.sectionTitle}>Trust Graph</h2>
        <p style={styles.mutedText}>Why should you trust these theorems?</p>
        {trustGraph.map((node) => (
          <TrustNode key={node.id} node={node} />
        ))}
      </section>

      {/* Recent Activity */}
      <section style={styles.section}>
        <h2 style={styles.sectionTitle}>Recent Activity</h2>
        {recentActivity.map((item, idx) => (
          <ActivityItem key={idx} date={item.date} action={item.action} />
        ))}
      </section>

      {/* Footer */}
      <footer style={styles.footer}>
        <p>
          AQARION is an open, evidence‑centered research ecosystem for finite observable
          dynamical systems.
        </p>
        <p>
          <a href="https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-" style={styles.link}>
            Repository
          </a>
          {' · '}
          <a href="/docs/OBSERVATORY/LEDGER-V0.MD" style={styles.link}>
            Observatory Ledger
          </a>
        </p>
      </footer>
    </div>
  );
};

// ──────────────────────────────────────────────
// Inline Styles (feel free to replace with CSS modules / Tailwind)
// ──────────────────────────────────────────────
const styles = {
  container: {
    maxWidth: 1200,
    margin: '0 auto',
    padding: '2rem 1rem',
    fontFamily: 'system-ui, -apple-system, sans-serif',
    color: '#1e293b',
    backgroundColor: '#f8fafc',
  },
  header: {
    textAlign: 'center',
    marginBottom: '2.5rem',
  },
  title: {
    fontSize: '2.5rem',
    fontWeight: 700,
    margin: 0,
    letterSpacing: '-0.5px',
  },
  subtitle: {
    color: '#64748b',
    margin: '0.25rem 0 1rem',
  },
  tagline: {
    fontSize: '0.9rem',
    color: '#475569',
    fontStyle: 'italic',
    maxWidth: '700px',
    margin: '0 auto',
  },
  section: {
    backgroundColor: '#ffffff',
    borderRadius: '12px',
    padding: '1.5rem',
    marginBottom: '1.5rem',
    boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
  },
  sectionTitle: {
    fontSize: '1.4rem',
    fontWeight: 600,
    marginBottom: '1rem',
    color: '#0f172a',
  },
  cardGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
    gap: '1rem',
    marginBottom: '1.5rem',
  },
  statCard: {
    padding: '1rem',
    borderRadius: '8px',
    border: '1px solid #e2e8f0',
    textAlign: 'center',
    backgroundColor: '#f1f5f9',
  },
  statValue: {
    fontSize: '2rem',
    fontWeight: 700,
    color: '#1e293b',
    lineHeight: 1.2,
  },
  statLabel: {
    fontSize: '0.85rem',
    color: '#64748b',
    marginTop: '0.25rem',
  },
  leanBox: {
    marginTop: '0.5rem',
  },
  leanHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    fontSize: '0.95rem',
    marginBottom: '0.3rem',
    fontWeight: 500,
  },
  leanTrack: {
    height: '10px',
    backgroundColor: '#e2e8f0',
    borderRadius: '5px',
    overflow: 'hidden',
  },
  leanFill: {
    height: '100%',
    backgroundColor: '#3b82f6',
    borderRadius: '5px',
  },
  genomeRow: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '0.75rem',
    gap: '0.75rem',
  },
  genomeLabel: {
    width: '180px',
    fontSize: '0.9rem',
    color: '#334155',
  },
  progressTrack: {
    flex: 1,
    height: '8px',
    backgroundColor: '#e2e8f0',
    borderRadius: '4px',
  },
  progressFill: {
    height: '100%',
    borderRadius: '4px',
  },
  percentText: {
    width: '40px',
    textAlign: 'right',
    fontSize: '0.85rem',
    fontWeight: 600,
    color: '#475569',
  },
  trustNode: {
    padding: '0.75rem 0',
    borderBottom: '1px solid #f1f5f9',
  },
  trustName: {
    fontWeight: 600,
    fontSize: '1rem',
    marginRight: '0.5rem',
  },
  confidenceBadge: {
    display: 'inline-block',
    padding: '2px 8px',
    borderRadius: '12px',
    fontSize: '0.75rem',
    fontWeight: 600,
    color: '#fff',
    marginLeft: '0.5rem',
  },
  trustSupports: {
    marginTop: '0.4rem',
    display: 'flex',
    gap: '0.5rem',
    flexWrap: 'wrap',
  },
  supportTag: {
    backgroundColor: '#e0f2fe',
    color: '#0c4a6e',
    padding: '2px 10px',
    borderRadius: '14px',
    fontSize: '0.8rem',
    fontWeight: 500,
  },
  mutedText: {
    color: '#64748b',
    fontSize: '0.9rem',
    marginBottom: '1rem',
  },
  activityItem: {
    display: 'flex',
    gap: '1rem',
    padding: '0.4rem 0',
    borderBottom: '1px solid #f1f5f9',
    fontSize: '0.9rem',
  },
  activityDate: {
    minWidth: '90px',
    color: '#94a3b8',
    fontWeight: 500,
  },
  activityAction: {
    color: '#1e293b',
  },
  footer: {
    textAlign: 'center',
    color: '#64748b',
    fontSize: '0.85rem',
    paddingTop: '2rem',
    borderTop: '1px solid #e2e8f0',
    marginTop: '2rem',
  },
  link: {
    color: '#2563eb',
    textDecoration: 'none',
  },
};

export default Dashboard;
