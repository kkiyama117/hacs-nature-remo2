from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

"""Sample API Client."""
import asyncio
import logging
import socket

import aiohttp
import async_timeout
from remo import NatureRemoError
from remo.models import *
from ..const import NATURE_REMO_API_BASE_URL, NATURE_REMO_API_TIMEOUT_SEC

BASE_URL = NATURE_REMO_API_BASE_URL
__version__ = ""
__url__ = ""

_LOGGER: logging.Logger = logging.getLogger(__package__)
HEADERS = {"Content-type": "application/json; charset=UTF-8"}
LOCAL_HEADERS = {
    "Accept": "application/json",
    "X-Requested-With": f"nature-remo/{__version__} ({__url__})",
}


def enable_debug_mode():
    import logging
    from http.client import HTTPConnection

    HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)


@dataclass
class RateLimit:
    checked_at: Optional[datetime] = None
    limit: Optional[int] = None
    remaining: Optional[int] = None
    reset: Optional[datetime] = None


class HacsNatureRemoApiClient:
    def __init__(
            self,
            access_token: str,
            session: aiohttp.ClientSession,
            nature_remo_api_version: str = "1",
            debug: bool = False
    ) -> None:
        if debug:
            enable_debug_mode()
        # http session
        self._session = session
        self.access_token = access_token
        self.url = f"{BASE_URL}/{nature_remo_api_version}"
        self.rate_limit = RateLimit()
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "User-Agent": f"nature-remo/{__version__} ({__url__})",
        }

    # USER =============================================================================================================
    async def get_user(self) -> User:
        """Fetch the authenticated user's information.

        Returns:
            A User object.
        """
        endpoint = f"{self.url}/users/me"
        try:
            response = await self.api_wrapper_json("get", endpoint)
            return UserSchema().load(response)
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    async def update_user(self, nickname: str) -> User:
        """Update authenticated user's information.

        Args:
            nickname: User's nickname.

        Returns:
            A User object.
        """
        endpoint = f"{self.url}/users/me"
        try:
            response = await self.api_wrapper_json("post", endpoint, data={"nickname": nickname})
            return UserSchema().load(response)
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    # DEVICES ==========================================================================================================
    async def get_devices(self) -> List[Device]:
        """Fetch the list of Remo devices the user has access to.

        Returns:
            A List of Device objects.
        """
        endpoint = f"{self.url}/devices"
        try:
            response = await self.api_wrapper_json("get", endpoint)
            return DeviceSchema(many=True).load(response)
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    async def update_device(self, device: str, name: str):
        """Update Remo.

        Args:
            device: Device ID.
            name: Device name.
        """
        endpoint = f"{self.url}/devices/{device}"
        try:
            await self.api_wrapper_json("post", endpoint, data={"name": name})
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    async def delete_device(self, device: str):
        """Delete Remo.

        Args:
            device: Device ID.
        """
        endpoint = f"{self.url}/devices/{device}/delete"
        try:
            await self.api_wrapper_json("post", endpoint)
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    # OFFSETS ==========================================================================================================
    async def update_temperature_offset(self, device: str, offset: int):
        """Update temperature offset.

        Args:
            device: Device ID.
            offset: Temperature offset value added to the measured temperature.
        """
        endpoint = f"{self.url}/devices/{device}/temperature_offset"
        try:
            await self.api_wrapper_json("post", endpoint, data={"offset": offset})
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    async def update_humidity_offset(self, device: str, offset: int):
        """Update humidity offset.

        Args:
            device: Device ID.
            offset: Temperature offset value added to the measured humidity
        """
        endpoint = f"{self.url}/devices/{device}/humidity_offset"
        try:
            await self.api_wrapper_json("post", endpoint, data={"offset": offset})
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    # APPLIANCES =======================================================================================================
    async def detect_appliance(self, message: str) -> List[ApplianceModelAndParams]:
        """Find the air conditioner best matching the provided infrared signal.

        Args:
            message: JSON serialized object describing infrared signals.
              Includes "data", "freq" and "format" keys.
        """
        endpoint = f"{self.url}/detectappliance"
        try:
            resp = await self.api_wrapper_json("post", endpoint, data={"message": message})
            return ApplianceModelAndParamsSchema(many=True).load(resp)
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    async def get_appliances(self) -> List[Appliance]:
        """Fetch the list of appliances.

        Returns:
            A list of Appliance objects.
        """
        endpoint = f"{self.url}/appliances"
        try:
            resp = await self.api_wrapper_json("get", endpoint, )
            return ApplianceSchema(many=True).load(resp)
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    async def create_appliance(
            self,
            device: str,
            nickname: str,
            image: str,
            model: str = None,
            model_type: str = None,
    ) -> Appliance:
        """Create a new appliance.

        Args:
            device: Device ID.
            nickname: Appliance name.
            image: Basename of the image file included in the app.
            model: ApplianceModel ID if the appliance we're trying to create
              is included in IRDB.
            model_type: Type of model.
        """
        endpoint = f"{self.url}/appliances"
        data = {"device": device, "nickname": nickname, "image": image}
        if model:
            data["model"] = model
        if model_type:
            data["model_type"] = model_type
        try:
            resp = await self.api_wrapper_json("post", endpoint, data=data)
            return ApplianceSchema().load(resp)
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    async def update_appliance_orders(self, appliances: str) -> Appliance:
        """Reorder appliances.

        Args:
            appliances: List of all appliances' IDs comma separated.
        """
        endpoint = f"{self.url}/appliance_orders"
        try:
            resp = await self.api_wrapper_json("post", endpoint, data={"appliances": appliances})
            return ApplianceSchema().load(resp)
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    async def update_appliance(
            self, appliance: str, nickname: str, image: str
    ) -> Appliance:
        """Update appliance.

        Args:
            appliance: Appliance ID.
            nickname: Appliance name.
            image: Basename of the image file included in the app.
        """
        endpoint = f"{self.url}/appliances/{appliance}"
        try:
            resp = await self.api_wrapper_json("post", endpoint,
                                               data={"nickname": nickname, "image": image})
            return ApplianceSchema().load(resp)
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    async def delete_appliance(self, appliance: str):
        """Delete appliance.

        Args:
            appliance: Appliance ID.
        """
        endpoint = f"{self.url}/appliances/{appliance}/delete"
        try:
            await self.api_wrapper_json("post", endpoint)
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    # Aircon Settings ==================================================================================================
    async def update_aircon_settings(
            self,
            appliance: str,
            operation_mode: str = None,
            temperature: str = None,
            air_volume: str = None,
            air_direction: str = None,
            button: str = None,
    ):
        """Update air conditioner settings.

        Args:
            appliance: Appliance ID.
            operation_mode: AC operation mode.
            temperature: Temperature.
            air_volume: AC air volume.
            air_direction: AC air direction.
            button: Button.
        """
        endpoint = f"{self.url}/appliances/{appliance}/aircon_settings"
        data = {}
        if operation_mode:
            data["operation_mode"] = operation_mode
        if temperature:
            data["temperature"] = temperature
        if air_volume:
            data["air_volume"] = air_volume
        if air_direction:
            data["air_direction"] = air_direction
        if button:
            data["button"] = button
        try:
            await self.api_wrapper_json("post", endpoint, data=data)
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    # TV ===============================================================================================================
    async def send_tv_infrared_signal(self, appliance: str, button: str):
        """Send tv infrared signal.

        Args:
            appliance: Appliance ID.
            button: Button name.
        """
        endpoint = f"{self.url}/appliances/{appliance}/tv"
        try:
            await self.api_wrapper_json("post", endpoint, data={"button": button})
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    # Light ============================================================================================================
    async def send_light_infrared_signal(self, appliance: str, button: str):
        """Send light infrared signal.

        Args:
            appliance: Appliance ID.
            button: Button name.
        """
        endpoint = f"{self.url}/appliances/{appliance}/light"
        try:
            await self.api_wrapper_json("post", endpoint, data={"button": button})
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    # SIGNALS ==========================================================================================================
    async def get_signals(self, appliance: str) -> List[Signal]:
        """Fetch signals registered under this appliance.

        Args:
            appliance: Appliance ID.
        """
        endpoint = f"{self.url}/appliances/{appliance}/signals"
        try:
            response = await self.api_wrapper_json("get", endpoint)
            return SignalSchema(many=True).load(response)
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    async def create_signal(
            self, appliance: str, name: str, message: str, image: str
    ) -> Signal:
        """Create a signal under this appliance.

        Args:
            appliance: Appliance ID.
            name: Signal name.
            message: JSON serialized object describing infrared signals.
              Includes "data", "freq" and "format" keys.
            image: Basename of the image file included in the app.
        """
        endpoint = f"{self.url}/appliances/{appliance}/signals"
        try:

            response = await self.api_wrapper_json(
                "post", endpoint, data={"name": name, "message": message, "image": image},
            )
            return SignalSchema().load(response)
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    async def update_signal_orders(self, appliance: str, signals: str):
        """Reorder signals under this appliance.

        Args:
            appliance: Appliance ID.
            signals: List of all signals' IDs comma separated.
        """
        endpoint = f"{self.url}/appliances/{appliance}/signal_orders"
        try:
            await self.api_wrapper_json(
                "post", endpoint, data={"signals": signals},
            )
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    async def update_signal(self, signal: str, name: str, image: str):
        """Update infrared signal.

        Args:
            signal: Signal ID.
            name: Signal name.
            image: Basename of the image file included in the app.
        """
        endpoint = f"{self.url}/signals/{signal}"
        try:
            await self.api_wrapper_json(
                "post", endpoint, data={"name": name, "image": image}
            )
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    async def delete_signal(self, signal: str):
        """Delete infrared signal.

        Args:
            signal: Signal ID.
        """
        endpoint = f"{self.url}/signals/{signal}/delete"
        try:
            await self.api_wrapper_json("post", endpoint)
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    async def send_signal(self, signal: str):
        """Send infrared signal.

        Args:
            signal: Signal ID.
        """
        endpoint = f"{self.url}/signals/{signal}/send"
        try:
            await self.api_wrapper_json("post", endpoint)
        except Exception as e:
            _LOGGER.error(f"Error: {e}")

    # ------------------------------------------------------------------------------------------------------------------
    async def api_wrapper_json(self, method: str, url: str, data: dict = None, headers: dict = None) -> dict | None:
        try:
            api_response = await self.api_wrapper(method, url, data, headers, is_raise_error=True)
            return api_response
        except Exception as e:
            _LOGGER.error(f"Json Error: {e}")
            raise NatureRemoError()

    async def api_wrapper(
            self, method: str, url: str, data: dict = None, headers: dict = None,
            is_raise_error: bool = False
    ) -> dict:
        """Get information from the API."""
        if headers is None:
            headers = self.headers
        else:
            headers = headers
        if data is None:
            data = {}
        else:
            data = data
        try:
            async with async_timeout.timeout(NATURE_REMO_API_TIMEOUT_SEC):
                if method == "get":
                    response = await self._session.get(url, headers=headers)
                elif method == "put":
                    response = await self._session.put(url, headers=headers, json=data)
                elif method == "patch":
                    response = await self._session.patch(url, headers=headers, json=data)
                elif method == "post":
                    response = await self._session.post(url, headers=headers, json=data)
                self.__set_api_rate_limit(response)
                return await response.json()

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                url,
                exception,
            )
            if is_raise_error:
                raise exception

        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
            if is_raise_error:
                raise exception

        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )
            if is_raise_error:
                raise exception

        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)
            if is_raise_error:
                raise exception

    def __set_api_rate_limit(self, response: aiohttp.ClientResponse) -> None:
        """Set the rate limit information from the API."""
        if "Date" in response.headers:
            self.rate_limit.checked_at = datetime.strptime(
                response.headers["Date"], "%a, %d %b %Y %H:%M:%S GMT"
            )
        if "X-Rate-Limit-Limit" in response.headers:
            self.rate_limit.limit = int(response.headers["X-Rate-Limit-Limit"])
        if "X-Rate-Limit-Remaining" in response.headers:
            self.rate_limit.remaining = int(
                response.headers["X-Rate-Limit-Remaining"]
            )
        if "X-Rate-Limit-Reset" in response.headers:
            self.rate_limit.reset = datetime.utcfromtimestamp(
                int(response.headers["X-Rate-Limit-Reset"])
            )
