"""Switch platform for Cookiecutter Home Assistant Custom Component Instance."""

import remo
from homeassistant.components.switch import SwitchEntity

from . import LOGGER
from .coordinators import HacsNatureRemoDataUpdateCoordinator
from .domain.config_schema import KEY_APPLIANCES, PluginDataDict
from .domain.const import SWITCH, DOMAIN
from .entity import HacsNatureRemoApplianceEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup switch platform."""
    LOGGER.debug("Setting up IR platform")
    if DOMAIN not in hass.data or entry.entry_id not in hass.data[DOMAIN]:
        LOGGER.error(f"Coordinator not found for entry {entry.entry_id}")
        return
    coordinator: HacsNatureRemoDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    _data: PluginDataDict = coordinator.data
    appliances: dict[str, remo.Appliance] = _data.get(KEY_APPLIANCES)
    async_add_devices(
        [
            NatureRemoIR(coordinator, appliance_key)
            for appliance_key, app in appliances.items()
            if app.type == "IR"
        ]
    )


class NatureRemoIR(HacsNatureRemoApplianceEntity, SwitchEntity):
    """Switch Entity for Nature Remo IR"""

    _attr_assumed_state = True

    def __init__(
        self, coordinator: HacsNatureRemoDataUpdateCoordinator, idx: str
    ) -> None:
        super().__init__(coordinator, idx)
        self._attr_name = f"{self._base_name.strip()} {SWITCH}"
        self._signals: list[remo.Signal] = self.appliance.signals

    async def _async_turn_switch(self, is_on: bool):
        LOGGER.debug(f"{self.unique_id}: set state {is_on}")
        _names = ["ico_onico_io"] if is_on else ["ico_offico_io"]
        try:
            images = [x.image for x in self._signals]
            for name in _names:
                if name in images:
                    # Post Signal to API and write ha state
                    signal = self._signals[images.index(name)].id
                    await self.coordinator.raw_api().send_signal(signal)
                    break
            self._attr_is_on = is_on
            self.async_write_ha_state()
        except Exception as e:
            LOGGER.error(f"Cannot find {is_on} signal: {e}")
        await self.coordinator.async_request_refresh()

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        await self._async_turn_switch(True)

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        await self._async_turn_switch(False)
