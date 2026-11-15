"""The MacStudio AI Conversation integration."""

from __future__ import annotations

import openai

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.httpx_client import get_async_client

from .const import CONF_BASE_URL, LOGGER

PLATFORMS = (Platform.CONVERSATION,)

type MacStudioAiConfigEntry = ConfigEntry[openai.AsyncClient]


def _preload_chat_resource(client: openai.AsyncClient) -> None:
    """Load OpenAI's lazy chat resource outside the Home Assistant event loop."""
    client.chat.completions


async def async_setup_entry(hass: HomeAssistant, entry: MacStudioAiConfigEntry) -> bool:
    """Set up MacStudio AI Conversation from a config entry."""
    client = openai.AsyncOpenAI(
        api_key=entry.data.get(CONF_API_KEY) or "not-needed",
        http_client=get_async_client(hass),
        base_url=entry.data[CONF_BASE_URL],
    )
    await hass.async_add_executor_job(_preload_chat_resource, client)

    try:
        await client.with_options(timeout=10.0).models.list()
    except openai.AuthenticationError as err:
        LOGGER.error("Authentifizierung an der MacStudio-AI-Bridge fehlgeschlagen: %s", err)
        return False
    except openai.OpenAIError as err:
        raise ConfigEntryNotReady(err) from err

    entry.runtime_data = client

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload MacStudio AI Conversation."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
