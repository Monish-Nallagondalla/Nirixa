# CLI Playbook & Command Reference

[Documentation](../README.md) / [Reference](ARCHITECTURE.md) / [CLI Playbook](CLI_PLAYBOOK.md)

**A reference of all command-line scripts, background daemons, evaluators, and maintenance routines.**

---

## 1. Core Daemon & Listener Commands

```bash
# Start the real-time background Telegram listener (PID singleton guarded)
python system/scripts/telegram_listener.py

# Dispatch live system hardware and database status dashboard to Telegram
python system/scripts/send_status.py

# Synchronize mobile inbox captures and run 7-day rolling chat cleanup
python system/scripts/sync.py
```

---

## 2. Evaluation & Self-Evolution Suite

```bash
# Run deterministic system unit test and evaluation suite
python system/engine/evals/run_system_evals.py

# Run self-evolution engine and audit feedback ratio (+1 vs -1)
python system/engine/evolver.py

# Run privacy anonymization filter test
python system/engine/anonymizer.py
```

---

## 3. Publisher & Compounding Scripts

```bash
# Generate LinkedIn multi-slide visual PDF document and 280-char X thread
python system/engine/publisher_core.py

# Send interactive multi-choice decision prompts to Telegram
python scratch/send_options.py
```
