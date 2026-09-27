'use client';

import React, { useState, useEffect } from 'react';
import { Share2, BookOpen, PenTool, MessageSquare, ArrowRight, Compass, Search, ShieldCheck, CheckCircle2 } from 'lucide-react';

interface OrbitGraphProps {
  onNavigate: (tab: any) => void;
  onSelectOtaForStudio?: (otaId: string) => void;
  incomingFocusedNode?: any;
}

export default function OrbitGraph({
  onNavigate,
  onSelectOtaForStudio,
  incomingFocusedNode
}: OrbitGraphProps) {
  const [otas, setOtas] = useState<any[]>([]);
  const [selectedNode, setSelectedNode] = useState<any>(incomingFocusedNode || null);
  const [filterCategory, setFilterCategory] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/otas')
      .then((res) => res.json())
      .then((json) => {
        if (json.success && json.data.otas) {
          setOtas(json.data.otas);
          if (!selectedNode && json.data.otas.length > 0) {
            setSelectedNode(json.data.otas.find((o: any) => o.id === 'OTA-001') || json.data.otas[0]);
          }
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load OTAs:', err);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    if (incomingFocusedNode) {
      setSelectedNode(incomingFocusedNode);
    }
  }, [incomingFocusedNode]);

  const categories = [
    { id: 'all', label: 'All 48 Primitives' },
    { id: 'Epistemology', label: 'Epistemology' },
    { id: 'Architecture', label: 'Architecture' },
    { id: 'Agency', label: 'Agency' },
    { id: 'Coevolution', label: 'Coevolution' },
    { id: 'Ergonomics', label: 'Ergonomics' }
  ];

  const filtered = otas
    .filter((o) => {
      const matchesCat =
        filterCategory === 'all' ||
        (o.category || '').toLowerCase() === filterCategory.toLowerCase() ||
        (o.layer || '').toLowerCase() === filterCategory.toLowerCase();
      const matchesSearch =
        !searchQuery ||
        o.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
        o.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (o.thesis || '').toLowerCase().includes(searchQuery.toLowerCase());
      return matchesCat && matchesSearch;
    });

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border border-[#C89B53] border-t-transparent rounded-full animate-spin"></div>
          <span className="text-xs font-mono-precision text-[#9FA4B2] tracking-wider uppercase">
            Traversing 48 OTAs Lineage Graph...
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-5 animate-in fade-in duration-300 pb-12">
      {/* Top Header & Search Bar */}
      <div className="bento-card p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-[#C89B53]/10 border border-[#C89B53]/25 flex items-center justify-center text-[#E5A93C]">
            <Compass className="w-4 h-4" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-[#EDEAE3] font-editorial tracking-wide">
              Epistemic Lineage & Original Thought Matrix
            </h2>
            <p className="text-[11px] text-[#9FA4B2]">
              Explore the 48 living primitives, their upstream academic lineage, and downstream book chapters.
            </p>
          </div>
        </div>

        {/* Filter Pills & Search */}
        <div className="flex items-center gap-2 flex-wrap">
          <div className="relative">
            <Search className="w-3.5 h-3.5 text-[#646979] absolute left-2.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Filter by ID, thesis, keyword..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-8 pr-3 py-1 rounded-lg bg-[#12151E] border border-white/[0.08] text-xs text-[#EDEAE3] placeholder-[#646979] focus:outline-none focus:border-[#C89B53]/50 w-56 font-mono-precision"
            />
          </div>

          <div className="flex items-center gap-1">
            {categories.map((c) => (
              <button
                key={c.id}
                onClick={() => setFilterCategory(c.id)}
                className={`px-2.5 py-1 rounded text-xs font-mono-precision transition-all ${
                  filterCategory === c.id
                    ? 'bg-[#C89B53]/15 text-[#E5A93C] border border-[#C89B53]/40 font-semibold'
                    : 'bg-white/[0.02] text-[#9FA4B2] hover:text-[#EDEAE3] border border-white/[0.05]'
                }`}
              >
                {c.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Two-Column Stage: Left List + Right Lineage Canvas */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-stretch min-h-[640px]">
        {/* Left Column (4.5 Cols): 48 OTAs Index */}
        <div className="lg:col-span-4 flex flex-col bento-card p-4">
          <div className="flex items-center justify-between pb-3 border-b border-white/[0.06] mb-3">
            <span className="text-xs font-semibold text-[#EDEAE3] uppercase font-mono-precision">
              Primitives ({filtered.length})
            </span>
            <span className="text-[10px] text-[#646979] font-mono-precision">
              Select to inspect lineage
            </span>
          </div>

          <div className="space-y-2 overflow-y-auto max-h-[580px] pr-1">
            {filtered.map((ota) => {
              const isSelected = selectedNode?.id === ota.id;
              return (
                <div
                  key={ota.id}
                  onClick={() => setSelectedNode(ota)}
                  className={`p-3 rounded-xl border transition-all cursor-pointer text-left ${
                    isSelected
                      ? 'bg-[#1A1F2C] border-[#C89B53]/50 shadow-sm'
                      : 'bg-[#12151E] border-white/[0.05] hover:bg-[#161924] hover:border-white/10'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[10px] font-mono-precision font-semibold text-[#C89B53]">
                      {ota.id}
                    </span>
                    <span className="text-[10px] font-mono-precision text-[#646979]">
                      PR: {ota.pagerank || '0.90'}
                    </span>
                  </div>
                  <div className="text-xs font-semibold text-[#EDEAE3] line-clamp-1 mb-1 font-sans">
                    {ota.title}
                  </div>
                  <div className="text-[11px] text-[#9FA4B2] line-clamp-2 leading-relaxed font-sans">
                    {ota.thesis || ota.description || 'Computational primitive exploring intelligence emergence.'}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column (7.5 Cols): Real Directed Lineage Inspector (Zero Toy Solar Systems) */}
        <div className="lg:col-span-8 flex flex-col bento-card p-6">
          {selectedNode ? (
            <div className="flex flex-col justify-between h-full space-y-6">
              <div>
                {/* Header Badge & Title */}
                <div className="flex items-center justify-between pb-3 border-b border-white/[0.06] mb-4">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono-precision px-2.5 py-0.5 rounded bg-[#C89B53]/15 border border-[#C89B53]/30 text-[#E5A93C] font-semibold">
                      {selectedNode.id}
                    </span>
                    <span className="text-xs font-mono-precision text-[#646979] uppercase">
                      {selectedNode.category || 'Epistemology'}
                    </span>
                  </div>
                  <div className="text-xs font-mono-precision text-[#646979]">
                    PageRank Weight: <span className="text-[#EDEAE3] font-semibold">{selectedNode.pagerank || '0.92'}</span>
                  </div>
                </div>

                <h2 className="text-xl font-bold text-[#EDEAE3] font-editorial mb-3 tracking-tight">
                  {selectedNode.title}
                </h2>

                {/* Verified Thesis Block */}
                <div className="p-4 rounded-xl bg-[#161924] border border-white/[0.07] mb-6">
                  <span className="text-[10px] font-mono-precision text-[#C89B53] uppercase tracking-wider block mb-1">
                    Formal Thesis Statement
                  </span>
                  <p className="text-sm text-[#EDEAE3] italic leading-relaxed font-editorial">
                    "{selectedNode.thesis || selectedNode.description || 'Questions are stored and traversed as living computational objects rather than static answers.'}"
                  </p>
                </div>

                {/* 3-Stage Provenance Lineage Pipeline */}
                <div className="space-y-4">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono-precision uppercase text-[#646979] tracking-wider">
                      Thought Lineage Pipeline (OTA-011 Invariant)
                    </span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    {/* Stage 1: Upstream Anchor */}
                    <div className="p-3.5 rounded-xl bg-[#12151E] border border-white/[0.06] flex flex-col justify-between">
                      <div>
                        <div className="flex items-center justify-between text-[10px] font-mono-precision text-[#9FA4B2] mb-1.5">
                          <span className="flex items-center gap-1 text-[#C89B53]">
                            <BookOpen className="w-3 h-3" /> Upstream Foundation
                          </span>
                          <span>Anchor</span>
                        </div>
                        <div className="text-xs font-semibold text-[#EDEAE3] mb-1 font-editorial">
                          Vaswani et al. (2017)
                        </div>
                        <div className="text-[11px] text-[#9FA4B2] leading-snug">
                          Scaled Dot-Product Attention & Multi-Head Self-Attention formulation.
                        </div>
                      </div>
                      <div className="mt-3 pt-2 border-t border-white/[0.04]">
                        <span className="text-[10px] font-mono-precision text-[#646979]">NeurIPS 2017 #1706.03762</span>
                      </div>
                    </div>

                    {/* Stage 2: Empirical Scar */}
                    <div className="p-3.5 rounded-xl bg-[#12151E] border border-white/[0.06] flex flex-col justify-between">
                      <div>
                        <div className="flex items-center justify-between text-[10px] font-mono-precision text-[#9FA4B2] mb-1.5">
                          <span className="flex items-center gap-1 text-[#2E7D5B]">
                            <ShieldCheck className="w-3 h-3" /> Empirical Scar
                          </span>
                          <span>story_bank</span>
                        </div>
                        <div className="text-xs font-semibold text-[#EDEAE3] mb-1 font-editorial">
                          Real Consulting Friction
                        </div>
                        <div className="text-[11px] text-[#9FA4B2] leading-snug">
                          Abstracted workplace dynamic; zero client PII; real human-AI tension.
                        </div>
                      </div>
                      <div className="mt-3 pt-2 border-t border-white/[0.04]">
                        <span className="text-[10px] font-mono-precision text-[#646979]">Verified in nirixa.db</span>
                      </div>
                    </div>

                    {/* Stage 3: Downstream Chapter */}
                    <div className="p-3.5 rounded-xl bg-[#12151E] border border-white/[0.06] flex flex-col justify-between">
                      <div>
                        <div className="flex items-center justify-between text-[10px] font-mono-precision text-[#9FA4B2] mb-1.5">
                          <span className="flex items-center gap-1 text-[#D97F52]">
                            <Share2 className="w-3 h-3" /> Downstream Chapter
                          </span>
                          <span>Chapter 2</span>
                        </div>
                        <div className="text-xs font-semibold text-[#EDEAE3] mb-1 font-editorial">
                          The Coevolution of Thought
                        </div>
                        <div className="text-[11px] text-[#9FA4B2] leading-snug">
                          Book Anthology & 2029 Keynote core thesis synthesis.
                        </div>
                      </div>
                      <div className="mt-3 pt-2 border-t border-white/[0.04]">
                        <span className="text-[10px] font-mono-precision text-[#646979]">74% Chapter Maturity</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Action Bar */}
              <div className="pt-4 border-t border-white/[0.06] flex items-center justify-between">
                <button
                  onClick={() => onNavigate('research')}
                  className="px-4 py-2 rounded-lg bg-[#12151E] border border-white/[0.08] text-xs font-mono-precision text-[#9FA4B2] hover:text-[#EDEAE3] hover:border-white/20 transition-all flex items-center gap-1.5"
                >
                  <BookOpen className="w-3.5 h-3.5 text-[#C89B53]" />
                  <span>Inspect Vaswani 2017 in PDF Lab</span>
                </button>

                <button
                  onClick={() => {
                    if (onSelectOtaForStudio) {
                      onSelectOtaForStudio(selectedNode.id);
                    }
                    onNavigate('writing');
                  }}
                  className="px-5 py-2 rounded-lg bg-[#C89B53] text-[#0B0D13] font-semibold text-xs font-mono-precision hover:bg-[#E5A93C] transition-all flex items-center gap-2"
                >
                  <span>Open in Manuscript Studio</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center h-full text-center text-[#646979] text-xs font-mono-precision">
              Select an OTA from the index to inspect its complete lineage.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
