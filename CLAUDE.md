# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
When `/init` is called, Update this file. In particular, be sure to update the section enclosed by "~-" and "-~" according to the instructions therein. Then, delete the original instructions written between "~-" and "-~"

## Repository Overview

~- This is the overview of repository. Please rewrite this to suit this project. -~

## Repository Structure

~- This is the overview of `.claude`. make their files and create if it does not exist.  -~
- `.claude/` - Knowledge management system for Claude Code containing:
  - `context.md` - Project background.
  - `project-knowledge.md` - Technical insights and patterns to implement program in this repository and write constraint of repository also.
  - `project-improvements.md` - Improvement history and lessons learned
  - `common-patterns.md` - Frequently used command patterns especially called with claude in this project
  - `debug-log.md` - Important debug records and log.
    - If you took over 30 minutes to resolve some issue, need to write about description and how to resolve it here.
  - `debug/` - Directory for session-specific logs and archives to remind or tell what was doing and done.
~- For the remaining directories, list the structure excluding those specified in gitignore. -~

## Development Tools and Commands

~- Update this chapter to match the tools that are actually being used. -~

### Python Package

The repository includes a sophisticated Python package for prompt generation with the following tools:

1. **uv** - Fast Python package installer and resolver
   - Install dependencies: `uv sync`
   - Install with dev dependencies: `uv sync --all-extras --dev`

2. **Task** (Taskfile.yml) - Task runner for common operations
   ```bash
   task install         # Install dependencies
   task test            # Run tests
   task lint            # Run ruff linter
   task format          # Format code with ruff
   task build           # Build the package
   ```

3. **Testing**
   - Framework: pytest with ~98% code coverage
   - Run tests: `uv run pytest`
   - Coverage report: `uv run pytest --cov`

4. **Linting and Formatting**
   - Tool: ruff (configured in pyproject.toml)
   - Check: `uv run ruff check src tests`
   - Format: `uv run ruff format src tests`


## Architecture and Important Patterns

~- Update this chapter to match the tools that are actually being used. -~

### High-Level Architecture

1. **Package Structure** :
~- Update this chapter to match the tools that are actually being used. -~
~- example:  - `anthropic_client.py` - Claude API integration -~

3. **Key Design Patterns**:
~- Update this chapter to match the tools that are actually being used. -~
~- example
   - **Strategy Pattern**: Different generators (MetapromptGenerator, TemplateGenerator) implementing BaseGenerator
   - **Repository Pattern**: Separate file handling logic in utils/file_handler.py
   - **Configuration Management**: Environment variables via .env files with ConfigManager
   - **Type Safety**: Full type hints with py.typed marker
   example end -~ 


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
- The runner package is a fully-featured Python package with CI/CD, not just scripts
- Maintain type hints - the package includes py.typed for type checking
- Run tests before committing - aim to maintain >95% coverage
- Use the Task commands for consistency across development operations
- Update documentation when adding new development tools or changing workflows
- The package supports both online (AI-powered) and offline (template-based) prompt generation
- Use the knowledge management system in `.claude/` to maintain continuity across sessions
- Update relevant knowledge files when discovering new patterns or solutions

### Runner Package Development Guidelines

When working with the runner package:

1. **Maintain Type Hints**: The package includes py.typed, so ensure all new code includes proper type annotations
2. **Follow Existing Patterns**: 
   - Use the established class structure (PromptGenerator, TemplateManager, AnthropicPromptEngineer)
   - Maintain separation of concerns between core functionality, templates, and guidelines
3. **Testing**: Use `uv run pytest` to run the comprehensive test suite with 98% coverage
4. **Documentation**: Update the `README.md` when adding new features or changing APIs
5. **Error Handling**: Provide clear error messages, especially for template not found or invalid parameter scenarios

## CI/CD Pipeline

GitHub Actions workflows:
- **test.yml**: Runs on push/PR - linting, formatting, tests across Python 3.9-3.13
- **release.yml**: Automated package releases to GitHub
- **claude.yml**: Additional Claude-specific workflows

The CI pipeline includes:
- Linting with ruff
- Testing across multiple Python versions (3.9, 3.12, 3.13)
- Coverage reporting to Codecov
- Package building and distribution artifact upload