import remo
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed

from .api import HacsNatureRemoApiClient
from .domain import LOGGER
from .domain.config_schema import KEY_APPLIANCES
from .domain.config_schema import KEY_DEVICES
from .domain.config_schema import KEY_USER
from .domain.config_schema import PluginDataDict
from .domain.const import DEFAULT_SCAN_INTERVAL
from .domain.const import DOMAIN


class HacsNatureRemoDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: HacsNatureRemoApiClient,
    ) -> None:
        """Initialize."""
        self._api: HacsNatureRemoApiClient = client
        self.platforms = []
        # None if not initialized, but not None if initialized
        self.data: PluginDataDict = None  # type: ignore[assignment]
        super().__init__(
            hass, LOGGER, name=DOMAIN, update_interval=DEFAULT_SCAN_INTERVAL
        )

    async def _async_update_data(self) -> PluginDataDict:
        """Update data via library."""
        try:
            # return await self.api.get_user()
            LOGGER.debug("Try to fetch appliance and device list from API")
            if self.data is None or self.data.get(KEY_USER) is None:
                user: remo.User = await self._api.get_user()
            else:
                user: remo.User = self.data.get(KEY_USER)

            # other devices and sensors
            appliances: list[remo.Appliance] = await self._api.get_appliances()
            appliances_dict: dict[str, remo.Appliance] = {
                data.id: data for data in appliances
            }
            # controller itself
            devices: list[remo.Device] = await self._api.get_devices()
            devices_dict: dict[str, remo.Device] = {data.id: data for data in devices}
            result: PluginDataDict = {
                KEY_USER: user,
                KEY_APPLIANCES: appliances_dict,
                KEY_DEVICES: devices_dict,
            }
            LOGGER.debug(f"Finish fetching data from remote API: {result}")
            return result
        except Exception as exception:
            raise UpdateFailed() from exception

    def raw_api(self) -> HacsNatureRemoApiClient:
        return self._api
