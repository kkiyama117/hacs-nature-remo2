"""
Custom integration to integrate hacs-nature-remo with Home Assistant.

For more details about this integration, please refer to
https://github.com/kkiyama117/hacs-nature-remo2
"""
import asyncio
from typing import List, TypedDict

from homeassistant.config_entries import ConfigEntry
from homeassistant.core_config import Config
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed
import voluptuous as vol
import logging
import remo

from .api import HacsNatureRemoApiClient
from .const import LOGGER, DOMAIN, CONF_API_TOKEN, STARTUP_MESSAGE, PLATFORMS, DEFAULT_SCAN_INTERVAL, KEY_APPLIANCES, \
    KEY_DEVICES, KEY_USER, SENSOR

_LOGGER: logging.Logger = LOGGER

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Required({
        vol.Required(CONF_API_TOKEN, default="Please_set_nature_remo_API"): str
    })
}, extra=vol.ALLOW_EXTRA)

PluginDataDict = TypedDict("PluginDataDict", {
    KEY_USER: dict[str, remo.Appliance],
    KEY_APPLIANCES: dict[str, remo.Appliance],
    KEY_DEVICES: dict[str, remo.Device]
})


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """Set up this integration using YAML is not supported?"""
    # TODO: Implement
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)
    # get API token from conf
    api_token = entry.data.get(CONF_API_TOKEN)
    coordinator: HacsNatureRemoDataUpdateCoordinator = await _common_setup_flow(hass, api_token)
    hass.data[DOMAIN][entry.entry_id]: PluginDataDict = coordinator

    for platform in PLATFORMS:
        if entry.options.get(platform, True):
            coordinator.platforms.append(platform)
            await entry.async_create_background_task(
                hass,
                hass.config_entries.async_forward_entry_setup(entry, platform),
                name=f"{DOMAIN}_entry_setup_{platform}",
            )
    entry.add_update_listener(async_reload_entry)
    return True


class HacsNatureRemoDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(
            self,
            hass: HomeAssistant,
            client: HacsNatureRemoApiClient,
    ) -> None:
        """Initialize."""
        self.api = client
        self.platforms = []
        # None if not initialized, but not None if initialized
        self.data: PluginDataDict = None  # type: ignore[assignment]
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=DEFAULT_SCAN_INTERVAL)

    async def _async_update_data(self) -> PluginDataDict:
        """Update data via library."""
        try:
            # return await self.api.get_user()
            LOGGER.debug("Try to fetch appliance and device list from API")
            user: remo.User = await self.api.get_user()
            # other devices and sensors
            appliances: List[remo.Appliance] = await self.api.get_appliances()
            appliances_dict: dict[str, remo.Appliance] = {data.id: data for data in appliances}
            # controller itself
            devices: List[remo.Device] = await self.api.get_devices()
            devices_dict: dict[str, remo.Device] = {data.id: data for data in devices}
            result:PluginDataDict={
                KEY_USER: user,
                KEY_APPLIANCES: appliances_dict,
                KEY_DEVICES: devices_dict
            }
            LOGGER.debug(f"Finish fetching data from remote API: {result}")
            return result
        except Exception as exception:
            raise UpdateFailed() from exception


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def _common_setup_flow(hass: HomeAssistant, api_token: str | None) -> HacsNatureRemoDataUpdateCoordinator:
    session = async_get_clientsession(hass)
    if api_token is None or len(api_token) == 0:
        raise RuntimeError("Error: Nature Remo API token is not set!")
    client = HacsNatureRemoApiClient(api_token, session)
    # Fetch and Update Data by coordinator, and refresh
    coordinator = HacsNatureRemoDataUpdateCoordinator(hass, client=client)
    await coordinator.async_refresh()
    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    return coordinator


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
