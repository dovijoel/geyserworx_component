"""DataUpdateCoordinator for Geyserworx Component."""
from __future__ import annotations
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from geyserworx_api import GeyserworxAPI, PowerType, TemperatureType

from .const import (
    CONF_BASE_URL,
    CONF_GEYSER_SERIAL_NUMBER,
    CONF_GEYSER_NUMBER,
    CONF_UPDATE_INTERVAL,
    DOMAIN,
    LOGGER,
    ATTR_CURRENT_POWER_STATUS,
    ATTR_CURRENT_SETTINGS,
    ATTR_CURRENT_TEMPERATURE
)


class GeyserworxDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Geyserworx data."""

    config_entry: ConfigEntry

    def __init__(
            self,
            hass: HomeAssistant,
            entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.config_entry = entry

        base_url = entry.data[CONF_BASE_URL]
        geyser_serial_number = entry.data[CONF_GEYSER_SERIAL_NUMBER]
        geyser_number = entry.data[CONF_GEYSER_NUMBER]

        self.geyserworx = GeyserworxAPI(
            session=async_get_clientsession(hass),
            geyser_serial_number=geyser_serial_number,
            geyser_number=geyser_number,
            base_url=base_url
        )

        update_interval = timedelta(seconds=entry.data[CONF_UPDATE_INTERVAL])

        super().__init__(hass, LOGGER, name=DOMAIN, update_interval=update_interval)

    # TODO add error catching
    async def _async_update_data(self) -> dict:
        """Fetch data from Geyserworx API."""
        current_temp = await self.geyserworx.get_current_temperature()
        current_settings = await self.geyserworx.get_settings()
        current_power_status = await self.geyserworx.get_power_status()

        return {
            ATTR_CURRENT_TEMPERATURE: current_temp,
            ATTR_CURRENT_SETTINGS: current_settings,
            ATTR_CURRENT_POWER_STATUS: current_power_status
        }
    
    async def async_set_power_status(self, power_type: str, status: bool) -> None:
        """Set power status."""
        if power_type == 'AC':
            power_status = PowerType.AC
        elif power_type == 'AC_BOOST':
            power_status = PowerType.AC_BOOST
        elif power_type == 'PV':
            power_status = PowerType.PV
        else:
            raise ValueError('Invalid power type')
        await self.geyserworx.set_power(power_status, status)
        await self.async_refresh()

    async def async_set_temperature(self, temperature_type: str, temperature: int) -> None:
        """Set temperature."""
        if temperature_type == 'AC':
            temp_type = TemperatureType.AC
        elif temperature_type == 'AC_BOOST':
            temp_type = TemperatureType.AC_BOOST
        elif temperature_type == 'PV':
            temp_type = TemperatureType.PV
        else:
            raise ValueError('Invalid temperature type')
        await self.geyserworx.set_temp(temp_type, temperature)
        await self.async_refresh()