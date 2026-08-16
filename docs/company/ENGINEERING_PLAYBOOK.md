# Living Engineering Playbook (Template)

> **Objective**: A high-signal, deterministic guide to software architecture, code review standards, and autonomous AI system design for the team.

---

## 1. System Design & Architectural Invariants
* **DB-First State Management**: All critical application state must reside in ACID-compliant relational storage before async queues or vector operations.
* **Deterministic Circuit Breakers**: Any autonomous agent or background loop must have a maximum execution budget (time/tokens) and human-in-the-loop escalation gates.
* **Zero PII Exposure**: Client and company proprietary identifiers must be strictly anonymized at the ingestion layer.

---

## 2. Code Review & PR Standards
* **High Signal PR Descriptions**: Include Root Context, Before/After Diff, Risk Tier (Low/Med/High), and Exact Verification Command.
* **No Zombie Dependencies**: Never introduce a heavy external package for logic that can be solved in <30 lines of standard library Python/TypeScript.
* **Deterministic Unit Tests**: All business logic fast-paths must pass reproducible test suites with 0 network dependency.

---

## 3. Incident Escalation Protocol
* **P0 / Blocker**: Immediate notification to on-call Tech Lead via Telegram/Slack gateway.
* **P1 / High**: Logged in `POST_MORTEMS_AND_SCARS.md` within 24 hours of resolution.
* **P2 / Normal**: Synced in weekly asynchronous sprint review.
