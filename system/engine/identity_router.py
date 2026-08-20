#!/usr/bin/env python3
"""
Nirixa OS Engine - Identity & Context Router
Envelope Pattern for Multi-Member Multi-Bot Isolation & Persona Resolution.
"""

import os
import json
from dataclasses import dataclass, asdict
from system.engine import db

@dataclass
class MessageEnvelope:
    update_id: str
    chat_id: str
    telegram_id: str
    sender_name: str
    bot_origin: str          # 'monish_dev' | 'companion' | 'group'
    raw_text: str
    anonymized_text: str
    active_persona: str      # 'chief_of_staff_dev' | 'household_companion'
    privacy_scope: str       # 'private_monish' | 'private_partner' | 'shared'
    owner_id: str            # 'monish' | 'partner' | 'shared'

def resolve_identity_and_scope(telegram_id, sender_name, bot_origin="monish_dev", raw_text=""):
    """
    Resolves member identity, selects persona, and determines privacy scope.
    """
    str_tg_id = str(telegram_id)
    member = db.get_member(str_tg_id)

    # Default fallback mapping
    if not member:
        # Check if this matches primary owner chat ID from environment
        env_chat_id = os.environ.get("TELEGRAM_CHAT_ID", "7172048978")
        if str_tg_id == env_chat_id or bot_origin == "monish_dev":
            owner_id = "monish"
            persona = "chief_of_staff_dev"
            scope = "private_monish"
            db.save_member("monish", sender_name or "Monish", str_tg_id, role="admin", relationship_type="primary_owner", persona=persona, privacy_default="private")
        else:
            owner_id = "partner"
            persona = "household_companion"
            scope = "private_partner"
            db.save_member(f"partner_{str_tg_id}", sender_name or "Partner", str_tg_id, role="member", relationship_type="spouse", persona=persona, privacy_default="private")
    else:
        owner_id = member.get("member_key", "monish")
        persona = member.get("persona", "chief_of_staff")
        scope = f"private_{owner_id}"

    # Handle explicit shared triggers or group context
    text_lower = raw_text.lower()
    if bot_origin == "group" or "#shared" in text_lower or "[shared]" in text_lower:
        scope = "shared"
        owner_id = "shared"

    return {
        "owner_id": owner_id,
        "persona": persona,
        "privacy_scope": scope
    }

def create_envelope(update_id, chat_id, telegram_id, sender_name, raw_text, anonymized_text, bot_origin="monish_dev"):
    resolved = resolve_identity_and_scope(telegram_id, sender_name, bot_origin, raw_text)
    return MessageEnvelope(
        update_id=str(update_id),
        chat_id=str(chat_id),
        telegram_id=str(telegram_id),
        sender_name=sender_name or "User",
        bot_origin=bot_origin,
        raw_text=raw_text,
        anonymized_text=anonymized_text,
        active_persona=resolved["persona"],
        privacy_scope=resolved["privacy_scope"],
        owner_id=resolved["owner_id"]
    )
