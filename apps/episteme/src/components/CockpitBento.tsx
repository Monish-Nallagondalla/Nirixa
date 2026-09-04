'use client';

import React, { useState, useEffect } from 'react';
import { Play, Pause, SkipBack, SkipForward, Radio, BookOpen, Share2, Sparkles, Activity, Zap, ChevronRight, Layers } from 'lucide-react';
import { LifeSegment } from './HeaderNav';

interface CockpitBentoProps {
  activeSegment: LifeSegment;
  onNavigate: (tab: 'cockpit' | 'orbit' | 'research' | 'writing') => void;
}

export default function CockpitBento({ activeSegment, onNavigate }: CockpitBentoProps) {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [isPlaying, setIsPlaying] = useState(false);
  const [selectedCapture, setSelectedCapture] = useState<any>(null);
  const [activeConstellationNode, setActiveConstellationNode] = useState<any>(null);

  useEffect(() => {
    fetch('/api/cockpit')
      .then((res) => res.json())
      .then((json) => {
        if (json.success) {
          setData(json.data);
          if (json.data.recentCaptures && json.data.recentCaptures.length > 0) {
            setSelectedCapture(json.data.recentCaptures[0]);
          }
          if (json.data.constellation?.nodes && json.data.constellation.nodes.length > 0) {
            setActiveConstellationNode(json.data.constellation.nodes[0]);
          }
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load cockpit data:', err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[65vh]">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>
          <span className="text-xs font-mono text-slate-400">Loading Nirixa Episteme Cockpit...</span>
        </div>
      </div>
    );
  }

  const metrics = data?.metrics || {
    papersAnnotated: 14,
    otasConnected: 49,
    leadChapter: { maturity: 74, title: 'The Coevolution of Thought' },
    citationsBound: 38
  };

  const recentCaptures = data?.recentCaptures || [];
  const constellationNodes = data?.constellation?.nodes || [];
  const chapters = data?.chapters || [];

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      {/* 1. Life Segment Bar (Matching Image Header) */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { id: 'phd', label: 'PhD Core' },
          { id: 'linkedin', label: 'LinkedIn Authority' },
          { id: 'enterprise', label: 'Enterprise Strategy' },
          { id: 'personal', label: 'Personal Mastery' }
        ].map((seg) => {
          const isActive = activeSegment === seg.id;
          return (
            <div
              key={seg.id}
              className={`p-4 rounded-2xl border text-center transition-all ${
                isActive
                  ? 'bg-[#121826] border-cyan-500/40 text-white shadow-[0_0_25px_rgba(56,189,248,0.15)] font-semibold text-base'
                  : 'bg-[#0B0F17]/80 border-white/5 text-slate-400 hover:text-slate-200 text-sm font-medium'
              }`}
            >
              {seg.label}
            </div>
          );
        })}
      </div>

      {/* 2. The 3 Main Bento Columns (Matching Approved Image Layout) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* LEFT COLUMN (4 Cols): Weekly Compounding Metrics */}
        <div className="lg:col-span-4 flex flex-col gap-5">
          <div className="rounded-2xl bg-[#0B0F17]/90 border border-white/10 p-6 flex flex-col justify-between shadow-2xl backdrop-blur-xl relative overflow-hidden">
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-semibold text-slate-300">Weekly Compounding Metrics</span>
              <span className="text-slate-500 text-xs font-mono">• • •</span>
            </div>

            {/* 3 Glowing Circular Dials (Exactly like the approved image) */}
            <div className="grid grid-cols-3 gap-2 py-4 mb-4">
              {/* Dial 1: Papers */}
              <div className="flex flex-col items-center text-center">
                <div className="relative w-20 h-20 flex items-center justify-center">
                  <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                    <path
                      className="text-slate-800/80"
                      strokeWidth="2.5"
                      stroke="currentColor"
                      fill="none"
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                    <path
                      className="text-purple-400 drop-shadow-[0_0_10px_rgba(168,85,247,0.8)]"
                      strokeDasharray="65, 100"
                      strokeWidth="2.5"
                      strokeLinecap="round"
                      stroke="currentColor"
                      fill="none"
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                  </svg>
                  <div className="absolute text-center flex flex-col items-center">
                    <span className="text-lg font-bold text-white leading-none">{metrics.papersAnnotated}</span>
                    <BookOpen className="w-3 h-3 text-purple-400 mt-1" />
                  </div>
                </div>
                <span className="text-xs font-medium text-slate-200 mt-2">Papers</span>
                <span className="text-[10px] text-slate-500">Annotated</span>
              </div>

              {/* Dial 2: OTAs */}
              <div className="flex flex-col items-center text-center">
                <div className="relative w-20 h-20 flex items-center justify-center">
                  <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                    <path
                      className="text-slate-800/80"
                      strokeWidth="2.5"
                      stroke="currentColor"
                      fill="none"
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                    <path
                      className="text-cyan-400 drop-shadow-[0_0_10px_rgba(56,189,248,0.8)]"
                      strokeDasharray="100, 100"
                      strokeWidth="2.5"
                      strokeLinecap="round"
                      stroke="currentColor"
                      fill="none"
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                  </svg>
                  <div className="absolute text-center flex flex-col items-center">
                    <span className="text-lg font-bold text-white leading-none">{metrics.otasConnected}</span>
                    <Share2 className="w-3 h-3 text-cyan-400 mt-1" />
                  </div>
                </div>
                <span className="text-xs font-medium text-slate-200 mt-2">OTAs</span>
                <span className="text-[10px] text-cyan-400">Connected</span>
              </div>

              {/* Dial 3: Book Maturity */}
              <div className="flex flex-col items-center text-center">
                <div className="relative w-20 h-20 flex items-center justify-center">
                  <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                    <path
                      className="text-slate-800/80"
                      strokeWidth="2.5"
                      stroke="currentColor"
                      fill="none"
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                    <path
                      className="text-indigo-400 drop-shadow-[0_0_10px_rgba(129,140,248,0.8)]"
                      strokeDasharray="74, 100"
                      strokeWidth="2.5"
                      strokeLinecap="round"
                      stroke="currentColor"
                      fill="none"
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                  </svg>
                  <div className="absolute text-center flex flex-col items-center">
                    <span className="text-lg font-bold text-white leading-none">{metrics.leadChapter?.maturity || 74}%</span>
                    <Layers className="w-3 h-3 text-indigo-400 mt-1" />
                  </div>
                </div>
                <span className="text-xs font-medium text-slate-200 mt-2">Book Ch. 2</span>
                <span className="text-[10px] text-slate-500">Maturity at</span>
              </div>
            </div>

            {/* Sub-cards (matching image) */}
            <div className="space-y-3 pt-4 border-t border-white/5">
              <div className="flex items-start gap-3 text-xs">
                <Activity className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
                <div>
                  <div className="text-slate-200 font-medium">High-density data links</div>
                  <div className="text-[11px] text-slate-400">Modern high-density data typography, and clean integration.</div>
                </div>
              </div>

              <div className="flex items-start gap-3 text-xs">
                <div className="w-4 h-4 rounded-full border border-cyan-400 flex items-center justify-center shrink-0 mt-0.5">
                  <div className="w-1.5 h-1.5 bg-cyan-400 rounded-full"></div>
                </div>
                <div>
                  <div className="text-slate-200 font-medium">Razor-sharp 0.5px borders</div>
                  <div className="text-[11px] text-slate-400">Sub-pixel precision glassmorphism.</div>
                </div>
              </div>

              <div className="flex items-start gap-3 text-xs">
                <Sparkles className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                <div>
                  <div className="text-slate-200 font-medium">Ultra-luxury aesthetic</div>
                  <div className="text-[11px] text-slate-400">Inspired by Reflect.app, Linear, and Awwwards SOTD.</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* CENTER COLUMN (4.5 Cols): Beautiful Mobile Audio Waveform Player */}
        <div className="lg:col-span-4 flex flex-col gap-5">
          <div className="rounded-2xl bg-[#0B0F17]/90 border border-white/10 p-6 flex flex-col justify-between shadow-2xl backdrop-blur-xl">
            <div>
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-semibold text-slate-300">Beautiful mobile audio waveform player</span>
                <span className="text-slate-500 text-xs font-mono">• • •</span>
              </div>
              <p className="text-[11px] text-slate-400 mb-5">
                Recently captured Telegram voice notes with transcription tags.
              </p>

              {/* Centered Waveform Visualization */}
              <div className="py-6 flex items-center justify-center">
                <div className="flex items-center justify-center gap-1.5 h-16 w-full px-2">
                  {[25, 45, 70, 95, 60, 85, 40, 100, 75, 50, 90, 65, 80, 45, 95, 70, 30, 85, 100, 60, 40, 75, 90, 50, 65, 80].map((h, i) => (
                    <div
                      key={i}
                      style={{ height: `${h}%` }}
                      className={`w-1 rounded-full transition-all duration-300 ${
                        isPlaying
                          ? 'bg-gradient-to-t from-cyan-500 via-indigo-400 to-white shadow-[0_0_10px_rgba(56,189,248,0.6)]'
                          : 'bg-slate-700'
                      }`}
                    />
                  ))}
                </div>
              </div>

              {/* Player Controls (Back, Play/Pause, Next) */}
              <div className="flex items-center justify-center gap-6 mb-6">
                <button className="text-slate-500 hover:text-white transition-all">
                  <SkipBack className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setIsPlaying(!isPlaying)}
                  className="w-12 h-12 rounded-full bg-gradient-to-br from-cyan-400 to-indigo-500 flex items-center justify-center text-slate-950 shadow-[0_0_20px_rgba(56,189,248,0.5)] hover:scale-105 transition-all"
                >
                  {isPlaying ? <Pause className="w-5 h-5 fill-current" /> : <Play className="w-5 h-5 fill-current ml-0.5" />}
                </button>
                <button className="text-slate-500 hover:text-white transition-all">
                  <SkipForward className="w-4 h-4" />
                </button>
              </div>

              {/* Voice Notes List */}
              <div className="space-y-2.5">
                {recentCaptures.slice(0, 3).map((item: any, idx: number) => (
                  <div
                    key={item.id}
                    onClick={() => setSelectedCapture(item)}
                    className={`p-3 rounded-xl border transition-all cursor-pointer flex items-center justify-between ${
                      selectedCapture?.id === item.id
                        ? 'bg-white/[0.07] border-cyan-500/40 shadow-[0_0_15px_rgba(56,189,248,0.15)]'
                        : 'bg-white/[0.02] border-white/5 hover:bg-white/[0.04]'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <button className="w-7 h-7 rounded-full bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
                        <Play className="w-3 h-3 ml-0.5 fill-current" />
                      </button>
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-semibold text-white">Voice Note</span>
                          <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-white/5 text-slate-400 border border-white/5">
                            {item.tags || '#insight'}
                          </span>
                        </div>
                        <div className="text-[11px] text-slate-400 line-clamp-1">
                          {item.raw_text?.slice(0, 50) || 'Transcription: cognitive coevolution...'}
                        </div>
                      </div>
                    </div>
                    <span className="text-[10px] font-mono text-slate-500 shrink-0">00:3{idx + 2}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT COLUMN (3.5 Cols): Interactive Mini-Constellation */}
        <div className="lg:col-span-4 flex flex-col gap-5">
          <div className="rounded-2xl bg-[#0B0F17]/90 border border-white/10 p-6 flex flex-col justify-between shadow-2xl backdrop-blur-xl">
            <div>
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-semibold text-slate-300">Interactive mini-constellation of the 48 OTAs</span>
                <span className="text-slate-500 text-xs font-mono">• • •</span>
              </div>
              <p className="text-[11px] text-slate-400 mb-4">
                Click any node to inspect its epistemic lineage.
              </p>

              {/* The 3D Mini-Constellation SVG */}
              <div className="relative w-full aspect-square rounded-2xl bg-[#070A10] border border-white/5 flex items-center justify-center overflow-hidden">
                <svg className="w-full h-full p-4" viewBox="0 0 240 240">
                  <defs>
                    <radialGradient id="miniConstellationGlow" cx="50%" cy="50%" r="50%">
                      <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.4" />
                      <stop offset="100%" stopColor="#070a10" stopOpacity="0" />
                    </radialGradient>
                  </defs>

                  {/* Ambient Glow */}
                  <circle cx="120" cy="120" r="100" fill="url(#miniConstellationGlow)" />

                  {/* Glowing Connecting Beams */}
                  <line x1="120" y1="120" x2="65" y2="70" stroke="rgba(56,189,248,0.5)" strokeWidth="1.5" />
                  <line x1="120" y1="120" x2="175" y2="75" stroke="rgba(129,140,248,0.5)" strokeWidth="1.5" />
                  <line x1="120" y1="120" x2="80" y2="175" stroke="rgba(56,189,248,0.4)" strokeWidth="1.5" />
                  <line x1="120" y1="120" x2="170" y2="165" stroke="rgba(168,85,247,0.4)" strokeWidth="1.5" />
                  <line x1="65" y1="70" x2="40" y2="120" stroke="rgba(56,189,248,0.3)" strokeWidth="1" />
                  <line x1="40" y1="120" x2="80" y2="175" stroke="rgba(56,189,248,0.3)" strokeWidth="1" />
                  <line x1="175" y1="75" x2="200" y2="125" stroke="rgba(129,140,248,0.3)" strokeWidth="1" />
                  <line x1="200" y1="125" x2="170" y2="165" stroke="rgba(168,85,247,0.3)" strokeWidth="1" />
                  <line x1="65" y1="70" x2="175" y2="75" stroke="rgba(255,255,255,0.1)" strokeWidth="1" strokeDasharray="3 3" />
                  <line x1="80" y1="175" x2="170" y2="165" stroke="rgba(255,255,255,0.1)" strokeWidth="1" strokeDasharray="3 3" />

                  {/* Constellation Nodes */}
                  {/* Center Node */}
                  <circle
                    cx="120"
                    cy="120"
                    r="9"
                    fill="#38bdf8"
                    className="cursor-pointer drop-shadow-[0_0_12px_#38bdf8]"
                    onClick={() => setActiveConstellationNode({ id: 'OTA-044', title: 'Machine-Input Inversion Paradox', pagerank: 1.0 })}
                  />

                  {/* Node 1: Top Left */}
                  <circle
                    cx="65"
                    cy="70"
                    r="7"
                    fill="#818cf8"
                    className="cursor-pointer drop-shadow-[0_0_10px_#818cf8]"
                    onClick={() => setActiveConstellationNode({ id: 'OTA-014', title: 'Substrate-Neutral Tool Plasticity', pagerank: 0.88 })}
                  />

                  {/* Node 2: Top Right */}
                  <circle
                    cx="175"
                    cy="75"
                    r="8"
                    fill="#a855f7"
                    className="cursor-pointer drop-shadow-[0_0_10px_#a855f7]"
                    onClick={() => setActiveConstellationNode({ id: 'OTA-047', title: 'Biological Memory Multi-Dimensionality', pagerank: 0.81 })}
                  />

                  {/* Node 3: Bottom Left */}
                  <circle
                    cx="80"
                    cy="175"
                    r="6.5"
                    fill="#34d399"
                    className="cursor-pointer drop-shadow-[0_0_8px_#34d399]"
                    onClick={() => setActiveConstellationNode({ id: 'OTA-045', title: 'Symbiotic Cognitive Coevolution', pagerank: 0.70 })}
                  />

                  {/* Node 4: Bottom Right */}
                  <circle
                    cx="170"
                    cy="165"
                    r="7"
                    fill="#fbbf24"
                    className="cursor-pointer drop-shadow-[0_0_8px_#fbbf24]"
                    onClick={() => setActiveConstellationNode({ id: 'OTA-046', title: 'Dual-Memory Epistemology: Head vs World', pagerank: 0.73 })}
                  />

                  {/* Node 5: Far Left */}
                  <circle
                    cx="40"
                    cy="120"
                    r="5"
                    fill="#38bdf8"
                    className="cursor-pointer"
                    onClick={() => setActiveConstellationNode({ id: 'OTA-001', title: 'Questions as First-Class Primitives', pagerank: 0.65 })}
                  />

                  {/* Node 6: Far Right */}
                  <circle
                    cx="200"
                    cy="125"
                    r="5.5"
                    fill="#c084fc"
                    className="cursor-pointer"
                    onClick={() => setActiveConstellationNode({ id: 'OTA-010', title: 'Adversarial Socratic Sparring', pagerank: 0.62 })}
                  />
                </svg>

                {/* Selected Node Overlay Tag */}
                <div className="absolute bottom-3 left-3 right-3 text-center">
                  <span className="text-[10px] font-mono text-cyan-300 bg-slate-900/90 px-2.5 py-1 rounded-full border border-cyan-500/30 shadow-md">
                    {activeConstellationNode?.id || 'OTA-044'}: {activeConstellationNode?.title?.slice(0, 30) || 'Cognitive Inversion'}
                  </span>
                </div>
              </div>

              <div className="mt-4 flex items-center justify-between">
                <span className="text-[11px] text-slate-400">PageRank: {activeConstellationNode?.pagerank || 0.88}</span>
                <button
                  onClick={() => onNavigate('orbit')}
                  className="text-xs font-medium text-cyan-400 hover:underline flex items-center gap-1"
                >
                  Full Orbit View <ChevronRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 3. The 8 Book Chapters Compounding Progress Strip */}
      <div className="rounded-2xl bg-[#0B0F17]/90 border border-white/10 p-6 shadow-2xl backdrop-blur-xl">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-semibold text-white">Book Anthology & 2029 Keynote Compounding Horizon</h3>
            <p className="text-xs text-slate-400">All 48 OTAs and research paper annotations compound into these 8 core chapters.</p>
          </div>
          <span className="text-xs font-mono text-cyan-400 font-medium">Chapter 2 Lead: 74% Maturity</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3.5">
          {chapters.map((ch: any) => (
            <div key={ch.id} className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 hover:border-white/10 transition-all flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between text-[11px] mb-1">
                  <span className="font-mono text-slate-400">Chapter {ch.chapter_number}</span>
                  <span className="font-mono text-cyan-400 font-semibold">{ch.maturity_percentage}%</span>
                </div>
                <div className="text-xs font-semibold text-slate-200 line-clamp-1 mb-1">{ch.title}</div>
              </div>

              <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden mt-3">
                <div
                  style={{ width: `${ch.maturity_percentage}%` }}
                  className="h-full bg-gradient-to-r from-cyan-500 to-indigo-500 rounded-full shadow-[0_0_8px_rgba(56,189,248,0.5)]"
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
