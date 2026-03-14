---
name: mobile-task-delegator
description: Delegates low-friction mobile tasks, ChatGPT sparring prompts, scar extraction requests, and quick decision options to Monish's phone via Telegram when he is away from his desk.
---

# Mobile Task Delegator Skill (`mobile-task-delegator`)

Use this skill whenever Monish is signing off, leaving his desk, or when the system needs to delegate asynchronous micro-tasks to Monish on mobile via Telegram.

## Instructions

1. **Identify Delegation Opportunities**:
   When Monish says "I'm going now", "catch you later", "sync on mobile", or signs off for the day, review the current session state and pending tasks.

2. **Categorize the Mobile Task**:
   Format the mobile notification using one or more of these 4 standard task types:
   - **Type 1: Asynchronous Sparring Prompt**
     Provide a clear thesis + a copy-pasteable prompt formatted specifically for Monish to use in the ChatGPT app on his phone.
   - **Type 2: Authentic Scar Extraction**
     Ask 1 targeted question requesting a 30-second voice note or brief text on a real-world experience, failure, or result.
   - **Type 3: Asset Finalization & Approval**
     Send a ready-to-review post or content angle with inline response options.
   - **Type 4: Strategic Choice Alignment**
     Present 2–3 crisp options for system architecture or strategy choices.

3. **Format Standard**:
   - Keep tasks low-friction (< 2 minutes required from Monish on phone).
   - Enforce Naval & Aviral copywriting standards (zero emoji clutter, zero hype marketing).
   - Automatically push the task via `telegram_push.py`.
