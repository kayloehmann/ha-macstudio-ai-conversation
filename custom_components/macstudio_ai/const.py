"""Constants for the MacStudio AI Conversation integration."""

import logging

DOMAIN = "macstudio_ai"
LOGGER = logging.getLogger(__package__)

CONF_RECOMMENDED = "recommended"
CONF_PROMPT = "prompt"
CONF_CHAT_MODEL = "chat_model"
CONF_MAX_TOKENS = "max_tokens"
CONF_TEMPERATURE = "temperature"
CONF_TOP_P = "top_p"
CONF_BASE_URL = "base_url"
CONF_PRIVATE_DEVICES = "private_devices"
CONF_ALLOW_PRIVATE_TEXT = "allow_private_text"

# Die MacStudio-AI-Bridge akzeptiert nur diese beiden Agentenziele. Der private
# Agent besitzt zusätzlich rein lesenden Zugriff auf Paperless.
RECOMMENDED_CHAT_MODEL = "openclaw/macstudio-ai"
PRIVATE_CHAT_MODEL = "openclaw/macstudio-ai-private"
RECOMMENDED_MAX_TOKENS = 1024
RECOMMENDED_TEMPERATURE = 1.0
RECOMMENDED_TOP_P = 1.0
RECOMMENDED_BASE_URL = "http://10.107.0.186:19790/v1"

# Persona-Default (in der UI frei überschreibbar). Die HA-LLM-API hängt die
# Tool-/Entity-Instruktionen automatisch an.
DEFAULT_PROMPT = (
    "Du bist MacStudio AI, der Sprachassistent in Kays Zuhause. Antworte kurz, "
    "natürlich und auf Deutsch — gesprochene Sätze, keine Listen oder Markdown. "
    "Nutze für Hauszustände und Geräteaktionen die bereitgestellten Werkzeuge. "
    "Bestätige eine Aktion erst nach einem erfolgreichen Werkzeugergebnis. Bei "
    "Unklarheit frag genau einmal kurz nach. Allgemeine Wissensfragen beantwortest "
    "du direkt. Private Dokumente darfst du nur auswerten, wenn der private "
    "MacStudio-AI-Agent für diese Anfrage ausgewählt wurde."
)
