# Quickstart Guide

[Documentation](../README.md) / [Getting Started](QUICKSTART.md)

**Get Nirixa OS running locally or in the cloud with Telegram connection in under 3 minutes.**

---

## 1. System Requirements

* Python 3.10+
* Git
* Telegram account (for mobile gateway)
* Supported OS: Windows 10/11, macOS, Linux (Ubuntu 22.04+ / Debian)

---

## 2. Installation

### Linux / macOS / WSL2
```bash
# Clone the repository
git clone https://github.com/Monish-Nallagondalla/My-Os.git
cd My-Os

# Create environment configuration
cp system/config/.env.example system/config/.env

# Install dependencies
pip install -r requirements.txt
```

### Windows (PowerShell)
```powershell
# Clone the repository
git clone https://github.com/Monish-Nallagondalla/My-Os.git
cd My-Os

# Create environment configuration
Copy-Item system/config/.env.example system/config/.env

# Install dependencies
pip install -r requirements.txt
```

---

## 3. Connect Telegram Mobile Gateway (2 Minutes)

1. Open Telegram and search for `@BotFather`.
2. Send `/newbot`, follow the prompts to choose a name, and copy the **API Token**.
3. Search for `@userinfobot`, press **Start**, and copy your numerical **Chat ID**.
4. Edit `system/config/.env` and paste your credentials:
   ```env
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   TELEGRAM_CHAT_ID=7172048978
   ```

---

## 4. Start the Background Listener

```bash
python system/scripts/telegram_listener.py
```

Test your setup by sending a message or voice note to your Telegram bot. You will see real-time updates and interactive buttons delivered to your phone.

---

## 5. Next Steps

* [Universal Coding Agent Onboarding](ONBOARDING_PROTOCOL.md) — Set up your personal or company preferences.
* [The 4-Quadrant Personal Compass](../frameworks/PERSONAL_COMPASS.md) — Configure your life domains.
* [Living Case Study: Monish's Daily Blueprint](../guides/MONISH_CASE_STUDY.md) — See real-world usage patterns.
