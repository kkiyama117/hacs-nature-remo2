from homeassistant.components.climate import HVACMode, ClimateEntity, ClimateEntityFeature

# TODO: Add more HVAC modes and Refactor
CLIMATE_MODE_HA_TO_REMO = {
    HVACMode.AUTO: "auto",
    HVACMode.FAN_ONLY: "blow",
    HVACMode.COOL: "cool",
    HVACMode.DRY: "dry",
    HVACMode.HEAT: "warm",
    HVACMode.OFF: "power-off",
}

CLIMATE_MODE_REMO_TO_HA = {
    "auto": HVACMode.AUTO,
    "blow": HVACMode.FAN_ONLY,
    "cool": HVACMode.COOL,
    "dry": HVACMode.DRY,
    "warm": HVACMode.HEAT,
    "power-off": HVACMode.OFF,
}

CLIMATE_SUPPORT_FLAGS = (
        ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.FAN_MODE | ClimateEntityFeature.SWING_MODE
        | ClimateEntityFeature.TURN_ON | ClimateEntityFeature.TURN_OFF)
