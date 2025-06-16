# project-knowledge.md

Updated when /init is run. Update also if new knowledge is acquired.

## プロジェクトの制約

### 開発上の制約
1. uv, ruff, pytestを用いてpythonで開発する
    - 必要に応じて別の言語・ツールを用いる (例: pyo3を用いて一部の処理をRustで記述する)
2. ファイル名は目的を明確に示すように命名する必要がある

### 言語に関する制約
- ドキュメントは主に日本語/英語で記述する
    - 日本語で記載されたドキュメントなら、ファイル名の拡張子の前に`_ja`を付けて`how_to_test_ja.md`のように命名する
- プロンプト自体は用途に応じて日本語または英語を使用
    - 日本語で記載されたドキュメントなら、ファイル名の拡張子の前に`_ja`を付けて`how_to_test_ja.md`のように命名する
- 同一ファイル内では、言語の一貫性を保つことが重要. ファイル間では、必要に応じて揃える.

## 実装上の技術的洞察

### ファイル命名規則
- プロンプト: `{purpose}_{lang}.md` (例: `code_review_ja.md`)

### バージョン管理のベストプラクティス
- 意味のあるコミットメッセージ
- プロンプトの更新履歴の記録
- 効果的だった変更の文書化

## Runner Package Technical Architecture

### Unified TOML Configuration System

#### Design Principles
1. **Logical Grouping**: Configuration organized into sections ([paths], [anthropic], [application], [generation], [output], [compatibility])
2. **Backward Compatibility**: Environment variables and legacy flat TOML continue to work
3. **Security Best Practices**: API keys default to environment variables with clear warnings
4. **Sensible Defaults**: All sections optional with comprehensive defaults

### Test Suite Architecture

#### Coverage Statistics
- **ConfigManager**: 94% test coverage (up from ~60%)
- **Total Tests**: 141 tests (52 new tests added)
- **Test Files**: 3 new test files created for unified configuration

#### Test Organization

#### Key Testing Patterns
2. **Type Safety**: String to appropriate type conversion
3. **Error Handling**: Graceful degradation
4. **Integration Testing**: Configuration affects behavior

### Implementation Details


### Runner Package Build System and Tools

1. **uv** - Fast Python package installer and resolver
   - Manages dependencies and virtual environments
   - Lock file: `uv.lock` ensures reproducible builds
   - Alternative to pip/poetry/pipenv with better performance

2. **Taskfile** - Task runner for common operations
   - Defined in `runner/Taskfile.yml`
   - Provides consistent development commands
   - Includes tasks for install, test, lint, format, build, and generate-prompt

3. **Hatchling** - Modern Python build backend
   - Configured in `pyproject.toml`
   - Handles package building and distribution
   - PEP 517/518 compliant build system

4. **pytest** - Testing framework
   - Comprehensive test suite with 94%+ coverage
   - Tests located in `runner/tests/`
   - Includes fixtures and integration tests

5. **ruff** - Fast Python linter and formatter
   - Replaces flake8, black, isort, and more
   - Configured in `pyproject.toml`
   - Used for both linting and code formatting
