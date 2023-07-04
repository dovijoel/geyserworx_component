import logging
from homeassistant.components.water_heater import (
    WaterHeaterEntityFeature,
    STATE_ECO,
    STATE_ELECTRIC,
    STATE_PERFORMANCE,
    STATE_OFF
)

DOMAIN = "geyserworx_component"

CONF_BASE_URL = "base_url"
CONF_GEYSER_SERIAL_NUMBER = "geyser_serial_number"
CONF_GEYSER_NUMBER = "geyser_number"
CONF_UPDATE_INTERVAL = "update_interval"
LOGGER = logging.getLogger(__package__)

OPERATION_LIST = [STATE_OFF, STATE_ECO, STATE_ELECTRIC, STATE_PERFORMANCE]
SUPPORTED_FEATURES = (WaterHeaterEntityFeature.TARGET_TEMPERATURE | WaterHeaterEntityFeature.OPERATION_MODE)

ATTR_CURRENT_TEMPERATURE = "current_temperature"
ATTR_CURRENT_SETTINGS = "current_settings"
ATTR_CURRENT_POWER_STATUS = "current_power_status"
ATTR_AC = "AC"
ATTR_AC_BOOST = "AC_BOOST"
ATTR_PV = "PV"
ATTR_SETTINGS_POWER = "POWER"
ATTR_SETTINGS_TEMP = "TEMP"