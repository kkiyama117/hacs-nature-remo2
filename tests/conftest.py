"""Global fixtures for hacs-nature-remo integration."""

from unittest.mock import patch

import pytest

pytest_plugins = "pytest_homeassistant_custom_component"


# This fixture allows our integration to be loaded by Home Assistant during tests
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations."""
    yield


# Ensure we're using the right event loop scope
@pytest.fixture(autouse=True)
def set_asyncio_fixture_loop_scope(request):
    """Set the event loop scope for async fixtures."""
    return "function"


# This fixture is used to prevent HomeAssistant from attempting to create and dismiss persistent
# notifications. These calls would fail without this fixture since the persistent_notification
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with (
        patch("homeassistant.components.persistent_notification.async_create"),
        patch("homeassistant.components.persistent_notification.async_dismiss"),
    ):
        yield


# This fixture mocks the Nature Remo API validation methods to succeed
@pytest.fixture(name="bypass_get_data")
def bypass_get_data_fixture():
    """Mock successful API calls."""
    from unittest.mock import Mock

    # Create mock user object
    mock_user = Mock()
    mock_user.id = "test_user_id"
    mock_user.nickname = "test_username"

    # Create mock device object
    mock_device = Mock()
    mock_device.id = "device1"
    mock_device.name = "Test Device"

    with (
        patch(
            "custom_components.hacs_nature_remo.api.HacsNatureRemoApiClient.get_user",
            return_value=mock_user,
        ),
        patch(
            "custom_components.hacs_nature_remo.api.HacsNatureRemoApiClient.get_devices",
            return_value=[mock_device],
        ),
        patch(
            "custom_components.hacs_nature_remo.api.HacsNatureRemoApiClient.get_appliances",
            return_value=[],
        ),
    ):
        yield


# This fixture forces API validation to fail
@pytest.fixture(name="error_on_get_data")
def error_get_data_fixture():
    """Simulate error when retrieving data from API."""
    with patch(
        "custom_components.hacs_nature_remo.api.HacsNatureRemoApiClient.get_user",
        side_effect=Exception("Authentication failed"),
    ):
        yield
