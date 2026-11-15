"""Privacy-aware request routing for MacStudio AI."""

from __future__ import annotations


def use_private_agent(
    *,
    device_id: str | None,
    user_id: str | None,
    private_devices: set[str],
    allow_private_text: bool,
) -> bool:
    """Return whether this trusted Home Assistant context may access Paperless."""
    if device_id is not None:
        return device_id in private_devices
    return bool(user_id and allow_private_text)


def session_user(
    *, device_id: str | None, user_id: str | None, conversation_id: str | None
) -> str:
    """Build a stable, source-separated OpenClaw session identity."""
    source = device_id or ("authenticated-text" if user_id else "unknown")
    return f"homeassistant:{source}:{conversation_id or 'new'}"
