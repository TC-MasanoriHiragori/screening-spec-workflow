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
- **包括的なテスト**: 146テスト（ユニット、統合、E2E）

## 技術スタック

- **言語**: Python 3.12
- **Webフレームワーク**: FastAPI
- **パッケージマネージャー**: uv
- **Linter/Formatter**: ruff
- **テストフレームワーク**: pytest
- **バリデーション**: Pydantic

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

# 本番モード
uv run fastapi run app/presentation/main.py
```

サーバー起動後、以下のURLにアクセス可能：

- API: <http://localhost:8000>
- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

### コード品質チェック

```bash
# Lintチェック
uv run ruff check .

# コードフォーマット
uv run ruff format .

# Lintとフォーマットを同時に実行
uv run ruff check . && uv run ruff format .
```

### テストの実行

```bash
# すべてのテストを実行
uv run pytest

# ユニットテストのみ（98テスト）
uv run pytest tests/unit/

# 統合テストのみ（36テスト）
uv run pytest tests/integration/

# E2Eテストのみ（12テスト）
uv run pytest tests/e2e/

# 詳細な出力
uv run pytest -v

# カバレッジ付きで実行（要: pytest-cov）
uv run pytest --cov=app --cov-report=html
```

### OpenAPI仕様のエクスポート

```bash
# OpenAPI 3.1仕様をYAML形式でエクスポート
python scripts/export_openapi.py

# 出力: openapi.yaml
```

## API使用方法

### エンドポイント

#### POST /v1/screenings - スクリーニング実行

採用情報のコンテンツをスクリーニングします（現在はエコー実装）。

**リクエスト例:**

```bash
curl -X POST http://localhost:8000/v1/screenings \
  -H "Content-Type: application/json" \
  -d '{"content": "この求人は素晴らしい機会です。"}'
```

**レスポンス例:**

```json
{
  "content": "この求人は素晴らしい機会です。"
}
```

#### GET /health - ヘルスチェック

APIサービスの稼働状況を確認します。

**リクエスト例:**

```bash
curl http://localhost:8000/health
```

**レスポンス例:**

```json
{
  "status": "ok"
}
```

## アーキテクチャ

### オニオンアーキテクチャ

このプロジェクトは、オニオンアーキテクチャを採用しています。各層は内側の層にのみ依存し、外側の層には依存しません。

```text
┌─────────────────────────────────────────────────────────┐
│     Presentation Layer (FastAPI)                        │
│     - REST APIエンドポイント                              │
│     - Pydanticスキーマ                                   │
│     - 依存性注入設定                                      │
├─────────────────────────────────────────────────────────┤
│     Application Layer (Use Cases)                       │
│     - ビジネスロジックのオーケストレーション                 │
│     - ドメインサービスの呼び出し                           │
├─────────────────────────────────────────────────────────┤
│     Domain Layer (Core Business)                        │
│     - ビジネスルールの定義                                 │
│     - インターフェース（Protocol）定義                     │
├─────────────────────────────────────────────────────────┤
│     Infrastructure Layer (Implementation)               │
│     - ドメインインターフェースの具体的実装                  │
│     - 外部サービスとの連携（将来拡張）                     │
└─────────────────────────────────────────────────────────┘
```

### 層の責務

#### Domain層 (`app/domain/`)

- ビジネスロジックのインターフェース定義
- Protocol を使用した構造的部分型付け
- 外部依存なし、Pure Python

#### Application層 (`app/usecase/`)

- ユースケースのオーケストレーション
- Domain層のインターフェースを使用
- Infrastructure層の実装には依存しない

#### Infrastructure層 (`app/infrastructure/`)

- Domain層のインターフェースの具体的実装
- 現在: エコースクリーニングサービス（暫定実装）
- 将来: 実際のスクリーニングロジック

#### Presentation層 (`app/presentation/`)

- FastAPI REST APIエンドポイント
- Pydanticスキーマによるバリデーション
- 依存性注入による疎結合

### ディレクトリ構造

```text
screening-api-core/
├── app/                           # アプリケーションコード
│   ├── domain/                   # ドメイン層
│   │   └── screening_service.py  #   - ScreeningService Protocol
│   ├── usecase/                  # アプリケーション層
│   │   └── screening_usecase.py  #   - ScreeningUsecase
│   ├── infrastructure/           # インフラストラクチャ層
│   │   └── screening_service_impl.py  #   - EchoScreeningService
│   └── presentation/             # プレゼンテーション層
│       ├── main.py              #   - FastAPIアプリケーション
│       └── api/                 #   - APIルーター・スキーマ
│           ├── dependencies.py  #     - 依存性注入設定
│           ├── schemas/         #     - Pydanticスキーマ
│           └── routes/          #     - APIルーター
├── tests/                        # テストコード
│   ├── unit/                    #   - ユニットテスト（98テスト）
│   │   ├── domain/             #     - Domain層テスト
│   │   ├── infrastructure/     #     - Infrastructure層テスト
│   │   ├── usecase/            #     - Application層テスト
│   │   └── presentation/       #     - Presentation層テスト
│   ├── integration/             #   - 統合テスト（36テスト）
│   │   ├── test_screening_integration.py
│   │   └── test_health_integration.py
│   └── e2e/                     #   - E2Eテスト（12テスト）
│       └── test_api_e2e.py
├── scripts/                      # ユーティリティスクリプト
│   └── export_openapi.py        #   - OpenAPI仕様エクスポート
├── openapi.yaml                  # OpenAPI 3.1仕様書
├── pyproject.toml                # プロジェクト設定
├── ruff.toml                     # Ruff設定
└── README.md                     # このファイル
```

詳細は以下を参照：

- [app/README.md](app/README.md) - アプリケーションコードの構造
- [tests/README.md](tests/README.md) - テストの構造と実行方法

## API ドキュメント

開発サーバー起動後、以下のURLでAPIドキュメントにアクセスできます：

- **Swagger UI**: <http://localhost:8000/docs> - インタラクティブなAPIドキュメント
- **ReDoc**: <http://localhost:8000/redoc> - 読みやすいAPIドキュメント
- **OpenAPI JSON**: <http://localhost:8000/openapi.json> - OpenAPI仕様（JSON形式）
- **OpenAPI YAML**: `openapi.yaml` - OpenAPI仕様（YAML形式、エクスポート済み）

## テスト

このプロジェクトは**146のテスト**で包括的にカバーされています：

- **ユニットテスト（98テスト）**: 各層の個別コンポーネントをテスト
- **統合テスト（36テスト）**: エンドポイントの統合動作をテスト
- **E2Eテスト（12テスト）**: 実際のユーザーワークフローをテスト

詳細は [tests/README.md](tests/README.md) を参照。

## 開発ワークフロー

1. **機能開発**
   - 適切な層に機能を実装
   - 依存方向を遵守（外側→内側）
   - 型ヒントとdocstringを追加

2. **テスト作成**
   - ユニットテスト: 各コンポーネントを独立してテスト
   - 統合テスト: エンドポイントの動作をテスト
   - E2Eテスト: ユーザーシナリオをテスト

3. **コード品質チェック**

   ```bash
   uv run ruff check .
   uv run ruff format .
   uv run pytest
   ```

4. **ドキュメント更新**
   - README更新
   - OpenAPI仕様エクスポート

## トラブルシューティング

### uvのインストールに失敗する

```bash
# Pythonのバージョンを確認
python --version  # 3.12以上が必要

# pipを使用してuvをインストール
pip install uv
```

### テストが失敗する

```bash
# 依存関係を再インストール
uv sync --extra dev

# キャッシュをクリア
uv clean

# 再度テストを実行
uv run pytest -v
```

### ポート8000が既に使用されている

```bash
# 別のポートで起動
uv run uvicorn app.presentation.main:app --port 8001
```

## ライセンス

このプロジェクトは内部開発用です。

## 貢献

このプロジェクトはspec-workflow MCPを使用した仕様駆動開発（SDD）で構築されています。

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
