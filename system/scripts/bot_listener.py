#!/usr/bin/env python3
"""
My-OS Real-time Telegram Listener Bot (Monthly Stream Log Version)
Runs locally to listen for incoming messages, appends them to inbox/YYYY-MM-mobile-inbox.md,
applies anonymization, and notifies you in chat.
"""

import os
import yaml
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

def load_env_token():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, "..", "config", ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
                    return line.strip().split("=", 1)[1].strip()
    return os.environ.get("TELEGRAM_BOT_TOKEN", "")

# Import save function from sync.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sync import append_thought_to_monthly_log, apply_anonymization, load_config

config, _ = load_config()
anonymize_rules = config.get("anonymization", {}).get("rules", [])
workspace_root = config.get("paths", {}).get("workspace_root", "c:/Users/MONISH/OneDrive/Documents/My-Os")

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 My-OS Brain Bot (@Nirixa_bot) is active!\nSend any thought, voice note, or quote here and it will sync into your monthly inbox log.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or update.message.caption or ""
    if not text and update.message.voice:
        text = "[Voice Note Received] (Saved in Telegram)"
        
    if text:
        cleaned_text = apply_anonymization(text, anonymize_rules)
        saved_path = append_thought_to_monthly_log(cleaned_text, source="telegram-bot", root_path=workspace_root)
        file_name = os.path.basename(saved_path)
        await update.message.reply_text(f"✅ Appended to My-OS Stream!\nLog File: `{file_name}`", parse_mode="Markdown")

def main():
    token = load_env_token()
    if not token:
        print("[Error] No Telegram Bot Token found in system/config/.env!")
        return

    print(f"[Bot] Starting @Nirixa_bot listener...")
    app = ApplicationBuilder().token(token).build()
    
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(MessageHandler(filters.TEXT | filters.VOICE, handle_message))
    
    app.run_polling()

if __name__ == "__main__":
    main()
