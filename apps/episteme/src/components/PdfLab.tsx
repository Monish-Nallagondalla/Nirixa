'use client';

import React, { useState, useEffect } from 'react';
import { BookOpen, Bookmark, CheckCircle2, ChevronRight, Plus, ExternalLink, Zap } from 'lucide-react';

const REAL_ATTENTION_EXCERPTS = [
  {
    label: 'Scaled Dot-Product',
    quote: 'Attention(Q, K, V) = softmax(QK^T / sqrt(d_k))V'
  },
  {
    label: 'Multi-Head Attention',
    quote: 'Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions.'
  },
  {
    label: 'Sequential Operations',
    quote: 'A self-attention layer connects all positions with a constant number of sequentially executed operations, whereas a recurrent layer requires O(n) sequential operations.'
  },
  {
    label: 'Positional Encoding',
    quote: 'PE(pos, 2i) = sin(pos / 10000^(2i/d_model)) — enabling the model to easily learn to attend by relative positions.'
  }
];

export default function PdfLab({ onNavigate }: { onNavigate: (tab: any) => void }) {
  const [papers, setPapers] = useState<any[]>([]);
  const [annotations, setAnnotations] = useState<any[]>([]);
  const [selectedPaper, setSelectedPaper] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeNoteText, setActiveNoteText] = useState('');
  const [selectedOtaId, setSelectedOtaId] = useState('OTA-001');
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 2500);
  };

  useEffect(() => {
    fetch('/api/papers')
      .then((res) => res.json())
      .then((json) => {
        if (json.success) {
          setPapers(json.data.papers);
          setAnnotations(json.data.annotations);
          if (json.data.papers.length > 0) {
            const attentionPaper = json.data.papers.find((p: any) => p.id === 'paper-vaswani-2017');
            setSelectedPaper(attentionPaper || json.data.papers[0]);
          }
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load papers:', err);
        setLoading(false);
      });
  }, []);

  const handleSaveAnnotation = async () => {
    if (!activeNoteText.trim()) return;

    try {
      const res = await fetch('/api/papers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'add_annotation',
          paperId: selectedPaper?.id || 'paper-vaswani-2017',
          pageNumber: 3,
          highlightedText: activeNoteText,
          note: `Anchored to ${selectedOtaId}`,
          annotationType: 'ota_anchor',
          linkedOtaId: selectedOtaId
        })
      });
      const json = await res.json();
      if (json.success) {
        setAnnotations([
          {
            id: json.id || Date.now(),
            paper_id: selectedPaper?.id,
            page_number: 3,
            highlighted_text: activeNoteText,
            note: `Anchored to ${selectedOtaId}`,
            annotation_type: 'ota_anchor',
            linked_ota_id: selectedOtaId,
            created_at: new Date().toISOString()
          },
          ...annotations
        ]);
        setActiveNoteText('');
        showToast(`Successfully anchored insight to ${selectedOtaId} in SQLite!`);
      }
    } catch (e) {
      console.error(e);
      showToast('Error persisting annotation');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border border-[#C89B53] border-t-transparent rounded-full animate-spin"></div>
          <span className="text-xs font-mono-precision text-[#9FA4B2] tracking-wider uppercase">Loading Academic PDF Lab...</span>
        </div>
      </div>
    );
  }

  const isVaswani = selectedPaper?.id === 'paper-vaswani-2017';

  return (
    <div className="space-y-5 animate-in fade-in duration-300 relative pb-12">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed top-20 right-6 z-50 bg-[#161A24] border border-[#C89B53]/40 text-[#EDEAE3] text-xs px-4 py-2.5 rounded-xl shadow-2xl flex items-center gap-2 animate-in fade-in zoom-in duration-200">
          <CheckCircle2 className="w-4 h-4 text-[#C89B53]" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Top Paper Header Bar */}
      <div className="bento-card p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-[#C89B53]/10 border border-[#C89B53]/25 flex items-center justify-center text-[#E5A93C]">
            <BookOpen className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-semibold text-[#EDEAE3] font-editorial tracking-wide">
                In-Situ Research Lab & PDF Annotator
              </h2>
              <span className="text-[10px] font-mono-precision px-2 py-0.5 rounded bg-[#C89B53]/10 text-[#E5A93C] border border-[#C89B53]/20">
                PhD RQ-1 Literature Anchor
              </span>
            </div>
            <p className="text-[11px] text-[#9FA4B2]">
              Read foundational academic literature, anchor mathematical formalisms to OTAs, and discover theoretical gaps.
            </p>
          </div>
        </div>

        {/* Paper Selector Dropdown */}
        <div className="flex items-center gap-3">
          <span className="text-xs text-[#9FA4B2] font-mono-precision">Select Paper:</span>
          <select
            value={selectedPaper?.id || ''}
            onChange={(e) => {
              const found = papers.find((p) => p.id === e.target.value);
              if (found) {
                setSelectedPaper(found);
                showToast(`Switched paper to: ${found.title}`);
              }
            }}
            style={{ colorScheme: 'dark' }}
            className="bg-[#12151E] border border-white/10 rounded-lg px-3 py-1.5 text-xs text-[#EDEAE3] focus:outline-none focus:border-[#C89B53]/50 max-w-[320px] font-mono-precision"
          >
            {papers.map((p) => (
              <option key={p.id} value={p.id} className="bg-[#12151E] text-[#EDEAE3]">
                {p.title} ({p.year})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Main Split-Screen Workspace */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
        {/* LEFT PANE (8 Cols): The Academic Paper Viewer */}
        <div className="lg:col-span-8 bento-card p-5 relative">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 mb-4 border-b border-white/[0.06] gap-2">
            <div>
              <div className="text-[10px] font-mono-precision text-[#C89B53] uppercase tracking-wider mb-1 flex items-center gap-2">
                <span>{selectedPaper?.venue || 'NeurIPS 2017'} • {selectedPaper?.year || 2017}</span>
                {selectedPaper?.doi && (
                  <span className="text-[#646979]">DOI: {selectedPaper.doi}</span>
                )}
              </div>
              <h1 className="text-lg font-bold text-[#EDEAE3] font-editorial tracking-tight">
                {selectedPaper?.title || 'Attention Is All You Need'}
              </h1>
              <div className="text-xs text-[#9FA4B2] mt-0.5">
                Authors: <span className="text-[#EDEAE3]">{selectedPaper?.authors || 'Ashish Vaswani et al.'}</span>
              </div>
            </div>

            <div className="flex items-center gap-2 shrink-0">
              <span className="text-xs font-mono-precision px-2.5 py-1 rounded-lg bg-white/[0.03] border border-white/[0.06] text-[#9FA4B2]">
                {selectedPaper?.total_pages || 15} Pages
              </span>
              <a
                href={selectedPaper?.file_path || '/papers/attention_is_all_you_need.pdf'}
                target="_blank"
                rel="noreferrer"
                className="p-1.5 rounded-lg bg-white/[0.03] border border-white/[0.08] text-[#9FA4B2] hover:text-[#EDEAE3] transition-colors"
                title="Open PDF in new tab"
              >
                <ExternalLink className="w-4 h-4" />
              </a>
            </div>
          </div>

          {/* Embedded Real PDF Viewer */}
          {selectedPaper?.file_path && selectedPaper.file_path.endsWith('.pdf') ? (
            <div className="w-full rounded-xl overflow-hidden border border-white/[0.08] bg-[#090C12] relative">
              <iframe
                src={selectedPaper.file_path}
                title={selectedPaper.title}
                className="w-full h-[720px] rounded-xl bg-[#0B0E15] border-none"
              />
            </div>
          ) : (
            <div className="p-8 text-center text-[#9FA4B2] text-xs font-mono-precision">
              <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 text-left text-xs leading-relaxed text-[#EDEAE3] font-editorial">
                <h3 className="text-sm font-bold text-[#EDEAE3] mb-2 font-sans">{selectedPaper?.title}</h3>
                <p className="mb-4 text-[#9FA4B2]">{selectedPaper?.abstract}</p>
                <div className="text-[11px] font-mono-precision text-[#C89B53]">
                  Venue: {selectedPaper?.venue} ({selectedPaper?.year}) • RQ-Anchor: {selectedPaper?.phd_rq_id || 'RQ-1'}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* RIGHT PANE (4 Cols): OTA Anchoring & Epistemic Synthesis */}
        <div className="lg:col-span-4 flex flex-col gap-4">
          {/* 1. Fast OTA Anchor Card with One-Click Chips */}
          <div className="bento-card p-5">
            <div className="flex items-center justify-between pb-3 mb-3 border-b border-white/[0.06]">
              <span className="text-xs font-mono-precision uppercase tracking-wider text-[#C89B53] font-semibold flex items-center gap-1.5">
                <Bookmark className="w-3.5 h-3.5" /> Anchor Insight to OTA
              </span>
              <span className="text-[10px] font-mono-precision text-[#646979]">SQLITE PERSISTENT</span>
            </div>

            {/* Quick Excerpt Chips */}
            {isVaswani && (
              <div className="mb-3">
                <label className="text-[10px] font-mono-precision text-[#646979] uppercase tracking-wider block mb-1.5">
                  One-Click Paper Excerpts:
                </label>
                <div className="flex flex-wrap gap-1.5">
                  {REAL_ATTENTION_EXCERPTS.map((chip, idx) => (
                    <button
                      key={idx}
                      onClick={() => {
                        setActiveNoteText(chip.quote);
                        showToast(`Selected "${chip.label}" excerpt!`);
                      }}
                      className="px-2 py-1 rounded bg-white/[0.03] border border-white/[0.08] hover:border-[#C89B53]/40 text-[10px] text-[#9FA4B2] hover:text-[#EDEAE3] transition-colors flex items-center gap-1 font-mono-precision"
                    >
                      <Zap className="w-2.5 h-2.5 text-[#C89B53]" />
                      {chip.label}
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div className="space-y-3">
              <div>
                <label className="text-[11px] text-[#EDEAE3] font-mono-precision block mb-1">Target OTA Primitive:</label>
                <select
                  value={selectedOtaId}
                  onChange={(e) => setSelectedOtaId(e.target.value)}
                  style={{ colorScheme: 'dark' }}
                  className="w-full bg-[#12151E] border border-white/10 rounded-lg px-3 py-1.5 text-xs text-[#EDEAE3] focus:outline-none focus:border-[#C89B53]/50 font-mono-precision"
                >
                  <option value="OTA-001" className="bg-[#12151E] text-[#EDEAE3]">OTA-001: Questions as First-Class Primitives</option>
                  <option value="OTA-044" className="bg-[#12151E] text-[#EDEAE3]">OTA-044: Machine-Input Inversion Paradox</option>
                  <option value="OTA-014" className="bg-[#12151E] text-[#EDEAE3]">OTA-014: Substrate-Neutral Tool Plasticity</option>
                  <option value="OTA-010" className="bg-[#12151E] text-[#EDEAE3]">OTA-010: Adversarial Socratic Sparring</option>
                  <option value="OTA-047" className="bg-[#12151E] text-[#EDEAE3]">OTA-047: Biological Memory Multi-Dimensionality</option>
                </select>
              </div>

              <div>
                <label className="text-[11px] text-[#EDEAE3] font-mono-precision block mb-1">Annotation / Insight Quote:</label>
                <textarea
                  rows={3}
                  value={activeNoteText}
                  onChange={(e) => setActiveNoteText(e.target.value)}
                  placeholder="Click an excerpt chip above or type an architectural insight..."
                  className="w-full bg-[#12151E] border border-white/10 rounded-lg p-3 text-xs text-[#EDEAE3] placeholder-[#646979] focus:outline-none focus:border-[#C89B53]/50 resize-none font-mono-precision"
                />
              </div>

              <button
                onClick={handleSaveAnnotation}
                disabled={!activeNoteText.trim()}
                className="w-full py-2 rounded-lg bg-[#C89B53] text-[#0B0D13] font-semibold text-xs font-mono-precision hover:bg-[#E5A93C] transition-all flex items-center justify-center gap-1.5 disabled:opacity-40 disabled:cursor-not-allowed"
              >
                <Plus className="w-3.5 h-3.5" />
                Anchor to {selectedOtaId}
              </button>
            </div>
          </div>

          {/* 2. Interactive Existing Paper Annotations List */}
          <div className="bento-card p-5">
            <div className="flex items-center justify-between pb-3 mb-3 border-b border-white/[0.06]">
              <span className="text-xs font-mono-precision uppercase tracking-wider text-[#EDEAE3] font-semibold">
                Saved Anchors ({annotations.length})
              </span>
              <span className="text-[10px] font-mono-precision text-[#3EB67F]">PERSISTENT</span>
            </div>

            <div className="space-y-2.5 max-h-[200px] overflow-y-auto pr-1">
              {annotations.map((ann) => (
                <div
                  key={ann.id}
                  onClick={() => showToast(`Anchor details: ${ann.linked_ota_id} • Page ${ann.page_number || 3}`)}
                  className="p-3 rounded-lg bg-[#12151E] border border-white/[0.05] hover:border-[#C89B53]/40 transition-all text-xs cursor-pointer group"
                >
                  <div className="flex items-center justify-between text-[10px] font-mono-precision text-[#C89B53] mb-1">
                    <span className="font-semibold group-hover:text-[#E5A93C]">{ann.linked_ota_id || 'OTA-001'}</span>
                    <span className="text-[#646979]">Page {ann.page_number || 1}</span>
                  </div>
                  <p className="text-[#EDEAE3] leading-snug line-clamp-2 font-editorial italic">
                    "{ann.highlighted_text}"
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* 3. PhD Research Question Theoretical Gap Analysis */}
          <div className="bento-card p-5">
            <div className="flex items-center justify-between pb-3 mb-3 border-b border-white/[0.06]">
              <span className="text-xs font-mono-precision uppercase tracking-wider text-[#C89B53] font-semibold flex items-center gap-1.5">
                Theoretical Gap (RQ-1)
              </span>
              <span className="text-[10px] font-mono-precision text-[#646979]">SYNTHESIS</span>
            </div>

            <div className="p-3 rounded-lg bg-[#12151E] border border-white/[0.06] text-xs text-[#EDEAE3] leading-relaxed font-editorial">
              <strong>Transformer Attention vs Biological Working Memory:</strong> Attention calculates global token weights with $O(n^2)$ matrix dot-products, whereas human cognition exhibits asymmetric intentional pruning and emotional valence gating.
            </div>

            <div className="mt-3 pt-3 border-t border-white/[0.06] flex items-center justify-between text-xs font-mono-precision">
              <span className="text-[11px] text-[#646979]">Ready to draft thesis section?</span>
              <button
                onClick={() => onNavigate('writing')}
                className="text-[#C89B53] hover:text-[#E5A93C] font-semibold flex items-center gap-1 transition-colors text-xs"
              >
                Open Studio <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
