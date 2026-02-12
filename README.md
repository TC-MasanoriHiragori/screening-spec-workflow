# screening-api-core

採用スクリーニングAPI - オニオンアーキテクチャに基づくRESTful APIバックエンド

## 概要

screening-api-core は、採用情報のスクリーニングを行うバックエンドAPIです。ドメイン駆動設計（DDD）とオニオンアーキテクチャを採用し、将来の機能拡張に対応可能な保守性の高い設計を実現しています。

### 主な特徴

- **オニオンアーキテクチャ**: 4層構造（Domain、Application、Infrastructure、Presentation）による保守性の高い設計
- **FastAPI**: 高性能な非同期Webフレームワーク、自動OpenAPI生成
- **Python 3.12**: 最新の型ヒント機能を活用
- **uv**: モダンな高速パッケージマネージャー
- **ruff**: 高速なLinter/Formatter

## 技術スタック

- **言語**: Python 3.12
- **Webフレームワーク**: FastAPI
- **パッケージマネージャー**: uv
- **Linter/Formatter**: ruff
- **テストフレームワーク**: pytest

## セットアップ

### 前提条件

- Python 3.12以上
- uv パッケージマネージャー

### uv のインストール

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### プロジェクトのセットアップ

```bash
# 依存関係のインストール
uv sync

# 開発用依存関係を含めてインストール
uv sync --extra dev
```

## 開発

### 開発サーバーの起動

```bash
# FastAPI開発サーバー（ホットリロード対応）
uv run fastapi dev app/presentation/main.py
```

### コード品質チェック

```bash
# Lintチェック
uv run ruff check .

# コードフォーマット
uv run ruff format .
```

### テストの実行

```bash
# すべてのテストを実行
uv run pytest

# ユニットテストのみ
uv run pytest tests/unit/

# 統合テストのみ
uv run pytest tests/integration/

# カバレッジ付きで実行
uv run pytest --cov=app --cov-report=html
```

## アーキテクチャ

### オニオンアーキテクチャ

```
┌─────────────────────────────────────────┐
│     Presentation Layer (FastAPI)        │ ← HTTPエンドポイント
├─────────────────────────────────────────┤
│      Application Layer (Use Cases)      │ ← ビジネスロジックオーケストレーション
├─────────────────────────────────────────┤
│       Domain Layer (Core Business)      │ ← インターフェース定義
├─────────────────────────────────────────┤
│   Infrastructure Layer (Implementation) │ ← 具体的実装
└─────────────────────────────────────────┘
```

### ディレクトリ構造

```
screening-api-core/
├── app/                    # アプリケーションコード
│   ├── domain/            # ドメイン層（インターフェース定義）
│   ├── usecase/           # アプリケーション層（ユースケース）
│   ├── infrastructure/    # インフラストラクチャ層（実装）
│   └── presentation/      # プレゼンテーション層（FastAPI）
├── tests/                 # テストコード
│   ├── unit/             # ユニットテスト
│   ├── integration/      # 統合テスト
│   └── e2e/              # End-to-Endテスト
├── pyproject.toml        # プロジェクト設定
├── ruff.toml             # Ruff設定
└── README.md             # このファイル
```

## API ドキュメント

開発サーバー起動後、以下のURLでAPIドキュメントにアクセスできます：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## ライセンス

このプロジェクトは内部開発用です。
