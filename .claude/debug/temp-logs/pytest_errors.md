# Pytest Error Report - 2025-06-18

## Summary
- **Total tests collected**: 7
- **Tests with errors**: 4
- **Tests skipped**: 3
- **Warnings**: 3
- **Critical issue**: AttributeError with `async_get_data` method

## Error Details

### 1. AttributeError: Missing `async_get_data` Method

**Affected Tests**:
1. `tests/test_config_flow.py::test_successful_config_flow`
2. `tests/test_config_flow.py::test_failed_config_flow`
3. `tests/test_init.py::test_setup_unload_and_reload_entry`
4. `tests/test_init.py::test_setup_entry_exception`

**Error Message**:
```
AttributeError: <class 'custom_components.hacs_nature_remo.api.HacsNatureRemoApiClient'> does not have the attribute 'async_get_data'
```

**Location**: 
- Error originates from `tests/conftest.py` lines 28 and 39
- In fixtures `bypass_get_data_fixture` and `error_get_data_fixture`

**Root Cause**:
The test fixtures are trying to patch a method `async_get_data` that doesn't exist in the `HacsNatureRemoApiClient` class.

### 2. Async Test Warnings

**Affected Tests**:
1. `tests/test_api.py::test_api`
2. `tests/test_config_flow.py::test_options_flow`
3. `tests/test_switch.py::test_switch_services`

**Warning Message**:
```
PytestUnhandledCoroutineWarning: async def functions are not natively supported and have been skipped.
```

**Issue**: These tests are defined as async functions but the test is not properly marked for async execution.

### 3. Configuration Warning

**Warning**:
```
PytestDeprecationWarning: The configuration option "asyncio_default_fixture_loop_scope" is unset.
```

**Location**: `pytest_asyncio/plugin.py:217`

## Error Analysis

### Primary Issue: API Method Mismatch
The test fixtures in `conftest.py` are attempting to mock a method called `async_get_data` on the `HacsNatureRemoApiClient` class, but this method doesn't exist. This suggests either:
1. The API client implementation has changed and the method was renamed/removed
2. The tests are outdated and referencing an old API structure

### Secondary Issue: Async Test Configuration
Several tests are defined as async functions but are not being run properly due to missing async markers or configuration issues.

## Files Requiring Investigation

1. **`custom_components/hacs_nature_remo/api.py`** or API client file
   - Need to check actual method names available
   - Identify the correct method to mock

2. **`tests/conftest.py`**
   - Lines 28 and 39 contain the problematic patches
   - Need to update to use correct method name

3. **`tests/test_api.py`**, **`tests/test_config_flow.py`**, **`tests/test_switch.py`**
   - Need to add proper async test markers

4. **`pytest.ini`** or test configuration
   - May need to set `asyncio_default_fixture_loop_scope`

## Next Steps for Fix Planning

1. **Investigate API Client Structure**
   - Check what methods are actually available in `HacsNatureRemoApiClient`
   - Find the equivalent of `async_get_data` method

2. **Update Test Fixtures**
   - Modify `bypass_get_data_fixture` and `error_get_data_fixture` to use correct method names
   - Ensure mocking strategy aligns with current API structure

3. **Fix Async Test Configuration**
   - Add appropriate pytest markers (`@pytest.mark.asyncio`) to async tests
   - Configure pytest-asyncio properly in configuration file

4. **Validate Test Structure**
   - Ensure all async tests follow Home Assistant testing patterns
   - Check if any other fixtures need updates