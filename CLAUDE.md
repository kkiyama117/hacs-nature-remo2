# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Home Assistant Custom Component (HACS) for integrating Nature Remo smart home devices with Home Assistant. Nature Remo is a device that can control air conditioners, lights, and other appliances via infrared signals and smart integrations.

**Key Facts:**
- Domain: `hacs_nature_remo`
- Version: 0.1.1
- Integration type: Cloud Polling (requires Nature Remo API token)
- Supported platforms: Climate, Sensor, Switch
- Configuration: UI-based (config flow)

## Repository Structure

- `.claude/` - Knowledge management system for Claude Code containing:
  - `context.md` - Project background.
  - `project-knowledge.md` - Technical insights and patterns to implement program in this repository and write constraint of repository also.
  - `project-improvements.md` - Improvement history and lessons learned
  - `common-patterns.md` - Frequently used command patterns especially called with claude in this project
  - `debug-log.md` - Important debug records and log.
    - If you took over 30 minutes to resolve some issue, need to write about description and how to resolve it here.
  - `debug/` - Directory for session-specific logs and archives to remind or tell what was doing and done.
- `custom_components/hacs_nature_remo/` - Main integration code
  - `api/` - Nature Remo API client implementation
  - `domain/` - Business logic, constants, and configuration schemas
  - `coordinators.py` - DataUpdateCoordinator for efficient data fetching
  - `climate.py`, `sensor.py`, `switch.py` - Entity platform implementations
  - `config_flow.py` - UI configuration flow
  - `translations/` - Multi-language support (en, fr, ja, nb)
- `tests/` - Comprehensive test suite with fixtures and mocks
- `.github/workflows/` - CI/CD pipelines for testing, linting, and validation

## Development Tools and Commands

### Setup and Dependencies

```bash
# Install development dependencies
pip install -r requirements_dev.txt
pip install -r requirements_test.txt

# Install the custom component in development mode
pip install -e .
```

### Testing

```bash
# Run full test suite with parallel execution
pytest --timeout=9 --durations=10 -n auto -p no:sugar tests

# Run specific test file
pytest tests/test_climate.py

# Run with coverage report
pytest --cov=custom_components.hacs_nature_remo --cov-report=html

# Run a single test
pytest tests/test_climate.py::test_climate_entity_setup
```

### Code Quality

```bash
# Run all pre-commit hooks (formatting, linting, type checking)
pre-commit run --all-files

# Run specific checks
flake8 custom_components/hacs_nature_remo
black custom_components/hacs_nature_remo --check
isort custom_components/hacs_nature_remo --check-only
```

### Validation

```bash
# Validate Home Assistant integration requirements
python -m script.hassfest

# Validate HACS requirements
python -m pytest tests/test_hacs.py
```

## Architecture and Important Patterns

### High-Level Architecture

1. **API Layer** (`api/`):
   - `NatureRemoAPI` - HTTP client for Nature Remo cloud API
   - Uses custom fork: `nature-remo-fork-only-for-hacs-nature-remo`
   - Handles authentication and request formatting

2. **Coordinator Pattern**:
   - `ApplianceCoordinator` - Manages appliance data updates
   - `DeviceCoordinator` - Manages device sensor data
   - 30-second default update interval
   - Shared data across all entities for efficiency

3. **Entity Implementation**:
   - All entities inherit from Home Assistant base classes
   - Use coordinator data to avoid redundant API calls
   - Implement proper availability and state update patterns

### Key Design Patterns

- **DataUpdateCoordinator Pattern**: Centralized data fetching to minimize API calls and share data across entities
- **Async/Await**: Fully asynchronous integration following Home Assistant patterns
- **Config Flow**: Modern UI-based configuration with proper error handling and validation
- **Entity Registry**: Proper unique ID assignment for entity tracking across restarts
- **Translation Support**: Full i18n implementation with multiple languages

### Configuration Constraints

- Single configuration entry allowed (`single_config_entry: true`)
- Requires valid Nature Remo API token
- Cannot be configured via YAML (UI-only)
- Automatic device and entity discovery

## Knowledge Management System

This repository implements a systematic knowledge management approach for Claude Code sessions. The `.claude/` directory structure helps maintain project context, technical insights, and operational patterns across different sessions.

### How to Use the Knowledge Management System

1. **Before starting work**: Review `.claude/context.md` for project constraints and background
2. **During development**: Refer to `.claude/common-patterns.md` for frequently used commands
3. **When debugging**: Check `.claude/debug-log.md` for known issues and solutions
4. **For best practices**: Consult `.claude/project-knowledge.md` for technical insights
5. **To track progress**: Update `.claude/project-improvements.md` with new learnings

## Development Notes

When working with this repository:
- Follow Home Assistant development guidelines and entity patterns
- Maintain 100% test coverage as configured in setup.cfg
- Use the coordinator pattern for any new data sources
- Ensure all strings are translatable and added to translation files
- Test with actual Nature Remo devices when possible
- Update manifest.json version for any changes
- Follow semantic versioning for releases

### Integration Development Guidelines

1. **Entity Development**:
   - Always use unique IDs based on appliance/device IDs
   - Implement proper availability checks
   - Use coordinator data, never fetch directly in entities
   
2. **API Changes**:
   - Maintain compatibility with the Nature Remo API
   - Handle rate limiting appropriately
   - Log API errors clearly for debugging

3. **Testing**:
   - Write tests for all new functionality
   - Use the provided fixtures for consistent test data
   - Mock API calls properly using the test fixtures

## CI/CD Pipeline

GitHub Actions workflows:
- **Linting**: Pre-commit hooks, flake8, black, isort
- **HACS Validation**: Ensures compatibility with HACS
- **Hassfest**: Validates Home Assistant integration requirements
- **Tests**: Runs full test suite on multiple Python versions
- **Release Drafter**: Automated release note generation
- **Dependabot**: Automated dependency updates

The CI pipeline ensures code quality and Home Assistant compatibility before any merge.