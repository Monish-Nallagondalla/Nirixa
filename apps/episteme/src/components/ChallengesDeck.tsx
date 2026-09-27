'use client';

import React, { useState, useEffect } from 'react';
import { AlertTriangle, ShieldCheck, Flame, Search, ArrowRight, CheckCircle2, RotateCcw } from 'lucide-react';
import { ActiveTab } from './HeaderNav';

interface ChallengesDeckProps {
  onNavigate: (tab: ActiveTab) => void;
  onSelectOtaForStudio?: (otaId: string) => void;
}

export default function ChallengesDeck({
  onNavigate,
  onSelectOtaForStudio,
}: ChallengesDeckProps) {
  const [challenges, setChallenges] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeActionId, setActiveActionId] = useState<string | null>(null);
  const [feedback, setFeedback] = useState<string | null>(null);

  const fetchChallenges = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/episteme/challenges');
      const json = await res.json();
      if (json.success) {
        setChallenges(json.data || []);
      }
    } catch (err) {
      console.error('Failed to load challenges:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchChallenges();
  }, []);

  const handleAction = async (id: string, newStatus: string, msg: string) => {
    try {
      const res = await fetch('/api/episteme/challenges', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, status: newStatus }),
      });
      const json = await res.json();
      if (json.success) {
        setFeedback(msg);
        setTimeout(() => setFeedback(null), 3000);
        fetchChallenges();
      }
    } catch (err) {
      console.error('Error modifying challenge:', err);
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Toast Feedback */}
      {feedback && (
        <div className="fixed top-16 right-6 z-50 bg-[#161A24] border border-[#E5A93C]/40 text-[#EDEAE3] text-xs px-4 py-2 rounded-xl shadow-2xl flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-[#E5A93C]" />
          <span>{feedback}</span>
        </div>
      )}

      {/* Header Banner */}
      <div className="p-6 rounded-2xl bg-[#0E121C] border border-white/[0.08] relative overflow-hidden">
        <div className="absolute -right-10 -bottom-10 w-72 h-72 bg-[#E5A93C]/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
          <div>
            <div className="flex items-center gap-2 text-[11px] font-mono-precision uppercase tracking-wider text-[#E5A93C]">
              <AlertTriangle className="w-4 h-4" />
              <span>Adversarial Epistemic Engine • PRD §14 & §31</span>
            </div>
            <h1 className="text-xl md:text-2xl font-serif text-[#EDEAE3] mt-1">
              "I think one of your current beliefs may be wrong."
            </h1>
            <p className="text-xs text-[#9FA4B2] mt-1 max-w-2xl">
              Nirixa challenges assumptions and tests unstated premises rather than auto-completing. Disagreement expands intellectual sharpness and prevents cognitive atrophy.
            </p>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <span className="px-3 py-1.5 rounded-xl bg-[#181D2A] border border-[#E5A93C]/30 text-xs text-[#E5A93C] font-mono-precision">
              {challenges.filter((c) => c.status === 'active').length} Active Disagreements
            </span>
          </div>
        </div>
      </div>

      {/* Challenges List */}
      {loading ? (
        <div className="py-20 flex flex-col items-center justify-center text-center">
          <div className="w-8 h-8 border-2 border-[#E5A93C] border-t-transparent rounded-full animate-spin"></div>
          <span className="text-xs text-[#9FA4B2] mt-3 font-mono-precision">Auditing belief graph for falsification targets...</span>
        </div>
      ) : challenges.length === 0 ? (
        <div className="p-12 rounded-2xl bg-[#0E121C] border border-white/[0.06] text-center">
          <ShieldCheck className="w-8 h-8 text-[#2E7D5B] mx-auto mb-2" />
          <h3 className="text-sm font-medium text-[#EDEAE3]">Nothing is currently being challenged</h3>
          <p className="text-xs text-[#646979] mt-1 max-w-sm mx-auto">
            "That may mean your beliefs are well-calibrated. Or it may mean Nirixa isn't pushing you hard enough." — PRD §83
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {challenges.map((c) => {
            const isDefended = c.status === 'defended';
            const isRevised = c.status === 'revised';
            const isRejected = c.status === 'rejected';

            return (
              <div
                key={c.id}
                className={`p-6 rounded-2xl bg-[#0F131D] border transition-all ${
                  isDefended
                    ? 'border-[#2E7D5B]/30 bg-[#0F161A]'
                    : isRevised
                    ? 'border-[#38BDF8]/30 bg-[#0E1520]'
                    : isRejected
                    ? 'border-red-500/20 bg-[#160E12] opacity-60'
                    : 'border-white/[0.08] hover:border-[#E5A93C]/40'
                }`}
              >
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-white/[0.06] pb-3">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-mono-precision px-2 py-0.5 rounded bg-[#E5A93C]/15 text-[#E5A93C] border border-[#E5A93C]/30">
                      {c.id}
                    </span>
                    <span className="text-xs font-mono-precision text-[#9FA4B2]">
                      Target Belief: {c.belief_id || 'B-001'}
                    </span>
                    {c.eo_id && (
                      <span className="text-[10px] font-mono-precision px-1.5 py-0.5 rounded bg-white/[0.05] text-[#C89B53]">
                        {c.eo_id}
                      </span>
                    )}
                  </div>

                  <div className="flex items-center gap-3">
                    {c.belief_confidence && (
                      <span className="text-[11px] font-mono-precision text-[#9FA4B2]">
                        Prior Confidence: {Math.round(c.belief_confidence * 100)}%
                      </span>
                    )}
                    <span
                      className={`text-[10px] font-mono-precision px-2 py-0.5 rounded uppercase ${
                        c.status === 'active'
                          ? 'bg-amber-500/10 text-amber-300 border border-amber-500/20'
                          : c.status === 'defended'
                          ? 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/20'
                          : 'bg-zinc-500/10 text-zinc-400'
                      }`}
                    >
                      {c.status}
                    </span>
                  </div>
                </div>

                {/* Body Content */}
                <div className="mt-4 grid grid-cols-1 lg:grid-cols-2 gap-5">
                  {/* Left Column: Held Proposition */}
                  <div className="p-4 rounded-xl bg-[#141824]/50 border border-white/[0.05]">
                    <div className="text-[10px] font-mono-precision uppercase tracking-wider text-[#646979] flex items-center gap-1.5">
                      <Flame className="w-3.5 h-3.5 text-[#A78BFA]" />
                      Held User Proposition
                    </div>
                    <p className="text-sm font-medium text-[#EDEAE3] mt-2 leading-relaxed">
                      "{c.held_belief || c.claim}"
                    </p>
                  </div>

                  {/* Right Column: AI Disagreement Thesis */}
                  <div className="p-4 rounded-xl bg-[#1A181C]/50 border border-[#E5A93C]/20">
                    <div className="text-[10px] font-mono-precision uppercase tracking-wider text-[#E5A93C] flex items-center gap-1.5">
                      <AlertTriangle className="w-3.5 h-3.5" />
                      Nirixa's Counter-Thesis
                    </div>
                    <p className="text-xs text-[#EDEAE3] mt-2 leading-relaxed font-sans">
                      {c.challenge_thesis}
                    </p>
                  </div>
                </div>

                {/* Counter-evidence and Falsifiers */}
                <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                  {c.counter_evidence && (
                    <div className="p-3 rounded-xl bg-[#12151E] border border-white/[0.05]">
                      <span className="text-[10px] font-mono-precision uppercase text-[#9FA4B2] block mb-1">
                        Supporting Counter-Evidence
                      </span>
                      <span className="text-[#C5C8D4]">{c.counter_evidence}</span>
                    </div>
                  )}

                  {c.potential_falsifier && (
                    <div className="p-3 rounded-xl bg-[#12151E] border border-white/[0.05]">
                      <span className="text-[10px] font-mono-precision uppercase text-[#C89B53] block mb-1">
                        Potential Falsifier Test
                      </span>
                      <span className="text-[#C5C8D4]">{c.potential_falsifier}</span>
                    </div>
                  )}
                </div>

                {/* Socratic Action Row */}
                <div className="mt-5 pt-4 border-t border-white/[0.06] flex flex-wrap items-center justify-between gap-3">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleAction(c.id, 'defended', 'Belief defended. Empirical scar noted in calibration record.')}
                      className="px-3 py-1.5 rounded-lg bg-[#1C212F] hover:bg-[#262D40] border border-white/[0.08] text-xs text-[#EDEAE3] font-medium transition-colors"
                    >
                      Defend Premise
                    </button>

                    <button
                      onClick={() => handleAction(c.id, 'investigating', 'Challenge queued for deep literature investigation.')}
                      className="px-3 py-1.5 rounded-lg bg-[#1C212F] hover:bg-[#262D40] border border-white/[0.08] text-xs text-[#EDEAE3] flex items-center gap-1.5 transition-colors"
                    >
                      <Search className="w-3.5 h-3.5 text-[#38BDF8]" />
                      Investigate Evidence
                    </button>

                    <button
                      onClick={() => handleAction(c.id, 'revised', 'Belief marked for revision based on counter-evidence.')}
                      className="px-3 py-1.5 rounded-lg bg-[#C89B53]/20 hover:bg-[#C89B53]/30 border border-[#C89B53]/40 text-xs text-[#E5A93C] font-medium transition-colors"
                    >
                      Revise Belief
                    </button>

                    <button
                      onClick={() => handleAction(c.id, 'rejected', 'Belief rejected and archived to invalidation history.')}
                      className="px-3 py-1.5 rounded-lg bg-red-500/15 hover:bg-red-500/25 border border-red-500/30 text-xs text-red-300 font-medium transition-colors"
                    >
                      Reject Belief
                    </button>
                  </div>

                  {c.eo_id && (
                    <button
                      onClick={() => {
                        if (onSelectOtaForStudio) onSelectOtaForStudio(c.eo_id);
                        onNavigate('writing');
                      }}
                      className="text-xs text-[#C89B53] hover:underline flex items-center gap-1 font-medium"
                    >
                      <span>Draft Counter-Thesis</span>
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
