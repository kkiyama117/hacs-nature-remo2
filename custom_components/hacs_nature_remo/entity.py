"""HacsNatureRemoEntity class"""
import remo
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import HacsNatureRemoDataUpdateCoordinator, KEY_APPLIANCES
from .const import DEFAULT_MANUFACTURER, ICON, KEY_DEVICES, DOMAIN
from .utils import find_by


class HacsNatureRemoEntity(CoordinatorEntity):
    def __init__(self, coordinator: HacsNatureRemoDataUpdateCoordinator):
        super().__init__(coordinator)


class HacsNatureRemoDeviceEntity(CoordinatorEntity):
    def __init__(self, coordinator: HacsNatureRemoDataUpdateCoordinator, idx: str):
        super().__init__(coordinator, context=idx)
        self.device_id = idx
        self._update_device_data()
        # Update
        self._attr_device_info = DeviceInfo(
            default_manufacturer=DEFAULT_MANUFACTURER,
            identifiers={(DOMAIN, self.device_id)},
            model=self.device.serial_number,
            name=self.device.name,
        )

    def update(self):
        self._update_device_data()

    def _update_device_data(self):
        self.device = self.coordinator.data.get(KEY_DEVICES).get(self.device_id)

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON


class HacsNatureRemoApplianceEntity(CoordinatorEntity):
    def __init__(self, coordinator: HacsNatureRemoDataUpdateCoordinator, idx: str):
        super().__init__(coordinator, context=idx)
        self.appliance_id = idx
        self._update_appliance_data()
        self._attr_name = f"Nature Remo {self.appliance.nickname}"
        self.device = self.appliance.device
        self._attr_should_poll = False
        self._attr_device_info = DeviceInfo(
            default_manufacturer=DEFAULT_MANUFACTURER,
            identifiers={(DOMAIN, self.appliance_id)},
            model=self.device.serial_number,
            name=self.device.name,
        )

    def update(self):
        self._update_appliance_data()

    def _update_appliance_data(self):
        self.appliance = self.coordinator.data.get(KEY_APPLIANCES).get(self.appliance_id)

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON