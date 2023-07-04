
from homeassistant.core import callback
from homeassistant.components.water_heater import (
    WaterHeaterEntity,
    STATE_PERFORMANCE,
    STATE_ELECTRIC,
    STATE_ECO,
    STATE_OFF

)
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature

from .const import (
    DOMAIN,
    OPERATION_LIST,
    SUPPORTED_FEATURES,
    ATTR_CURRENT_POWER_STATUS,
    ATTR_CURRENT_SETTINGS,
    ATTR_CURRENT_TEMPERATURE,
    ATTR_AC,
    ATTR_AC_BOOST,
    ATTR_PV,
    ATTR_SETTINGS_POWER,
    ATTR_SETTINGS_TEMP
)
from .coordinator import GeyserworxDataUpdateCoordinator

from typing import Any

async def async_setup_entry(hass, config_entry, async_add_entities) -> None:
    """Set up the Geyserworx water heater (geyser) device."""
    coordinator: GeyserworxDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        [
            GeyserworxWaterHeaterEntity(coordinator, config_entry.title)
        ])

class GeyserworxWaterHeaterEntity(CoordinatorEntity[GeyserworxDataUpdateCoordinator], WaterHeaterEntity):
    """Representation of a GeyserWorx water heater (geyser) device."""
    _attr_target_temperature_ac: float | None = None
    _attr_target_temperature_ac_boost: float | None = None
    _attr_target_temperature_pv: float | None = None
    _attr_operation_mode_ac_enabled: bool | None = None
    _attr_operation_mode_ac_boost_enabled: bool | None = None
    _attr_operation_mode_pv_enabled: bool | None = None

    def __init__(
            self,
            coordinator: GeyserworxDataUpdateCoordinator,
            name: str,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)

        self._attr_supported_features = SUPPORTED_FEATURES
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_operation_list = OPERATION_LIST

        self._attr_name = name
        
    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        self._attr_current_temperature = self.coordinator.data[ATTR_CURRENT_TEMPERATURE]

        # current state
        if self.coordinator.data[ATTR_CURRENT_POWER_STATUS][ATTR_AC]:
            self._attr_current_operation = STATE_ELECTRIC
        elif self.coordinator.data[ATTR_CURRENT_POWER_STATUS][ATTR_PV]:
            self._attr_current_operation = STATE_ECO
        elif self.coordinator.data[ATTR_CURRENT_POWER_STATUS][ATTR_AC_BOOST]:
            self._attr_current_operation = STATE_PERFORMANCE
        else:
            self._attr_current_operation = STATE_OFF

        # current temp settings
        self._attr_target_temperature_ac = self.coordinator.data[ATTR_CURRENT_SETTINGS][ATTR_SETTINGS_TEMP][ATTR_AC]
        self._attr_target_temperature_ac_boost = self.coordinator.data[ATTR_CURRENT_SETTINGS][ATTR_SETTINGS_TEMP][ATTR_AC_BOOST]
        self._attr_target_temperature_pv = self.coordinator.data[ATTR_CURRENT_SETTINGS][ATTR_SETTINGS_TEMP][ATTR_PV]

        # current power settings
        self._attr_is_on = self.coordinator.data[ATTR_CURRENT_POWER_STATUS][ATTR_AC] or self.coordinator.data[ATTR_CURRENT_POWER_STATUS][ATTR_PV] or self.coordinator.data[ATTR_CURRENT_POWER_STATUS][ATTR_AC_BOOST]
        self._attr_operation_mode_ac_enabled = self.coordinator.data[ATTR_CURRENT_SETTINGS][ATTR_SETTINGS_POWER][ATTR_AC]
        self._attr_operation_mode_ac_boost_enabled = self.coordinator.data[ATTR_CURRENT_SETTINGS][ATTR_SETTINGS_POWER][ATTR_AC_BOOST]
        self._attr_operation_mode_pv_enabled = self.coordinator.data[ATTR_CURRENT_SETTINGS][ATTR_SETTINGS_POWER][ATTR_PV]

    async def async_set_temperature(self, temperature: int, power_type: str) -> None:
        """Set new target temperatures."""
        await self.coordinator.async_set_temperature(power_type, temperature)

    async def async_set_power_status(self, enabled: bool, power_type: str) -> None:
        """Set new target temperatures."""
        await self.coordinator.async_set_power_status(power_type, enabled)
    



    

