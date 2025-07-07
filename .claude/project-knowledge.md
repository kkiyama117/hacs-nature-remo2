# project-knowledge.md

Updated when /init is run. Update also if new knowledge is acquired.

## プロジェクトの制約

### 開発上の制約

1. Home Assistant の開発ガイドラインに厳密に準拠
2. Python 3.9+ 互換性の維持（Home Assistant の要件）
3. 非同期処理（async/await）の完全実装
4. pytest によるテストカバレッジ 100% の維持
5. HACS（Home Assistant Community Store）の要件を満たす

### 言語に関する制約

- コード内のコメント・ドキュメント: 英語
- UI 文字列: 多言語対応（translations/ ディレクトリで管理）
  - 現在対応: 英語(en)、フランス語(fr)、日本語(ja)、ノルウェー語(nb)
- git コミットメッセージ: 英語
- 内部ドキュメント（.claude/）: 日本語・英語混在可

## 実装上の技術的洞察

### Home Assistant Integration パターン

#### DataUpdateCoordinator の活用

- **ApplianceCoordinator**: 家電データの集中管理
- **DeviceCoordinator**: センサーデータの集中管理
- 30 秒のデフォルト更新間隔（SCAN_INTERVAL）
- API 呼び出しの最小化とデータ共有の最大化

#### Entity 実装のベストプラクティス

1. **Unique ID**: アプライアンス/デバイス ID ベースで必須
2. **Availability**: コーディネーターの last_update_success を使用
3. **State Updates**: コーディネーターデータのみを参照
4. **Device Info**: 適切なデバイスグルーピングのために実装

### API クライアント設計

#### Nature Remo API の特徴

- RESTful API（OAuth2 認証）
- レート制限: 30 リクエスト/5 分
- カスタムフォーク使用: `nature-remo-fork-only-for-hacs-nature-remo`
- All Endpoint can get from here `https://swagger.nature.global/`
- エンドポイント:
  - `/appliances`: 家電一覧
  - `/devices`: センサーデバイス一覧
  - `/appliances/{id}/aircon_settings`: エアコン制御

### テスト戦略

#### フィクスチャの活用

- `tests/fixtures/`: API レスポンスのモックデータ
- `conftest.py`: 共通の pytest フィクスチャ定義
- モックの一貫性維持が重要

#### テストパターン

1. **Unit Tests**: 個別コンポーネントの機能テスト
2. **Integration Tests**: Home Assistant との統合テスト
3. **Config Flow Tests**: UI 設定フローの完全テスト

### CI/CD パイプライン

#### GitHub Actions ワークフロー

1. **Linting** (`.github/workflows/linting.yaml`)

   - pre-commit hooks の実行
   - flake8, black, isort によるコード品質チェック

2. **Tests** (`.github/workflows/tests.yaml`)

   - 複数の Python バージョンでのテスト実行
   - カバレッジレポートの生成

3. **HACS Validation** (`.github/workflows/validate.yaml`)

   - HACS 要件の検証
   - manifest.json の妥当性チェック

4. **Hassfest** (`.github/workflows/hassfest.yaml`)
   - Home Assistant 統合要件の検証

### 設定管理

#### Config Flow の実装

- ステップ: user → 認証情報入力 → 検証 → 作成
- エラーハンドリング: 無効なトークン、接続エラー
- 単一設定エントリーの強制

#### 翻訳システム

- `translations/` ディレクトリで管理
- キー構造: `config.step.user.data.access_token`
- 新機能追加時は全言語ファイルの更新が必要

### 開発ツールとコマンド

#### 依存関係管理

- `requirements.txt`: 実行時依存関係
- `requirements_dev.txt`: 開発ツール
- `requirements_test.txt`: テスト依存関係

#### よく使うコマンド

```bash
# 開発環境のセットアップ
pip install -r requirements_dev.txt -r requirements_test.txt

# テスト実行（並列実行）
pytest --timeout=9 --durations=10 -n auto -p no:sugar tests

# 特定のテストファイル実行
pytest tests/test_climate.py

# カバレッジレポート生成
pytest --cov=custom_components.hacs_nature_remo --cov-report=html

# コード品質チェック
pre-commit run --all-files

# Home Assistant 検証
python -m script.hassfest
```

### 既知の課題と回避策

1. **Nature Remo API のレート制限**

   - DataUpdateCoordinator で更新頻度を制御
   - 最小更新間隔: 30 秒

2. **エアコンの温度単位**

   - API は摂氏のみサポート
   - Home Assistant 側で華氏変換を実装

3. **デバイスのオフライン検出**
   - API はリアルタイムステータスを提供しない
   - 最終更新時刻で推定

### パフォーマンス最適化

1. **並行データ取得**

   - appliances と devices を並行取得
   - asyncio.gather() の活用

2. **キャッシュ戦略**

   - DataUpdateCoordinator による自動キャッシュ
   - エンティティは直接 API を呼ばない

3. **エラーリトライ**
   - 指数バックオフによる自動リトライ
   - 一時的なネットワークエラーに対応
