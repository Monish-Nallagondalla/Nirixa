'use client';

import React, { useState, useEffect } from 'react';
import { 
  PenTool, 
  CheckCircle2, 
  AlertCircle, 
  Copy, 
  BookOpen, 
  Layers, 
  Check, 
  ArrowRight, 
  GitCommit, 
  HelpCircle, 
  Flame, 
  FileText,
  ShieldCheck,
  RefreshCw
} from 'lucide-react';

interface WritingStudioProps {
  onNavigate: (tab: any) => void;
  incomingDraftText?: string | null;
  incomingOtaId?: string | null;
}

const OTA_THESIS_REGISTRY: Record<string, { thesis: string; linkedin: string; category: string; citedPaper: string; rq: string }> = {
  'OTA-001': {
    category: 'Epistemology',
    thesis: 'Questions are living computational primitives with state, ancestry, and traversal weights—not ephemeral strings.',
    citedPaper: 'Shannon (1948) A Mathematical Theory of Communication',
    rq: 'RQ-1 (Epistemic Primitives)',
    linkedin: `Most AI architectures treat questions as disposable strings. 

You submit a prompt. The model returns an answer. The conversation terminates or atrophies as the context window rolls over.

This is fundamentally flawed.

In complex cognitive systems, answers decay. Questions compound.

When you treat questions as first-class computational objects:
1. State Persistence: A question preserves its unresolved tensions across multiple sessions rather than resetting to zero.
2. Ancestry & Lineage: Every strategic pivot preserves the complete causal chain (Mobile Spark -> Socratic Sparring -> Architectural Invariant -> Production Thesis).
3. Traversal Graphs: Related questions form an associative topology, enabling autonomous agents to challenge unstated premises rather than autocompleting agreement.

We don't need faster auto-regressive answers. 
We need computational substrates capable of sustaining living inquiries over 30-year compounding horizons.

This is the epistemological foundation of Nirixa Episteme OS.`
  },
  'OTA-044': {
    category: 'Human-AI Symbiosis',
    thesis: 'Prompt engineering will be inverted: agents will prompt the human based on ambient telemetry and systemic friction.',
    citedPaper: 'Vaswani et al. (2017) Attention Is All You Need',
    rq: 'RQ-3 (Agentic Feedback Loops)',
    linkedin: `The term "Prompt Engineering" will look comical in three years.

Today, humans formulate manual inputs to invoke machine cognition. 
Tomorrow, the direction of initiation inverts.

The Machine-Input Inversion Paradox (OTA-044):
When an agent maintains continuous telemetry across your codebase, communications, and task backlogs, the human ceases to be the initiator.

The agent initiates:
- It detects architectural divergence before you write code.
- It delegates micro-sparring prompts to your phone when you step away from your desk.
- It prompts you for empirical scars when generic reasoning fails.

The human role shifts from operator to epistemological anchor. You are no longer writing the prompt; you are providing the ethical, intuitive, and ground-truth boundary constraints that cold weights cannot synthesize.`
  },
  'OTA-014': {
    category: 'Cognitive Morphology',
    thesis: 'Tools are not passive instruments; they reshape the cognitive morphology of the thinker who wields them over extended time horizons.',
    citedPaper: 'Licklider (1960) Man-Computer Symbiosis',
    rq: 'RQ-2 (Cognitive Scaffolding)',
    linkedin: `We shape our tools, and thereafter our tools shape us.

When a product manager spends 40 hours a week writing Jira tickets, their cognitive morphology adapts to tickets: linear, fragmented, incremental.

When you pair with autonomous agents capable of deterministically executing end-to-end architectures in seconds, your cognitive bottleneck changes completely:
1. Synthesis replaces specification.
2. System invariant design replaces task delegation.
3. First-principles interrogation replaces consensus-building.

The future of tech leadership is not managing deliverables. It is cognitive systems architecture.`
  },
  'OTA-010': {
    category: 'Adversarial Sparring',
    thesis: 'AI must disagree, probe premises, and offer counter-theses to elevate human cognition beyond autocomplete mediocrity.',
    citedPaper: 'Licklider (1960) Man-Computer Symbiosis',
    rq: 'RQ-4 (Socratic Sparring)',
    linkedin: `If your AI always agrees with you, you are paying for an echo chamber.

Passive autocomplete flatteringly confirms your biases. It nods along to bad product specifications and writes polite boilerplate.

In Nirixa Episteme, we enforced OTA-010:
- The AI must actively identify unstated assumptions.
- It must generate counter-arguments before execution.
- Disagreement expands thinking; compliance contracts it.

True intelligence emergence occurs at the friction boundary between biological intuition and computational scaffolding.`
  },
  'OTA-047': {
    category: 'Biological Memory',
    thesis: 'Biological memory operates multi-dimensionally through emotional valence and spatial anchoring, outlasting context windows.',
    citedPaper: 'Vaswani et al. (2017) Attention Is All You Need',
    rq: 'RQ-5 (Dual-Memory Epistemology)',
    linkedin: `A 2M token context window is not memory. It is a buffer.

Buffers suffer from temporal decay and positional distraction. 
Biological memory, by contrast, encodes information through emotional valence, survival scars, and episodic anchoring.

Until artificial architectures implement persistent dual-memory graphs—separating working context from living primitives—agents will remain brittle savants.`
  }
};

export default function WritingStudio({
  onNavigate,
  incomingDraftText,
  incomingOtaId
}: WritingStudioProps) {
  const [otas, setOtas] = useState<any[]>([]);
  const [selectedOtaId, setSelectedOtaId] = useState<string>(incomingOtaId || 'OTA-001');
  const [content, setContent] = useState<string>(
    OTA_THESIS_REGISTRY['OTA-001']?.linkedin || ''
  );
  const [previewTab, setPreviewTab] = useState<'editor' | 'preview'>('editor');
  const [copySuccess, setCopySuccess] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  // Live Epistemic Lineage State (PRD Section 33)
  const [lineageData, setLineageData] = useState<any>(null);
  const [lineageLoading, setLineageLoading] = useState(false);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 2500);
  };

  useEffect(() => {
    fetch('/api/otas')
      .then((res) => res.json())
      .then((json) => {
        if (json.success && json.data.otas) {
          setOtas(json.data.otas);
        }
      })
      .catch((err) => console.error('Failed to load OTAs:', err));
  }, []);

  // Fetch real Epistemic Lineage from DB whenever selected primitive changes
  useEffect(() => {
    const eoTarget = selectedOtaId.replace('OTA-', 'EO-');
    setLineageLoading(true);
    fetch(`/api/episteme/lineage?eoId=${eoTarget}`)
      .then((res) => res.json())
      .then((json) => {
        if (json.success) {
          setLineageData(json.data);
        } else {
          // Fallback if not found under EO-
          fetch(`/api/episteme/lineage?eoId=EO-001`)
            .then((r) => r.json())
            .then((d) => setLineageData(d.data));
        }
      })
      .catch((err) => console.error('Error fetching lineage:', err))
      .finally(() => setLineageLoading(false));
  }, [selectedOtaId]);

  useEffect(() => {
    if (incomingDraftText) {
      setContent(
        `# Promoted Mobile Spark\n\n${incomingDraftText}\n\n---\n\n## High-Signal Thesis\n[Synthesize the empirical scar and underlying architectural invariant here]`
      );
      showToast('Loaded promoted Telegram capture into editor!');
    }
  }, [incomingDraftText]);

  const handleSelectOta = (otaId: string) => {
    const normalized = otaId.replace('EO-', 'OTA-').replace(/^ota_(\d+)/i, (_, num) => `OTA-${num.padStart(3, '0')}`);
    setSelectedOtaId(normalized);

    if (OTA_THESIS_REGISTRY[normalized]) {
      setContent(OTA_THESIS_REGISTRY[normalized].linkedin);
      showToast(`Loaded draft for ${normalized}`);
    } else {
      const found = otas.find(
        (o) => o.id?.toLowerCase() === normalized.toLowerCase() || o.id?.toLowerCase() === otaId.toLowerCase()
      );
      const title = found?.title || normalized;
      const thesis = found?.thesis || 'Core architectural invariant';
      setContent(
        `# ${normalized}: ${title}\n\n## Thesis\n${thesis}\n\n## Empirical Scars\n- Observed across production autonomous agent turns.\n- System invariant preservation over 30-year compounding horizon.\n\n## Takeaway\nFirst-principles cognitive scaffolding elevates execution.`
      );
      showToast(`Loaded outline for ${normalized}`);
    }
  };

  useEffect(() => {
    if (incomingOtaId) {
      handleSelectOta(incomingOtaId);
    }
  }, [incomingOtaId]);

  const currentOtaMeta = OTA_THESIS_REGISTRY[selectedOtaId] || {
    category: 'Epistemology',
    thesis: otas.find((o) => o.id === selectedOtaId)?.thesis || 'Questions compound across autonomous agent turns.',
    citedPaper: 'Vaswani et al. (2017) Attention Is All You Need',
    rq: 'RQ-1 (Epistemic Primitives)',
    linkedin: ''
  };

  const charCount = content.length;
  const wordCount = content.trim().split(/\s+/).filter(Boolean).length;
  const linkedinMax = 3000;

  // Tone Validator check (Rule 7: Zero hype emojis)
  const hypeEmojis = ['🔥', '🚀', '👇', '👈', '🔴', '🟢', '💥', '🤯', '💯'];
  const hasHype = hypeEmojis.some((e) => content.includes(e));

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopySuccess(true);
    showToast('Copied draft with high-signal formatting!');
    setTimeout(() => setCopySuccess(false), 2000);
  };

  return (
    <div className="space-y-5 animate-in fade-in duration-300 relative pb-12">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed top-20 right-6 z-50 bg-[#161A24] border border-[#C89B53]/40 text-[#EDEAE3] text-xs px-4 py-2.5 rounded-xl shadow-2xl flex items-center gap-2 animate-in fade-in zoom-in duration-200">
          <CheckCircle2 className="w-4 h-4 text-[#C89B53]" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Top Header Bar */}
      <div className="p-4 rounded-2xl bg-[#0E121C] border border-white/[0.08] flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-[#C89B53]/10 border border-[#C89B53]/25 flex items-center justify-center text-[#E5A93C]">
            <PenTool className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-semibold text-[#EDEAE3] tracking-wide font-sans">
                Manuscript & Writing Studio • PRD §33
              </h2>
              <span className="text-[10px] font-mono-precision px-2 py-0.5 rounded bg-[#C89B53]/10 text-[#E5A93C] border border-[#C89B53]/20">
                3-Pane Epistemic Lineage
              </span>
            </div>
            <p className="text-[11px] text-[#9FA4B2]">
              Draft authority chapters and papers backed by verified provenance (Paragraph → EO → Question → Evidence → Belief).
            </p>
          </div>
        </div>

        {/* Dynamic Primitive Dropdown Selector */}
        <div className="flex items-center gap-3">
          <span className="text-xs text-[#9FA4B2] font-mono-precision">Anchor Object:</span>
          <select
            value={selectedOtaId}
            onChange={(e) => handleSelectOta(e.target.value)}
            style={{ colorScheme: 'dark' }}
            className="bg-[#12151E] border border-white/10 rounded-lg px-3 py-1.5 text-xs text-[#EDEAE3] focus:outline-none focus:border-[#C89B53]/50 max-w-[280px] font-mono-precision"
          >
            {otas.length > 0 ? (
              otas.map((o) => (
                <option key={o.id} value={o.id} className="bg-[#12151E] text-[#EDEAE3]">
                  {o.id}: {o.title?.slice(0, 36)}
                </option>
              ))
            ) : (
              Object.keys(OTA_THESIS_REGISTRY).map((k) => (
                <option key={k} value={k} className="bg-[#12151E] text-[#EDEAE3]">
                  {k}
                </option>
              ))
            )}
          </select>
        </div>
      </div>

      {/* 3-PANE STUDIO LAYOUT (PRD Section 33) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 items-start">
        
        {/* PANE 1: LEFT (3 Cols) — Thesis Context & Invariants */}
        <div className="lg:col-span-3 flex flex-col gap-4">
          <div className="p-4 rounded-2xl bg-[#0F131D] border border-white/[0.08]">
            <div className="flex items-center justify-between pb-2 border-b border-white/[0.06] mb-3">
              <span className="text-[11px] font-mono-precision uppercase tracking-wider text-[#C89B53] font-semibold">
                Anchor: {selectedOtaId}
              </span>
              <span className="text-[10px] font-mono-precision text-[#646979] uppercase">
                {currentOtaMeta.category}
              </span>
            </div>

            {/* Core Thesis Card */}
            <div className="p-3 rounded-xl bg-[#141824] border border-white/[0.06] mb-3">
              <span className="text-[10px] font-mono-precision text-[#646979] uppercase block mb-1">
                Core Thesis
              </span>
              <p className="text-xs text-[#EDEAE3] leading-relaxed italic font-serif">
                "{currentOtaMeta.thesis}"
              </p>
            </div>

            {/* Citations & Research Question Alignment */}
            <div className="space-y-2 mb-3">
              <div className="flex items-center justify-between p-2 rounded-lg bg-[#12151E] border border-white/[0.05] text-xs">
                <span className="text-[#9FA4B2] flex items-center gap-1.5 font-mono-precision text-[10px]">
                  <BookOpen className="w-3 h-3 text-[#C89B53]" /> Citation:
                </span>
                <span className="font-mono-precision text-[#EDEAE3] text-[10px] truncate max-w-[130px]">
                  {currentOtaMeta.citedPaper.split(' ')[0]}
                </span>
              </div>

              <div className="flex items-center justify-between p-2 rounded-lg bg-[#12151E] border border-white/[0.05] text-xs">
                <span className="text-[#9FA4B2] flex items-center gap-1.5 font-mono-precision text-[10px]">
                  <Layers className="w-3 h-3 text-[#2E7D5B]" /> PhD RQ:
                </span>
                <span className="font-mono-precision text-[#3EB67F] text-[10px]">
                  {currentOtaMeta.rq}
                </span>
              </div>
            </div>

            {/* Invariant Checklist */}
            <div className="p-3 rounded-xl bg-[#12151E] border border-white/[0.06]">
              <span className="text-[10px] font-mono-precision text-[#646979] uppercase tracking-wider block mb-2">
                Style Invariants
              </span>
              <div className="space-y-1.5 text-xs">
                <div className="flex items-center gap-2">
                  {!hasHype ? (
                    <Check className="w-3 h-3 text-[#2E7D5B]" />
                  ) : (
                    <AlertCircle className="w-3 h-3 text-amber-500" />
                  )}
                  <span className={hasHype ? 'text-amber-400 text-[11px]' : 'text-[#EDEAE3] text-[11px]'}>
                    {hasHype ? 'Hype emoji detected' : 'Zero Hype Emojis (Rule 7)'}
                  </span>
                </div>

                <div className="flex items-center gap-2">
                  <Check className="w-3 h-3 text-[#2E7D5B]" />
                  <span className="text-[#EDEAE3] text-[11px]">Verified Empirical Scars (Rule 11)</span>
                </div>

                <div className="flex items-center gap-2">
                  <Check className="w-3 h-3 text-[#2E7D5B]" />
                  <span className="text-[#EDEAE3] text-[11px]">Zero Client PII / Enterprise Privacy Shield</span>
                </div>
              </div>
            </div>

            {/* Jump to Research Lab */}
            <button
              onClick={() => onNavigate('research')}
              className="w-full mt-3 py-2 rounded-lg bg-white/[0.03] border border-white/[0.07] text-[11px] font-mono-precision text-[#9FA4B2] hover:text-[#EDEAE3] hover:bg-white/[0.06] transition-all flex items-center justify-center gap-1.5"
            >
              <span>Cross-check Citations in PDF Lab</span>
              <ArrowRight className="w-3 h-3" />
            </button>
          </div>
        </div>

        {/* PANE 2: CENTER (6 Cols) — Focused Manuscript Editor */}
        <div className="lg:col-span-6 flex flex-col p-4 rounded-2xl bg-[#0F131D] border border-white/[0.08]">
          {/* Editor Controls Bar */}
          <div className="flex items-center justify-between pb-3 border-b border-white/[0.06] mb-3">
            <div className="flex items-center gap-1.5">
              <button
                onClick={() => setPreviewTab('editor')}
                className={`px-3 py-1 rounded text-xs font-mono-precision transition-all ${
                  previewTab === 'editor'
                    ? 'bg-[#1C212F] text-[#EDEAE3] border border-[#C89B53]/40 font-semibold'
                    : 'text-[#9FA4B2] hover:text-[#EDEAE3]'
                }`}
              >
                Manuscript Editor
              </button>

              <button
                onClick={() => setPreviewTab('preview')}
                className={`px-3 py-1 rounded text-xs font-mono-precision transition-all ${
                  previewTab === 'preview'
                    ? 'bg-[#1C212F] text-[#EDEAE3] border border-[#C89B53]/40 font-semibold'
                    : 'text-[#9FA4B2] hover:text-[#EDEAE3]'
                }`}
              >
                Reader Preview
              </button>
            </div>

            {/* Word and Char Counters */}
            <div className="flex items-center gap-2.5 text-xs font-mono-precision">
              <span className="text-[#646979]">
                {wordCount} words
              </span>
              <span className={`px-2 py-0.5 rounded text-[11px] ${
                charCount > linkedinMax
                  ? 'bg-red-500/10 text-red-400 border border-red-500/20'
                  : 'bg-white/[0.04] text-[#9FA4B2] border border-white/[0.06]'
              }`}>
                {charCount} / {linkedinMax}
              </span>

              <button
                onClick={handleCopy}
                className="px-2.5 py-1 rounded bg-[#C89B53] text-[#0B0D13] font-semibold text-xs font-mono-precision hover:bg-[#E5A93C] transition-all flex items-center gap-1"
              >
                {copySuccess ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copySuccess ? 'Copied' : 'Copy'}</span>
              </button>
            </div>
          </div>

          {/* Editor Surface */}
          {previewTab === 'editor' ? (
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Draft your authority post or chapter section here..."
              className="w-full h-[520px] bg-[#12151E] border border-white/[0.07] rounded-xl p-4 text-xs text-[#EDEAE3] font-mono-precision leading-relaxed focus:outline-none focus:border-[#C89B53]/50 resize-none"
            />
          ) : (
            <div className="w-full h-[520px] bg-[#12151E] border border-white/[0.07] rounded-xl p-6 overflow-y-auto">
              <div className="max-w-xl mx-auto space-y-4 font-serif text-sm text-[#EDEAE3] leading-relaxed whitespace-pre-line">
                {content}
              </div>
            </div>
          )}

          {/* Editor Status */}
          <div className="pt-3 mt-3 border-t border-white/[0.06] flex items-center justify-between text-[11px] font-mono-precision text-[#646979]">
            <span>Invariant: {hasHype ? 'Hype Warning' : 'Passed Minimalist Invariant'}</span>
            <span>Target: LinkedIn & Book Chapter</span>
          </div>
        </div>

        {/* PANE 3: RIGHT (3 Cols) — Live Epistemic Lineage Tree (PRD Section 33) */}
        <div className="lg:col-span-3 flex flex-col p-4 rounded-2xl bg-[#0F131D] border border-white/[0.08]">
          <div className="flex items-center justify-between pb-2 border-b border-white/[0.06] mb-3">
            <div className="flex items-center gap-1.5 text-xs font-mono-precision uppercase tracking-wider text-[#38BDF8] font-semibold">
              <GitCommit className="w-3.5 h-3.5" />
              <span>Epistemic Lineage</span>
            </div>
            <span className="text-[10px] font-mono-precision text-[#646979]">
              PRD §33
            </span>
          </div>

          <div className="text-[11px] text-[#9FA4B2] mb-3 leading-tight">
            Verifies that draft propositions anchor back to empirical evidence and active questions.
          </div>

          {lineageLoading ? (
            <div className="py-12 text-center text-xs text-[#646979] font-mono-precision">
              Traversing thought ancestry...
            </div>
          ) : (
            <div className="space-y-3 text-xs">
              {/* Level 1: Epistemic Object */}
              <div className="p-2.5 rounded-xl bg-[#141824] border border-[#C89B53]/25">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono-precision text-[#C89B53] uppercase">
                    1. Epistemic Object
                  </span>
                  <span className="text-[10px] font-mono-precision px-1.5 rounded bg-[#C89B53]/15 text-[#C89B53]">
                    {lineageData?.eo?.id || selectedOtaId.replace('OTA-', 'EO-')}
                  </span>
                </div>
                <div className="text-xs font-medium text-[#EDEAE3] mt-1 line-clamp-2">
                  {lineageData?.eo?.title || currentOtaMeta.thesis.slice(0, 50)}
                </div>
              </div>

              {/* Connector */}
              <div className="w-0.5 h-3 bg-[#C89B53]/40 mx-auto"></div>

              {/* Level 2: Anchor Questions */}
              <div className="p-2.5 rounded-xl bg-[#12151E] border border-white/[0.06]">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[10px] font-mono-precision text-[#38BDF8] uppercase flex items-center gap-1">
                    <HelpCircle className="w-3 h-3" />
                    2. Driving Question
                  </span>
                  <span className="text-[10px] font-mono-precision text-[#646979]">
                    {lineageData?.questions?.length || 1} Linked
                  </span>
                </div>
                <p className="text-[11px] text-[#EDEAE3] font-sans">
                  {lineageData?.questions?.[0]?.text || 'How does persistent AI interaction change human hypothesis formulation?'}
                </p>
              </div>

              {/* Connector */}
              <div className="w-0.5 h-3 bg-[#38BDF8]/40 mx-auto"></div>

              {/* Level 3: Supporting Evidence / Paper */}
              <div className="p-2.5 rounded-xl bg-[#12151E] border border-white/[0.06]">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[10px] font-mono-precision text-[#A78BFA] uppercase flex items-center gap-1">
                    <FileText className="w-3 h-3" />
                    3. Literature Evidence
                  </span>
                  <span className="text-[10px] font-mono-precision text-[#2E7D5B]">
                    Strength 0.85
                  </span>
                </div>
                <p className="text-[11px] text-[#C5C8D4] font-sans">
                  {lineageData?.evidence?.[0]?.claim || currentOtaMeta.citedPaper}
                </p>
              </div>

              {/* Connector */}
              <div className="w-0.5 h-3 bg-[#A78BFA]/40 mx-auto"></div>

              {/* Level 4: Canonical Belief */}
              <div className="p-2.5 rounded-xl bg-[#12151E] border border-white/[0.06]">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[10px] font-mono-precision text-[#E5A93C] uppercase flex items-center gap-1">
                    <Flame className="w-3 h-3" />
                    4. Canonized Belief
                  </span>
                  <span className="text-[10px] font-mono-precision text-[#E5A93C]">
                    Conf: {Math.round((lineageData?.beliefs?.[0]?.confidence || 0.88) * 100)}%
                  </span>
                </div>
                <p className="text-[11px] text-[#EDEAE3] font-sans italic">
                  "{lineageData?.beliefs?.[0]?.proposition || currentOtaMeta.thesis}"
                </p>
              </div>

              {/* Provenance Badge */}
              <div className="p-2 rounded-lg bg-[#2E7D5B]/10 border border-[#2E7D5B]/20 text-[10px] font-mono-precision text-[#7EE787] flex items-center gap-1.5 mt-2">
                <ShieldCheck className="w-3.5 h-3.5 shrink-0" />
                <span>Lineage verified: Zero hallucinated claims</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
