from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .const import (
    DOMAIN,
    CONF_BASE_URL,
    CONF_GEYSER_SERIAL_NUMBER,
    CONF_GEYSER_NUMBER,
    CONF_UPDATE_INTERVAL
)

from typing import Any

import voluptuous as vol

class GeyserworxConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Geyserworx config flow."""
    VERSION = 1

    def __init__(self) -> None:
        """Initialize."""
        self.data_schema = vol.Schema({
            vol.Required(CONF_BASE_URL): str,
            vol.Required(CONF_GEYSER_SERIAL_NUMBER): str,
            vol.Required(CONF_GEYSER_NUMBER, default=1): int,
            vol.Required(CONF_UPDATE_INTERVAL, default=5): int
        })

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle a flow initialized by the user."""
        if user_input is not None:
            await self.async_set_unique_id(f"{user_input[CONF_GEYSER_SERIAL_NUMBER]}_{user_input[CONF_GEYSER_NUMBER]}")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="Geyserworx", data={
            CONF_BASE_URL: user_input[CONF_BASE_URL],
            CONF_GEYSER_SERIAL_NUMBER: user_input[CONF_GEYSER_SERIAL_NUMBER],
            CONF_GEYSER_NUMBER: user_input[CONF_GEYSER_NUMBER],
            CONF_UPDATE_INTERVAL: user_input[CONF_UPDATE_INTERVAL]
            })
            
        return self.async_show_form(
                step_id="user",
                data_schema=self.data_schema,
            )
        
        