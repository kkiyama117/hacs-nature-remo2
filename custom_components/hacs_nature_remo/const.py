"""Constants for hacs-nature-remo."""
# Should be equal to the name of your component.
from datetime import timedelta
import logging

from homeassistant.components.climate.const import (
    HVAC_MODES, HVACMode
)

LOGGER: logging.Logger = logging.getLogger(__package__)

# Base component constants
NAME = "Nature Remo integration"
DOMAIN: str = "hacs_nature_remo"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"
DEFAULT_UPDATE_INTERVAL = timedelta(seconds=60)

ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
ISSUE_URL = "https://github.com/kkiyama117/hacs-nature-remo2/issues"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
SWITCH = "switch"
CLIMATE = "climate"
LIGHT = "light"
SENSOR = "sensor"
BINARY_SENSOR = "binary_sensor"
PLATFORMS = [BINARY_SENSOR, SENSOR, SWITCH, CLIMATE, LIGHT]

# Configuration and options
CONF_ENABLED = "enabled"
# CONF_USERNAME = "username"
# CONF_PASSWORD = "password"
CONF_API_TOKEN = "api_token"

# Defaults
DEFAULT_NAME = DOMAIN

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""

# Nature Remo API
NATURE_REMO_API_BASE_URL = "https://api.nature.global"
NATURE_REMO_API_TIMEOUT_SEC = 10

KEY_API = "api"
KEY_CONFIG = "api"
KEY_COORDINATOR = "coordinator"
KEY_APPLIANCES = "appliances"
KEY_DEVICES = "devices"

# For climate
# TODO: Add more HVAC modes
MODE_HA_TO_REMO = {
    HVAC_MODES.AUTO: "auto",
    HVAC_MODES.FAN_ONLY: "blow",
    HVAC_MODES.COOL: "cool",
    HVAC_MODES.DRY: "dry",
    HVAC_MODES.HEAT: "warm",
    HVAC_MODES.OFF: "power-off",
}

MODE_REMO_TO_HA = {
    "auto": HVAC_MODES.AUTO,
    "blow": HVAC_MODES.FAN_ONLY,
    "cool": HVAC_MODES.COOL,
    "dry": HVAC_MODES.DRY,
    "warm": HVAC_MODES.HEAT,
    "power-off": HVAC_MODES.OFF,
}
AIRCON_MODES_REMO = MODE_REMO_TO_HA.keys()
