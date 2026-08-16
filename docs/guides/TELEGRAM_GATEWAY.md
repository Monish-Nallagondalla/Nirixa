# Telegram Mobile Gateway Guide

[Documentation](../README.md) / [Guides](MONISH_CASE_STUDY.md) / [Telegram Gateway](TELEGRAM_GATEWAY.md)

**A high-reliability, zero-latency mobile bridge enabling voice/text capture, deterministic telemetry dashboards, inline interactive button callbacks, and sleep control.**

---

## Capabilities Overview

```
┌───────────────────────────────┬───────────────────────────────┐
│ Feature                       │ Implementation Standard       │
├───────────────────────────────┼───────────────────────────────┤
│ 🎙️ Voice & Text Ingestion     │ Auto-transcription & anonymize│
│ 📊 Live Hardware Telemetry    │ 200ms in-process fast path    │
│ 🔘 Interactive Inline Buttons │ 1-Click approvals & triggers  │
│ 💤 Remote Laptop Sleep        │ Windows Suspend PowerShell API│
│ 🔄 7-Day Rolling Retention    │ Auto-cleanup of stale messages│
└───────────────────────────────┴───────────────────────────────┘
```

---

## Interactive Inline Commands & Buttons

| Button / Command | Trigger | Action Performed |
| :--- | :--- | :--- |
| `[ System Status ]` | Callback `status_0` | Dispatches live CPU, RAM, Disk, DB captures & background task count. |
| `[ Check Reminders ]` | Callback `remind_0` | Queries pending reminders from SQLite and returns formatted checklist. |
| `[ Put Laptop to Sleep ]` | Callback `sys_sleep` | Invokes `SetSuspendState` to put the host Windows machine to sleep. |
| `[ Auto-Compile Assets ]` | Callback `pub_0` | Compiles weekly scars into LinkedIn PDF carousels. |

---

## Architecture & Singleton Process Lock

To eliminate race conditions, `system/scripts/telegram_listener.py` enforces a strict PID lock at `system/data/listener.pid`. If a new listener is started, it automatically terminates any stale background processes, ensuring single-instance message delivery.

```bash
# Start the listener
python system/scripts/telegram_listener.py
```
