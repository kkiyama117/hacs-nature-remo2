"""HacsNatureRemoEntity class"""
import remo
from homeassistant.helpers.device_registry import DeviceInfo, DeviceEntryType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import HacsNatureRemoDataUpdateCoordinator, KEY_APPLIANCES
from .const import DEFAULT_MANUFACTURER, ICON, KEY_DEVICES, DOMAIN, LOGGER


class HacsNatureRemoEntity(CoordinatorEntity):
    """Base Entity of this integration"""
    def __init__(self, coordinator: HacsNatureRemoDataUpdateCoordinator, idx:str):
        super().__init__(coordinator,context=idx)
        self.idx = idx
        self._attr_unique_id = idx

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON


class HacsNatureRemoDeviceEntity(HacsNatureRemoEntity):
    def __init__(self, coordinator: HacsNatureRemoDataUpdateCoordinator, idx: str):
        super().__init__(coordinator, idx)
        # Update
        self._update_data()
        self._attr_name = f"Nature Remo {self.device.name}"
        self._attr_device_info = DeviceInfo(
            manufacturer=DEFAULT_MANUFACTURER,
            identifiers={(DOMAIN, self.unique_id)},
            model=self.device.serial_number,
            name=self.device.name,
            sw_version=self.device.firmware_version,
        )

    def _update_data(self):
        LOGGER.debug(f"device data update({self.idx})")
        self.device = self.coordinator.data.get(KEY_DEVICES).get(self.idx)


class HacsNatureRemoApplianceEntity(HacsNatureRemoEntity):
    def __init__(self, coordinator: HacsNatureRemoDataUpdateCoordinator, idx: str):
        super().__init__(coordinator, context=idx)
        self._update_data()
        self._attr_name = f"Nature Remo {self.appliance.nickname}"
        self.device: remo.DeviceCore = self.appliance.device
        # self._attr_should_poll = False
        self._attr_unique_id = self.idx
        self._attr_device_info = DeviceInfo(
            manufacturer=DEFAULT_MANUFACTURER,
            identifiers={(DOMAIN, self.unique_id)},
            model=self.device.serial_number,
            name=self.device.name,
            sw_version=self.device.firmware_version,
        )

    def _update_data(self):
        LOGGER.debug(f"appliance data update({self.idx})")
        self.appliance = self.coordinator.data.get(KEY_APPLIANCES).get(self.idx)
