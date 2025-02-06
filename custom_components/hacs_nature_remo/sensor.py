"""Sensor platform for hacs-nature-remo."""
import remo
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfTemperature, LIGHT_LUX, PERCENTAGE, UnitOfPower
from homeassistant.core import callback
from homeassistant.helpers.entity import Entity

from . import HacsNatureRemoDataUpdateCoordinator, PluginDataDict
from .const import DOMAIN, KEY_DEVICES, LOGGER, KEY_APPLIANCES
from .entity import HacsNatureRemoDeviceEntity, HacsNatureRemoApplianceEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    LOGGER.debug("Setting up sensor platform")
    # Use config entry
    coordinator: HacsNatureRemoDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    _data: PluginDataDict = coordinator.data
    devices: dict[str, remo.Device] = _data.get(KEY_DEVICES)
    appliances: dict[str, remo.Appliance] = _data.get(KEY_APPLIANCES)
    entities:list[Entity] = [NatureRemoE(coordinator, key) for key, appliance in appliances.items() if
                 appliance.type == "EL_SMART_METER"]
    for device_id, device in devices.items():
        if device_id in [appliance.device.id for appliance in appliances.values()]:
            continue
        for sensor_key in device.newest_events.keys():
            if sensor_key == "te":
                entities.append(HacsNatureRemoTemperatureSensor(coordinator, device_id))
            elif sensor_key == "hu":
                entities.append(HacsNatureRemoHumiditySensor(coordinator, device_id))
            elif sensor_key == "il":
                entities.append(HacsNatureRemoIlluminanceSensor(coordinator, device_id))
    LOGGER.debug(f"entities setup (count: {len(entities)})")
    async_add_devices(
        entities
    )


class NatureRemoE(HacsNatureRemoApplianceEntity, SensorEntity):
    """Implementation of a Nature Remo E sensor."""
    _attr_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = SensorDeviceClass.POWER

    def __init__(self, coordinator: HacsNatureRemoDataUpdateCoordinator, appliance_id: str):
        super().__init__(coordinator, appliance_id)
        self._attr_name = self._base_name.strip() + " Power"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_data()
        if hasattr(self.appliance, "smart_meter"):
            smart_meter = self.appliance.smart_meter
            echonetlite_properties = smart_meter["echonetlite_properties"]
            measured_instantaneous = next(
                value.val for value in echonetlite_properties if value["epc"] == 231
            )
            LOGGER.debug("Current state: %sW", measured_instantaneous)
            self._attr_native_value = measured_instantaneous
        self.async_write_ha_state()


class HacsNatureRemoTemperatureSensor(HacsNatureRemoDeviceEntity, SensorEntity):
    """Implementation of a Nature Remo sensor."""
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: HacsNatureRemoDataUpdateCoordinator, idx: str):
        HacsNatureRemoDeviceEntity.__init__(self, coordinator, idx)
        self._attr_name = self._base_name.strip() + " Temperature"
        LOGGER.debug(f"device initialize: {self._attr_name}")
        self._attr_unique_id = f"{self.device.id}-te"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_data()
        self._attr_native_value: float = self.device.newest_events.get("te").val
        LOGGER.debug(f"{self._attr_unique_id}: updated to {self._attr_native_value}")
        self.async_write_ha_state()


class HacsNatureRemoHumiditySensor(HacsNatureRemoDeviceEntity, SensorEntity):
    """Implementation of a Nature Remo sensor."""
    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unit_of_measurement = PERCENTAGE

    def __init__(self, coordinator: HacsNatureRemoDataUpdateCoordinator, idx: str):
        HacsNatureRemoDeviceEntity.__init__(self, coordinator, idx)
        self._attr_name = self._base_name.strip() + " Humidity"
        LOGGER.debug(f"device initialize: {self._attr_name}")
        self._attr_unique_id = f"{self.device.id}-hu"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_data()
        self._attr_native_value: float = self.device.newest_events.get("hu").val
        LOGGER.debug(f"{self._attr_unique_id}: updated to {self._attr_native_value}")
        self.async_write_ha_state()

    # async def async_update(self) -> None:
    #     """Fetch new state data for the sensor.
    #
    #     This is the only method that should fetch new data for Home Assistant.
    #     """
    #     await super().async_update()
    #     self._attr_native_value: float = self.device.newest_events.get("hu").val


class HacsNatureRemoIlluminanceSensor(HacsNatureRemoDeviceEntity, SensorEntity):
    """Implementation of a Nature Remo sensor."""
    _attr_device_class = SensorDeviceClass.ILLUMINANCE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unit_of_measurement = LIGHT_LUX

    def __init__(self, coordinator: HacsNatureRemoDataUpdateCoordinator, idx: str):
        HacsNatureRemoDeviceEntity.__init__(self, coordinator, idx)
        self._attr_name = f"Nature Remo Illuminance: {self._attr_unique_id}"
        self._attr_name = self._base_name.strip() + " Illuminance"
        LOGGER.debug(f"device initialize: {self._attr_name}")
        self._attr_unique_id = f"{self._attr_unique_id}-il"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_data()
        self._attr_native_value: float = self.device.newest_events.get("il").val
        LOGGER.debug(f"{self._attr_unique_id}: updated to {self._attr_native_value}")
        self.async_write_ha_state()
