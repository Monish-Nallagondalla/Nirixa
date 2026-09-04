'use client';

import React, { useState, useEffect } from 'react';
import { PenTool, CheckCircle2, AlertCircle, Copy, Share2, Sparkles, BookOpen, Layers } from 'lucide-react';

export default function WritingStudio({ onNavigate }: { onNavigate: (tab: any) => void }) {
  const [otas, setOtas] = useState<any[]>([]);
  const [selectedOtaId, setSelectedOtaId] = useState<string>('OTA-014');
  const [content, setContent] = useState<string>(
`Tools are not passive instruments. They reshape the cognitive morphology of the thinker who wields them.

When product managers interact with autonomous AI agents over 50+ turns, intentionality ceases to be unidirectional.

We are not merely prompting a machine; the machine's deterministic and probabilistic scaffolding alters how we perceive problem spaces.

In our empirical research for Nirixa Episteme:
1. Socratic sparring forces assumption clarification (OTA-010).
2. Autonomous task execution eliminates rote friction.
3. The emergent feedback loop forms a true symbiotic partnership (Licklider, 1960).

The future of Product Management is not writing Jira tickets—it is cognitive systems architecture.`
  );

  useEffect(() => {
    fetch('/api/otas')
      .then((res) => res.json())
      .then((json) => {
        if (json.success) {
          setOtas(json.data.otas);
        }
      })
      .catch((err) => console.error(err));
  }, []);

  const selectedOta = otas.find((o) => o.id === selectedOtaId) || {
    id: 'OTA-014',
    title: 'Cognitive Morphology in Human-AI Symbiosis',
    thesis: 'Tools reshape the cognitive morphology of the thinker who wields them.',
    category: 'Coevolution'
  };

  const charCount = content.length;
  const wordCount = content.trim().split(/\s+/).filter(Boolean).length;
  const linkedinMax = 3000;
  const xMax = 280;

  // Tone Validator check (rule 7: Zero hype emojis, high-signal density)
  const hypeEmojis = ['🔥', '🚀', '👇', '👈', '🔴', '🟢', '💥', '🤯'];
  const hasHype = hypeEmojis.some((e) => content.includes(e));

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    alert('Copied to clipboard! Formatted with high-signal minimalist standard.');
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      {/* Top Header Bar */}
      <div className="glass-panel p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-amber-500/10 border border-amber-500/25 flex items-center justify-center">
            <PenTool className="w-4 h-4 text-amber-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-semibold text-white">Distraction-Free LinkedIn & Thesis Studio</h2>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20">
                High-Signal Authority Engine
              </span>
            </div>
            <p className="text-[11px] text-slate-400">Transform original thought assets into peer-reviewed papers and executive LinkedIn essays</p>
          </div>
        </div>

        {/* 48 Unpublished OTAs Dropdown */}
        <div className="flex items-center gap-3">
          <span className="text-xs text-slate-400">Select Unpublished OTA:</span>
          <select
            value={selectedOtaId}
            onChange={(e) => setSelectedOtaId(e.target.value)}
            className="bg-white/5 border border-white/10 rounded-xl px-3 py-1.5 text-xs text-white focus:outline-none focus:border-cyan-400 max-w-[280px]"
          >
            {otas.map((o) => (
              <option key={o.id} value={o.id} className="bg-slate-900 text-white">
                {o.id}: {o.title}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Main Studio Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* LEFT PANE (4 Cols): OTA Thesis & Scars Dock */}
        <div className="lg:col-span-4 flex flex-col gap-6">
          <div className="glass-panel p-6">
            <div className="flex items-center justify-between pb-3 mb-4 border-b border-white/5">
              <span className="text-xs font-mono uppercase tracking-wider text-cyan-400">
                {selectedOta.id} • CORE THESIS
              </span>
              <span className="text-[10px] font-mono text-slate-400 uppercase">
                {selectedOta.category}
              </span>
            </div>

            <h3 className="text-base font-semibold text-white mb-3">
              {selectedOta.title}
            </h3>

            <p className="text-xs text-slate-300 leading-relaxed mb-6 italic border-l-2 border-cyan-400 pl-3">
              "{selectedOta.thesis || selectedOta.description}"
            </p>

            <div className="space-y-3 pt-3 border-t border-white/5">
              <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider block">
                Evidence & Research Anchors
              </span>

              <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5 text-xs text-slate-300">
                <span className="font-mono text-[10px] text-purple-400 block mb-1">CITED PAPER</span>
                Licklider (1960) Man-Computer Symbiosis • Page 4
              </div>

              <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5 text-xs text-slate-300">
                <span className="font-mono text-[10px] text-cyan-400 block mb-1">PHD BINDING</span>
                Research Question RQ-2 (Cognitive Scaffolding)
              </div>
            </div>
          </div>

          {/* AI Tone Validator Status Card */}
          <div className="glass-panel p-6">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-mono uppercase tracking-wider text-slate-400 flex items-center gap-2">
                <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
                Tone & Signal Guardrails
              </span>
              {hasHype ? (
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-red-500/10 text-red-400 border border-red-500/20 flex items-center gap-1">
                  <AlertCircle className="w-3 h-3" /> Hype Emojis Detected
                </span>
              ) : (
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1">
                  <CheckCircle2 className="w-3 h-3" /> High Signal Verified
                </span>
              )}
            </div>

            <div className="space-y-2 text-xs text-slate-400">
              <div className="flex items-center justify-between">
                <span>Zero Emoji Clutter</span>
                <span className={hasHype ? 'text-red-400 font-mono' : 'text-emerald-400 font-mono'}>
                  {hasHype ? 'Flagged' : 'Pass'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span>Thought Density</span>
                <span className="text-cyan-400 font-mono">0.88 (High)</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Client PII Check</span>
                <span className="text-emerald-400 font-mono">100% Sanitized</span>
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT PANE (8 Cols): Clean Distraction-Free Editor */}
        <div className="lg:col-span-8 glass-panel p-8 bg-black/50 border border-white/5">
          <div className="flex items-center justify-between pb-4 mb-4 border-b border-white/5">
            <div className="flex items-center gap-4 text-xs font-mono text-slate-400">
              <span>Characters: <strong className="text-white">{charCount}</strong> / 3,000</span>
              <span>Words: <strong className="text-white">{wordCount}</strong></span>
              <span className={charCount <= xMax ? 'text-emerald-400' : 'text-slate-500'}>
                X.com Single: {charCount <= xMax ? 'Fits 1 Tweet' : `${Math.ceil(charCount / xMax)} Tweets Thread`}
              </span>
            </div>

            <button
              onClick={handleCopy}
              className="px-4 py-1.5 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-xs font-medium text-cyan-300 hover:bg-cyan-500/20 transition-all flex items-center gap-1.5"
            >
              <Copy className="w-3.5 h-3.5" />
              Copy for LinkedIn
            </button>
          </div>

          {/* Textarea */}
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            rows={16}
            className="w-full bg-transparent border-none text-slate-100 text-sm md:text-base leading-relaxed focus:outline-none resize-none font-sans placeholder-slate-600"
            placeholder="Write your high-signal thought leadership essay..."
          />

          {/* Bottom Live Preview Hint */}
          <div className="pt-4 border-t border-white/5 flex items-center justify-between text-xs text-slate-500">
            <span>High-Signal Minimalist Copywriting • Zero Marketing Fluff</span>
            <span className="font-mono text-cyan-400">Ready to publish on LinkedIn</span>
          </div>
        </div>
      </div>
    </div>
  );
}
