"""HacsNatureRemoEntity class"""
import remo
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import HacsNatureRemoDataUpdateCoordinator, KEY_APPLIANCES
from custom_components.hacs_nature_remo.domain.const import DEFAULT_MANUFACTURER, ICON, KEY_DEVICES, DOMAIN, LOGGER


class HacsNatureRemoEntity(CoordinatorEntity):
    """Base Entity of this integration"""
    _attr_should_poll = False

    def __init__(self, coordinator: HacsNatureRemoDataUpdateCoordinator, idx: str):
        super().__init__(coordinator, context=idx)
        self._attr_unique_id = idx
        self._update_data()
        # Update
        self.device: remo.Device | None = None
        self._base_name= f"Nature Remo {self.device.name}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            name=self.device.name,
            manufacturer=DEFAULT_MANUFACTURER,
            model=self.device.serial_number,
            sw_version=self.device.firmware_version,
        )

    async def _update_data(self):
        pass

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON


class HacsNatureRemoDeviceEntity(HacsNatureRemoEntity):
    def __init__(self, coordinator: HacsNatureRemoDataUpdateCoordinator, idx: str):
        super().__init__(coordinator, idx)
        self._attr_name = f"Nature Remo {self.device.name}"

    def _update_data(self):
        LOGGER.debug(f"device data update({self._attr_unique_id})")
        self.device = self.coordinator.data.get(KEY_DEVICES).get(self._attr_unique_id)


class HacsNatureRemoApplianceEntity(HacsNatureRemoEntity):
    def __init__(self, coordinator: HacsNatureRemoDataUpdateCoordinator, idx: str):
        super().__init__(coordinator, idx)
        # self._attr_should_poll = False

    def _update_data(self):
        LOGGER.debug(f"appliance data update({self._attr_unique_id})")
        self.appliance = self.coordinator.data.get(KEY_APPLIANCES).get(self._attr_unique_id)
        self.device: remo.DeviceCore = self.appliance.device
