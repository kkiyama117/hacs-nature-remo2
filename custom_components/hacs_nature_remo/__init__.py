"""
Custom integration to integrate hacs-nature-remo with Home Assistant.

For more details about this integration, please refer to
https://github.com/kkiyama117/hacs-nature-remo2
"""
import asyncio
from typing import TypedDict
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core_config import Config
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import remo

from .coordinators import HacsNatureRemoDataUpdateCoordinator

from .domain import LOGGER
from .api import HacsNatureRemoApiClient
from .domain.const import (DOMAIN, CONF_API_TOKEN, KEY_USER, KEY_APPLIANCES, KEY_DEVICES, STARTUP_MESSAGE, PLATFORMS,
                           DEFAULT_SCAN_INTERVAL)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Required({
        vol.Required(CONF_API_TOKEN, default="Please_set_nature_remo_API"): str
    })
}, extra=vol.ALLOW_EXTRA)

PluginDataDict = TypedDict("PluginDataDict", {
    KEY_USER: dict[str, remo.User],
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
        LOGGER.info(STARTUP_MESSAGE)
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
