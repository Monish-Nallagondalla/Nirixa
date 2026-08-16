# GBrain, GStack & Nirixa OS: Comprehensive Synthesis
### How Nirixa OS Compares, Adopts, and Advances Garry Tan's Open-Source Cognitive Architecture

---

## Executive Summary

Garry Tan (CEO of Y Combinator) introduced **GBrain** (the persistent memory layer) and **GStack** (the opinionated skill-file team) to solve agent amnesia and enable "Personal AGI."

Nirixa OS shares this exact philosophy while taking the architecture further by grounding it in **The Question Project**, **Socratic debate AI**, and **sub-millisecond local SQLite memory**.

---

## Architectural Comparison: GBrain vs Nirixa OS

| Architectural Dimension | Garry Tan's GBrain & GStack | Nirixa OS Architecture |
| :--- | :--- | :--- |
| **Foundational Philosophy** | Personal AGI & Spinoza's Conatus | **The Question Project & Personal AGI** (`OTA-001` to `OTA-015`) |
| **Storage Substrate** | Markdown files + PGLite / Postgres | **Markdown files + SQLite (`nirixa.db`) with FTS5** |
| **Search Engine** | Hybrid BM25 + Vector + Reciprocal Rank Fusion (RRF) | **3-Layer Memory**: FTS5 ($<1\text{ms}$) + 3-Signal Resonance + Associative Graph |
| **Agent Reasoning** | Role-based skills (CEO, Designer, EM, QA) | **Context-Adaptive Sparring**: Socratic debate on ideas, scar extraction on friction |
| **Skill Compilation** | `skillify` protocol | **Automated `skillify.py` & merge-first governance** |
| **IDE Connectivity** | Local MCP Server | **Standard Model Context Protocol (`system/engine/nirixa_mcp_server.py`)** |
| **Mobile Friction Ingestion** | Batch note exports & manual diarization | **Real-Time Telegram Long-Polling + 8s Burst Debouncer** |
| **Privacy Model** | Local repo or hosted `gbrain.io` | **100% Air-Gapped Local-First Core** with zero data leakage |

---

## What We Adopted & Integrated into Nirixa OS:

1. **The `skillify` Protocol (`system/engine/skillify.py`)**:
- At the end of any complex session or task, Nirixa can automatically compile the interaction into an immutable, reusable `.agents/skills/<name>/SKILL.md` file.
2. **Model Context Protocol (MCP) Server (`system/engine/nirixa_mcp_server.py`)**:
- Exposes Nirixa's memory, OTAs, and active milestones via standard JSON-RPC so that any future IDE (Cursor, Windsurf, Claude Code) connects directly without Monish repeating himself.
3. **Knowledge Hygiene & Provenance Standard**:
- Contradiction detection heuristics and hot-memory vs cold-reference pruning.
4. **Fat Skills, Thin Harness**:
- Keeping the harness lightweight while encoding deep taste and domain judgment into clear English Markdown files.
