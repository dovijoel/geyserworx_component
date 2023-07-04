"""The Geyserworx Integration"""
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .coordinator import GeyserworxDataUpdateCoordinator

from .const import (
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.WATER_HEATER]
async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Migrate old entry."""
    _LOGGER.debug("Migrating from version %s", config_entry.version)

    if config_entry.version == 1:

        new = {**config_entry.data}

        config_entry.version = 2
        hass.config_entries.async_update_entry(config_entry, data=new)

    _LOGGER.info("Migration to version %s successful", config_entry.version)

    return True    


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the ge_home component."""
    hass.data.setdefault(DOMAIN, {})

    """Set up ge_home from a config entry."""
    coordinator = GeyserworxDataUpdateCoordinator(hass, entry)
    hass.data[DOMAIN][entry.entry_id] = coordinator
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "water_heater")
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    coordinator: GeyserworxDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    ok = await coordinator.async_refresh()
    if ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return ok


async def async_update_options(hass, config_entry):
    """Update options."""
    await hass.config_entries.async_reload(config_entry.entry_id)