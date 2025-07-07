# common-patterns.md

## よく使うコマンドパターン

### 開発環境セットアップ

```bash
# 依存関係のインストール
pip install -r requirements_dev.txt -r requirements_test.txt

# 開発モードでのインストール
pip install -e .

# pre-commit フックの設定
pre-commit install
```

### テスト実行

```bash
# 全テストを並列実行（推奨）
pytest --timeout=9 --durations=10 -n auto -p no:sugar tests

# 特定のプラットフォームのテスト
pytest tests/test_climate.py
pytest tests/test_sensor.py
pytest tests/test_switch.py

# カバレッジレポート付きテスト
pytest --cov=custom_components.hacs_nature_remo --cov-report=html

# 単一テストの実行
pytest tests/test_climate.py::test_climate_entity_setup -v

# 失敗したテストのみ再実行
pytest --lf
```

### コード品質チェック

```bash
# すべての pre-commit フックを実行
pre-commit run --all-files

# 個別のリンターを実行
flake8 custom_components/hacs_nature_remo
black custom_components/hacs_nature_remo --check
isort custom_components/hacs_nature_remo --check-only

# 自動修正を適用
black custom_components/hacs_nature_remo
isort custom_components/hacs_nature_remo
```

### Home Assistant 検証

```bash
# manifest.json の検証
python -m script.hassfest

# HACS 要件の検証
hacs-action

# 統合の基本チェック
python -m homeassistant --script check_config
```

### デバッグとログ

```bash
# Home Assistant のログを確認
tail -f /config/home-assistant.log | grep hacs_nature_remo

# 詳細ログの有効化（configuration.yaml に追加）
logger:
  default: info
  logs:
    custom_components.hacs_nature_remo: debug

# API レスポンスの確認
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.nature.global/1/appliances
```

### リリース準備

```bash
# バージョン番号の更新
# manifest.json の version を更新

# 変更履歴の確認
git log --oneline --graph --decorate

# タグの作成
git tag -a v0.1.2 -m "Release version 0.1.2"
git push origin v0.1.2
```

## Claude Commands パターン

### エラー修正時のプロンプト

```
/fix_error
エラー: [エラーメッセージ]
ファイル: [ファイルパス]
コンテキスト: [エラーが発生した状況]
```

### 新機能追加時のプロンプト

```
/add_feature
機能: [追加したい機能の説明]
プラットフォーム: [climate/sensor/switch]
要件:
- [要件1]
- [要件2]
```

### リファクタリング依頼

```
/refactor
対象: [リファクタリング対象のコード/ファイル]
目的: [パフォーマンス改善/可読性向上/etc]
制約: [後方互換性の維持/etc]
```

## トラブルシューティングパターン

### API エラーの調査

```bash
# API トークンの検証
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.nature.global/1/users/me

# レート制限の確認
# レスポンスヘッダーの X-Rate-Limit-* を確認
curl -I -H "Authorization: Bearer YOUR_TOKEN" https://api.nature.global/1/appliances
```

### エンティティが表示されない場合

```bash
# エンティティレジストリの確認
grep -r "hacs_nature_remo" /config/.storage/core.entity_registry

# デバイスレジストリの確認
grep -r "hacs_nature_remo" /config/.storage/core.device_registry

# 設定エントリーの確認
grep -r "hacs_nature_remo" /config/.storage/core.config_entries
```

### テスト失敗の調査

```bash
# 詳細なテスト出力
pytest -vvs tests/test_climate.py::test_climate_entity_setup

# デバッグモードでテスト実行
pytest --pdb tests/test_climate.py

# 特定のマーカーでテスト実行
pytest -m "not slow" tests/
```

## 効率化のためのエイリアス（推奨）

```bash
# ~/.bashrc または ~/.zshrc に追加
alias nr-test='pytest --timeout=9 --durations=10 -n auto -p no:sugar tests'
alias nr-lint='pre-commit run --all-files'
alias nr-coverage='pytest --cov=custom_components.hacs_nature_remo --cov-report=html'
alias nr-validate='python -m script.hassfest'
alias nr-logs='tail -f /config/home-assistant.log | grep hacs_nature_remo'
```

## Git ワークフローパターン

```bash
# 機能ブランチの作成
git checkout -b feature/add-light-support

# 変更のステージングと確認
git add -p  # 対話的に変更を選択
git diff --staged  # ステージした変更の確認

# コミット（conventional commits 形式）
git commit -m "feat: add light entity support"
git commit -m "fix: correct temperature conversion for F units"
git commit -m "docs: update README with new features"

# プルリクエスト用にプッシュ
git push -u origin feature/add-light-support
```
