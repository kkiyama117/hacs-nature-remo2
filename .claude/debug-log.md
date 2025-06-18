# debug-log.md

## 重要なデバッグ記録

### 記録フォーマット
```
日付: YYYY-MM-DD HH:MM
問題: [問題の概要]
症状: [具体的な症状・エラーメッセージ]
原因: [判明した原因]
解決方法: [実施した解決策]
所要時間: [解決までにかかった時間]
関連ファイル: [影響を受けたファイル]
学び: [今後のための教訓]
```

---

### 2025-01-16 10:00
**問題**: 初期セットアップ時の Knowledge Management System 構築
**症状**: .claude ディレクトリの構造と内容が未定義
**原因**: 新規プロジェクトへの導入
**解決方法**: 
- プロジェクト分析を実施
- Home Assistant 統合の特性に合わせた内容を作成
- 各ファイルに適切なテンプレートと情報を配置
**所要時間**: 30分
**関連ファイル**: 
- `.claude/context.md`
- `.claude/project-knowledge.md`
- `.claude/project-improvements.md`
- `.claude/common-patterns.md`
- `.claude/debug-log.md`
**学び**: Home Assistant カスタムコンポーネントには特有の開発パターンがあり、これらを文書化することで効率的な開発が可能

---

### テンプレート: API レート制限エラー
**問題**: Nature Remo API のレート制限超過
**症状**: 
```
Error: 429 Too Many Requests
X-Rate-Limit-Remaining: 0
```
**原因**: 30リクエスト/5分の制限を超過
**解決方法**: 
- DataUpdateCoordinator の更新間隔を延長
- 並行リクエストの削減
- キャッシュ戦略の見直し
**所要時間**: [時間]
**関連ファイル**: `coordinators.py`
**学び**: API制限は厳密に管理する必要がある

---

### テンプレート: エンティティ認識エラー
**問題**: Home Assistant がエンティティを認識しない
**症状**: デバイスは表示されるがエンティティが作成されない
**原因**: [原因]
**解決方法**: 
- unique_id の確認と修正
- platform の async_setup_entry 実装確認
- エンティティレジストリの手動クリア
**所要時間**: [時間]
**関連ファイル**: [platform].py
**学び**: unique_id は必須で、一貫性が重要

---

### テンプレート: 非同期処理エラー
**問題**: 同期的なコードによるブロッキング
**症状**: Home Assistant の UI がフリーズ
**原因**: [原因]
**解決方法**: 
- 同期関数を async/await に変換
- executor を使用して同期コードをラップ
**所要時間**: [時間]
**関連ファイル**: [ファイル名]
**学び**: Home Assistant では完全な非同期実装が必須

---

### テンプレート: テスト環境エラー
**問題**: pytest が Home Assistant のモックに失敗
**症状**: ImportError または AttributeError
**原因**: [原因]
**解決方法**: 
- pytest-homeassistant-custom-component の更新
- フィクスチャの適切な使用
- conftest.py の設定確認
**所要時間**: [時間]
**関連ファイル**: tests/conftest.py
**学び**: Home Assistant のテスト環境は特殊で、専用のツールが必要

---

## デバッグのベストプラクティス

### ログレベルの活用
```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.hacs_nature_remo: debug
    custom_components.hacs_nature_remo.api: debug
    custom_components.hacs_nature_remo.coordinators: debug
```

### よくあるエラーパターン

1. **KeyError in coordinator data**
   - 原因: API レスポンスの形式変更
   - 対策: データ取得時の get() メソッド使用とデフォルト値設定

2. **Config flow timeout**
   - 原因: API 接続の遅延
   - 対策: タイムアウト値の調整と非同期処理の確認

3. **Entity state update failure**
   - 原因: coordinator のデータ更新失敗
   - 対策: available プロパティの適切な実装

### デバッグツール

```python
# デバッグ用のログ出力
_LOGGER.debug("Coordinator data: %s", self.coordinator.data)
_LOGGER.debug("Entity state: %s", self.state)

# API レスポンスの確認
import json
_LOGGER.debug("API response: %s", json.dumps(response, indent=2))
```

### パフォーマンス問題の調査

```python
# 実行時間の計測
import time
start = time.time()
# 処理
_LOGGER.debug("Execution time: %.3f seconds", time.time() - start)

# メモリ使用量の確認
import tracemalloc
tracemalloc.start()
# 処理
current, peak = tracemalloc.get_traced_memory()
_LOGGER.debug("Current memory: %.1f MB, Peak: %.1f MB", 
              current / 10**6, peak / 10**6)
```# Debug Log

## 2025-06-18: Pytest Error Resolution

### Issue
Pytest was failing with multiple errors:
- AttributeError: `async_get_data` method not found in API client
- Async tests being skipped due to missing configuration
- Import errors with test fixtures

### Root Cause
1. Tests were based on a generic template and didn't match the actual Nature Remo API implementation
2. Wrong constructor arguments for API client
3. Missing pytest-asyncio configuration
4. Mocking non-existent methods

### Solution
1. Updated API client instantiation to use correct constructor: `HacsNatureRemoApiClient(token, session)`
2. Added pytest-asyncio configuration with `asyncio_mode = auto`
3. Updated mock methods to match actual API: `get_user()`, `get_devices()`, `get_appliances()`
4. Fixed object vs dictionary access patterns in tests
5. Added custom integration enabler fixture

### Result
- 6 out of 9 tests now passing
- Remaining 3 failures are due to mock data structure mismatches
- Tests are properly executing with async support

### Time Spent
Approximately 45 minutes to diagnose and fix the core issues

### Key Learning
When working with Home Assistant custom components, tests must match the actual API implementation rather than using generic templates. The Nature Remo API returns typed objects (User, Device, Appliance) not dictionaries.# Debug Log

## 2025-06-18: Complete Pytest Fix

### Issue
Multiple pytest failures after fixing async_generator error:
- Config flow tests failing on assertions
- Switch test failing with AttributeError
- Init test error in teardown with ConfigEntryState

### Root Causes
1. Test assertions didn't match actual config schema defaults
2. Switch test was mocking the wrong functions
3. Init test wasn't properly managing config entry states

### Solutions
1. Updated config flow assertions to include default heat/cool values
2. Rewrote switch tests to test entities directly with proper mocks
3. Fixed async_reload_entry to use HA's built-in reload method
4. Added proper config entry registration in tests

### Result
- All 11 tests passing
- No more async_generator errors
- Switch module at 95% coverage
- Proper test isolation achieved

### Time Spent
Approximately 30 minutes using orchestrator workflow

### Key Learning
When testing Home Assistant integrations:
- Use built-in HA methods for config operations
- Test entities directly for better coverage
- Ensure mock data matches actual API structure
- State management is critical for config entry tests