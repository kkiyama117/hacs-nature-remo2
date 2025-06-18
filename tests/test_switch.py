"""Test hacs-nature-remo switch."""

from unittest.mock import AsyncMock, Mock, patch

import pytest
from custom_components.hacs_nature_remo.coordinators import HacsNatureRemoDataUpdateCoordinator
from custom_components.hacs_nature_remo.domain.const import DEFAULT_NAME, DOMAIN, SWITCH
from custom_components.hacs_nature_remo.domain.config_schema import KEY_APPLIANCES, KEY_DEVICES, KEY_USER
from custom_components.hacs_nature_remo.switch import NatureRemoIR


@pytest.fixture
def mock_coordinator(hass):
    """Create a mock coordinator with IR appliance data."""
    # Create mock API client
    mock_api = Mock()
    mock_api.send_signal = AsyncMock(return_value=None)
    
    # Create mock user object
    mock_user = Mock()
    mock_user.id = "test_user_id"
    mock_user.nickname = "test_username"
    
    # Create mock device object
    mock_device = Mock()
    mock_device.id = "device1"
    mock_device.name = "Test Device"
    mock_device.newest_events = {}  # Empty events for sensor platform
    
    # Create mock IR appliance with signals
    mock_signal_on = Mock()
    mock_signal_on.id = "signal_on_id"
    mock_signal_on.name = "ON"
    mock_signal_on.image = "ico_onico_io"
    
    mock_signal_off = Mock()
    mock_signal_off.id = "signal_off_id"
    mock_signal_off.name = "OFF"
    mock_signal_off.image = "ico_offico_io"
    
    # Create mock device core for appliance
    mock_device_core = Mock()
    mock_device_core.id = "device_core_1"
    mock_device_core.name = "Test Device"
    mock_device_core.serial_number = "12345"
    mock_device_core.firmware_version = "1.0.0"
    
    mock_appliance = Mock()
    mock_appliance.id = "appliance1"
    mock_appliance.nickname = DEFAULT_NAME
    mock_appliance.type = "IR"
    mock_appliance.signals = [mock_signal_on, mock_signal_off]
    mock_appliance.device = mock_device_core
    
    # Create coordinator
    coordinator = HacsNatureRemoDataUpdateCoordinator(hass, mock_api)
    coordinator.data = {
        KEY_USER: mock_user,
        KEY_DEVICES: {"device1": mock_device},
        KEY_APPLIANCES: {"appliance1": mock_appliance}
    }
    coordinator.async_request_refresh = AsyncMock()
    
    return coordinator, mock_api


async def test_switch_entity(hass, mock_coordinator):
    """Test NatureRemoIR switch entity."""
    coordinator, mock_api = mock_coordinator
    
    # Create switch entity
    switch = NatureRemoIR(coordinator, "appliance1")
    switch.hass = hass
    
    # Test entity properties
    assert switch.name == f"Nature Remo Test Device {SWITCH}"
    assert switch.unique_id == "appliance1"
    assert switch.assumed_state is True
    
    # Test turn on
    await switch.async_turn_on()
    mock_api.send_signal.assert_called_with("signal_on_id")
    assert switch.is_on is True
    
    # Reset mock
    mock_api.send_signal.reset_mock()
    
    # Test turn off
    await switch.async_turn_off()
    mock_api.send_signal.assert_called_with("signal_off_id")
    assert switch.is_on is False


async def test_switch_entity_no_matching_signal(hass, mock_coordinator):
    """Test switch entity when signals don't match expected images."""
    coordinator, mock_api = mock_coordinator
    
    # Modify signals to have different images
    appliance = coordinator.data[KEY_APPLIANCES]["appliance1"]
    for signal in appliance.signals:
        signal.image = "unknown_image"
    
    # Create switch entity
    switch = NatureRemoIR(coordinator, "appliance1")
    switch.hass = hass
    
    # Test turn on - should not call API when no matching signal
    await switch.async_turn_on()
    mock_api.send_signal.assert_not_called()
    
    # Test turn off - should not call API when no matching signal
    await switch.async_turn_off()
    mock_api.send_signal.assert_not_called()


async def test_async_setup_entry(hass, mock_coordinator):
    """Test async_setup_entry for switch platform."""
    coordinator, _ = mock_coordinator
    
    from custom_components.hacs_nature_remo.switch import async_setup_entry
    
    # Mock config entry
    config_entry = Mock()
    config_entry.entry_id = "test"
    
    # Set up coordinator in hass data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = coordinator
    
    # Track entities added
    entities_added = []
    
    def mock_async_add_entities(entities):
        """Mock async add entities."""
        entities_added.extend(entities)
    
    # Call async_setup_entry
    await async_setup_entry(hass, config_entry, mock_async_add_entities)
    
    # Verify that one switch entity was created for the IR appliance
    assert len(entities_added) == 1
    assert isinstance(entities_added[0], NatureRemoIR)
    assert entities_added[0].unique_id == "appliance1"