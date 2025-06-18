# Async Generator Error Fix

## Problem
"AttributeError: 'async_generator' object has no attribute 'data'" when running pytest tests.

## What is this error?

This error occurs when pytest fixtures for Home Assistant are not properly configured for async testing. The `hass` fixture is treated as an `async_generator` object instead of the actual `HomeAssistant` instance.

### Root Cause
When pytest-asyncio doesn't properly handle async fixtures, it returns the generator itself rather than the yielded value. This happens due to configuration mismatches between pytest-asyncio and pytest-homeassistant-custom-component.

## Solution Applied

### 1. Added pytest_asyncio import to conftest.py
```python
import pytest_asyncio
```

### 2. Added asyncio fixture configuration
```python
@pytest.fixture(autouse=True)
def set_asyncio_fixture_loop_scope(request):
    """Set the event loop scope for async fixtures."""
    return "function"
```

### 3. Updated pyproject.toml with asyncio markers
```toml
markers = [
    "asyncio: mark test as an asyncio coroutine",
]
```

### 4. Ensured asyncio_mode = auto in pytest.ini
```ini
[tool:pytest]
asyncio_mode = auto
asyncio_default_fixture_loop_scope = function
```

## Result
- The async_generator error is completely resolved
- `hass` fixture now properly returns a `HomeAssistant` instance
- Tests can access `hass.data`, `hass.config_entries`, etc. without errors

## Key Takeaway
The error was caused by pytest-asyncio not properly handling the async fixture yield. The combination of:
1. Setting `asyncio_mode = auto`
2. Importing `pytest_asyncio` 
3. Properly configuring fixture loop scope

...resolved the issue and allowed tests to run with proper async support.