'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Search, Sparkles, AlertTriangle, HelpCircle, Flame, ArrowRight, X, Cpu } from 'lucide-react';
import { ActiveTab } from './HeaderNav';

interface JarvisCommandModalProps {
  isOpen: boolean;
  onClose: () => void;
  onNavigate: (tab: ActiveTab) => void;
  onSelectOta?: (otaId: string) => void;
}

export default function JarvisCommandModal({
  isOpen,
  onClose,
  onNavigate,
  onSelectOta,
}: JarvisCommandModalProps) {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [resultData, setResultData] = useState<any>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    } else {
      setQuery('');
      setResultData(null);
    }
  }, [isOpen]);

  const handleSearch = async (overrideQuery?: string) => {
    const q = overrideQuery !== undefined ? overrideQuery : query;
    if (!q.trim()) return;

    setLoading(true);
    try {
      const res = await fetch('/api/episteme/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: q }),
      });
      const data = await res.json();
      if (data.success) {
        setResultData(data);
      }
    } catch (err) {
      console.error('Jarvis command error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose();
    } else if (e.key === 'Enter') {
      handleSearch();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4 bg-black/75 backdrop-blur-md animate-in fade-in duration-150">
      <div 
        className="w-full max-w-3xl bg-[#0F121A] border border-white/[0.12] rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[80vh]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Top Input Bar */}
        <div className="flex items-center gap-3 px-5 py-4 border-b border-white/[0.08] bg-[#141824]/60">
          <div className="w-8 h-8 rounded-lg bg-[#C89B53]/15 border border-[#C89B53]/30 flex items-center justify-center text-[#C89B53]">
            <Cpu className="w-4 h-4" />
          </div>
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask Nirixa about your thinking, graph, research, or contradictions..."
            className="flex-1 bg-transparent text-[#EDEAE3] placeholder-[#646979] text-sm focus:outline-none font-sans"
          />
          {loading ? (
            <div className="w-4 h-4 border-2 border-[#C89B53] border-t-transparent rounded-full animate-spin"></div>
          ) : (
            <button
              onClick={() => handleSearch()}
              className="px-3 py-1.5 rounded-lg bg-[#1C212F] border border-white/[0.08] text-xs text-[#EDEAE3] hover:border-[#C89B53]/40 flex items-center gap-1.5 transition-colors"
            >
              <span>Query</span>
              <ArrowRight className="w-3 h-3 text-[#C89B53]" />
            </button>
          )}
          <button
            onClick={onClose}
            className="p-1 rounded-md text-[#9FA4B2] hover:text-[#EDEAE3] transition-colors ml-1"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Quick Suggestion Chips */}
        {!resultData && !loading && (
          <div className="p-5 flex flex-col gap-3">
            <div className="text-[11px] font-mono-precision uppercase tracking-wider text-[#646979]">
              Suggested Inquiries
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <button
                onClick={() => {
                  setQuery('Find contradictions in my beliefs');
                  handleSearch('Find contradictions in my beliefs');
                }}
                className="flex items-center gap-2.5 p-3 rounded-xl bg-[#141824]/50 border border-white/[0.06] hover:border-[#C89B53]/30 hover:bg-[#1A1E2E] text-left transition-all group"
              >
                <AlertTriangle className="w-4 h-4 text-[#E5A93C] shrink-0" />
                <div className="flex flex-col">
                  <span className="text-xs font-medium text-[#EDEAE3] group-hover:text-[#F7F4EB]">
                    Find contradictions in beliefs
                  </span>
                  <span className="text-[10px] text-[#646979]">Surfaces beliefs under cognitive challenge</span>
                </div>
              </button>

              <button
                onClick={() => {
                  setQuery('Surface forgotten ideas and neglected inquiries');
                  handleSearch('Surface forgotten ideas and neglected inquiries');
                }}
                className="flex items-center gap-2.5 p-3 rounded-xl bg-[#141824]/50 border border-white/[0.06] hover:border-[#C89B53]/30 hover:bg-[#1A1E2E] text-left transition-all group"
              >
                <Sparkles className="w-4 h-4 text-[#38BDF8] shrink-0" />
                <div className="flex flex-col">
                  <span className="text-xs font-medium text-[#EDEAE3] group-hover:text-[#F7F4EB]">
                    Surface forgotten ideas
                  </span>
                  <span className="text-[10px] text-[#646979]">Unearth dormant EOs & unpursued leads</span>
                </div>
              </button>

              <button
                onClick={() => {
                  setQuery('Show weakly supported beliefs');
                  handleSearch('Show weakly supported beliefs');
                }}
                className="flex items-center gap-2.5 p-3 rounded-xl bg-[#141824]/50 border border-white/[0.06] hover:border-[#C89B53]/30 hover:bg-[#1A1E2E] text-left transition-all group"
              >
                <HelpCircle className="w-4 h-4 text-[#A78BFA] shrink-0" />
                <div className="flex flex-col">
                  <span className="text-xs font-medium text-[#EDEAE3] group-hover:text-[#F7F4EB]">
                    Audit belief calibration
                  </span>
                  <span className="text-[10px] text-[#646979]">Sort beliefs by lowest empirical confidence</span>
                </div>
              </button>

              <button
                onClick={() => {
                  setQuery('Contextual memory');
                  handleSearch('Contextual memory');
                }}
                className="flex items-center gap-2.5 p-3 rounded-xl bg-[#141824]/50 border border-white/[0.06] hover:border-[#C89B53]/30 hover:bg-[#1A1E2E] text-left transition-all group"
              >
                <Flame className="w-4 h-4 text-[#F97316] shrink-0" />
                <div className="flex flex-col">
                  <span className="text-xs font-medium text-[#EDEAE3] group-hover:text-[#F7F4EB]">
                    Inquire on "Contextual Memory"
                  </span>
                  <span className="text-[10px] text-[#646979]">Cross-traverse EOs, questions, and papers</span>
                </div>
              </button>
            </div>
          </div>
        )}

        {/* Results Stream */}
        {resultData && (
          <div className="p-5 overflow-y-auto space-y-4 max-h-[60vh]">
            {/* Intent Header */}
            <div className="p-3.5 rounded-xl bg-[#141824] border border-[#C89B53]/25 flex items-start justify-between">
              <div>
                <div className="text-[10px] font-mono-precision uppercase tracking-wider text-[#C89B53]">
                  {resultData.intent || 'Epistemic Search Results'}
                </div>
                <div className="text-xs text-[#EDEAE3] mt-1">
                  {resultData.summary}
                </div>
              </div>
            </div>

            {/* If Challenges & Beliefs */}
            {resultData.data?.challenges && resultData.data.challenges.length > 0 && (
              <div className="space-y-2">
                <div className="text-xs font-mono-precision uppercase text-[#E5A93C] flex items-center gap-1.5">
                  <AlertTriangle className="w-3.5 h-3.5" />
                  Active Challenges ({resultData.data.challenges.length})
                </div>
                {resultData.data.challenges.map((c: any) => (
                  <div key={c.id} className="p-3 rounded-xl bg-[#12151E] border border-white/[0.06] flex items-start justify-between gap-3">
                    <div>
                      <span className="text-[10px] font-mono-precision px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/20">
                        {c.id}
                      </span>
                      <p className="text-xs text-[#EDEAE3] font-medium mt-1">{c.claim}</p>
                      <p className="text-[11px] text-[#9FA4B2] mt-0.5">{c.challenge_thesis}</p>
                    </div>
                    <button
                      onClick={() => {
                        onClose();
                        onNavigate('challenges');
                      }}
                      className="px-2.5 py-1 rounded bg-[#1C212F] hover:bg-[#252C3E] text-[11px] text-[#EDEAE3] border border-white/[0.08] shrink-0 transition-colors"
                    >
                      Debate →
                    </button>
                  </div>
                ))}
              </div>
            )}

            {/* If Epistemic Objects */}
            {resultData.data?.epistemicObjects && resultData.data.epistemicObjects.length > 0 && (
              <div className="space-y-2">
                <div className="text-xs font-mono-precision uppercase text-[#C89B53] flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5" />
                  Epistemic Objects ({resultData.data.epistemicObjects.length})
                </div>
                {resultData.data.epistemicObjects.map((eo: any) => (
                  <div key={eo.id} className="p-3 rounded-xl bg-[#12151E] border border-white/[0.06] flex items-start justify-between gap-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] font-mono-precision px-1.5 py-0.5 rounded bg-[#C89B53]/15 text-[#C89B53] border border-[#C89B53]/30">
                          {eo.id}
                        </span>
                        <span className="text-xs font-medium text-[#EDEAE3]">{eo.title}</span>
                      </div>
                      <p className="text-[11px] text-[#9FA4B2] mt-1 line-clamp-2">{eo.description}</p>
                    </div>
                    <button
                      onClick={() => {
                        if (onSelectOta) onSelectOta(eo.id);
                        onClose();
                        onNavigate('orbit');
                      }}
                      className="px-2.5 py-1 rounded bg-[#1C212F] hover:bg-[#252C3E] text-[11px] text-[#EDEAE3] border border-white/[0.08] shrink-0 transition-colors"
                    >
                      View in Graph →
                    </button>
                  </div>
                ))}
              </div>
            )}

            {/* If Questions */}
            {resultData.data?.questions && resultData.data.questions.length > 0 && (
              <div className="space-y-2">
                <div className="text-xs font-mono-precision uppercase text-[#38BDF8] flex items-center gap-1.5">
                  <HelpCircle className="w-3.5 h-3.5" />
                  Questions ({resultData.data.questions.length})
                </div>
                {resultData.data.questions.map((q: any) => (
                  <div key={q.id} className="p-3 rounded-xl bg-[#12151E] border border-white/[0.06] flex items-start justify-between gap-3">
                    <div>
                      <span className="text-[10px] font-mono-precision px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-300 border border-sky-500/20">
                        {q.id}
                      </span>
                      <p className="text-xs text-[#EDEAE3] font-medium mt-1">{q.text}</p>
                      <span className="text-[10px] text-[#646979] font-mono-precision">Status: {q.status} • Priority: {q.priority}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* If Beliefs */}
            {resultData.data?.beliefs && resultData.data.beliefs.length > 0 && (
              <div className="space-y-2">
                <div className="text-xs font-mono-precision uppercase text-[#A78BFA] flex items-center gap-1.5">
                  <Flame className="w-3.5 h-3.5" />
                  Beliefs ({resultData.data.beliefs.length})
                </div>
                {resultData.data.beliefs.map((b: any) => (
                  <div key={b.id} className="p-3 rounded-xl bg-[#12151E] border border-white/[0.06] flex items-start justify-between gap-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] font-mono-precision px-1.5 py-0.5 rounded bg-purple-500/10 text-purple-300 border border-purple-500/20">
                          {b.id}
                        </span>
                        <span className="text-[10px] text-[#C89B53] font-mono-precision">
                          Confidence: {Math.round((b.confidence || 0.7) * 100)}%
                        </span>
                      </div>
                      <p className="text-xs text-[#EDEAE3] font-medium mt-1">{b.proposition}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Footer info */}
        <div className="px-5 py-2.5 border-t border-white/[0.06] bg-[#0E1118] flex items-center justify-between text-[11px] text-[#646979]">
          <span>Tip: Press <kbd className="px-1.5 py-0.5 rounded bg-white/[0.06] text-[#9FA4B2] font-mono-precision">Esc</kbd> to close</span>
          <span>Nirixa Episteme Jarvis Engine</span>
        </div>
      </div>
    </div>
  );
}
