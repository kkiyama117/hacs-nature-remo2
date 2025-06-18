# Pytest Error Fix Plan

## Problem Summary
The tests are using a generic template structure that doesn't match the actual Nature Remo API implementation. Key mismatches include:
- Wrong constructor arguments
- Non-existent methods being mocked
- Incorrect API endpoints
- Missing async test markers

## Fix Strategy

### Phase 1: Update Test Fixtures (Priority: High)

#### 1.1 Fix API Client Initialization in conftest.py
**File**: `tests/conftest.py`
**Issue**: Constructor expects 4 args, tests provide 3
**Fix**: Update all API client instantiations to:
```python
api = HacsNatureRemoApiClient(
    access_token="test_token",
    session=session,
    nature_remo_api_version=NatureRemoAPIVersion.V1,
    debug=False
)
```

#### 1.2 Replace Mock Methods
**Current**: Mocking `async_get_data()` which doesn't exist
**Fix**: Mock actual Nature Remo methods:
- `get_user()`
- `get_devices()`
- `get_appliances()`
- `update_aircon_settings()`
- `send_light_turn_on_signal()`
- `send_light_turn_off_signal()`

### Phase 2: Fix Async Test Configuration (Priority: High)

#### 2.1 Add Async Markers
**Files**: `test_api.py`, `test_config_flow.py`, `test_switch.py`
**Fix**: Add `@pytest.mark.asyncio` decorator to all async test functions

#### 2.2 Configure pytest-asyncio
**File**: `pytest.ini` or `pyproject.toml`
**Fix**: Add configuration:
```ini
[tool.pytest.ini_options]
asyncio_default_fixture_loop_scope = "function"
```

### Phase 3: Update Test Logic (Priority: Medium)

#### 3.1 Update test_api.py
- Remove jsonplaceholder.typicode.com references
- Test actual Nature Remo API endpoints
- Mock responses should match Nature Remo API format

#### 3.2 Update test_config_flow.py
- Fix fixtures to return proper Nature Remo data structures
- Test should validate API token with actual Nature Remo methods

#### 3.3 Update test_switch.py
- Use correct methods for switch operations
- Mock `send_light_turn_on_signal()` and `send_light_turn_off_signal()`

### Phase 4: Create Proper Test Data (Priority: Medium)

#### 4.1 Define Test Fixtures
Create realistic test data matching Nature Remo API responses:
- User data structure
- Device data (with sensors)
- Appliance data (AC, lights, etc.)

### Implementation Order

1. **Immediate fixes** (breaks all tests):
   - Fix API client constructor arguments
   - Add pytest.mark.asyncio decorators

2. **Core functionality** (makes tests runnable):
   - Update mock method names
   - Fix fixture return values

3. **Complete test coverage**:
   - Update test logic to match actual API
   - Add comprehensive test data

## Expected Outcomes

After implementing these fixes:
- All 7 tests should run without setup errors
- Async tests will execute properly
- Tests will validate actual Nature Remo functionality
- No deprecation warnings

## Additional Recommendations

1. Consider using `pytest-homeassistant-custom-component` fixtures for consistency
2. Add integration tests with actual API responses
3. Create a mock Nature Remo API server for comprehensive testing
4. Document test structure in `.claude/project-knowledge.md`