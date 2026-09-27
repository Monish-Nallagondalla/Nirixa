'use client';

import React, { useState } from 'react';
import { 
  Bell, 
  Orbit, 
  BookOpen, 
  PenTool, 
  LayoutDashboard, 
  CheckCircle2, 
  Sparkles, 
  AlertTriangle, 
  GitBranch, 
  Search 
} from 'lucide-react';
import NirixaLogo from './NirixaLogo';

export type ActiveTab = 
  | 'cockpit' 
  | 'orbit' 
  | 'discoveries' 
  | 'challenges' 
  | 'research' 
  | 'writing' 
  | 'evolution';

export type LifeSegment = 'phd' | 'linkedin' | 'enterprise' | 'personal';

interface HeaderNavProps {
  activeTab: ActiveTab;
  setActiveTab: (tab: ActiveTab) => void;
  activeSegment: LifeSegment;
  setActiveSegment: (segment: LifeSegment) => void;
  onOpenJarvis?: () => void;
  discoveryCount?: number;
  challengeCount?: number;
}

export default function HeaderNav({
  activeTab,
  setActiveTab,
  activeSegment,
  setActiveSegment,
  onOpenJarvis,
  discoveryCount = 3,
  challengeCount = 2,
}: HeaderNavProps) {
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 2500);
  };

  return (
    <header className="w-full border-b border-white/[0.07] bg-[#0E1118]/90 backdrop-blur-md sticky top-0 z-40">
      {/* Toast Alert */}
      {toastMessage && (
        <div className="absolute top-14 right-6 z-50 bg-[#161A24] border border-[#C89B53]/40 text-[#EDEAE3] text-xs px-4 py-2 rounded-xl shadow-2xl flex items-center gap-2 animate-in fade-in zoom-in duration-200">
          <CheckCircle2 className="w-4 h-4 text-[#C89B53]" />
          <span>{toastMessage}</span>
        </div>
      )}

      <div className="max-w-[1540px] mx-auto px-6 py-2.5 flex items-center justify-between gap-4">
        {/* Left: Logo & Brand Title */}
        <div className="flex items-center gap-4 shrink-0">
          <div onClick={() => setActiveTab('cockpit')} className="cursor-pointer">
            <NirixaLogo size={32} showText={true} version="v1.1.0" />
          </div>

          {/* Quick Return to Cockpit (If in sub-workbench) */}
          {activeTab !== 'cockpit' && (
            <button
              onClick={() => setActiveTab('cockpit')}
              className="hidden lg:flex px-2 py-1 rounded text-xs text-[#9FA4B2] hover:text-[#EDEAE3] hover:bg-white/[0.04] transition-all font-mono-precision items-center gap-1 border border-white/[0.06]"
            >
              <span>← Cockpit</span>
            </button>
          )}
        </div>

        {/* Center: Global Jarvis Search / Command HUD Bar */}
        <div className="flex-1 max-w-md mx-2">
          <button
            onClick={onOpenJarvis}
            className="w-full h-8 px-3 rounded-xl bg-[#12151E] hover:bg-[#161A25] border border-white/[0.08] hover:border-[#C89B53]/40 flex items-center justify-between text-xs text-[#646979] hover:text-[#EDEAE3] transition-all group shadow-inner"
          >
            <div className="flex items-center gap-2">
              <Search className="w-3.5 h-3.5 text-[#C89B53]/80 group-hover:text-[#C89B53]" />
              <span className="truncate">Ask Nirixa about your thinking, graph, research...</span>
            </div>
            <kbd className="hidden sm:inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded bg-white/[0.06] text-[10px] text-[#9FA4B2] font-mono-precision">
              Ctrl+K
            </kbd>
          </button>
        </div>

        {/* Center-Right: 7 Workbench Views */}
        <div className="hidden xl:flex items-center bg-[#12151E] border border-white/[0.07] rounded-xl p-1 gap-1">
          <button
            onClick={() => setActiveTab('cockpit')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'cockpit'
                ? 'bg-[#1C212F] text-[#EDEAE3] border border-[#C89B53]/40 font-semibold shadow-sm'
                : 'text-[#9FA4B2] hover:text-[#EDEAE3]'
            }`}
            title="Cockpit (1)"
          >
            <LayoutDashboard className="w-3.5 h-3.5" />
            Cockpit
          </button>

          <button
            onClick={() => setActiveTab('orbit')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'orbit'
                ? 'bg-[#1C212F] text-[#EDEAE3] border border-[#C89B53]/40 font-semibold shadow-sm'
                : 'text-[#9FA4B2] hover:text-[#EDEAE3]'
            }`}
            title="Knowledge Graph (2)"
          >
            <Orbit className="w-3.5 h-3.5" />
            Graph
          </button>

          <button
            onClick={() => setActiveTab('discoveries')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'discoveries'
                ? 'bg-[#1C212F] text-[#EDEAE3] border border-[#C89B53]/40 font-semibold shadow-sm'
                : 'text-[#9FA4B2] hover:text-[#EDEAE3]'
            }`}
            title="AI Discoveries (3)"
          >
            <Sparkles className="w-3.5 h-3.5 text-[#38BDF8]" />
            Discoveries
            {discoveryCount > 0 && (
              <span className="px-1.5 py-0.2 rounded-full bg-[#38BDF8]/20 text-[#38BDF8] text-[10px] font-mono-precision">
                {discoveryCount}
              </span>
            )}
          </button>

          <button
            onClick={() => setActiveTab('challenges')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'challenges'
                ? 'bg-[#1C212F] text-[#EDEAE3] border border-[#C89B53]/40 font-semibold shadow-sm'
                : 'text-[#9FA4B2] hover:text-[#EDEAE3]'
            }`}
            title="Epistemic Challenges (4)"
          >
            <AlertTriangle className="w-3.5 h-3.5 text-[#E5A93C]" />
            Challenges
            {challengeCount > 0 && (
              <span className="px-1.5 py-0.2 rounded-full bg-[#E5A93C]/20 text-[#E5A93C] text-[10px] font-mono-precision">
                {challengeCount}
              </span>
            )}
          </button>

          <button
            onClick={() => setActiveTab('research')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'research'
                ? 'bg-[#1C212F] text-[#EDEAE3] border border-[#C89B53]/40 font-semibold shadow-sm'
                : 'text-[#9FA4B2] hover:text-[#EDEAE3]'
            }`}
            title="PDF Lab (5)"
          >
            <BookOpen className="w-3.5 h-3.5" />
            PDF Lab
          </button>

          <button
            onClick={() => setActiveTab('writing')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'writing'
                ? 'bg-[#1C212F] text-[#EDEAE3] border border-[#C89B53]/40 font-semibold shadow-sm'
                : 'text-[#9FA4B2] hover:text-[#EDEAE3]'
            }`}
            title="Manuscript Studio (6)"
          >
            <PenTool className="w-3.5 h-3.5" />
            Studio
          </button>

          <button
            onClick={() => setActiveTab('evolution')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'evolution'
                ? 'bg-[#1C212F] text-[#EDEAE3] border border-[#C89B53]/40 font-semibold shadow-sm'
                : 'text-[#9FA4B2] hover:text-[#EDEAE3]'
            }`}
            title="Coevolution Timeline 2026-2029 (7)"
          >
            <GitBranch className="w-3.5 h-3.5 text-[#2E7D5B]" />
            Evolution
          </button>
        </div>

        {/* Right: Telemetry Bell & User Profile */}
        <div className="flex items-center gap-3 shrink-0">
          {/* Notification Bell with Emerald Online Dot */}
          <button
            onClick={() => showToast('Telegram Listener active • 303 Captures indexed')}
            className="w-8 h-8 rounded-lg bg-[#12151E] border border-white/[0.07] flex items-center justify-center text-[#9FA4B2] hover:text-[#EDEAE3] transition-colors relative"
            title="System Status"
          >
            <Bell className="w-3.5 h-3.5" />
            <span className="w-1.5 h-1.5 rounded-full bg-[#2E7D5B] absolute top-2 right-2 ring-2 ring-[#12151E]"></span>
          </button>

          {/* User Profile Pill */}
          <div className="flex items-center gap-2 pl-2 border-l border-white/[0.08]">
            <div className="w-7 h-7 rounded-lg bg-[#1A1E2B] border border-white/[0.08] flex items-center justify-center text-[#C89B53] font-mono-precision text-xs font-semibold">
              MN
            </div>
            <div className="hidden sm:flex flex-col text-left">
              <span className="text-xs font-medium text-[#EDEAE3] leading-none">Researcher</span>
              <span className="text-[10px] text-[#646979] font-mono-precision mt-0.5">Enterprise / Researcher</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
