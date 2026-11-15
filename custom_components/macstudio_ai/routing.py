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


def deny_document_request(*, text: str, private_allowed: bool) -> bool:
    """Return whether a document request must be rejected before the model call."""
    return is_document_request(text) and not private_allowed


def action_claim_guard(
    *, tool_results: list[tuple[str, bool]], read_only_tools: dict[str, bool]
) -> str | None:
    """Return a model guard when no successful device mutation occurred."""
    if not tool_results:
        return None

    successful_mutation = any(
        not read_only_tools.get(tool_name, False) and not result_error
        for tool_name, result_error in tool_results
    )
    if successful_mutation:
        return None

    attempted_mutation = any(
        not read_only_tools.get(tool_name, False)
        for tool_name, _result_error in tool_results
    )
    if attempted_mutation:
        return (
            "Es wurde keine Geräteaktion erfolgreich ausgeführt. Behaupte keinen "
            "Erfolg und nenne den Fehler knapp."
        )
    return (
        "Es wurde ausschließlich ein Zustand abgefragt und keine Geräteaktion "
        "ausgeführt. Antworte nur mit dem Zustand. Sage insbesondere nicht, du "
        "hättest etwas ein-, aus- oder umgeschaltet."
    )


def session_user(
    *, device_id: str | None, user_id: str | None, conversation_id: str | None
) -> str:
    """Build a stable, source-separated OpenClaw session identity."""
    source = device_id or ("authenticated-text" if user_id else "unknown")
    return f"homeassistant:{source}:{conversation_id or 'new'}"
