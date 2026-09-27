'use client';

import React, { useState, useEffect } from 'react';
import { Sparkles, ArrowRight, CheckCircle2, XCircle, Search, HelpCircle, AlertCircle, RefreshCw } from 'lucide-react';
import { ActiveTab } from './HeaderNav';

interface DiscoveriesDeckProps {
  onNavigate: (tab: ActiveTab) => void;
  onSelectOtaForStudio?: (otaId: string) => void;
}

export default function DiscoveriesDeck({
  onNavigate,
  onSelectOtaForStudio,
}: DiscoveriesDeckProps) {
  const [discoveries, setDiscoveries] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState<string>('all');
  const [actionFeedback, setActionFeedback] = useState<string | null>(null);

  const fetchDiscoveries = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/episteme/discoveries');
      const json = await res.json();
      if (json.success) {
        setDiscoveries(json.data || []);
      }
    } catch (err) {
      console.error('Failed to load discoveries:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDiscoveries();
  }, []);

  const handleUpdateStatus = async (id: string, newStatus: string) => {
    try {
      const res = await fetch('/api/episteme/discoveries', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, status: newStatus }),
      });
      const json = await res.json();
      if (json.success) {
        setActionFeedback(`Discovery ${id} updated to ${newStatus}.`);
        setTimeout(() => setActionFeedback(null), 3000);
        fetchDiscoveries();
      }
    } catch (err) {
      console.error('Error updating discovery status:', err);
    }
  };

  const filtered = discoveries.filter((d) => {
    if (filterType === 'all') return true;
    return d.type === filterType;
  });

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Action Toast */}
      {actionFeedback && (
        <div className="fixed top-16 right-6 z-50 bg-[#161A24] border border-[#38BDF8]/40 text-[#EDEAE3] text-xs px-4 py-2 rounded-xl shadow-2xl flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-[#38BDF8]" />
          <span>{actionFeedback}</span>
        </div>
      )}

      {/* Header Banner */}
      <div className="p-6 rounded-2xl bg-[#0E121C] border border-white/[0.08] relative overflow-hidden">
        <div className="absolute -right-10 -bottom-10 w-72 h-72 bg-[#38BDF8]/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
          <div>
            <div className="flex items-center gap-2 text-[11px] font-mono-precision uppercase tracking-wider text-[#38BDF8]">
              <Sparkles className="w-4 h-4" />
              <span>Autonomous AI Discovery Inbox • PRD §30</span>
            </div>
            <h1 className="text-xl md:text-2xl font-serif text-[#EDEAE3] mt-1">
              "I found something you didn't ask me to look for."
            </h1>
            <p className="text-xs text-[#9FA4B2] mt-1 max-w-2xl">
              Nirixa scans your longitudinal graph in the background to surface unprompted conceptual analogies, latent contradictions, and forgotten research inquiries.
            </p>
          </div>

          <button
            onClick={fetchDiscoveries}
            className="px-3 py-1.5 rounded-xl bg-[#141824] hover:bg-[#1A2030] border border-white/[0.08] text-xs text-[#EDEAE3] flex items-center gap-2 transition-all shrink-0 self-start md:self-auto"
          >
            <RefreshCw className={`w-3.5 h-3.5 text-[#38BDF8] ${loading ? 'animate-spin' : ''}`} />
            <span>Rescan Graph</span>
          </button>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-2 mt-5 pt-4 border-t border-white/[0.06] overflow-x-auto">
          {[
            { id: 'all', label: 'All Discoveries' },
            { id: 'unexpected_connection', label: 'Unexpected Connections' },
            { id: 'contradiction', label: 'Contradictions' },
            { id: 'forgotten_idea', label: 'Forgotten Ideas' },
            { id: 'research_opportunity', label: 'Research Opportunities' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setFilterType(tab.id)}
              className={`px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap transition-all ${
                filterType === tab.id
                  ? 'bg-[#1C2333] text-[#38BDF8] border border-[#38BDF8]/30 font-semibold'
                  : 'text-[#9FA4B2] hover:text-[#EDEAE3] hover:bg-white/[0.03]'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Discovery Cards Grid */}
      {loading ? (
        <div className="py-20 flex flex-col items-center justify-center text-center">
          <div className="w-8 h-8 border-2 border-[#38BDF8] border-t-transparent rounded-full animate-spin"></div>
          <span className="text-xs text-[#9FA4B2] mt-3 font-mono-precision">Traversing longitudinal knowledge graph...</span>
        </div>
      ) : filtered.length === 0 ? (
        <div className="p-12 rounded-2xl bg-[#0E121C] border border-white/[0.06] text-center">
          <Sparkles className="w-8 h-8 text-[#646979] mx-auto mb-2" />
          <h3 className="text-sm font-medium text-[#EDEAE3]">No active discoveries in this category</h3>
          <p className="text-xs text-[#646979] mt-1 max-w-sm mx-auto">
            Nirixa will evaluate new connections as you ingest research papers or log mobile thoughts.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {filtered.map((d) => {
            const isAccepted = d.status === 'accepted';
            const isDismissed = d.status === 'dismissed';

            return (
              <div
                key={d.id}
                className={`p-5 rounded-2xl bg-[#0F131D] border transition-all flex flex-col justify-between ${
                  isAccepted
                    ? 'border-[#2E7D5B]/40 bg-[#0F161A]'
                    : isDismissed
                    ? 'border-white/[0.04] opacity-50'
                    : 'border-white/[0.08] hover:border-[#38BDF8]/30'
                }`}
              >
                <div>
                  {/* Top metadata */}
                  <div className="flex items-center justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] font-mono-precision px-2 py-0.5 rounded bg-[#38BDF8]/10 text-[#38BDF8] border border-[#38BDF8]/20">
                        {d.id}
                      </span>
                      <span className="text-[10px] font-mono-precision uppercase text-[#9FA4B2]">
                        {d.type.replace('_', ' ')}
                      </span>
                    </div>

                    <div className="flex items-center gap-2">
                      <span className="text-[11px] font-mono-precision text-[#C89B53]">
                        {Math.round(d.confidence * 100)}% Confidence
                      </span>
                      <span
                        className={`text-[10px] font-mono-precision px-1.5 py-0.5 rounded uppercase ${
                          d.status === 'candidate'
                            ? 'bg-amber-500/10 text-amber-300'
                            : d.status === 'accepted'
                            ? 'bg-emerald-500/10 text-emerald-300'
                            : 'bg-zinc-500/10 text-zinc-400'
                        }`}
                      >
                        {d.status}
                      </span>
                    </div>
                  </div>

                  {/* Title & Description */}
                  <h3 className="text-sm font-semibold text-[#EDEAE3] mt-3">
                    {d.title}
                  </h3>
                  <p className="text-xs text-[#9FA4B2] mt-1.5 leading-relaxed">
                    {d.description}
                  </p>

                  {/* Reasoning block */}
                  {d.reasoning && (
                    <div className="mt-3 p-3 rounded-xl bg-[#141824] border border-white/[0.05] text-xs">
                      <div className="text-[10px] font-mono-precision uppercase text-[#646979] mb-1">
                        Reasoning & Epistemic Basis
                      </div>
                      <div className="text-[#C5C8D4] leading-normal font-sans">
                        {d.reasoning}
                      </div>
                    </div>
                  )}

                  {/* Objects involved */}
                  {d.objectsInvolved && d.objectsInvolved.length > 0 && (
                    <div className="mt-3 flex items-center gap-1.5 flex-wrap">
                      <span className="text-[10px] font-mono-precision text-[#646979]">Involved:</span>
                      {d.objectsInvolved.map((obj: string) => (
                        <span
                          key={obj}
                          className="px-2 py-0.5 rounded bg-white/[0.05] border border-white/[0.08] text-[10px] font-mono-precision text-[#EDEAE3]"
                        >
                          {obj}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {/* Bottom Action Footer */}
                <div className="mt-5 pt-3 border-t border-white/[0.06] flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleUpdateStatus(d.id, 'accepted')}
                      className="px-2.5 py-1.5 rounded-lg bg-[#2E7D5B]/20 hover:bg-[#2E7D5B]/30 border border-[#2E7D5B]/40 text-xs text-[#7EE787] flex items-center gap-1 transition-all"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>Canonize</span>
                    </button>

                    <button
                      onClick={() => handleUpdateStatus(d.id, 'investigating')}
                      className="px-2.5 py-1.5 rounded-lg bg-[#1C212F] hover:bg-[#252C3E] border border-white/[0.08] text-xs text-[#EDEAE3] flex items-center gap-1 transition-all"
                    >
                      <Search className="w-3.5 h-3.5 text-[#38BDF8]" />
                      <span>Investigate</span>
                    </button>

                    <button
                      onClick={() => handleUpdateStatus(d.id, 'dismissed')}
                      className="px-2 py-1.5 rounded-lg text-xs text-[#646979] hover:text-[#9FA4B2] transition-colors"
                    >
                      Dismiss
                    </button>
                  </div>

                  {d.objectsInvolved && d.objectsInvolved.length > 0 && (
                    <button
                      onClick={() => {
                        const targetOta = d.objectsInvolved[0];
                        if (onSelectOtaForStudio) onSelectOtaForStudio(targetOta);
                        onNavigate('writing');
                      }}
                      className="text-xs text-[#C89B53] hover:underline flex items-center gap-1 font-medium"
                    >
                      <span>Write from this</span>
                      <ArrowRight className="w-3 h-3" />
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
