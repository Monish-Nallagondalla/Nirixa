'use client';

import React, { useState, useEffect } from 'react';
import { BookOpen, FileText, Bookmark, Sparkles, ChevronRight, Plus, Check, Link2, ExternalLink } from 'lucide-react';

export default function PdfLab({ onNavigate }: { onNavigate: (tab: any) => void }) {
  const [papers, setPapers] = useState<any[]>([]);
  const [annotations, setAnnotations] = useState<any[]>([]);
  const [selectedPaper, setSelectedPaper] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selectedText, setSelectedText] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'paper' | 'annotations'>('paper');

  useEffect(() => {
    fetch('/api/papers')
      .then((res) => res.json())
      .then((json) => {
        if (json.success) {
          setPapers(json.data.papers);
          setAnnotations(json.data.annotations);
          if (json.data.papers.length > 0) {
            setSelectedPaper(json.data.papers[0]);
          }
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load papers:', err);
        setLoading(false);
      });
  }, []);

  const handleAnchorToOta = async (otaId: string) => {
    if (!selectedText) return;

    try {
      const res = await fetch('/api/papers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'add_annotation',
          paperId: selectedPaper?.id || 'paper-licklider-1960',
          pageNumber: 4,
          highlightedText: selectedText,
          note: `Anchored to ${otaId}`,
          annotationType: 'ota_anchor',
          linkedOtaId: otaId
        })
      });
      const json = await res.json();
      if (json.success) {
        setAnnotations([
          {
            id: json.id,
            paper_id: selectedPaper?.id,
            page_number: 4,
            highlighted_text: selectedText,
            note: `Anchored to ${otaId}`,
            annotation_type: 'ota_anchor',
            linked_ota_id: otaId,
            created_at: new Date().toISOString()
          },
          ...annotations
        ]);
        setSelectedText('');
        alert(`Successfully anchored highlight to ${otaId}! Persisted in SQLite.`);
      }
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      {/* Top Paper Header Bar */}
      <div className="glass-panel p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-violet-500/10 border border-violet-500/25 flex items-center justify-center">
            <BookOpen className="w-4 h-4 text-violet-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-semibold text-white">In-Situ Research Lab & PDF Annotator</h2>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-violet-500/10 text-violet-400 border border-violet-500/20">
                PhD RQ-1 to RQ-8 Literature Matrix
              </span>
            </div>
            <p className="text-[11px] text-slate-400">Read academic papers, anchor highlights directly to OTAs, and discover cross-paper gaps</p>
          </div>
        </div>

        {/* Paper Selector Dropdown */}
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400">Active Paper:</span>
          <select
            value={selectedPaper?.id || ''}
            onChange={(e) => {
              const found = papers.find(p => p.id === e.target.value);
              if (found) setSelectedPaper(found);
            }}
            className="bg-white/5 border border-white/10 rounded-xl px-3 py-1.5 text-xs text-white focus:outline-none focus:border-cyan-400"
          >
            {papers.map((p) => (
              <option key={p.id} value={p.id} className="bg-slate-900 text-white">
                {p.title} ({p.year})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Main Split-Screen Workspace */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* LEFT PANE (7 Cols): The Academic Paper Viewer */}
        <div className="lg:col-span-7 glass-panel p-8 bg-black/60 border border-white/5 relative">
          <div className="flex items-center justify-between pb-4 mb-6 border-b border-white/5">
            <div>
              <div className="text-[10px] font-mono text-cyan-400 uppercase tracking-wider mb-1">
                {selectedPaper?.venue || 'IRE Transactions on Human Factors in Electronics'} • {selectedPaper?.year || 1960}
              </div>
              <h1 className="text-xl font-bold text-white tracking-tight">
                {selectedPaper?.title || 'Man-Computer Symbiosis'}
              </h1>
              <div className="text-xs text-slate-400 mt-1">
                Author: <span className="text-slate-200">{selectedPaper?.authors || 'J. C. R. Licklider'}</span>
              </div>
            </div>

            <span className="text-xs font-mono px-2.5 py-1 rounded-lg bg-white/5 border border-white/5 text-slate-400">
              Page 4 of {selectedPaper?.total_pages || 8}
            </span>
          </div>

          {/* 2-Column Academic Paper Typography */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-[13px] text-slate-300 leading-relaxed font-serif">
            <div>
              <p className="mb-4">
                <strong>Abstract</strong> — Man-computer symbiosis is an expected development in cooperative interaction between men and electronic computers. It involves very close coupling among human and electronic members of the partnership.
              </p>
              <p className="mb-4">
                The main aims are: 1) to let computers facilitate formulatory thinking as they now facilitate the solution of formulated problems, and 2) to enable men and computers to cooperate in making decisions and controlling complex situations without inflexible dependence on predetermined programs.
              </p>
              <p>
                In the anticipated symbiotic partnership, men will set the goals, formulate the hypotheses, determine the criteria, and perform the evaluations. Computing machines will do the routinizable work that must be done to prepare the way for insights and decisions in technical and scientific thinking.
              </p>
            </div>

            <div>
              <div className="p-3.5 rounded-xl bg-cyan-950/20 border border-cyan-500/30 mb-4">
                <div className="text-[10px] font-mono text-cyan-400 uppercase tracking-wider mb-1 flex items-center justify-between">
                  <span>ANCHORED TO OTA-014</span>
                  <span>PAGE 4</span>
                </div>
                <p className="text-xs italic text-cyan-200">
                  "The hope is that, in not too many years, human brains and computing machines will be{' '}
                  <span className="bg-cyan-500/30 text-white px-1 rounded font-medium">
                    coupled together very tightly
                  </span>
                  , and that the resulting partnership will think as no human brain has ever thought."
                </p>
              </div>

              <p className="mb-4">
                Preliminary analyses indicate that the symbiotic partnership will perform intellectually much more effectively than alone. Machines will serve as extensions in information-processing capacity and speed.
              </p>

              <div
                className="p-3 rounded-lg border border-dashed border-white/10 text-xs text-slate-400 cursor-pointer hover:border-cyan-400/40 hover:text-slate-200 transition-all"
                onClick={() => setSelectedText('Partnership will think as no human brain has ever thought, altering the cognitive trajectory.')}
              >
                + Click to select excerpt for anchoring...
              </div>
            </div>
          </div>

          {/* Floating Context Action Pill (Reflect / Chronicle Awwwards SOTD Style) */}
          {selectedText && (
            <div className="mt-6 p-3 rounded-xl bg-slate-900/90 border border-cyan-500/40 shadow-2xl flex items-center justify-between gap-3 animate-in fade-in slide-in-from-bottom-2">
              <span className="text-xs text-slate-200 line-clamp-1 italic">
                "{selectedText}"
              </span>

              <div className="flex items-center gap-2 shrink-0">
                <button
                  onClick={() => handleAnchorToOta('OTA-014')}
                  className="px-3 py-1 rounded-lg bg-cyan-500 text-black text-xs font-semibold hover:bg-cyan-400 transition-all flex items-center gap-1.5 shadow-[0_0_15px_rgba(56,189,248,0.4)]"
                >
                  <Sparkles className="w-3 h-3" />
                  Anchor to OTA-014
                </button>
                <button
                  onClick={() => handleAnchorToOta('OTA-010')}
                  className="px-3 py-1 rounded-lg bg-white/10 text-white text-xs font-medium hover:bg-white/15 transition-all"
                >
                  Anchor to OTA-010
                </button>
              </div>
            </div>
          )}
        </div>

        {/* RIGHT PANE (5 Cols): Anchored Research Notes & Synthesis Matrix */}
        <div className="lg:col-span-5 flex flex-col gap-6">
          <div className="glass-panel p-6">
            <div className="flex items-center justify-between pb-3 mb-4 border-b border-white/5">
              <span className="text-xs font-mono uppercase tracking-wider text-slate-400 flex items-center gap-2">
                <Bookmark className="w-3.5 h-3.5 text-cyan-400" />
                Anchored Paper Annotations ({annotations.length})
              </span>
              <span className="text-[10px] font-mono text-cyan-400">Persisted in SQLite</span>
            </div>

            <div className="space-y-3 max-h-[500px] overflow-y-auto pr-1">
              {annotations.map((a: any) => (
                <div key={a.id} className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 hover:border-white/10 transition-all">
                  <div className="flex items-center justify-between text-[10px] font-mono mb-1.5">
                    <span className="px-2 py-0.5 rounded bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 font-semibold">
                      {a.linked_ota_id || 'OTA-014'}
                    </span>
                    <span className="text-slate-500">Page {a.page_number}</span>
                  </div>

                  <p className="text-xs text-slate-200 mb-2 italic">
                    "{a.highlighted_text}"
                  </p>

                  <div className="text-[11px] text-slate-400 pt-2 border-t border-white/5 flex items-center justify-between">
                    <span>{a.note}</span>
                    <span className="text-slate-500 font-mono text-[9px]">Just now</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Cross-Paper Gap Suggestion Box */}
          <div className="glass-panel p-6 bg-gradient-to-br from-violet-950/20 to-indigo-950/20 border border-violet-500/20">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="w-4 h-4 text-violet-400" />
              <h3 className="text-xs font-semibold text-white uppercase tracking-wider font-mono">
                Cross-Paper Synapse Matrix
              </h3>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed mb-4">
              Licklider (1960) emphasizes <em>symbiotic coupling</em>, while Engelbart (1962) focuses on <em>artifact-mediated augmentation</em>. Your PhD RQ-2 bridges this exact theoretical gap.
            </p>

            <button
              onClick={() => onNavigate('writing')}
              className="w-full py-2 rounded-xl bg-violet-500/20 border border-violet-500/30 text-xs font-medium text-violet-300 hover:bg-violet-500/30 transition-all flex items-center justify-center gap-2"
            >
              Draft Synthesis Essay in Studio →
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
