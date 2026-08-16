# Configuration & Environment Reference

[Documentation](../README.md) / [Reference](ARCHITECTURE.md) / [Configuration](CONFIGURATION.md)

**A reference of all environment variables, provider endpoints, and security configurations.**

---

## 1. Environment Variables (`system/config/.env`)

| Variable | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `TELEGRAM_BOT_TOKEN` | Yes | None | Bot authentication token generated from `@BotFather`. |
| `TELEGRAM_CHAT_ID` | Yes | None | Numerical chat ID of the authorized owner (from `@userinfobot`). |
| `TELEGRAM_API_BASE_URL` | No | `https://api.telegram.org` | Telegram API base endpoint (supports local reverse proxies). |
| `HTTPS_PROXY` / `HTTP_PROXY` | No | None | Optional corporate or local proxy URL. |
| `GEMINI_API_KEY` | No | None | Google AI Gemini API key for multimodal analysis and synthesis. |
| `OPENAI_API_KEY` | No | None | OpenAI API key (optional fallback). |
| `ANTHROPIC_API_KEY` | No | None | Anthropic Claude API key (optional fallback). |

---

## 2. Security & Anonymization Invariants

* **Single-User Lock**: The Telegram gateway rejects updates from any `chat_id` other than `TELEGRAM_CHAT_ID`.
* **PII Sanitization**: Before storing any capture to long-term storage or public asset generators, `system/engine/anonymizer.py` replaces proprietary client names, company identifiers, and secrets with abstract architectural tokens.
