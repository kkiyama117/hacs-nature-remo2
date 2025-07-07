# context.md

## プロジェクト概要

Nature Remo デバイスを Home Assistant に統合するためのカスタムコンポーネント（HACS）です。Nature Remo は、赤外線信号やスマート連携を通じてエアコン、照明、その他の家電を制御できるスマートホームデバイスです。

## 技術的背景

### リポジトリの特性

- **タイプ**: Home Assistant カスタムインテグレーション（HACS 対応）
- **言語**: Python（Home Assistant フレームワーク準拠）
- **目的**: Nature Remo API を通じた家電制御の Home Assistant 統合

### ディレクトリ構造の設計思想

- `custom_components/hacs_nature_remo/`: メインインテグレーションコード
  - `api/`: Nature Remo API クライアント実装（カスタムフォーク使用）
  - `domain/`: ビジネスロジック、定数、設定スキーマ
  - `coordinators.py`: データ更新の効率化のための DataUpdateCoordinator
  - 各プラットフォーム実装: `climate.py`, `sensor.py`, `switch.py`
- `tests/`: pytest による包括的なテストスイート（100%カバレッジ目標）
- `.github/workflows/`: CI/CD パイプライン（テスト、リンティング、検証）

### 開発の制約事項

- Home Assistant の開発ガイドラインに準拠
- 非同期処理（async/await）の完全実装
- DataUpdateCoordinator パターンによる効率的なデータ取得
- UI 設定のみ対応（YAML 設定は非対応）
- シングルコンフィグエントリー制限

## 重要な注意事項

- 不要なファイルの作成は避ける
- 既存ファイルの編集を新規作成より優先する
- Home Assistant のエンティティパターンに従う
- すべての文字列は翻訳可能にし、翻訳ファイルに追加する
- API 呼び出しはコーディネーター経由で行い、エンティティから直接呼び出さない
- テストカバレッジ 100%を維持する
- セマンティックバージョニングに従う
