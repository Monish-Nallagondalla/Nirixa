'use client';

import React, { useState } from 'react';
import { GitBranch, Calendar, User, Cpu, Sparkles, Trophy, ArrowRight, ShieldCheck, HelpCircle } from 'lucide-react';
import { ActiveTab } from './HeaderNav';

interface EvolutionTimelineProps {
  onNavigate: (tab: ActiveTab) => void;
  onSelectOtaForStudio?: (otaId: string) => void;
}

export default function EvolutionTimeline({
  onNavigate,
  onSelectOtaForStudio,
}: EvolutionTimelineProps) {
  const [selectedYear, setSelectedYear] = useState<string>('all');

  const timelineEvents = [
    {
      year: '2026',
      date: 'Q3 2026',
      track: 'human',
      title: 'Inquiry Primitive Emergence',
      desc: 'Monish shifts mental model: questions are living computational objects, not ephemeral prompts. 48 OTAs codified in My-Os.',
      objects: ['EO-001', 'Q-001', 'B-001'],
      badge: 'Epistemic Foundation',
      status: 'verified',
    },
    {
      year: '2026',
      date: 'Q3 2026',
      track: 'system',
      title: 'Nirixa Episteme OS v1.1 Deployment',
      desc: 'Local-first SQLite WAL architecture with 7 signature workbenches, zero-emoji minimalist typography, and sub-30ms query latency.',
      objects: ['PRD v1.0', 'SQLite WAL'],
      badge: 'Substrate Hardening',
      status: 'verified',
    },
    {
      year: '2026',
      date: 'Q4 2026',
      track: 'coevolution',
      title: 'Active Socratic Sparring Invariant Enforced',
      desc: 'Nirixa AI is forbidden from sycophantic auto-completion. AI starts identifying unstated premises and issuing counter-theses.',
      objects: ['EO-010', 'CHAL-001'],
      badge: 'Adversarial Shift',
      status: 'active',
    },
    {
      year: '2027',
      date: 'Q1 2027',
      track: 'human',
      title: 'Belief Revision & Empirical Falsification Testing',
      desc: 'First longitudinal falsification experiments run across 500 mobile captures. Monish formally invalidates 3 early architecture assumptions.',
      objects: ['B-004', 'Q-004'],
      badge: 'Calibration Milestone',
      status: 'projected',
    },
    {
      year: '2027',
      date: 'Q3 2027',
      track: 'system',
      title: 'Nirixa v1.5 Autonomous Research Agent',
      desc: 'Agent autonomously digests arXiv/PubMed PDFs, extracts claims with strength scores, and binds evidence to EOs in the background.',
      objects: ['PDF Lab v2', 'Auto-Ingest'],
      badge: 'Autonomous Ingestion',
      status: 'projected',
    },
    {
      year: '2028',
      date: 'Q2 2028',
      track: 'human',
      title: 'European Doctoral Submission (RQ1–RQ8)',
      desc: 'Submission of PhD thesis: "Human-AI Coevolution: Longitudinal Observational Study of Persistent Cognitive Scaffolding".',
      objects: ['PhD Thesis', 'Papers P1-P4'],
      badge: 'Academic Summit',
      status: 'projected',
    },
    {
      year: '2028',
      date: 'Q4 2028',
      track: 'system',
      title: 'Nirixa Open-Source Global Community Release',
      desc: 'Enterprise-grade generalized release of Nirixa OS on GitHub with synthetic benchmark datasets, sanitized of personal consulting scars.',
      objects: ['Nirixa OSS', 'v2.0'],
      badge: 'Open Source',
      status: 'projected',
    },
    {
      year: '2029',
      date: 'Q3 2029',
      track: 'coevolution',
      title: 'Milestone 2029: Global Keynote / TED Talk & AI Research Institute',
      desc: 'Monish delivers the landmark keynote on "How Intelligence Emerges Across Biological and Artificial Systems" (Age 32). Release of the completed 8-chapter book.',
      objects: ['Keynote', 'Book Anthology', 'Research Lab'],
      badge: 'North Star Target',
      status: 'projected',
    },
  ];

  const filteredEvents = timelineEvents.filter((ev) => {
    if (selectedYear === 'all') return true;
    return ev.year === selectedYear;
  });

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header Banner */}
      <div className="p-6 rounded-2xl bg-[#0E121C] border border-white/[0.08] relative overflow-hidden">
        <div className="absolute -right-10 -bottom-10 w-80 h-80 bg-[#2E7D5B]/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
          <div>
            <div className="flex items-center gap-2 text-[11px] font-mono-precision uppercase tracking-wider text-[#3EB67F]">
              <GitBranch className="w-4 h-4" />
              <span>Longitudinal Coevolution Observatory • PRD §34 & §77</span>
            </div>
            <h1 className="text-xl md:text-2xl font-serif text-[#EDEAE3] mt-1">
              "The product evolved with the person."
            </h1>
            <p className="text-xs text-[#9FA4B2] mt-1 max-w-2xl">
              Tracing Monish's intellectual trajectory against Nirixa's system architecture from 2026 across the 30-year compounding horizon toward the 2029 Global Keynote.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="px-3 py-1.5 rounded-xl bg-[#141824] border border-[#2E7D5B]/30 text-xs text-[#7EE787] font-mono-precision">
              Target: Age 32 Keynote (2029)
            </span>
          </div>
        </div>

        {/* Year Filter Pills */}
        <div className="flex items-center gap-2 mt-5 pt-4 border-t border-white/[0.06] overflow-x-auto">
          {['all', '2026', '2027', '2028', '2029'].map((yr) => (
            <button
              key={yr}
              onClick={() => setSelectedYear(yr)}
              className={`px-3 py-1 rounded-lg text-xs font-mono-precision transition-all ${
                selectedYear === yr
                  ? 'bg-[#18261E] text-[#7EE787] border border-[#2E7D5B]/40 font-semibold'
                  : 'text-[#9FA4B2] hover:text-[#EDEAE3] hover:bg-white/[0.03]'
              }`}
            >
              {yr === 'all' ? 'Full 2026–2029 Horizon' : yr}
            </button>
          ))}
        </div>
      </div>

      {/* Dual-Track Timeline View */}
      <div className="relative pl-6 sm:pl-10 border-l border-white/[0.1] space-y-8 ml-3 sm:ml-6">
        {filteredEvents.map((ev, idx) => {
          const isHuman = ev.track === 'human';
          const isSystem = ev.track === 'system';
          const isCoevolution = ev.track === 'coevolution';

          return (
            <div key={idx} className="relative group">
              {/* Timeline Marker Dot */}
              <div
                className={`absolute -left-[31px] sm:-left-[47px] top-1.5 w-4 h-4 rounded-full border-2 flex items-center justify-center transition-all ${
                  isHuman
                    ? 'bg-[#0B0D13] border-[#C89B53] text-[#C89B53]'
                    : isSystem
                    ? 'bg-[#0B0D13] border-[#38BDF8] text-[#38BDF8]'
                    : 'bg-[#0B0D13] border-[#2E7D5B] text-[#7EE787]'
                }`}
              >
                <div
                  className={`w-1.5 h-1.5 rounded-full ${
                    isHuman ? 'bg-[#C89B53]' : isSystem ? 'bg-[#38BDF8]' : 'bg-[#7EE787]'
                  }`}
                />
              </div>

              {/* Event Card */}
              <div
                className={`p-5 rounded-2xl bg-[#0F131D] border transition-all ${
                  ev.status === 'verified'
                    ? 'border-white/[0.08] hover:border-white/20'
                    : ev.status === 'active'
                    ? 'border-[#C89B53]/40 bg-[#141216]'
                    : 'border-white/[0.05] border-dashed hover:border-white/15'
                }`}
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-white/[0.06] pb-2.5">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono-precision font-semibold text-[#EDEAE3]">
                      {ev.date}
                    </span>
                    <span
                      className={`text-[10px] font-mono-precision px-2 py-0.5 rounded uppercase flex items-center gap-1 ${
                        isHuman
                          ? 'bg-[#C89B53]/15 text-[#E5A93C] border border-[#C89B53]/30'
                          : isSystem
                          ? 'bg-[#38BDF8]/15 text-[#38BDF8] border border-[#38BDF8]/30'
                          : 'bg-[#2E7D5B]/15 text-[#7EE787] border border-[#2E7D5B]/30'
                      }`}
                    >
                      {isHuman && <User className="w-3 h-3" />}
                      {isSystem && <Cpu className="w-3 h-3" />}
                      {isCoevolution && <Sparkles className="w-3 h-3" />}
                      {ev.track}
                    </span>
                    <span className="text-[10px] font-mono-precision text-[#646979]">
                      {ev.badge}
                    </span>
                  </div>

                  <span
                    className={`text-[10px] font-mono-precision px-1.5 py-0.2 rounded uppercase ${
                      ev.status === 'verified'
                        ? 'bg-emerald-500/10 text-emerald-400'
                        : ev.status === 'active'
                        ? 'bg-amber-500/10 text-amber-300'
                        : 'bg-zinc-500/10 text-zinc-400'
                    }`}
                  >
                    {ev.status}
                  </span>
                </div>

                <h3 className="text-sm font-semibold text-[#EDEAE3] mt-2.5">
                  {ev.title}
                </h3>
                <p className="text-xs text-[#9FA4B2] mt-1 leading-relaxed">
                  {ev.desc}
                </p>

                {/* Objects involved */}
                <div className="mt-3 flex items-center justify-between gap-2 pt-2 border-t border-white/[0.04]">
                  <div className="flex items-center gap-1.5 flex-wrap">
                    {ev.objects.map((obj) => (
                      <span
                        key={obj}
                        className="px-2 py-0.5 rounded bg-white/[0.04] text-[10px] font-mono-precision text-[#EDEAE3] border border-white/[0.06]"
                      >
                        {obj}
                      </span>
                    ))}
                  </div>

                  {isHuman && (
                    <button
                      onClick={() => onNavigate('writing')}
                      className="text-[11px] font-mono-precision text-[#C89B53] hover:underline flex items-center gap-1"
                    >
                      <span>Draft Chapter</span>
                      <ArrowRight className="w-3 h-3" />
                    </button>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
