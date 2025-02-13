from typing import TypedDict

import remo
import voluptuous as vol
from homeassistant.components.climate import HVACMode

CONF_API_TOKEN_KEY = "api_token"
CONF_CLIMATE_KEY = "climate"
CLIMATE_CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(str(HVACMode.HEAT), default=23): vol.Coerce(float),
        vol.Required(str(HVACMode.COOL), default=27): vol.Coerce(float),
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(
            CONF_API_TOKEN_KEY, default="Please_set_nature_remo_API"
        ): str,
        vol.Required(CONF_CLIMATE_KEY): CLIMATE_CONFIG_SCHEMA,
    },
    extra=vol.ALLOW_EXTRA,
)

KEY_USER = "user"
KEY_APPLIANCES = "appliances"
KEY_DEVICES = "devices"
KEY_CLIMATE_CONFIGS = "climate_configs"

PluginDataDict = TypedDict(
    "PluginDataDict",
    {
        KEY_USER: dict[str, remo.User],
        KEY_APPLIANCES: dict[str, remo.Appliance],
        KEY_DEVICES: dict[str, remo.Device],
    },
)
