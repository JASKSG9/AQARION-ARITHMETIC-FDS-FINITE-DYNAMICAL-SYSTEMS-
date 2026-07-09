import React, { useState, useEffect, useCallback } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

// Simulated atlas query function (replace with actual API call)
const queryAtlas = async (operator, partition, n, k) => {
  // In a real app, fetch from /api/atlas?operator=... etc.
  // This mock returns deterministic data based on parameters
  const rank = operator === 'koopman1d' ? 0 : Math.min(k, n - k);
  const exact = rank === 0;
  const singularValues = exact ? [] : Array.from({ length: Math.min(k, 4) }, (_, i) => Math.pow(0.5, i));
  const entropy = singularValues.length ? -singularValues.reduce((sum, sv) => sum + sv * Math.log2(sv || 1e-12), 0) : 0;
  const delta1 = rank;
  const deltaInf = rank + (operator === 'random_markov' ? 2 : 1);
  const horizon = exact ? 0 : (operator === 'random_markov' ? 3 : 2);
  const classification = exact ? 'I' : (operator.includes('random') ? 'III' : 'II');
  return {
    operator, partition, n, k,
    rank,
    exact,
    singularValues,
    entropy: +entropy.toFixed(4),
    compressionDiagnostic: { delta1, deltaInf, horizon },
    classification
  };
};

const OPERATORS = ['koopman1d', 'pf1d', 'baker2d', 'cat', 'rotation', 'random_markov'];
const PARTITIONS = ['strip', 'adversarial', 'random', 'spectral', 'hierarchical'];

// Small formatters
const formatSV = (val) => val.toFixed(4);

// Recent queries table component
function RecentQueriesTable({ queries }) {
  if (!queries.length) return <p className="text-gray-400 italic">No queries yet.</p>;
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-sm">
        <thead className="bg-gray-800 text-gray-300">
          <tr>
            <th className="p-2">Operator</th>
            <th className="p-2">Partition</th>
            <th className="p-2">n</th>
            <th className="p-2">k</th>
            <th className="p-2">Rank</th>
            <th className="p-2">Exact?</th>
            <th className="p-2">Class</th>
          </tr>
        </thead>
        <tbody>
          {queries.map((q, i) => (
            <tr key={i} className="border-t border-gray-700">
              <td className="p-2 font-mono">{q.operator}</td>
              <td className="p-2">{q.partition}</td>
              <td className="p-2">{q.n}</td>
              <td className="p-2">{q.k}</td>
              <td className="p-2">{q.rank}</td>
              <td className="p-2">{q.exact ? '✅ Yes' : '❌ No'}</td>
              <td className="p-2">{q.classification}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function DefectAtlasDashboard() {
  const [operator, setOperator] = useState('koopman1d');
  const [partition, setPartition] = useState('strip');
  const [n, setN] = useState(16);
  const [k, setK] = useState(4);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [recentQueries, setRecentQueries] = useState([]);

  const fetchResult = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await queryAtlas(operator, partition, n, k);
      setResult(data);
      // Add to recent queries (keep last 10)
      setRecentQueries(prev => {
        const newQueries = [{ ...data }, ...prev].slice(0, 10);
        return newQueries;
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [operator, partition, n, k]);

  useEffect(() => {
    fetchResult();
  }, [fetchResult]);

  const singularChartData = result?.singularValues.map((sv, idx) => ({
    index: idx + 1,
    value: sv
  })) || [];

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="mb-6">
          <h1 className="text-3xl font-bold text-teal-400">AQARION Defect Atlas</h1>
          <p className="text-gray-400 mt-1">
            Explore exact quotients, defect fingerprints, and spectral geometry.
          </p>
        </header>

        {/* Control Panel */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium mb-1">Operator</label>
            <select
              value={operator}
              onChange={(e) => setOperator(e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              {OPERATORS.map(op => (
                <option key={op} value={op}>{op}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Partition</label>
            <select
              value={partition}
              onChange={(e) => setPartition(e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              {PARTITIONS.map(p => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">System size n = {n}</label>
            <input
              type="range"
              min={4} max={128} step={4}
              value={n}
              onChange={(e) => setN(Number(e.target.value))}
              className="w-full"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Block count k = {k}</label>
            <input
              type="range"
              min={2} max={Math.min(32, n)}
              step={1}
              value={k}
              onChange={(e) => setK(Number(e.target.value))}
              className="w-full"
            />
          </div>
        </div>

        {/* Error display */}
        {error && (
          <div className="bg-red-900/50 border border-red-700 text-red-300 p-3 rounded mb-4">
            Error: {error}
          </div>
        )}

        {/* Main content */}
        {loading && <div className="text-center text-gray-400 py-8">Computing defect operator...</div>}

        {result && !loading && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left column: fingerprint cards */}
            <div className="lg:col-span-1 space-y-4">
              <div className="bg-gray-800 rounded-xl p-5 shadow-lg">
                <h2 className="text-xl font-semibold mb-3 text-teal-300">Defect Fingerprint</h2>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Exact Quotient:</span>
                    <span className={`font-bold ${result.exact ? 'text-green-400' : 'text-red-400'}`}>
                      {result.exact ? '✅ Yes' : '❌ No'}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Rank(D):</span>
                    <span className="font-mono">{result.rank}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Defect Entropy:</span>
                    <span className="font-mono">{result.entropy}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Class:</span>
                    <span className="font-mono text-teal-300">{result.classification}</span>
                  </div>
                </div>
              </div>

              <div className="bg-gray-800 rounded-xl p-5 shadow-lg">
                <h2 className="text-xl font-semibold mb-3 text-teal-300">Compression Diagnostic</h2>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-400">δ₁ (immediate):</span>
                    <span className="font-mono">{result.compressionDiagnostic.delta1}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">δ∞ (total):</span>
                    <span className="font-mono">{result.compressionDiagnostic.deltaInf}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Horizon h:</span>
                    <span className="font-mono">{result.compressionDiagnostic.horizon}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Right column: chart + table */}
            <div className="lg:col-span-2 space-y-6">
              <div className="bg-gray-800 rounded-xl p-5 shadow-lg">
                <h2 className="text-xl font-semibold mb-3 text-teal-300">Singular Value Spectrum</h2>
                {singularChartData.length ? (
                  <ResponsiveContainer width="100%" height={200}>
                    <BarChart data={singularChartData} layout="vertical" margin={{ left: 30, right: 20 }}>
                      <XAxis type="number" />
                      <YAxis dataKey="index" type="category" />
                      <Tooltip formatter={(value) => formatSV(value)} />
                      <Bar dataKey="value" fill="#2dd4bf" />
                    </BarChart>
                  </ResponsiveContainer>
                ) : (
                  <p className="text-gray-400 italic">No singular values (exact quotient).</p>
                )}
              </div>

              <div className="bg-gray-800 rounded-xl p-5 shadow-lg">
                <h2 className="text-xl font-semibold mb-3 text-teal-300">Recent Queries</h2>
                <RecentQueriesTable queries={recentQueries} />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
