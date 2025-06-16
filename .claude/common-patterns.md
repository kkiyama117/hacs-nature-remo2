# common-patterns.md

Write commands of claude and simple command of shell.
Claude commands (`./claude/commands/xxx.md` is called by typing `/project:xxx` in claude code).


## よく使うコマンドパターン

Please add and edit as necessary.

## 頻出するプロンプトテンプレート

### 基本構造テンプレート
```markdown
# [タスク名]

## 役割
あなたは[役割]として振る舞ってください。

## コンテキスト
[背景情報や前提条件]

## タスク
以下のタスクを実行してください：
1. [タスク1]
2. [タスク2]
3. [タスク3]

## 制約条件
- [制約1]
- [制約2]
- [制約3]

## 出力形式
[期待される出力の形式]

## 例
[入出力の例（必要に応じて）]
```

### 学術分野用テンプレート
```markdown
# [学術分野]に関する[タスク]

## 専門知識の前提
- 分野: [具体的な分野]
- 必要な背景知識: [前提知識]
- 使用する理論/手法: [理論名]

## タスクの詳細
[具体的な問題や質問]

## 技術的要件
- 数式記法: [LaTeX/プレーンテキスト]
- 単位系: [SI単位系/その他]
- 精度: [必要な精度]

## 期待される回答
- 理論的説明
- 計算過程（該当する場合）
- 結論と考察
```

### コード生成用テンプレート
```markdown
# [プログラミング言語]での[機能]実装

## 要件
- 言語: [言語名とバージョン]
- フレームワーク: [使用するフレームワーク]
- 目的: [実装の目的]

## 仕様
[詳細な仕様]

## 制約
- パフォーマンス要件
- セキュリティ考慮事項
- コーディング規約

## サンプル入出力
入力: [入力例]
出力: [出力例]
```

## デバッグ時の確認事項

### プロンプトが期待通りに動作しない場合
1. 役割定義が明確か確認
2. コンテキストが十分か確認
3. 制約条件が適切か確認
4. 出力形式の指定が明確か確認

## 効率化のためのエイリアス（推奨）

```bash
# ~/.bashrc または ~/.zshrc に追加
alias prompt-gen='cd ~/AI_prompts/runner && python -m runner.generate'
alias prompt-list='ls -la ~/AI_prompts/prompts/'
alias prompt-search='grep -r --include="*.md" -i'
```