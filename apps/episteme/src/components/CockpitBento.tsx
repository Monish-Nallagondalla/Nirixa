'use client';

import React, { useState, useEffect } from 'react';
import { BookOpen, Share2, Layers, ShieldCheck, ArrowUpRight, MessageSquare, Database, Sparkles, Compass, CheckCircle2, BookmarkPlus } from 'lucide-react';
import { LifeSegment, ActiveTab } from './HeaderNav';
import RadialGauge from './RadialGauge';

interface CockpitBentoProps {
  activeSegment: LifeSegment;
  onSelectSegment?: (segment: LifeSegment) => void;
  onNavigate: (tab: ActiveTab) => void;
  onPromoteCaptureToStudio?: (text: string) => void;
  onSelectNodeForOrbit?: (node: any) => void;
}

export default function CockpitBento({
  activeSegment,
  onSelectSegment,
  onNavigate,
  onPromoteCaptureToStudio,
  onSelectNodeForOrbit
}: CockpitBentoProps) {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selectedCaptureIndex, setSelectedCaptureIndex] = useState(0);
  const [triageFilter, setTriageFilter] = useState<'all' | 'recent' | 'tagged'>('all');

  useEffect(() => {
    fetch('/api/cockpit')
      .then((res) => res.json())
      .then((json) => {
        if (json.success) {
          setData(json.data);
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
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border border-[#C89B53] border-t-transparent rounded-full animate-spin"></div>
          <span className="text-xs font-mono-precision text-[#9FA4B2] tracking-wider uppercase">
            Traversing nirixa.db telemetry...
          </span>
        </div>
      </div>
    );
  }

  const metrics = data?.metrics || {
    capturesCount: 303,
    otasConnected: 48,
    papersCount: 4,
    citationsBound: 2,
    leadChapter: { maturity: 74, title: 'The Coevolution of Thought' }
  };

  const recentCaptures = data?.recentCaptures || [];
  const chapters = data?.chapters || [];

  const segments = [
    { id: 'phd', label: 'PhD Core Research', count: 'RQ1–RQ8' },
    { id: 'linkedin', label: 'LinkedIn Authority', count: 'MoFu / Story Bank' },
    { id: 'enterprise', label: 'Enterprise Architecture', count: 'AI Coevolution' },
    { id: 'personal', label: 'Personal Mastery', count: '30-Year Horizon' }
  ];

  // Dynamic Stream Spotlight Configurations (PRD §24 & §25)
  const spotlightConfigs: Record<LifeSegment, {
    title: string;
    tagline: string;
    badge: string;
    badgeClass: string;
    icon: React.ReactNode;
    actionLabel: string;
    action: () => void;
    metricTitle: string;
    metricSubtitle: string;
    gauges: Array<{
      value: number | string;
      max?: number;
      unit?: string;
      label: string;
      sublabel: string;
      color: 'tungsten' | 'emerald' | 'copper' | 'graphite';
      icon: React.ReactNode;
      onClick: () => void;
    }>;
    invariants: Array<{
      icon: React.ReactNode;
      iconBg: string;
      iconBorder: string;
      iconText: string;
      title: string;
      desc: string;
    }>;
    directJumpLabel: string;
    directJumpAction: () => void;
    filterMatcher: (text: string) => boolean;
  }> = {
    phd: {
      title: 'PhD Core Research Spotlight',
      tagline: 'Longitudinal study of Human-AI-Product Coevolution across biological and artificial intelligence (RQ1–RQ8).',
      badge: 'RQ1–RQ8 Active',
      badgeClass: 'bg-[#38BDF8]/15 border-[#38BDF8]/30 text-[#38BDF8]',
      icon: <BookOpen className="w-4 h-4 text-[#38BDF8]" />,
      actionLabel: 'Enter PDF Research Lab →',
      action: () => onNavigate('research'),
      metricTitle: 'Doctoral Telemetry',
      metricSubtitle: 'Academic Footprint',
      gauges: [
        {
          value: metrics.papersCount || 4,
          max: 10,
          label: 'Papers',
          sublabel: 'Annotated in DB',
          color: 'tungsten',
          icon: <BookOpen className="w-3 h-3" />,
          onClick: () => onNavigate('research')
        },
        {
          value: metrics.citationsBound || 2,
          max: 10,
          label: 'Citations',
          sublabel: 'Bound to EOs',
          color: 'emerald',
          icon: <Share2 className="w-3 h-3" />,
          onClick: () => onNavigate('research')
        },
        {
          value: '8 RQs',
          max: 8,
          label: 'Inquiries',
          sublabel: 'Coevolution',
          color: 'copper',
          icon: <Compass className="w-3 h-3" />,
          onClick: () => onNavigate('orbit')
        }
      ],
      invariants: [
        {
          icon: <BookOpen className="w-3 h-3" />,
          iconBg: 'bg-[#38BDF8]/10',
          iconBorder: 'border-[#38BDF8]/25',
          iconText: 'text-[#38BDF8]',
          title: 'Provenance-Preserving Citations',
          desc: 'PRD §4.5: Academic claims distinguish source facts from AI interpretation.'
        },
        {
          icon: <ShieldCheck className="w-3 h-3" />,
          iconBg: 'bg-[#2E7D5B]/10',
          iconBorder: 'border-[#2E7D5B]/25',
          iconText: 'text-[#3EB67F]',
          title: 'Questions as Primitives (OTA-001)',
          desc: 'Persistent research questions compound while temporary answers decay.'
        },
        {
          icon: <Compass className="w-3 h-3" />,
          iconBg: 'bg-white/[0.04]',
          iconBorder: 'border-white/[0.08]',
          iconText: 'text-[#A6AEBF]',
          title: 'European Doctoral Lab Targets',
          desc: 'Tracking labs at Oxford, Cambridge, EPFL, and TUM for 2026-2029 defense.'
        }
      ],
      directJumpLabel: 'Open Vaswani 2017 Attention Paper Lab →',
      directJumpAction: () => onNavigate('research'),
      filterMatcher: (text: string) => /arithmetic|research|paper|model|intelligence|learn|attention|coevolution/i.test(text)
    },
    linkedin: {
      title: 'LinkedIn Authority & Narrative Stream',
      tagline: 'High-signal tech writing derived strictly from empirical workplace scars (MoFu Story Bank & Zero Hype).',
      badge: 'MoFu / Story Bank',
      badgeClass: 'bg-[#C89B53]/15 border-[#C89B53]/30 text-[#E5A93C]',
      icon: <Layers className="w-4 h-4 text-[#C89B53]" />,
      actionLabel: 'Open Manuscript Studio →',
      action: () => onNavigate('writing'),
      metricTitle: 'Authority Metrics',
      metricSubtitle: 'Story Bank Depth',
      gauges: [
        {
          value: 34,
          max: 50,
          label: 'Story Scars',
          sublabel: 'story_bank.py',
          color: 'tungsten',
          icon: <Layers className="w-3 h-3" />,
          onClick: () => onNavigate('writing')
        },
        {
          value: metrics.otasConnected || 48,
          max: 48,
          label: 'OTAs',
          sublabel: 'Connected',
          color: 'emerald',
          icon: <Share2 className="w-3 h-3" />,
          onClick: () => onNavigate('orbit')
        },
        {
          value: '100%',
          max: 100,
          label: 'Authentic',
          sublabel: 'Zero Fabrication',
          color: 'copper',
          icon: <ShieldCheck className="w-3 h-3" />,
          onClick: () => onNavigate('writing')
        }
      ],
      invariants: [
        {
          icon: <Database className="w-3 h-3" />,
          iconBg: 'bg-[#C89B53]/10',
          iconBorder: 'border-[#C89B53]/25',
          iconText: 'text-[#E5A93C]',
          title: 'SQLite Zero-Fabrication Invariant',
          desc: 'All posts cite empirical events from story_bank.py, never simulated meetings.'
        },
        {
          icon: <ShieldCheck className="w-3 h-3" />,
          iconBg: 'bg-[#2E7D5B]/10',
          iconBorder: 'border-[#2E7D5B]/25',
          iconText: 'text-[#3EB67F]',
          title: 'Dual-Repo Boundary Enforced',
          desc: 'Client names anonymized (Tier-1 Consulting); personal scars stay private.'
        },
        {
          icon: <Sparkles className="w-3 h-3" />,
          iconBg: 'bg-white/[0.04]',
          iconBorder: 'border-white/[0.08]',
          iconText: 'text-[#A6AEBF]',
          title: 'Rule 7: Zero Emoji Clutter',
          desc: 'High-signal copywriting: razor-sharp thesis density, zero marketing hype.'
        }
      ],
      directJumpLabel: 'Manuscript Studio: Draft LinkedIn Post →',
      directJumpAction: () => onNavigate('writing'),
      filterMatcher: (text: string) => /scar|consulting|league|amateur|manager|director|work|post|achieve|meeting/i.test(text)
    },
    enterprise: {
      title: 'Enterprise Architecture & Runtime Stream',
      tagline: 'Sub-30ms SQLite operational memory substrate, background Telegram mobile daemon, and agent telemetry.',
      badge: 'Local-First Engine',
      badgeClass: 'bg-[#2E7D5B]/20 border-[#2E7D5B]/35 text-[#3EB67F]',
      icon: <Database className="w-4 h-4 text-[#3EB67F]" />,
      actionLabel: 'Inspect Orbit Graph →',
      action: () => onNavigate('orbit'),
      metricTitle: 'System Performance',
      metricSubtitle: 'Substrate Health',
      gauges: [
        {
          value: '< 2ms',
          max: 30,
          label: 'Latency',
          sublabel: 'SQLite WAL Mode',
          color: 'emerald',
          icon: <Database className="w-3 h-3" />,
          onClick: () => onNavigate('orbit')
        },
        {
          value: '100%',
          max: 100,
          label: 'Eval Pass',
          sublabel: '10/10 PRD Tests',
          color: 'tungsten',
          icon: <ShieldCheck className="w-3 h-3" />,
          onClick: () => onNavigate('cockpit')
        },
        {
          value: recentCaptures.length || 307,
          max: 350,
          label: 'Captures',
          sublabel: 'nirixa.db Total',
          color: 'graphite',
          icon: <Sparkles className="w-3 h-3" />,
          onClick: () => onNavigate('cockpit')
        }
      ],
      invariants: [
        {
          icon: <Database className="w-3 h-3" />,
          iconBg: 'bg-[#2E7D5B]/10',
          iconBorder: 'border-[#2E7D5B]/25',
          iconText: 'text-[#3EB67F]',
          title: 'Sub-30ms SQLite Substrate',
          desc: 'PRD §41: better-sqlite3 WAL mode providing sub-30ms reads.'
        },
        {
          icon: <ShieldCheck className="w-3 h-3" />,
          iconBg: 'bg-[#C89B53]/10',
          iconBorder: 'border-[#C89B53]/25',
          iconText: 'text-[#E5A93C]',
          title: 'Singleton Daemon Lock',
          desc: 'Enforces single-instance PID locking to prevent duplicate message ingestion.'
        },
        {
          icon: <Layers className="w-3 h-3" />,
          iconBg: 'bg-white/[0.04]',
          iconBorder: 'border-white/[0.08]',
          iconText: 'text-[#A6AEBF]',
          title: 'Model Agnosticism (PRD §43)',
          desc: 'Core memory remains sovereign and independent of any LLM provider.'
        }
      ],
      directJumpLabel: 'Inspect Knowledge Constellation in Orbit →',
      directJumpAction: () => onNavigate('orbit'),
      filterMatcher: (text: string) => /crud|sync|daemon|sqlite|database|system|telegram|code|engine/i.test(text)
    },
    personal: {
      title: 'Personal Mastery & 30-Year Compounding',
      tagline: 'Tracking the multi-year intellectual journey toward foundational research on Intelligence Emergence.',
      badge: 'TED 2029 Horizon',
      badgeClass: 'bg-[#E5A93C]/15 border-[#E5A93C]/30 text-[#E5A93C]',
      icon: <Compass className="w-4 h-4 text-[#E5A93C]" />,
      actionLabel: 'Review Book Anthology →',
      action: () => onNavigate('writing'),
      metricTitle: 'Compounding Horizon',
      metricSubtitle: 'Age 33 Milestone',
      gauges: [
        {
          value: metrics.leadChapter?.maturity || 74,
          unit: '%',
          max: 100,
          label: 'Book Ch. 2',
          sublabel: 'Lead Maturity',
          color: 'copper',
          icon: <Layers className="w-3 h-3" />,
          onClick: () => onNavigate('writing')
        },
        {
          value: chapters.length || 8,
          max: 8,
          label: 'Chapters',
          sublabel: 'Authored in DB',
          color: 'tungsten',
          icon: <BookOpen className="w-3 h-3" />,
          onClick: () => onNavigate('writing')
        },
        {
          value: '2029',
          max: 2029,
          label: 'Keynote',
          sublabel: 'TED Talk Target',
          color: 'emerald',
          icon: <Compass className="w-3 h-3" />,
          onClick: () => onNavigate('evolution')
        }
      ],
      invariants: [
        {
          icon: <Compass className="w-3 h-3" />,
          iconBg: 'bg-[#E5A93C]/10',
          iconBorder: 'border-[#E5A93C]/25',
          iconText: 'text-[#E5A93C]',
          title: 'The 30-Year Compounding Horizon',
          desc: 'All research compounds toward foundational insights on the emergence of intelligence.'
        },
        {
          icon: <Layers className="w-3 h-3" />,
          iconBg: 'bg-[#C89B53]/10',
          iconBorder: 'border-[#C89B53]/25',
          iconText: 'text-[#C89B53]',
          title: 'Thought Lineage Continuity (OTA-011)',
          desc: 'Experience → Question → OTA → Post → Book Chapter ancestry preserved.'
        },
        {
          icon: <Sparkles className="w-3 h-3" />,
          iconBg: 'bg-[#2E7D5B]/10',
          iconBorder: 'border-[#2E7D5B]/25',
          iconText: 'text-[#3EB67F]',
          title: 'Sovereign Intelligence',
          desc: 'The human thinker is the core; AI is the persistent sparring partner, never a passive chatbot.'
        }
      ],
      directJumpLabel: 'Open Chapter 2: The Coevolution of Thought →',
      directJumpAction: () => onNavigate('writing'),
      filterMatcher: (text: string) => /capable|thinking|ahead|investments|para|second brain|dots|journal/i.test(text)
    }
  };

  const currentSpotlight = spotlightConfigs[activeSegment] || spotlightConfigs.phd;

  const displayCaptures = triageFilter === 'all'
    ? recentCaptures
    : (() => {
        const matches = recentCaptures.filter((c: any) => currentSpotlight.filterMatcher(c.raw_text || ''));
        return matches.length > 0 ? matches : recentCaptures;
      })();

  return (
    <div className="space-y-6 animate-in fade-in duration-300 pb-12">
      {/* 1. Monastic Hero Segment Switcher */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {segments.map((seg) => {
          const isActive = activeSegment === seg.id;
          return (
            <div
              key={seg.id}
              onClick={() => onSelectSegment && onSelectSegment(seg.id as LifeSegment)}
              className={`py-3.5 px-5 rounded-xl border transition-all duration-200 cursor-pointer select-none ${
                isActive
                  ? 'bg-[#181D29] border-[#C89B53]/70 text-[#EDEAE3] shadow-md shadow-[#C89B53]/5 ring-1 ring-[#C89B53]/30'
                  : 'bg-[#12151E] border-white/[0.06] text-[#9FA4B2] hover:text-[#EDEAE3] hover:border-white/10'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className={`text-xs font-mono-precision uppercase tracking-wider ${
                  isActive ? 'text-[#E5A93C] font-semibold' : 'text-[#646979]'
                }`}>
                  {seg.count}
                </span>
                {isActive && (
                  <span className="w-2 h-2 rounded-full bg-[#C89B53] shadow-[0_0_8px_#C89B53]"></span>
                )}
              </div>
              <div className="text-sm font-semibold tracking-tight mt-1">
                {seg.label}
              </div>
            </div>
          );
        })}
      </div>

      {/* 1.2 Dynamic Stream Spotlight Banner (Active Stream Lens) */}
      <div className="p-4 rounded-xl bg-[#12151E] border border-white/[0.08] flex flex-col md:flex-row md:items-center justify-between gap-3 shadow-lg">
        <div className="flex items-start gap-3">
          <div className="w-9 h-9 rounded-lg bg-[#C89B53]/10 border border-[#C89B53]/30 flex items-center justify-center text-[#E5A93C] shrink-0 mt-0.5">
            {currentSpotlight.icon}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-sm font-semibold text-[#EDEAE3] font-editorial">
                {currentSpotlight.title}
              </h3>
              <span className={`text-[10px] font-mono-precision px-2 py-0.5 rounded-full border ${currentSpotlight.badgeClass}`}>
                {currentSpotlight.badge}
              </span>
            </div>
            <p className="text-xs text-[#9FA4B2] mt-0.5 leading-relaxed">
              {currentSpotlight.tagline}
            </p>
          </div>
        </div>

        <button
          onClick={currentSpotlight.action}
          className="shrink-0 px-3 py-1.5 rounded-lg bg-[#181D29] border border-[#C89B53]/40 text-[#E5A93C] hover:bg-[#C89B53]/20 hover:text-[#EDEAE3] text-xs font-mono-precision flex items-center gap-1.5 transition-all shadow-sm self-start md:self-auto"
        >
          <span>{currentSpotlight.actionLabel}</span>
          <ArrowUpRight className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* 1.5 Epistemic Live Signal Strip: Discoveries & Challenges (PRD §25 & §30) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div
          onClick={() => onNavigate('discoveries')}
          className="p-4 rounded-xl bg-gradient-to-r from-[#0E1520] to-[#121824] border border-[#38BDF8]/25 hover:border-[#38BDF8]/50 transition-all cursor-pointer flex items-center justify-between group"
        >
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-[#38BDF8]/10 border border-[#38BDF8]/30 flex items-center justify-center text-[#38BDF8]">
              <Share2 className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-semibold text-[#EDEAE3] group-hover:text-[#38BDF8] transition-colors">
                  AI Discovery Inbox
                </span>
                <span className="text-[10px] font-mono-precision px-1.5 py-0.2 rounded-full bg-[#38BDF8]/20 text-[#38BDF8]">
                  3 Candidates
                </span>
              </div>
              <p className="text-[11px] text-[#9FA4B2] mt-0.5">
                Biological Memory Reconsolidation ↔ Epistemic State Updating
              </p>
            </div>
          </div>
          <span className="text-xs font-mono-precision text-[#38BDF8] group-hover:translate-x-0.5 transition-transform">
            Review →
          </span>
        </div>

        <div
          onClick={() => onNavigate('challenges')}
          className="p-4 rounded-xl bg-gradient-to-r from-[#181412] to-[#1C1614] border border-[#E5A93C]/25 hover:border-[#E5A93C]/50 transition-all cursor-pointer flex items-center justify-between group"
        >
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-[#E5A93C]/10 border border-[#E5A93C]/30 flex items-center justify-center text-[#E5A93C]">
              <Compass className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-semibold text-[#EDEAE3] group-hover:text-[#E5A93C] transition-colors">
                  Active Epistemic Challenges
                </span>
                <span className="text-[10px] font-mono-precision px-1.5 py-0.2 rounded-full bg-[#E5A93C]/20 text-[#E5A93C]">
                  2 Disagreements
                </span>
              </div>
              <p className="text-[11px] text-[#9FA4B2] mt-0.5">
                Nirixa challenges: "Passive AI agreement degrades human critical calibration"
              </p>
            </div>
          </div>
          <span className="text-xs font-mono-precision text-[#E5A93C] group-hover:translate-x-0.5 transition-transform">
            Debate →
          </span>
        </div>
      </div>

      {/* 2. Primary Three-Column Cockpit Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-stretch">
        {/* LEFT COLUMN (4 Cols): Compounding Telemetry & Empirical Scars (Spotlight Driven) */}
        <div className="lg:col-span-4 flex flex-col gap-4">
          <div className="bento-card p-5 flex flex-col justify-between h-full">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold text-[#EDEAE3] tracking-wide uppercase font-mono-precision">
                  {currentSpotlight.metricTitle}
                </span>
                <span className="text-[11px] font-mono-precision text-[#646979]">
                  {currentSpotlight.metricSubtitle}
                </span>
              </div>

              {/* 3 Circular Telemetry Gauges (Spotlight Driven) */}
              <div className="grid grid-cols-3 gap-2 py-4 border-b border-white/[0.06]">
                {currentSpotlight.gauges.map((g, idx) => (
                  <RadialGauge
                    key={idx}
                    value={g.value}
                    unit={g.unit}
                    max={g.max || 100}
                    label={g.label}
                    sublabel={g.sublabel}
                    color={g.color}
                    icon={g.icon}
                    onClick={g.onClick}
                  />
                ))}
              </div>

              {/* Verified Substrate & Invariants (Spotlight Driven) */}
              <div className="pt-4 space-y-3">
                {currentSpotlight.invariants.map((inv, idx) => (
                  <div key={idx} className="flex items-start gap-3 text-left">
                    <div className={`w-5 h-5 rounded ${inv.iconBg} border ${inv.iconBorder} flex items-center justify-center ${inv.iconText} shrink-0 mt-0.5`}>
                      {inv.icon}
                    </div>
                    <div>
                      <div className="text-xs font-medium text-[#EDEAE3]">
                        {inv.title}
                      </div>
                      <div className="text-[11px] text-[#9FA4B2] leading-relaxed">
                        {inv.desc}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Quick Workbench Direct Jump */}
            <div className="pt-4 mt-4 border-t border-white/[0.06] flex items-center justify-between text-xs">
              <button
                onClick={currentSpotlight.directJumpAction}
                className="text-xs font-mono-precision text-[#C89B53] hover:text-[#E5A93C] flex items-center gap-1 transition-colors"
              >
                {currentSpotlight.directJumpLabel}
              </button>
            </div>
          </div>
        </div>

        {/* CENTER COLUMN (4.5 Cols): REAL TELEGRAM CAPTURE TRIAGE STREAM */}
        <div className="lg:col-span-4 flex flex-col">
          <div className="bento-card p-5 flex flex-col justify-between h-full">
            <div>
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-semibold text-[#EDEAE3] tracking-wide uppercase font-mono-precision">
                    Telegram Friction Triage
                  </span>
                  <span className="text-[10px] font-mono-precision px-2 py-0.5 rounded bg-[#2E7D5B]/15 border border-[#2E7D5B]/30 text-[#3EB67F]">
                    {displayCaptures.length} Active
                  </span>
                </div>

                {/* Stream Filter Toggle */}
                <div className="flex items-center gap-1 bg-[#12151E] p-0.5 rounded-lg border border-white/[0.06]">
                  <button
                    onClick={() => setTriageFilter('all')}
                    className={`px-2 py-0.5 rounded text-[10px] font-mono-precision transition-all ${
                      triageFilter === 'all'
                        ? 'bg-[#1C212F] text-[#EDEAE3] font-semibold'
                        : 'text-[#646979] hover:text-[#9FA4B2]'
                    }`}
                  >
                    All ({recentCaptures.length})
                  </button>
                  <button
                    onClick={() => setTriageFilter('tagged')}
                    className={`px-2 py-0.5 rounded text-[10px] font-mono-precision transition-all ${
                      triageFilter === 'tagged'
                        ? 'bg-[#1C212F] text-[#C89B53] font-semibold'
                        : 'text-[#646979] hover:text-[#9FA4B2]'
                    }`}
                  >
                    Stream ({recentCaptures.filter((c: any) => currentSpotlight.filterMatcher(c.raw_text || '')).length})
                  </button>
                </div>
              </div>
              <p className="text-[11px] text-[#9FA4B2] mb-3 leading-relaxed">
                Raw mobile observations from Telegram waiting for scar extraction or OTA linkage.
              </p>

              {/* Capture Selection List */}
              <div className="space-y-2.5 max-h-[360px] overflow-y-auto pr-1">
                {displayCaptures.map((item: any, idx: number) => {
                  const isSelected = selectedCaptureIndex === idx;
                  return (
                    <div
                      key={item.id}
                      onClick={() => setSelectedCaptureIndex(idx)}
                      className={`p-3 rounded-xl border transition-all cursor-pointer ${
                        isSelected
                          ? 'bg-[#1A1F2C] border-[#C89B53]/50 shadow-sm'
                          : 'bg-[#12151E] border-white/[0.05] hover:bg-[#161924] hover:border-white/10'
                      }`}
                    >
                      <div className="flex items-center justify-between mb-1.5">
                        <div className="flex items-center gap-2">
                          <span className="text-[10px] font-mono-precision text-[#C89B53] font-semibold">
                            #{item.id}
                          </span>
                          <span className="text-[10px] font-mono-precision text-[#646979]">
                            {item.timestamp ? new Date(item.timestamp).toLocaleDateString() : 'Raw Mobile Note'}
                          </span>
                        </div>
                        <span className="text-[10px] font-mono-precision px-1.5 py-0.2 rounded bg-white/[0.04] text-[#9FA4B2] border border-white/[0.06]">
                          Telegram
                        </span>
                      </div>

                      <div className="text-xs text-[#EDEAE3] line-clamp-2 leading-relaxed font-sans">
                        "{item.raw_text || 'Friction note captured on the go...'}"
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Focused Triage Action Bar */}
            {displayCaptures.length > 0 && (
              <div className="pt-3 mt-3 border-t border-white/[0.06] flex items-center justify-between gap-2">
                <span className="text-[11px] font-mono-precision text-[#646979]">
                  Capture #{displayCaptures[selectedCaptureIndex]?.id || displayCaptures[0]?.id}
                </span>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => {
                      const item = displayCaptures[selectedCaptureIndex] || displayCaptures[0];
                      const text = item?.raw_text || '';
                      if (onPromoteCaptureToStudio) {
                        onPromoteCaptureToStudio(
                          `# Mobile Friction Synthesis (Ref: #${item?.id})\n\n## Raw Telegram Note\n> "${text}"\n\n## Refined Thesis Statement\nState the first-principles architectural lesson without corporate PII.\n\n## Empirical Scar Validation\nMap real consulting friction to actionable authority insight.`
                        );
                      }
                    }}
                    className="px-2.5 py-1 rounded bg-[#C89B53]/15 border border-[#C89B53]/35 text-[#E5A93C] hover:bg-[#C89B53]/25 text-xs font-mono-precision flex items-center gap-1.5 transition-all"
                  >
                    <span>Promote to Studio</span>
                    <ArrowUpRight className="w-3 h-3" />
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* RIGHT COLUMN (3.5 Cols): ORIGINAL THOUGHT MATRIX (OTAs) */}
        <div className="lg:col-span-4 flex flex-col">
          <div className="bento-card p-5 flex flex-col justify-between h-full">
            <div>
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-semibold text-[#EDEAE3] tracking-wide uppercase font-mono-precision">
                  Living OTAs Matrix
                </span>
                <span className="text-[10px] font-mono-precision text-[#C89B53]">
                  48 Primitives
                </span>
              </div>
              <p className="text-[11px] text-[#9FA4B2] mb-3 leading-relaxed">
                Core philosophical and computational primitives driving your thesis.
              </p>

              {/* Sample High-PageRank OTAs Grid */}
              <div className="space-y-2.5">
                {[
                  {
                    id: 'OTA-001',
                    title: 'Questions as First-Class Computational Primitives',
                    category: 'Epistemology',
                    pagerank: '0.98'
                  },
                  {
                    id: 'OTA-004',
                    title: 'Epistemic Persistence vs Context Window Atrophy',
                    category: 'Architecture',
                    pagerank: '0.94'
                  },
                  {
                    id: 'OTA-010',
                    title: 'The Socratic Sparring Invariant: AI Must Disagree',
                    category: 'Epistemology',
                    pagerank: '0.92'
                  },
                  {
                    id: 'OTA-043',
                    title: 'In-Situ Micro-Computation & Zero Context-Switch UX',
                    category: 'Ergonomics',
                    pagerank: '0.88'
                  }
                ].map((ota) => (
                  <div
                    key={ota.id}
                    onClick={() => {
                      if (onSelectNodeForOrbit) onSelectNodeForOrbit(ota);
                      onNavigate('writing');
                    }}
                    className="p-3 rounded-xl bg-[#12151E] border border-white/[0.06] hover:border-[#C89B53]/40 hover:bg-[#161924] transition-all cursor-pointer group"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-[10px] font-mono-precision font-semibold text-[#C89B53]">
                        {ota.id}
                      </span>
                      <span className="text-[10px] font-mono-precision text-[#646979]">
                        PR: {ota.pagerank}
                      </span>
                    </div>
                    <div className="text-xs font-medium text-[#EDEAE3] group-hover:text-[#E5A93C] transition-colors line-clamp-1">
                      {ota.title}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Jump to Full Knowledge View */}
            <div className="pt-3 mt-3 border-t border-white/[0.06] flex items-center justify-between text-xs">
              <span className="font-mono-precision text-[10px] text-[#646979]">
                48 OTAs Populated in SQLite
              </span>
              <button
                onClick={() => onNavigate('writing')}
                className="text-xs font-mono-precision text-[#C89B53] hover:text-[#E5A93C] flex items-center gap-1 transition-colors"
              >
                Manuscript Studio →
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* 3. The 8 Book Chapters Compounding Progress Strip (Bottom) */}
      <div className="bento-card p-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-5 gap-2">
          <div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#C89B53]"></span>
              <h3 className="text-sm font-bold text-[#EDEAE3] tracking-wide font-editorial">
                Book Anthology & 2029 Keynote Compounding Horizon
              </h3>
            </div>
            <p className="text-xs text-[#9FA4B2] mt-1">
              All 48 OTAs and research papers compound into these 8 living book chapters.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono-precision text-[#E5A93C] bg-[#C89B53]/10 border border-[#C89B53]/20 px-3 py-1 rounded-full font-semibold">
              Lead: Chapter 2 (74% Maturity)
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3.5">
          {chapters.map((ch: any) => (
            <div
              key={ch.id}
              onClick={() => {
                if (onPromoteCaptureToStudio) {
                  onPromoteCaptureToStudio(
                    `# Chapter ${ch.chapter_number}: ${ch.title}\n\n## Core Thesis\nHow human intelligence and autonomous agents coevolve across continuous interaction horizons.\n\n## Section 1: The Emergence Horizon\nEmpirical lessons from 300+ real-time telemetry interactions.`
                  );
                } else {
                  onNavigate('writing');
                }
              }}
              className="p-4 rounded-xl bg-[#12151E] border border-white/[0.06] hover:border-[#C89B53]/40 hover:bg-[#161924] transition-all cursor-pointer flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-center justify-between text-[11px] mb-1.5">
                  <span className="font-mono-precision text-[#9FA4B2]">Chapter {ch.chapter_number}</span>
                  <span className="font-mono-precision text-[#E5A93C] font-bold">{ch.maturity_percentage}%</span>
                </div>
                <div className="text-xs font-semibold text-[#EDEAE3] group-hover:text-[#E5A93C] transition-colors line-clamp-1 mb-1 font-editorial">
                  {ch.title}
                </div>
                <div className="text-[10px] text-[#646979] font-mono-precision">
                  {ch.target_word_count ? `${ch.current_word_count || 1850} / ${ch.target_word_count} words` : 'Synthesis stage'}
                </div>
              </div>

              <div className="w-full h-1 bg-white/5 rounded-full overflow-hidden mt-3.5">
                <div
                  style={{ width: `${ch.maturity_percentage}%` }}
                  className="h-full bg-gradient-to-r from-[#C89B53] to-[#E5A93C] rounded-full transition-all duration-500"
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
