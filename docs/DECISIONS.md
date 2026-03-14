# Architecture Decisions

This document records important decisions made while building My-OS.

The goal is to remember **why** decisions were made, not just **what** was decided.

---

## ADR-001

### Title

My-OS is a repository, not an application.

### Decision

My-OS is the source of truth for knowledge, thinking, and workflows.

It is built using simple files and Git before any automation or software.

### Reason

- Easy to understand
- Easy to version
- Easy to migrate
- No vendor lock-in
- Future AI models can be swapped without losing knowledge

### Status

Accepted

---

## ADR-002

### Title

AI is a reasoning engine, not the operating system.

### Decision

ChatGPT, Claude, Gemini or any future model may interact with My-OS.

None of them own the knowledge.

The repository remains the permanent source of truth.

### Status

Accepted

---

## ADR-003

### Title

Build manually before automating.

### Decision

Every workflow must first prove its value manually before we automate it.

### Reason

Automation should remove pain, not create complexity.

### Status

Accepted

---

## ADR-004

### Title

Capture only transformations.

### Decision

My-OS is not a diary.

Only information that changes thinking, decisions, or future actions should be stored.

### Status

Accepted