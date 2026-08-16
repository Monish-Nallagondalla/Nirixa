#!/usr/bin/env python3
"""
Nirixa OS Engine - Anonymization Engine
Enforces Rule 5: Strict Anonymization. Extracts abstract architectural scars
without exposing proprietary PII (like specific company names or client data).
"""

import re

# Default PII rules for My-OS
DEFAULT_ANONYMIZATION_RULES = [
    {"match": r"(?i)\bEY\b", "replace": "Tier-1 Consulting Firm"},
    {"match": r"(?i)\bErnst & Young\b", "replace": "Tier-1 Consulting Firm"},
    {"match": r"(?i)\bManager\b", "replace": "Senior Engagement Lead"},
    # Add other rules here over time
]

class AnonymizerEngine:
    def __init__(self, rules=None):
        self.rules = rules if rules is not None else DEFAULT_ANONYMIZATION_RULES
        self._compiled_rules = [
            (re.compile(rule["match"]), rule["replace"]) 
            for rule in self.rules
        ]

    def apply(self, text):
        """
        Applies all anonymization regex rules to the input text.
        """
        if not text:
            return text
            
        anonymized_text = text
        for pattern, replacement in self._compiled_rules:
            anonymized_text = pattern.sub(replacement, anonymized_text)
            
        return anonymized_text

# Singleton instance for quick access
_instance = AnonymizerEngine()

def apply_anonymization(text):
    return _instance.apply(text)
