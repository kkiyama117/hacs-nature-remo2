"""Switch platform for hacs-nature-remo."""

import dataclasses
from copy import deepcopy

import remo
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE
from homeassistant.core import callback
from homeassistant.components.climate import ClimateEntity, HVACMode, HVAC_MODES

from . import LOGGER
from .coordinators import HacsNatureRemoDataUpdateCoordinator
from .domain import climate as climate_const
from .domain.config_schema import KEY_APPLIANCES, KEY_DEVICES, PluginDataDict
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


@dataclasses.dataclass(frozen=True)
class DefaultClimateConfig:
    cool_temperature: float
    heat_temperature: float


def config_entry_to_default_climate_config(entry: ConfigEntry) -> DefaultClimateConfig:
    _ct = entry.data.get(str(HVACMode.COOL))
    _ht = entry.data.get(str(HVACMode.HEAT))
    return DefaultClimateConfig(cool_temperature=_ct, heat_temperature=_ht)


@dataclasses.dataclass(frozen=True)
class HacsNatureRemoACData:
    default_config: DefaultClimateConfig
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
        entry_config = entry.data
        default_config: DefaultClimateConfig = DefaultClimateConfig(
            cool_temperature=entry_config.get(str(HVACMode.COOL)),
            heat_temperature=entry_config.get(str(HVACMode.HEAT)),
        )
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
            last_target_temperatures={v: None for v in HVAC_MODES},
            default_config=default_config,
        )
        # Update(Init)
        self._update_data(ac_settings, None)

    # Fetch from coordinator and set new attribute data
    # This method need to get AC params
    # https://swagger.nature.global/#/default/post_1_appliances__applianceid__aircon_settings
    def _update_data(self, ac_settings: remo.AirConParams, device=None):
        LOGGER.debug("Climate data update")
        self._update_inner_data(ac_settings, device)
        self._update_from_inner_data()

    # Fetch from coordinator
    def _update_inner_data(
        self, ac_settings: remo.AirConParams, device: remo.Device | None = None
    ):
        LOGGER.debug("Update climate data")
        LOGGER.debug(f"ac_settings: {ac_settings}")
        LOGGER.debug(f"Device: {device}")
        result = {}
        current_mode = climate_const.CLIMATE_MODE_REMO_TO_HA.get(ac_settings.mode)
        if current_mode is not None:
            result.setdefault("current_mode", current_mode)
        else:
            result.setdefault(self._inner_data.current_mode)
        result.setdefault("all_modes", self._inner_data.all_modes)
        _fan = ac_settings.vol or None
        result.setdefault("current_fan", _fan)
        _swing = ac_settings.dir or None
        result.setdefault("current_swing", _swing)
        if device is not None:
            _ce: remo.SensorValue = device.newest_events.get("te")
            result.setdefault("current_temperature", float(_ce.val))
        else:
            result.setdefault("current_temperature", None)
        last_target_temperatures = deepcopy(self._inner_data.last_target_temperatures)
        target_temperature = float(ac_settings.temp)
        last_target_temperatures[current_mode] = target_temperature
        if current_mode is not HVACMode.OFF and current_mode is not None:
            result.setdefault("target_temperature", target_temperature)
        else:
            result.setdefault(
                "target_temperature", self._inner_data.current_temperature
            )
        current_mode_temp_range = self._get_current_mode_temp_range(current_mode)
        result.setdefault("current_mode_temp_range", current_mode_temp_range)
        result.setdefault("last_target_temperatures", last_target_temperatures)
        result.setdefault("default_config", self._inner_data.default_config)
        LOGGER.debug(
            f"climate: last temperatures:{self._inner_data.last_target_temperatures}"
        )
        self._inner_data = HacsNatureRemoACData(**result)
        LOGGER.debug("Update Climate Data from coordinator finished")
        LOGGER.debug(f"{self._inner_data}")

    # Update attributes
    def _update_from_inner_data(self):
        """Update HA Entity value"""
        LOGGER.debug("Update Climate Data for view")
        LOGGER.debug(f"{self._inner_data}")
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
        elif len(temperature_range) == 0:
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
            elif self._inner_data.current_mode is HVACMode.COOL:
                data["temperature"] = self._inner_data.default_config.cool_temperature
            elif self._inner_data.current_mode is HVACMode.HEAT:
                data["temperature"] = self._inner_data.default_config.heat_temperature
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
        ap_data: remo.AirConParams = aps_data.get(self.appliance.id).settings
        device_data = self.coordinator.data.get(KEY_DEVICES).get(
            self.appliance.device.id
        )
        LOGGER.debug(f"Climate update coordinator:{ap_data} AND {device_data}")
        if ap_data is not None:
            self._update_data(ap_data, device_data)
        else:
            LOGGER.warning("Climate update failed")
        self.async_write_ha_state()

    # HELPERS ----------------------------------------------------------------------------------------------------------
    async def _post_aircon_settings(self, data):
        # Maybe this API return appliances
        response: dict = await self.coordinator.raw_api().update_aircon_settings(
            appliance=self.appliance.id, **data
        )
        if response is not None:
            temp_unit = response.pop("temp_unit")
            updated_at = response.pop("updated_at")
            dirh = response.pop("dirh")
            try:
                ac_params = remo.AirConParams(**response)
                self._update_data(ac_params, None)
            except ValueError:
                LOGGER.warning(
                    "This is Illegal response of Nature Remo API for this plugin. "
                    "Please send issue to HACS NATURE REMO plugin developer"
                    "https://github.com/kkiyama117/hacs-nature-remo2"
                )
                LOGGER.debug(f"{response}, {temp_unit}, {updated_at}, {dirh}")

        self.async_write_ha_state()

    def _get_current_mode_temp_range(self, mode_name: HVACMode) -> list[float]:
        mode_data: remo.AirConRangeMode | None = self._inner_data.all_modes.get(
            climate_const.CLIMATE_MODE_HA_TO_REMO.get(mode_name)
        )
        if mode_data is not None:
            temp_range = mode_data.temp
            result = list(map(float, filter(None, temp_range)))
            LOGGER.debug(f"current mode({mode_name}) temp_range: {result}")
            return result
        else:
            return [0, 0]

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
