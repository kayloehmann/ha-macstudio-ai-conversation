"""Privacy-aware request routing for MacStudio AI."""

from __future__ import annotations


DOCUMENT_TERMS = (
    "paperless",
    "dokument",
    "unterlage",
    "rechnung",
    "quittung",
    "beleg",
    "vertrag",
    "bescheid",
    "brief",
    "mahnung",
    "abrechnung",
    "versicherungspolice",
    "garantie",
)


def private_context_allowed(
    *,
    device_id: str | None,
    user_id: str | None,
    private_devices: set[str],
    allow_private_text: bool,
) -> bool:
    """Return whether this Home Assistant context may access Paperless."""
    if device_id is not None:
        return device_id in private_devices
    return bool(user_id and allow_private_text)


def is_document_request(text: str) -> bool:
    """Return whether a spoken request asks about a private document."""
    normalized = text.casefold()
    return any(term in normalized for term in DOCUMENT_TERMS)


def session_user(
    *, device_id: str | None, user_id: str | None, conversation_id: str | None
) -> str:
    """Build a stable, source-separated OpenClaw session identity."""
    source = device_id or ("authenticated-text" if user_id else "unknown")
    return f"homeassistant:{source}:{conversation_id or 'new'}"
