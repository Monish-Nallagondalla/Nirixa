'use client';

import React from 'react';
import { Sparkles, Orbit, BookOpen, PenTool, LayoutDashboard, Search, Bell, Command } from 'lucide-react';

export type ActiveTab = 'cockpit' | 'orbit' | 'research' | 'writing';
export type LifeSegment = 'phd' | 'linkedin' | 'enterprise' | 'personal';

interface HeaderNavProps {
  activeTab: ActiveTab;
  setActiveTab: (tab: ActiveTab) => void;
  activeSegment: LifeSegment;
  setActiveSegment: (segment: LifeSegment) => void;
}

export default function HeaderNav({
  activeTab,
  setActiveTab,
  activeSegment,
  setActiveSegment
}: HeaderNavProps) {
  const segments = [
    { id: 'phd', label: 'PhD Core' },
    { id: 'linkedin', label: 'LinkedIn Authority' },
    { id: 'enterprise', label: 'Enterprise Strategy' },
    { id: 'personal', label: 'Personal Mastery' }
  ];

  return (
    <header className="w-full border-b border-white/5 bg-[#06080F]/80 backdrop-blur-xl sticky top-0 z-50">
      <div className="max-w-[1440px] mx-auto px-6 py-3 flex flex-col md:flex-row md:items-center justify-between gap-4">
        {/* Brand & Mode Switcher */}
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500/20 to-indigo-500/30 border border-white/10 flex items-center justify-center shadow-[0_0_15px_rgba(56,189,248,0.25)]">
              <Sparkles className="w-4 h-4 text-cyan-400" />
            </div>
            <div>
              <span className="text-base font-semibold tracking-tight text-white flex items-center gap-2">
                Nirixa Episteme
                <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
                  OS v1.0
                </span>
              </span>
            </div>
          </div>

          {/* Core View Tabs (Awwwards Style) */}
          <nav className="flex items-center bg-white/[0.03] border border-white/5 rounded-xl p-1 gap-1">
            <button
              onClick={() => setActiveTab('cockpit')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                activeTab === 'cockpit'
                  ? 'bg-white/10 text-white shadow-sm border border-white/10'
                  : 'text-slate-400 hover:text-white hover:bg-white/[0.04]'
              }`}
            >
              <LayoutDashboard className="w-3.5 h-3.5" />
              Cockpit Bento
            </button>

            <button
              onClick={() => setActiveTab('orbit')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                activeTab === 'orbit'
                  ? 'bg-white/10 text-white shadow-sm border border-white/10'
                  : 'text-slate-400 hover:text-white hover:bg-white/[0.04]'
              }`}
            >
              <Orbit className="w-3.5 h-3.5 text-cyan-400" />
              Orbit Graph
            </button>

            <button
              onClick={() => setActiveTab('research')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                activeTab === 'research'
                  ? 'bg-white/10 text-white shadow-sm border border-white/10'
                  : 'text-slate-400 hover:text-white hover:bg-white/[0.04]'
              }`}
            >
              <BookOpen className="w-3.5 h-3.5 text-violet-400" />
              Research Lab
            </button>

            <button
              onClick={() => setActiveTab('writing')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                activeTab === 'writing'
                  ? 'bg-white/10 text-white shadow-sm border border-white/10'
                  : 'text-slate-400 hover:text-white hover:bg-white/[0.04]'
              }`}
            >
              <PenTool className="w-3.5 h-3.5 text-amber-400" />
              Writing Studio
            </button>
          </nav>
        </div>

        {/* Right Tools: Search & Life Segments */}
        <div className="flex items-center gap-3">
          <div className="relative hidden lg:flex items-center">
            <Search className="w-3.5 h-3.5 absolute left-3 text-slate-500" />
            <input
              type="text"
              placeholder="Search 48 OTAs, Papers, Notes..."
              className="bg-white/[0.03] border border-white/5 rounded-xl pl-8 pr-9 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500/40 w-64 transition-all"
            />
            <kbd className="absolute right-2.5 px-1.5 py-0.5 rounded text-[10px] font-mono text-slate-500 bg-white/5 border border-white/5">
              ⌘K
            </kbd>
          </div>

          <div className="flex items-center bg-white/[0.02] border border-white/5 rounded-xl p-1 gap-1">
            {segments.map((seg) => (
              <button
                key={seg.id}
                onClick={() => setActiveSegment(seg.id as LifeSegment)}
                className={`px-3 py-1 rounded-lg text-[11px] font-medium transition-all ${
                  activeSegment === seg.id
                    ? 'bg-gradient-to-r from-cyan-500/20 to-indigo-500/20 text-cyan-300 border border-cyan-500/30'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {seg.label}
              </button>
            ))}
          </div>

          <button className="w-8 h-8 rounded-xl bg-white/[0.03] border border-white/5 flex items-center justify-center text-slate-400 hover:text-white transition-all">
            <Bell className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </header>
  );
}
