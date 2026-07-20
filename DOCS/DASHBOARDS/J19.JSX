```jsx
import React, { useState, useEffect } from 'react';

// ─── DATA (Inlined for self-containment) ───────────────────────────

const THEOREMS = [
  { id: 'AQ-THM-EXACT', name: 'Exact Descent Equivalence', status: 'proven', readiness: 42 },
  { id: 'AQ-THM-DR', name: 'Defect Rank Bound (Row-Stochastic)', status: 'verified', readiness: 56 },
  { id: 'AQ-THM-DR-SHARP', name: 'Sharpness of Rank Bound', status: 'verified', readiness: 23 },
  { id: 'AQ-THM-AFFINE', name: 'Kaprekar Affine Lift Identity', status: 'verified', readiness: 44 },
  { id: 'AQ-THM-DEPTH', name: 'Depth Reduction Conjecture', status: 'conjecture', readiness: 0 },
];

const EXPERIMENTS = [
  { id: 'AQ-E1', name: 'Reliability over Discovery', status: 'READY', priority: 1 },
  { id: 'AQ-E2', name: 'Evidence Governance Trial', status: 'COMPLETE', priority: 2 },
  { id: 'AQ-E3', name: 'Error Ecology Taxonomy', status: 'READY', priority: 3 },
  { id: 'AQ-E4', name: 'Evidence Growth Curves', status: 'READY', priority: 2 },
  { id: 'AQ-E5', name: 'Adversarial Mathematics', status: 'NEEDS_ARCHITECTURE', priority: 4 },
  { id: 'AQ-E6', name: 'Complete Ground Truth Worlds', status: 'IN_PROGRESS', priority: 1 },
  { id: 'AQ-E7', name: 'Scientific Governance Metrics', status: 'READY', priority: 2 },
  { id: 'AQ-E8', name: 'Claim Lifecycle Statistics', status: 'NEEDS_HISTORICAL_DATA', priority: 3 },
  { id: 'AQ-E9', name: 'Formalization Cost Analysis', status: 'NEEDS_LEAN_SKELETON', priority: 4 },
  { id: 'AQ-E10', name: 'Observable Quotient Discovery Challenge', status: 'READY', priority: 3 },
];

const GOVERNANCE_TOOLS = [
  { id: 'AQ-COMPATIBILITY-001', name: 'Evidence-Claim Compatibility Validator', checks: 17 },
  { id: 'AQ-PULL-AUDIT-CHECKLIST-001', name: 'PULL-Specific Audit Checklist', checks: 8 },
  { id: 'AQ-PUSH-PULL-CLASSIFIER-001', name: 'Automated PUSH/PULL Classifier', classes: 5 },
];

const FILES = [
  { name: 'AQ-OBJECT-001.json', size: '2.6 KB', purpose: 'Research Object Identity' },
  { name: 'AQ-CLAIM-001.json', size: '3.2 KB', purpose: 'Falsifiable Claims Schema' },
  { name: 'AQ-EVIDENCE-001.json', size: '4.1 KB', purpose: 'Typed Evidence Schema' },
  { name: 'AQ-CERTIFICATE-001.json', size: '3.1 KB', purpose: 'Immutable Attestation Schema' },
  { name: 'AQ-AUDIT-001.json', size: '4.2 KB', purpose: 'Independent Review Schema' },
  { name: 'AQ-REGRESSION-001.json', size: '4.4 KB', purpose: 'Reproducibility Schema' },
  { name: 'AQ-GOVERNANCE-REPORT-001.json', size: '4.2 KB', purpose: 'Final Governance Report' },
  { name: 'AQARION-GOV-SPEC-001.json', size: '10.5 KB', purpose: 'Standalone Specification' },
  { name: 'AQARION_v21_registry.json', size: '20.5 KB', purpose: 'Full Artifact Registry' },
];

// ─── COMPONENTS ─────────────────────────────────────────────────────

const StatusBadge = ({ status }) => {
  const colors = {
    proven: 'bg-green-600',
    verified: 'bg-blue-600',
    conjecture: 'bg-yellow-500',
    complete: 'bg-indigo-500',
    ready: 'bg-green-500',
    in_progress: 'bg-yellow-400',
    needs_architecture: 'bg-red-500',
    needs_historical_data: 'bg-orange-500',
    needs_lean_skeleton: 'bg-purple-500',
  };
  const color = colors[status.toLowerCase()] || 'bg-gray-500';
  return (
    <span className={`px-2 py-1 text-xs font-semibold text-white rounded-full ${color}`}>
      {status.replace(/_/g, ' ')}
    </span>
  );
};

const ProgressBar = ({ value }) => (
  <div className="w-full bg-gray-700 rounded-full h-2.5">
    <div className="bg-blue-500 h-2.5 rounded-full" style={{ width: `${value}%` }} />
  </div>
);

// ─── MAIN DASHBOARD ─────────────────────────────────────────────────

export default function AQARIONDashboard() {
  const [selectedTab, setSelectedTab] = useState('overview');

  return (
    <div className="min-h-screen bg-[#0d1528] text-[#c8d8f0] font-sans p-4">
      {/* ── Header ── */}
      <header className="border-b border-[#1c3054] pb-4 mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-[#4f7ef8]">⚡ AQARION v21.8</h1>
            <p className="text-sm text-[#5d7a9a]">
              Certificate-First Research Operating System
            </p>
          </div>
          <div className="text-right">
            <div className="text-xs text-[#5d7a9a]">Status</div>
            <div className="text-green-400 font-semibold">● ACTIVE · FROZEN</div>
          </div>
        </div>
        <div className="flex gap-2 mt-4">
          {['overview', 'theorems', 'experiments', 'tools', 'files'].map((tab) => (
            <button
              key={tab}
              onClick={() => setSelectedTab(tab)}
              className={`px-4 py-1 text-sm rounded-full transition-colors ${
                selectedTab === tab
                  ? 'bg-[#4f7ef8] text-white'
                  : 'bg-[#111e35] text-[#5d7a9a] hover:bg-[#1c3054]'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>
      </header>

      {/* ── Content ── */}
      <main>
        {selectedTab === 'overview' && <OverviewTab />}
        {selectedTab === 'theorems' && <TheoremsTab />}
        {selectedTab === 'experiments' && <ExperimentsTab />}
        {selectedTab === 'tools' && <ToolsTab />}
        {selectedTab === 'files' && <FilesTab />}
      </main>

      {/* ── Footer ── */}
      <footer className="mt-8 border-t border-[#1c3054] pt-4 text-xs text-[#5d7a9a] flex justify-between">
        <span>Canonical Hash: f53844fc92de1d8771be993fa54e93fc01a15b8112080c192d13f607d87756b4</span>
        <span>Maintained by Node #10878</span>
      </footer>
    </div>
  );
}

// ─── TABS ───────────────────────────────────────────────────────────

function OverviewTab() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Left: Theorem Readiness */}
        <div className="bg-[#111e35] rounded-lg p-4 border border-[#1c3054]">
          <h2 className="text-lg font-semibold mb-3 text-[#4f7ef8]">Theorem Readiness</h2>
          <div className="space-y-3">
            {THEOREMS.map((t) => (
              <div key={t.id} className="flex items-center gap-3">
                <span className="w-24 text-xs truncate">{t.id}</span>
                <div className="flex-1">
                  <ProgressBar value={t.readiness} />
                </div>
                <span className="text-xs w-8 text-right">{t.readiness}%</span>
                <StatusBadge status={t.status} />
              </div>
            ))}
          </div>
        </div>

        {/* Right: Governance Stats */}
        <div className="bg-[#111e35] rounded-lg p-4 border border-[#1c3054]">
          <h2 className="text-lg font-semibold mb-3 text-[#4f7ef8]">Governance Substrate</h2>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-[#0d1528] p-3 rounded">
              <div className="text-2xl font-bold text-[#2de08b]">6</div>
              <div className="text-xs text-[#5d7a9a]">Core Schemas</div>
            </div>
            <div className="bg-[#0d1528] p-3 rounded">
              <div className="text-2xl font-bold text-[#f5a623]">3</div>
              <div className="text-xs text-[#5d7a9a]">Governance Tools</div>
            </div>
            <div className="bg-[#0d1528] p-3 rounded">
              <div className="text-2xl font-bold text-[#4f7ef8]">24</div>
              <div className="text-xs text-[#5d7a9a]">Artifacts</div>
            </div>
            <div className="bg-[#0d1528] p-3 rounded">
              <div className="text-2xl font-bold text-[#f75a5a]">2</div>
              <div className="text-xs text-[#5d7a9a]">Findings Resolved</div>
            </div>
          </div>
          <div className="mt-3 text-xs text-[#5d7a9a]">
            <span className="text-[#2de08b]">●</span> Immutable SHA-256 hashes
            <span className="ml-2 text-[#f5a623]">●</span> Append‑only logs
          </div>
        </div>
      </div>

      {/* AQ-E2 Result Highlight */}
      <div className="bg-[#0a1220] border border-[#2de08b] rounded-lg p-4">
        <h2 className="text-lg font-semibold text-[#2de08b] mb-2">📊 AQ-E2: Evidence Governance Trial</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <div className="text-[#5d7a9a]">System A (Autonomous)</div>
            <div className="text-[#f75a5a]">45.1% false claims</div>
            <div className="text-xs">EL0.7 avg</div>
          </div>
          <div>
            <div className="text-[#5d7a9a]">System B (Collaborative)</div>
            <div className="text-[#f5a623]">19.4% false claims</div>
            <div className="text-xs">EL1.2 avg</div>
          </div>
          <div>
            <div className="text-[#5d7a9a]">System C (AQARION)</div>
            <div className="text-[#2de08b] font-bold">2.5% false claims</div>
            <div className="text-xs">EL3.8 avg · 97.5% reliability</div>
          </div>
        </div>
        <div className="mt-2 text-xs text-[#5d7a9a]">
          → 94.5% reduction in false claims vs. autonomous.
        </div>
      </div>
    </div>
  );
}

function TheoremsTab() {
  return (
    <div className="bg-[#111e35] rounded-lg border border-[#1c3054] p-4">
      <h2 className="text-lg font-semibold text-[#4f7ef8] mb-4">Theorem Status</h2>
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-[#5d7a9a] border-b border-[#1c3054]">
            <th className="py-2">ID</th>
            <th className="py-2">Name</th>
            <th className="py-2">Status</th>
            <th className="py-2 text-right">Readiness</th>
          </tr>
        </thead>
        <tbody>
          {THEOREMS.map((t) => (
            <tr key={t.id} className="border-b border-[#1c3054]/50">
              <td className="py-2 font-mono text-[#4f7ef8]">{t.id}</td>
              <td className="py-2">{t.name}</td>
              <td className="py-2"><StatusBadge status={t.status} /></td>
              <td className="py-2 text-right">
                <div className="flex items-center justify-end gap-2">
                  <span className="w-8 text-right">{t.readiness}%</span>
                  <div className="w-24">
                    <ProgressBar value={t.readiness} />
                  </div>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ExperimentsTab() {
  return (
    <div className="bg-[#111e35] rounded-lg border border-[#1c3054] p-4">
      <h2 className="text-lg font-semibold text-[#4f7ef8] mb-4">Experiments</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {EXPERIMENTS.map((e) => (
          <div key={e.id} className="bg-[#0d1528] p-3 rounded border border-[#1c3054]">
            <div className="flex justify-between items-start">
              <div>
                <div className="font-mono text-[#4f7ef8] text-xs">{e.id}</div>
                <div className="font-semibold">{e.name}</div>
              </div>
              <StatusBadge status={e.status} />
            </div>
            <div className="text-xs text-[#5d7a9a] mt-1">Priority: {e.priority}/4</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function ToolsTab() {
  return (
    <div className="bg-[#111e35] rounded-lg border border-[#1c3054] p-4">
      <h2 className="text-lg font-semibold text-[#4f7ef8] mb-4">Governance Tools</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {GOVERNANCE_TOOLS.map((tool) => (
          <div key={tool.id} className="bg-[#0d1528] p-4 rounded border border-[#1c3054]">
            <div className="font-mono text-xs text-[#4f7ef8]">{tool.id}</div>
            <div className="font-semibold mt-1">{tool.name}</div>
            <div className="text-xs text-[#5d7a9a] mt-2">
              {tool.checks && `${tool.checks} checks`}
              {tool.classes && `${tool.classes} classes`}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function FilesTab() {
  return (
    <div className="bg-[#111e35] rounded-lg border border-[#1c3054] p-4">
      <h2 className="text-lg font-semibold text-[#4f7ef8] mb-4">Artifact Registry</h2>
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-[#5d7a9a] border-b border-[#1c3054]">
            <th className="py-2">File</th>
            <th className="py-2">Size</th>
            <th className="py-2">Purpose</th>
          </tr>
        </thead>
        <tbody>
          {FILES.map((f, i) => (
            <tr key={i} className="border-b border-[#1c3054]/50">
              <td className="py-2 font-mono text-[#4f7ef8]">{f.name}</td>
              <td className="py-2">{f.size}</td>
              <td className="py-2">{f.purpose}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="mt-3 text-xs text-[#5d7a9a] text-right">
        + 15 more files (total 24 artifacts, 164 KB)
      </div>
    </div>
  );
}
```
