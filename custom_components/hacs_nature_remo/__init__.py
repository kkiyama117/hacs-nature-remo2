"""
Custom integration to integrate hacs-nature-remo with Home Assistant.

For more details about this integration, please refer to
https://github.com/kkiyama117/hacs-nature-remo2
"""

import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core_config import Config
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .coordinators import HacsNatureRemoDataUpdateCoordinator

from .domain import LOGGER
from .api import HacsNatureRemoApiClient
from .domain.config_schema import PluginDataDict, CONF_API_TOKEN_KEY
from .domain.const import (
    DOMAIN,
    STARTUP_MESSAGE,
    PLATFORMS,
    DEFAULT_SCAN_INTERVAL,
)


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """Set up this integration using YAML is not supported?"""
    # TODO: Implement
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        LOGGER.info(STARTUP_MESSAGE)
    # get API token from user config
    conf_data = entry.data
    api_token = conf_data.get(CONF_API_TOKEN_KEY)
    coordinator: HacsNatureRemoDataUpdateCoordinator = await _common_setup_flow(
        hass, api_token
    )
    hass.data[DOMAIN][entry.entry_id]: PluginDataDict = coordinator
    coordinator.platforms = [
        platform for platform in PLATFORMS if entry.options.get(platform, True)
    ]
    entry.async_create_background_task(
        hass,
        hass.config_entries.async_forward_entry_setups(entry, coordinator.platforms),
        name=f"{DOMAIN}_entry_setup_all",
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


async def _common_setup_flow(
    hass: HomeAssistant, api_token: str | None
) -> HacsNatureRemoDataUpdateCoordinator:
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
