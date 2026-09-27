'use client';

import React, { useState, useEffect } from 'react';
import HeaderNav, { ActiveTab, LifeSegment } from '@/components/HeaderNav';
import CockpitBento from '@/components/CockpitBento';
import OrbitGraph from '@/components/OrbitGraph';
import DiscoveriesDeck from '@/components/DiscoveriesDeck';
import ChallengesDeck from '@/components/ChallengesDeck';
import PdfLab from '@/components/PdfLab';
import WritingStudio from '@/components/WritingStudio';
import EvolutionTimeline from '@/components/EvolutionTimeline';
import JarvisCommandModal from '@/components/JarvisCommandModal';

export default function Home() {
  const [activeTab, setActiveTab] = useState<ActiveTab>('cockpit');
  const [activeSegment, setActiveSegment] = useState<LifeSegment>('phd');
  const [selectedOtaForStudio, setSelectedOtaForStudio] = useState<string | null>(null);
  const [incomingDraftText, setIncomingDraftText] = useState<string | null>(null);
  const [focusedOrbitNode, setFocusedOrbitNode] = useState<any>(null);
  const [isJarvisOpen, setIsJarvisOpen] = useState(false);

  // Keyboard shortcut listener (1-7, Cmd+K / Ctrl+K)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Command / Ctrl + K for Jarvis
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsJarvisOpen((prev) => !prev);
        return;
      }

      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) {
        return;
      }

      if (e.key === '1') setActiveTab('cockpit');
      if (e.key === '2') setActiveTab('orbit');
      if (e.key === '3') setActiveTab('discoveries');
      if (e.key === '4') setActiveTab('challenges');
      if (e.key === '5') setActiveTab('research');
      if (e.key === '6') setActiveTab('writing');
      if (e.key === '7') setActiveTab('evolution');
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <main className="min-h-screen bg-[#0B0D13] text-[#EDEAE3] selection:bg-[#C89B53]/25 selection:text-[#F7F4EB] relative pb-16">
      {/* Top Navigation with 7 Views & Persistent Jarvis Command Bar */}
      <HeaderNav
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        activeSegment={activeSegment}
        setActiveSegment={setActiveSegment}
        onOpenJarvis={() => setIsJarvisOpen(true)}
        discoveryCount={3}
        challengeCount={2}
      />

      {/* Global Jarvis Command HUD Modal */}
      <JarvisCommandModal
        isOpen={isJarvisOpen}
        onClose={() => setIsJarvisOpen(false)}
        onNavigate={setActiveTab}
        onSelectOta={(otaId) => {
          setSelectedOtaForStudio(otaId);
          setActiveTab('writing');
        }}
      />

      {/* View Container with Real Cross-View Linkage */}
      <div className="max-w-[1540px] mx-auto px-6 pt-6 relative z-10">
        {activeTab === 'cockpit' && (
          <CockpitBento
            activeSegment={activeSegment}
            onSelectSegment={setActiveSegment}
            onNavigate={setActiveTab}
            onPromoteCaptureToStudio={(text) => {
              setIncomingDraftText(text);
              setActiveTab('writing');
            }}
            onSelectNodeForOrbit={(node) => {
              setFocusedOrbitNode(node);
            }}
          />
        )}

        {activeTab === 'orbit' && (
          <OrbitGraph
            onNavigate={setActiveTab}
            incomingFocusedNode={focusedOrbitNode}
            onSelectOtaForStudio={(otaId) => {
              setSelectedOtaForStudio(otaId);
              setIncomingDraftText(null);
            }}
          />
        )}

        {activeTab === 'discoveries' && (
          <DiscoveriesDeck
            onNavigate={setActiveTab}
            onSelectOtaForStudio={(otaId) => {
              setSelectedOtaForStudio(otaId);
              setIncomingDraftText(null);
            }}
          />
        )}

        {activeTab === 'challenges' && (
          <ChallengesDeck
            onNavigate={setActiveTab}
            onSelectOtaForStudio={(otaId) => {
              setSelectedOtaForStudio(otaId);
              setIncomingDraftText(null);
            }}
          />
        )}

        {activeTab === 'research' && (
          <PdfLab onNavigate={setActiveTab} />
        )}

        {activeTab === 'writing' && (
          <WritingStudio
            onNavigate={setActiveTab}
            incomingDraftText={incomingDraftText}
            incomingOtaId={selectedOtaForStudio}
          />
        )}

        {activeTab === 'evolution' && (
          <EvolutionTimeline
            onNavigate={setActiveTab}
            onSelectOtaForStudio={(otaId) => {
              setSelectedOtaForStudio(otaId);
              setIncomingDraftText(null);
            }}
          />
        )}
      </div>
    </main>
  );
}
