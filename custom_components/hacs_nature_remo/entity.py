"""HacsNatureRemoEntity class"""
import remo
from homeassistant.helpers.device_registry import DeviceInfo, DeviceEntryType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import HacsNatureRemoDataUpdateCoordinator, KEY_APPLIANCES
from .const import DEFAULT_MANUFACTURER, ICON, KEY_DEVICES, DOMAIN


class HacsNatureRemoEntity(CoordinatorEntity):
    def __init__(self, coordinator: HacsNatureRemoDataUpdateCoordinator):
        super().__init__(coordinator)


class HacsNatureRemoDeviceEntity(CoordinatorEntity):
    def __init__(self, coordinator: HacsNatureRemoDataUpdateCoordinator, idx: str):
        super().__init__(coordinator, context=idx)
        self.idx = idx
        # Update
        self._update_device_data()
        self._attr_name = f"Nature Remo {self.device.name}"
        self._attr_unique_id = self.idx
        self._attr_device_info = DeviceInfo(
            manufacturer=DEFAULT_MANUFACTURER,
            identifiers={(DOMAIN, self.unique_id)},
            model=self.device.serial_number,
            name=self.device.name,
            sw_version=self.device.firmware_version,
        )

    def update(self):
        self._update_device_data()

    def _update_device_data(self):
        self.device = self.coordinator.data.get(KEY_DEVICES).get(self.idx)

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON


class HacsNatureRemoApplianceEntity(CoordinatorEntity):
    def __init__(self, coordinator: HacsNatureRemoDataUpdateCoordinator, idx: str):
        super().__init__(coordinator, context=idx)
        self.idx = idx
        self._update_appliance_data()
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

    def update(self):
        self._update_appliance_data()

    def _update_appliance_data(self):
        self.appliance = self.coordinator.data.get(KEY_APPLIANCES).get(self.idx)

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    @property
    def device_info(self) -> DeviceInfo | None:
        return DeviceInfo(

        )