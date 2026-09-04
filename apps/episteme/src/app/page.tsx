'use client';

import React, { useState, useEffect } from 'react';
import HeaderNav, { ActiveTab, LifeSegment } from '@/components/HeaderNav';
import CockpitBento from '@/components/CockpitBento';
import OrbitGraph from '@/components/OrbitGraph';
import PdfLab from '@/components/PdfLab';
import WritingStudio from '@/components/WritingStudio';

export default function Home() {
  const [activeTab, setActiveTab] = useState<ActiveTab>('cockpit');
  const [activeSegment, setActiveSegment] = useState<LifeSegment>('phd');

  // Keyboard shortcut listener
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) {
        return;
      }
      if (e.key === '1') setActiveTab('cockpit');
      if (e.key === '2') setActiveTab('orbit');
      if (e.key === '3') setActiveTab('research');
      if (e.key === '4') setActiveTab('writing');
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <main className="min-h-screen bg-[#06080F] text-slate-100 selection:bg-cyan-500/30 selection:text-cyan-200 relative pb-16">
      {/* Cosmic Ambient Lighting */}
      <div className="glow-orb-1" />
      <div className="glow-orb-2" />

      {/* Top Navigation */}
      <HeaderNav
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        activeSegment={activeSegment}
        setActiveSegment={setActiveSegment}
      />

      {/* View Container */}
      <div className="max-w-[1440px] mx-auto px-6 pt-6 relative z-10">
        {activeTab === 'cockpit' && (
          <CockpitBento activeSegment={activeSegment} onNavigate={setActiveTab} />
        )}

        {activeTab === 'orbit' && (
          <OrbitGraph onNavigate={setActiveTab} />
        )}

        {activeTab === 'research' && (
          <PdfLab onNavigate={setActiveTab} />
        )}

        {activeTab === 'writing' && (
          <WritingStudio onNavigate={setActiveTab} />
        )}
      </div>
    </main>
  );
}
