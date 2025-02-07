"""Constants for hacs-nature-remo."""
# Should be equal to the name of your component.
from datetime import timedelta

# Base component constants
NAME = "Nature Remo integration"
DOMAIN: str = "hacs_nature_remo"
DOMAIN_DATA = f"{DOMAIN}_data"
DEFAULT_MANUFACTURER = "Nature Remo"

VERSION = "0.1.0"
# DEFAULT_UPDATE_INTERVAL = timedelta(seconds=60)
# TODO: fetch action
DEFAULT_SCAN_INTERVAL = timedelta(seconds=30)

ATTRIBUTION = "Data provided by Nature Remo"
ISSUE_URL = "https://github.com/kkiyama117/hacs-nature-remo2/issues"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
# BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
SWITCH = "switch"
CLIMATE = "climate"
LIGHT = "light"
SENSOR = "sensor"
# BINARY_SENSOR = "binary_sensor"
# PLATFORMS = [SENSOR, SWITCH, LIGHT]
PLATFORMS = [SENSOR, SWITCH, CLIMATE]

# Configuration and options
CONF_ENABLED = "enabled"
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
KEY_USER = "user"
KEY_APPLIANCES = "appliances"
KEY_DEVICES = "devices"
