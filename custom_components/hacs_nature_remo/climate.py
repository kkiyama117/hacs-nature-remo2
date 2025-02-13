"""Switch platform for hacs-nature-remo."""

from copy import deepcopy
from dataclasses import dataclass

import remo
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE
from homeassistant.core import callback
from homeassistant.components.climate import ClimateEntity, HVACMode

from . import LOGGER
from .coordinators import HacsNatureRemoDataUpdateCoordinator
from .domain import climate as climate_const
from .domain.config_schema import (
    CLIMATE_CONFIG_SCHEMA,
    KEY_APPLIANCES,
    CONF_CLIMATE_KEY,
    KEY_DEVICES,
    PluginDataDict,
)
from .domain.const import DEFAULT_NAME, DOMAIN, ICON, SWITCH
from .entity import HacsNatureRemoApplianceEntity


async def async_setup_entry(hass, entry: ConfigEntry, async_add_devices):
    """Setup AC platform."""
    LOGGER.debug("Setting up Air Conditioner platform")
    coordinator: HacsNatureRemoDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    _data: PluginDataDict = coordinator.data
    appliances: dict[str, remo.Appliance] = _data.get(KEY_APPLIANCES)
    async_add_devices(
        [
            HacsNatureRemoAC(coordinator, appliance_key, entry)
            for appliance_key, app in appliances.items()
            if app.type == "AC"
        ]
    )


@dataclass
class HacsNatureRemoACData:
    default_config: CLIMATE_CONFIG_SCHEMA
    # Mode of HA
    current_mode: HVACMode
    # Mode list of Remo
    all_modes: dict[str, remo.AirConRangeMode] | None
    current_fan: str | None
    current_swing: str | None
    current_mode_temp_range: list[float]
    # current_remo_mode:str|None
    current_temperature: float | None
    target_temperature: float | None
    last_target_temperatures: dict[str, float | None]


class HacsNatureRemoAC(HacsNatureRemoApplianceEntity, ClimateEntity):
    """hacs_nature_remo switch class."""

    _attr_supported_features = climate_const.CLIMATE_SUPPORT_FLAGS
    _attr_temperature_unit = climate_const.CLIMATE_DEFAULT_TEMPERATURE_UNIT

    def __init__(
            self, coordinator: HacsNatureRemoDataUpdateCoordinator, idx, entry: ConfigEntry
    ):
        super().__init__(coordinator, idx)
        ac_settings: remo.AirConParams = self.appliance.settings
        if ac_settings is None:
            LOGGER.warning("Empty AC is added")
        self._inner_data: HacsNatureRemoACData = HacsNatureRemoACData(
            # DEFAULT VALUE
            current_mode=HVACMode.OFF,
            all_modes=self.appliance.aircon.range.modes,
            current_fan=None,
            current_swing=None,
            current_temperature=None,
            target_temperature=None,
            current_mode_temp_range=[],
            # set None for each HVAC mode
            last_target_temperatures={v: None for v in HVACMode},
            default_config=entry.data.get(CONF_CLIMATE_KEY),
        )
        # Update(Init)
        self._update_data(ac_settings, None)

    # Fetch from coordinator and set new attribute data
    # This method need to get AC params
    # https://swagger.nature.global/#/default/post_1_appliances__applianceid__aircon_settings
    def _update_data(self, ac_settings:remo.AirConParams, device=None):
        self._update_inner_data(ac_settings, device)
        self._update_from_inner_data()

    # Fetch from coordinator
    def _update_inner_data(
            self, ac_settings: remo.AirConParams, device: remo.Device | None = None
    ):
        previous_data: HacsNatureRemoACData = deepcopy(self._inner_data)
        try:
            current_mode = climate_const.CLIMATE_MODE_REMO_TO_HA.get(ac_settings.mode)
        except:
            current_mode = previous_data.current_mode
        _last_target_temperatures = previous_data.last_target_temperatures
        try:
            _target_temperature = float(ac_settings.temp)
            _last_target_temperature_key = previous_data.current_mode
            _last_target_temperature_value = float(ac_settings.temp)
            _last_target_temperatures[_last_target_temperature_key] = (
                _last_target_temperature_value
            )
        except:
            _target_temperature = None
        try:
            _fan = ac_settings.vol or None
        except:
            _fan = None
        try:
            _swing = ac_settings.dir or None
        except:
            _swing = None
        if device is not None:
            _ce: remo.SensorValue = device.newest_events.get("te")
            _current_temperature = float(_ce.val)
        else:
            _current_temperature = None
        current_mode_temp_range = self._get_current_mode_temp_range(current_mode)
        new_one = HacsNatureRemoACData(
            current_mode=current_mode,
            all_modes=previous_data.all_modes,
            target_temperature=_target_temperature,
            last_target_temperatures=_last_target_temperatures,
            current_fan=_fan,
            current_swing=_swing,
            current_temperature=_current_temperature,
            default_config=previous_data.default_config,
            current_mode_temp_range=current_mode_temp_range,
        )
        self._inner_data = new_one

    # Update attributes
    def _update_from_inner_data(self):
        """Update HA Entity value"""
        self._attr_current_temperature = self._inner_data.current_temperature
        self._attr_target_temperature = self._inner_data.target_temperature
        self._attr_hvac_mode = self._inner_data.current_mode
        self._attr_hvac_modes = self._convert_to_hvac_list(self._inner_data.all_modes)
        # set min and max temperature, and target_temperature step
        temperature_range = self._inner_data.current_mode_temp_range
        if len(temperature_range) >= 2:
            self._attr_max_temp = max(temperature_range)
            self._attr_min_temp = min(temperature_range)
            step = round(temperature_range[1] - temperature_range[0], 1)
            if step in [1.0, 0.5]:
                self._attr_target_temperature_step = step
        elif len(temperature_range)==0:
            self._attr_max_temp = max(temperature_range)
            self._attr_min_temp = min(temperature_range)
            self._attr_target_temperature_step = 1
        else:
            self._attr_max_temp = 0
            self._attr_min_temp = 0
            self._attr_target_temperature_step = 1
        self._attr_fan_mode = self._inner_data.current_fan
        self._attr_fan_modes = self._inner_data.all_modes.get(
            climate_const.CLIMATE_MODE_HA_TO_REMO.get(self._inner_data.current_mode)
        ).vol
        self._attr_swing_mode = self._inner_data.current_swing
        self._attr_swing_modes = self._inner_data.all_modes.get(
            climate_const.CLIMATE_MODE_HA_TO_REMO.get(self._inner_data.current_mode)
        ).dir

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        if self._inner_data.current_mode is None:
            await self.async_set_hvac_mode(HVACMode.COOL)
        else:
            await self.async_set_hvac_mode(self._inner_data.current_mode)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        await self.async_set_hvac_mode(HVACMode.OFF)

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        target_temp = kwargs.get(ATTR_TEMPERATURE)
        if target_temp is None:
            return
        if target_temp.is_integer():
            # has to cast to whole number otherwise API will return an error
            target_temp = int(target_temp)
        LOGGER.debug("Set temperature: %d", target_temp)
        await self._post_aircon_settings({"temperature": f"{target_temp}"})

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode"""
        LOGGER.debug("Set hvac mode: %s", hvac_mode)
        mode = climate_const.CLIMATE_MODE_HA_TO_REMO[hvac_mode]
        if mode == climate_const.CLIMATE_MODE_HA_TO_REMO[HVACMode.OFF]:
            await self._post_aircon_settings({"button": mode})
        else:
            data = {"operation_mode": mode}
            if self._inner_data.last_target_temperatures[mode]:
                data["temperature"] = self._inner_data.last_target_temperatures[mode]
            elif self._inner_data.default_config[hvac_mode].get(hvac_mode):
                data["temperature"] = self._inner_data.default_config[hvac_mode]
            await self._post_aircon_settings(data)

    async def async_set_fan_mode(self, fan_mode):
        """Set new target fan mode."""
        LOGGER.debug("Set fan mode: %s", fan_mode)
        await self._post_aircon_settings({"air_volume": fan_mode})

    async def async_set_swing_mode(self, swing_mode):
        """Set new target swing operation."""
        LOGGER.debug("Set swing mode: %s", swing_mode)
        await self._post_aircon_settings({"air_direction": swing_mode})

    @property
    def name(self):
        """Return the name of the switch."""
        return f"{DEFAULT_NAME}_{SWITCH}"

    @property
    def icon(self):
        """Return the icon of this switch."""
        return ICON

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        aps_data = self.coordinator.data.get(KEY_APPLIANCES)
        # GET AC_PARAMS
        ap_data:remo.AirConParams = aps_data.get(self.appliance.id).settings
        device_data = self.coordinator.data.get(KEY_DEVICES).get(
            self.appliance.device.id
        )
        LOGGER.debug(f"Climate update coordinator:{ap_data} AND {device_data}")
        if ap_data is not None:
            self._update_data(ap_data, device_data)
        else:
            LOGGER.warning(f"Climate update failed")
        self.async_write_ha_state()

    # HELPERS ----------------------------------------------------------------------------------------------------------
    async def _post_aircon_settings(self, data):
        # Maybe this API return appliances
        response = await self.coordinator.raw_api().update_aircon_settings(
            appliance=self.appliance.id, **data
        )
        self._update_data(response)
        self.async_write_ha_state()

    def _get_current_mode_temp_range(self, mode_name: HVACMode) -> list[float]:
        mode_data: remo.AirConRangeMode | None = self._inner_data.all_modes.get(
            climate_const.CLIMATE_MODE_HA_TO_REMO.get(mode_name)
        )
        if mode_data is not None:
            temp_range = mode_data.temp
            result =  list(map(float, filter(None, temp_range)))
            LOGGER.debug(f"current mode({mode_name}) temp_range: {result}")
            return result
        else:
            return [0,0]

    @staticmethod
    def _convert_to_hvac_list(
            modes: dict[str, remo.AirConRangeMode] | None,
    ) -> list[HVACMode]:
        remo_modes = list(modes.keys())
        ha_modes = list(
            map(
                lambda mode: climate_const.CLIMATE_MODE_REMO_TO_HA.get(mode), remo_modes
            )
        )
        ha_modes.append(HVACMode.OFF)
        return ha_modes
