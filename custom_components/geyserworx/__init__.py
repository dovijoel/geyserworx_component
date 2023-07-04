"""The Geyserworx Integration"""
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.WATER_HEATER]

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry
) -> bool:
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})
    hass_data = dict(entry.data)
    # Registers update listener to update config entry when options are updated.
    unsub_options_update_listener = entry.add_update_listener(options_update_listener)
    # Store a reference to the unsubscribe function to cleanup if an entry is unloaded.
    hass_data["unsub_options_update_listener"] = unsub_options_update_listener
    hass.data[DOMAIN][entry.entry_id] = hass_data

    # Forward the setup to the water heater platform.
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "water_heater")
    )
    return True


async def options_update_listener(
    hass: HomeAssistant, config_entry: ConfigEntry
):
    """Handle options update."""
    await hass.config_entries.async_reload(config_entry.entry_id)


async def async_unload_entry(
    hass: HomeAssistant, entry: ConfigEntry
) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        # Remove config entry from domain.
        entry_data = hass.data[DOMAIN].pop(entry.entry_id)
        # Remove options_update_listener.
        entry_data["unsub_options_update_listener"]()

    return unload_ok


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Geyserworx component from yaml configuration."""
    hass.data.setdefault(DOMAIN, {})
    return True