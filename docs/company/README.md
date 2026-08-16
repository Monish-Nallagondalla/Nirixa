# Company & Team Living Operating System

> **The Invariant**: Company Notion wikis and documentation hubs turn into stale graveyards because updating docs is separated from daily engineering friction. Nirixa OS turns team communication into a **self-updating living engineering playbook**.

---

## 🏛️ How Companies & Teams Use Nirixa OS

```mermaid
graph TD
    Devs["👥 Engineers & Product Managers"] -->|"Post-Mortem / Standup / RFC"| Gateway["📱 Slack / Telegram / Terminal Bridge"]
    Gateway --> Ingest["⚡ Nirixa Ingestion & Anonymization Engine"]
    Ingest --> DB[("💾 Team SQLite Knowledge Graph")]
    DB --> LivingWiki["📚 Living Company Playbook<br/>(Architecture, Scars, Standards)"]
    LivingWiki --> Standups["🤖 Automated Async Standups & Blocker Radar"]
    LivingWiki --> Onboarding["🚀 Instant Day-1 New Engineer Onboarding"]
```

---

## 🛠️ The 3 Core Company Modules

### 1. [Living Engineering Playbook](ENGINEERING_PLAYBOOK.md)
* Architectural standards, PR review protocols, API design conventions, and deployment checklists that update as lessons are learned.

### 2. [Post-Mortem Scars Vault](POST_MORTEMS_AND_SCARS.md)
* Incident root cause analyses, outages, and production bugs transformed into living algorithmic guardrails.

### 3. Automated Team Standup & Blocker Radar
* Daily async friction sync: Engineers log 1-sentence blockers; AI groups common dependencies and alerts the Tech Lead before standup.

---

## 🚀 Setting Up for Your Team
1. Initialize in team mode:
   ```text
   "Configure Nirixa OS for Company Living Wiki mode."
   ```
2. Connect your team's Slack or Telegram group channel.
3. Invite engineers to log post-mortems and architecture RFCs directly into the stream.
