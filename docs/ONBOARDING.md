# Quickstart & Universal Onboarding Guide

> Launch your personalized **Personal Chief of Staff** or **Company Living Wiki** in under **5 minutes** using your coding agent (Antigravity, Cursor, Claude Code, Windsurf).

---

## ⚡ 3 Simple Steps to Get Started

```
1. Open in IDE & Run Setup ───► 2. Connect Telegram ───► 3. Send First Note
(Agent conducts 3-min Q&A)      (2-Minute Free Bot)      (Voice/Text from Phone)
```

---

### Step 1: Open in Your IDE & Run the Agent Interview (2 Minutes)

1. Clone the repository:
   ```bash
   git clone https://github.com/Monish-Nallagondalla/My-Os.git
   cd My-Os
   cp system/config/.env.example system/config/.env
   ```
2. Open the project in your preferred AI editor:
   * **Google Antigravity**: Automatically loads `.agents/skills/user-onboarding/` and rules.
   * **Cursor**: Automatically reads [`.cursorrules`](file:///c:/Users/MONISH/OneDrive/Documents/My-Os/.cursorrules).
   * **Claude Code**: Automatically reads [`CLAUDE.md`](file:///c:/Users/MONISH/OneDrive/Documents/My-Os/CLAUDE.md).
3. Type in chat:
   > *"Set up my OS"* or *"Onboard me"*
4. Your agent will conduct a 3-question interview:
   * **Personal Mode**: Choose between the **4-Quadrant Compass** (Mission, Mastery, Money, Mind) or **3-Horizon Engine** (North Star ➔ Friction ➔ Weekly Top 3).
   * **Company Mode**: Configure your team's **Living Engineering Playbook** and **Post-Mortem Scars Vault**.

---

### Step 2: Connect Telegram Mobile Capture (2 Minutes)

Nirixa OS gives you a private, 24/7 Chief of Staff on Telegram with **zero monthly subscription fees**:

1. **Create your Bot**:
   * Open Telegram and search for `@BotFather`.
   * Send `/newbot`, name your bot (e.g. `MyChiefOfStaff_bot`), and copy the **API Token**.
2. **Get your Chat ID**:
   * Search for `@userinfobot` in Telegram, click Start, and copy your **ID**.
3. **Save in `system/config/.env`**:
   ```env
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRstuVWxYZ
   TELEGRAM_CHAT_ID=123456789
   ```

---

### Step 3: Start the Listener & Send Your First Note (1 Minute)

1. Start the background listener:
   ```bash
   python system/scripts/telegram_listener.py
   ```
2. Open your new bot on your phone and send a 10-second voice note or text:
   > *"Finished our architecture sprint review. Need to add backoff logic to the agent retry handler before Friday."*

3. **What happens automatically**:
   * Your note is securely indexed in your local SQLite memory (`nirixa.db`).
   * The AI automatically classifies it under your chosen framework.
   * You receive an instant interactive status dashboard with 1-click buttons directly on your phone!

---

## 🌿 Your 30-Day Progressive Enlightenment Path
* 🌱 **Day 1**: Instant capture, reminders, and daily briefings.
* 🌿 **Day 7**: Weekly pattern recognition and Socratic sparring sessions.
* 🌳 **Day 30+**: Auto-compiling public assets/playbooks and building custom agent skills.
* 👉 **[Read the Full Progressive Enlightenment Model](file:///c:/Users/MONISH/OneDrive/Documents/My-Os/docs/PROGRESSIVE_ENLIGHTENMENT.md)**
