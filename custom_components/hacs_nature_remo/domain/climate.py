from typing import Literal

from homeassistant.components.climate import ClimateEntityFeature
from homeassistant.components.climate import HVACMode
from homeassistant.const import UnitOfTemperature

CLIMATE_MODE_NATURE_REMO_AUTO = "auto"
CLIMATE_MODE_NATURE_REMO_FAN_ONLY = "blow"
CLIMATE_MODE_HA_COOL = "cool"
CLIMATE_MODE_HA_DRY = "dry"
CLIMATE_MODE_HA_HEAT = "warm"
CLIMATE_MODE_HA_OFF = "power-off"

# TODO: Use strings above
type CLIMATE_MODE_NATURE_REMO = Literal[
    "auto", "blow", "cool", "dry", "warm", "power-off"
]

AIRCON_MODE_KEYS = [
    CLIMATE_MODE_NATURE_REMO_AUTO,
    CLIMATE_MODE_NATURE_REMO_FAN_ONLY,
    CLIMATE_MODE_HA_COOL,
    CLIMATE_MODE_HA_DRY,
    CLIMATE_MODE_HA_HEAT,
    CLIMATE_MODE_HA_OFF,
]

CLIMATE_MODE_HA_TO_REMO = {
    HVACMode.AUTO: CLIMATE_MODE_NATURE_REMO_AUTO,
    HVACMode.FAN_ONLY: CLIMATE_MODE_NATURE_REMO_FAN_ONLY,
    HVACMode.COOL: CLIMATE_MODE_HA_COOL,
    HVACMode.DRY: CLIMATE_MODE_HA_DRY,
    HVACMode.HEAT: CLIMATE_MODE_HA_HEAT,
    HVACMode.OFF: CLIMATE_MODE_HA_OFF,
}

CLIMATE_DEFAULT_TEMPERATURE_UNIT = UnitOfTemperature.CELSIUS
CLIMATE_MODE_REMO_TO_HA = {value: key for key, value in CLIMATE_MODE_HA_TO_REMO.items()}

CLIMATE_SUPPORT_FLAGS = (
    ClimateEntityFeature.TARGET_TEMPERATURE
    | ClimateEntityFeature.FAN_MODE
    | ClimateEntityFeature.SWING_MODE
    | ClimateEntityFeature.TURN_ON
    | ClimateEntityFeature.TURN_OFF
)
