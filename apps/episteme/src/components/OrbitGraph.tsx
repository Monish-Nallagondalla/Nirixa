'use client';

import React, { useState, useEffect } from 'react';
import { Orbit, Sparkles, X, ChevronRight, Share2, BookOpen, PenTool, Radio } from 'lucide-react';

export default function OrbitGraph({ onNavigate }: { onNavigate: (tab: any) => void }) {
  const [otas, setOtas] = useState<any[]>([]);
  const [selectedNode, setSelectedNode] = useState<any>(null);
  const [filterCategory, setFilterCategory] = useState<string>('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/otas')
      .then((res) => res.json())
      .then((json) => {
        if (json.success) {
          setOtas(json.data.otas);
          if (json.data.otas.length > 0) {
            setSelectedNode(json.data.otas.find((o: any) => o.id === 'OTA-014') || json.data.otas[0]);
          }
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load OTAs:', err);
        setLoading(false);
      });
  }, []);

  const categories = [
    { id: 'all', label: 'All 48 OTAs' },
    { id: 'Epistemology', label: 'Epistemology' },
    { id: 'Architecture', label: 'Architecture' },
    { id: 'Agency', label: 'Agency' },
    { id: 'Coevolution', label: 'Coevolution' }
  ];

  const filtered = filterCategory === 'all'
    ? otas
    : otas.filter(o => o.category?.toLowerCase() === filterCategory.toLowerCase() || o.layer?.toLowerCase() === filterCategory.toLowerCase());

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      {/* Top Filter Bar */}
      <div className="glass-panel p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-cyan-500/10 border border-cyan-500/25 flex items-center justify-center">
            <Orbit className="w-4 h-4 text-cyan-400" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-white">Cosmic Knowledge Orbit • Planetary Constellation</h2>
            <p className="text-[11px] text-slate-400">Interactive planetary graph of the 48 Original Thought Assets and PhD Research Questions</p>
          </div>
        </div>

        <div className="flex items-center gap-1.5 overflow-x-auto">
          {categories.map((c) => (
            <button
              key={c.id}
              onClick={() => setFilterCategory(c.id)}
              className={`px-3 py-1 rounded-lg text-xs font-medium transition-all shrink-0 ${
                filterCategory === c.id
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 shadow-[0_0_12px_rgba(56,189,248,0.2)]'
                  : 'bg-white/[0.03] text-slate-400 hover:text-white border border-white/5'
              }`}
            >
              {c.label}
            </button>
          ))}
        </div>
      </div>

      {/* Main Orbit Stage + Floating Inspector */}
      <div className="relative w-full h-[650px] glass-panel bg-black/50 border border-white/5 overflow-hidden flex items-center justify-center">
        {/* SVG Planetary Canvas */}
        <svg className="w-full h-full" viewBox="0 0 900 650">
          <defs>
            <radialGradient id="sunGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.8" />
              <stop offset="50%" stopColor="#818cf8" stopOpacity="0.3" />
              <stop offset="100%" stopColor="#08090e" stopOpacity="0" />
            </radialGradient>
            <filter id="glow">
              <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>

          {/* Central Core Sun: Human-AI Coevolution */}
          <circle cx="450" cy="325" r="70" fill="url(#sunGlow)" />
          <circle cx="450" cy="325" r="22" fill="#06080f" stroke="#38bdf8" strokeWidth="2" filter="url(#glow)" />
          <text x="450" y="329" textAnchor="middle" fill="#38bdf8" fontSize="10" fontFamily="monospace" fontWeight="bold">
            EPISTEME
          </text>

          {/* Concentric Planetary Orbit Rings */}
          <circle cx="450" cy="325" r="100" fill="none" stroke="rgba(255,255,255,0.06)" strokeDasharray="4 4" />
          <circle cx="450" cy="325" r="170" fill="none" stroke="rgba(255,255,255,0.05)" strokeDasharray="3 3" />
          <circle cx="450" cy="325" r="240" fill="none" stroke="rgba(255,255,255,0.04)" strokeDasharray="4 4" />
          <circle cx="450" cy="325" r="300" fill="none" stroke="rgba(255,255,255,0.03)" />

          {/* Connecting Filaments from Center and between nodes */}
          {filtered.slice(0, 30).map((ota, i) => {
            const orbitIndex = (i % 4) + 1;
            const radius = orbitIndex * 70 + 40;
            const angle = (i / Math.min(filtered.length, 30)) * 2 * Math.PI - Math.PI / 2;
            const cx = 450 + radius * Math.cos(angle);
            const cy = 325 + radius * Math.sin(angle);

            const isSelected = selectedNode?.id === ota.id;

            return (
              <g key={ota.id}>
                {/* Synaptic filament to center */}
                <line
                  x1="450"
                  y1="325"
                  x2={cx}
                  y2={cy}
                  stroke={isSelected ? '#38bdf8' : 'rgba(56,189,248,0.15)'}
                  strokeWidth={isSelected ? '2' : '1'}
                />

                {/* Planetary Node */}
                <circle
                  cx={cx}
                  cy={cy}
                  r={isSelected ? 10 : (ota.pagerank ? Math.max(5, ota.pagerank * 8) : 6)}
                  fill={isSelected ? '#38bdf8' : orbitIndex === 1 ? '#38bdf8' : orbitIndex === 2 ? '#818cf8' : orbitIndex === 3 ? '#a855f7' : '#fbbf24'}
                  filter={isSelected ? 'url(#glow)' : ''}
                  className="cursor-pointer transition-all duration-300 hover:scale-125"
                  onClick={() => setSelectedNode(ota)}
                />

                {/* Node Label */}
                <text
                  x={cx}
                  y={cy + 16}
                  textAnchor="middle"
                  fill={isSelected ? '#ffffff' : '#94a3b8'}
                  fontSize="9"
                  fontFamily="monospace"
                  className="pointer-events-none"
                >
                  {ota.id}
                </text>
              </g>
            );
          })}
        </svg>

        {/* Floating Frosted Glass Inspector Card (Reflect / Chronicle Style) */}
        {selectedNode && (
          <div className="absolute right-6 top-6 bottom-6 w-96 glass-panel p-6 bg-slate-950/80 backdrop-blur-2xl border border-white/10 flex flex-col justify-between shadow-2xl animate-in slide-in-from-right duration-300">
            <div>
              <div className="flex items-center justify-between pb-3 border-b border-white/5 mb-4">
                <div className="flex items-center gap-2">
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 font-semibold">
                    {selectedNode.id}
                  </span>
                  <span className="text-[10px] font-mono text-slate-400 uppercase">
                    {selectedNode.category || 'Epistemology'}
                  </span>
                </div>
                <button
                  onClick={() => setSelectedNode(null)}
                  className="text-slate-500 hover:text-white transition-all"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              <h3 className="text-base font-semibold text-white leading-snug mb-3">
                {selectedNode.title}
              </h3>

              <p className="text-xs text-slate-300 leading-relaxed mb-6">
                {selectedNode.thesis || selectedNode.description || 'Tools are not passive instruments; they reshape the cognitive morphology of the thinker who wields them over extended time horizons.'}
              </p>

              {/* Lineage Provenance Box */}
              <div className="space-y-3 pt-3 border-t border-white/5">
                <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider block">
                  Provenance Lineage
                </span>

                {/* Upstream */}
                <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5">
                  <div className="flex items-center justify-between text-[11px] mb-1">
                    <span className="font-mono text-cyan-400 flex items-center gap-1.5">
                      <Radio className="w-3 h-3" /> Upstream Spark
                    </span>
                    <span className="text-[10px] text-slate-500">Telegram Audio</span>
                  </div>
                  <div className="text-xs text-slate-200">
                    Mobile voice note on agent feedback loops & cognitive morphology.
                  </div>
                </div>

                {/* Downstream */}
                <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5">
                  <div className="flex items-center justify-between text-[11px] mb-1">
                    <span className="font-mono text-amber-400 flex items-center gap-1.5">
                      <Share2 className="w-3 h-3" /> Downstream Output
                    </span>
                    <span className="text-[10px] text-slate-500">LinkedIn Essay #4</span>
                  </div>
                  <div className="text-xs text-slate-200">
                    Draft essay ready: "The Coevolution of Thought: Why Agents Reshape PMs"
                  </div>
                </div>

                {/* Academic Citation Anchor */}
                <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5">
                  <div className="flex items-center justify-between text-[11px] mb-1">
                    <span className="font-mono text-purple-400 flex items-center gap-1.5">
                      <BookOpen className="w-3 h-3" /> PhD Academic Citation
                    </span>
                    <span className="text-[10px] text-slate-500">RQ-2 Binding</span>
                  </div>
                  <div className="text-xs text-slate-200">
                    Licklider (1960) Man-Computer Symbiosis, IRE Transactions.
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="pt-4 border-t border-white/5 flex gap-2">
              <button
                onClick={() => onNavigate('research')}
                className="flex-1 py-2 rounded-xl bg-white/5 border border-white/10 text-xs font-medium text-white hover:bg-white/10 flex items-center justify-center gap-1.5"
              >
                <BookOpen className="w-3.5 h-3.5 text-cyan-400" />
                View in Lab
              </button>
              <button
                onClick={() => onNavigate('writing')}
                className="flex-1 py-2 rounded-xl bg-gradient-to-r from-cyan-500/20 to-indigo-500/20 border border-cyan-500/30 text-xs font-medium text-cyan-300 hover:shadow-[0_0_15px_rgba(56,189,248,0.2)] flex items-center justify-center gap-1.5"
              >
                <PenTool className="w-3.5 h-3.5 text-cyan-400" />
                Draft Post
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
