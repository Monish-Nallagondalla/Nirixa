---
name: daily-login
description: Triggered when the user logs back in or says "I am back". Automates context resumption by syncing async Telegram messages and summarizing them.
---
# Daily Login Protocol (`daily-login`)

Use this skill whenever the user returns for a new session, says "I am back", or initiates a new working day.

## Protocol Steps
1. **Automated Sync**: Before asking the user any questions, immediately run the sync script to pull any async thoughts or replies the user sent via Telegram overnight:
   `python system/scripts/sync.py`
2. **Contextualize**: Read the last 20 lines of the current month's inbox file (`inbox/YYYY-MM-mobile-inbox.md`) to see if the user sent any new thoughts, feedback on the pending tasks, or directives while they were away.
3. **Welcome & Handover**: 
   - Welcome the user back.
   - Summarize any new context you found in the inbox file.
   - List the pending tasks from `task.md`.
   - Ask: "Should we tackle these pending tasks first, or do you want to explore the new thoughts you sent overnight?"
