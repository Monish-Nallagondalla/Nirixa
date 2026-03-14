---
name: daily-signoff
description: Triggered when the user is signing off for the day. Prompts for a status update, logs completed tasks, and automatically pushes pending items to Telegram for async review.
---
# Daily Sign-Off Protocol (`daily-signoff`)

Use this skill whenever the user says they are leaving, signing off, "I am off", "I am going", or wrapping up for the day.

## Protocol Steps
1. **Intercept the Goodbye**: Acknowledge that the day is wrapping up.
2. **Elicit Status**: Ask the user explicitly:
   - "Before you go, what exactly did we complete from today's discussion?"
   - "What is pending or blocking us that we need to tackle tomorrow?"
3. **Capture & Stage**: Once the user provides the pending tasks, stage them in the active task tracker (`task.md`).
4. **Automated Telegram Push**: Ask the user to confirm, and then run the following command to push a formatted summary to their phone:
   `python system/scripts/telegram_push.py "🌙 *My-OS Daily Sign-Off*\n\n✅ *Completed:*\n[Insert Completed]\n\n⏳ *Pending:*\n[Insert Pending]"`
