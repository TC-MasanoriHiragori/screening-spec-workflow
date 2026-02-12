# Requirements Document

## Introduction

「screening-api-core」は、採用スクリーニングAPIの基盤となるコア機能を実装する仕様です。本仕様では、オニオンアーキテクチャに基づいた4層構造（Presentation、Application、Domain、Infrastructure）を構築し、スクリーニングエンドポイントとヘルスチェックエンドポイントを提供します。

初期実装では、スクリーニングロジックは暫定的に「入力値をそのまま返す」シンプルな実装とし、将来的な機械学習モデルやルールエンジンへの置き換えを見据えた拡張可能な設計を採用します。

### 提供価値
- **アーキテクチャ基盤の確立**: 将来の機能拡張に対応可能なオニオンアーキテクチャの実装
- **API基盤の構築**: RESTful APIの基本エンドポイントとOpenAPI仕様の提供
- **開発環境の整備**: uv、pytest、ruffによるモダンな開発基盤の構築

## Alignment with Product Vision

本仕様は product.md で定義された以下の目標に整合します：

- **シンプルさ優先**: 必要最小限の機能（スクリーニング + ヘルスチェック）から開始
- **保守性重視**: オニオンアーキテクチャとDDDによる保守性の高い設計
- **標準準拠**: OpenAPI仕様の厳格な遵守

tech.md で定義された技術スタック（Python 3.12、FastAPI、uv、pytest、ruff）を採用し、structure.md で定義されたディレクトリ構成に従います。

## Requirements

### REQ-1: スクリーニングエンドポイントの提供

**User Story:** API利用者として、応募者情報をスクリーニングするエンドポイントにリクエストを送信し、処理結果を受け取りたい。

#### Acceptance Criteria

1. **EARS-01**: WHEN クライアントが `POST /v1/screenings` に `{"content": "テキスト"}` 形式のJSONリクエストを送信する THEN システムは HTTP 200 を返し、レスポンスボディに `{"content": "テキスト"}` を返す SHALL
   - 入力された `content` フィールドの値を、そのままレスポンスの `content` フィールドとして返すこと
   - レスポンスには `content` フィールドのみを含み、`status`、`result` 等の追加フィールドは含めない SHALL

2. **EARS-02**: WHEN リクエストボディが不正なJSON形式である、または `content` フィールドが存在しない THEN システムは HTTP 422 (Unprocessable Entity) を返し、エラー詳細を含む SHALL

3. **EARS-03**: WHEN リクエストの Content-Type が `application/json` でない THEN システムは HTTP 415 (Unsupported Media Type) を返す SHALL

4. **EARS-04**: WHEN 正常なリクエストを受信した THEN システムは 500ms 以内にレスポンスを返す SHALL（95パーセンタイル）

#### 技術的要件

- **エンドポイントパス**: `/v1/screenings`
- **HTTPメソッド**: POST
- **リクエストボディ**:
  ```json
  {
    "content": "string"
  }
  ```
- **レスポンスボディ（成功時）**:
  ```json
  {
    "content": "string"
  }
  ```
- **ステータスコード**:
  - 200 OK: 正常処理
  - 422 Unprocessable Entity: バリデーションエラー
  - 415 Unsupported Media Type: Content-Type エラー
  - 500 Internal Server Error: サーバーエラー

### REQ-2: ヘルスチェックエンドポイントの提供

**User Story:** 運用担当者として、APIの稼働状態を確認するためのヘルスチェックエンドポイントを利用したい。

#### Acceptance Criteria

1. **EARS-05**: WHEN クライアントが `GET /health` にリクエストを送信する THEN システムは HTTP 200 を返し、レスポンスボディに `{"status": "ok"}` を返す SHALL

2. **EARS-06**: WHEN ヘルスチェックリクエストを受信した THEN システムは 100ms 以内にレスポンスを返す SHALL

3. **EARS-07**: WHEN ヘルスチェックエンドポイントにアクセスする THEN システムは認証を要求しない SHALL

#### 技術的要件

- **エンドポイントパス**: `/health`
- **HTTPメソッド**: GET
- **リクエストボディ**: なし
- **レスポンスボディ**:
  ```json
  {
    "status": "ok"
  }
  ```
- **ステータスコード**:
  - 200 OK: 正常稼働

### REQ-3: オニオンアーキテクチャの実装

**User Story:** 開発者として、将来の機能拡張に対応可能なオニオンアーキテクチャに基づいたコードベースを構築したい。

#### Acceptance Criteria

1. **EARS-08**: IF コードベースを実装する THEN システムは以下の4層構造を持つ SHALL:
   - **Presentation層** (`app/presentation`): FastAPIルーター、リクエスト/レスポンススキーマ
   - **Application層** (`app/usecase`): ユースケース（アプリケーションサービス）
   - **Domain層** (`app/domain`): インターフェース定義、ドメインモデル
   - **Infrastructure層** (`app/infrastructure`): インターフェースの具体的実装

2. **EARS-09**: WHEN 各層を実装する THEN 依存関係は以下のルールに従う SHALL:
   - Presentation層 → Application層 → Domain層
   - Infrastructure層 → Domain層（インターフェース実装）
   - Domain層 → 他層への依存なし（依存性逆転の原則）

3. **EARS-10**: WHEN スクリーニングロジックを実装する THEN Infrastructure層で具体的なロジック（入力値をそのまま返す）を実装し、Domain層でインターフェースを定義し、Application層（Usecase層）がDomain層のインターフェースを呼び出す SHALL

4. **EARS-11**: WHEN ディレクトリ構造を作成する THEN 以下の構成に従う SHALL:
   ```
   app/
   ├── presentation/
   │   ├── api/
   │   │   ├── routes/
   │   │   └── schemas/
   │   └── main.py
   ├── usecase/
   │   └── screening_usecase.py
   ├── domain/
   │   └── screening_service.py (インターフェース)
   └── infrastructure/
       └── screening_service_impl.py (実装)
   ```

### REQ-4: OpenAPI仕様書の出力

**User Story:** API利用者として、標準化されたOpenAPI仕様書を参照し、APIの仕様を理解したい。

#### Acceptance Criteria

1. **EARS-12**: WHEN システムを構築する THEN プロジェクトルートに `openapi.yaml` ファイルを出力する SHALL

2. **EARS-13**: WHEN OpenAPI仕様書を生成する THEN OpenAPI 3.0 以上の形式に準拠する SHALL

3. **EARS-14**: WHEN OpenAPI仕様書を出力する THEN 以下の情報を含む SHALL:
   - `/v1/screenings` エンドポイントの定義（リクエスト/レスポンススキーマ）
   - `/health` エンドポイントの定義
   - スキーマ定義（ScreeningRequest、ScreeningResponse、HealthResponse）

### REQ-5: 開発環境とコード品質ツールの構成

**User Story:** 開発者として、モダンな開発ツールを使用して効率的に開発し、コード品質を維持したい。

#### Acceptance Criteria

1. **EARS-15**: WHEN プロジェクトをセットアップする THEN `uv` を使用して依存関係を管理する SHALL
   - `pyproject.toml` による依存関係定義
   - `uv.lock` によるロックファイル管理

2. **EARS-16**: WHEN テストを実行する THEN `pytest` を使用してテストを実行できる SHALL
   - ユニットテスト: 各層のテスト（Domain、Application、Infrastructure、Presentation）
   - 統合テスト: API エンドポイントの統合テスト

3. **EARS-17**: WHEN コード品質チェックを実行する THEN `ruff` を使用してLintとFormatを実行できる SHALL
   - `ruff check`: Lintチェック
   - `ruff format`: コードフォーマット

4. **EARS-18**: WHEN 開発サーバーを起動する THEN `uv run fastapi dev app/presentation/main.py` でホットリロード対応の開発サーバーが起動する SHALL

## Non-Functional Requirements

### Code Architecture and Modularity

- **Single Responsibility Principle**: 各ファイル、クラス、関数は単一の責務のみを持つ
  - Presentation層: HTTPリクエスト/レスポンス処理のみ
  - Application層: ユースケースのオーケストレーションのみ
  - Domain層: ビジネスロジックのインターフェース定義のみ
  - Infrastructure層: 外部依存の具体的実装のみ

- **Modular Design**: 各層は独立したモジュールとして構成され、テスト可能な設計とする
  - Domain層のインターフェースは Pure Python（FastAPI非依存）
  - Infrastructure層の実装はモック可能な設計

- **Dependency Management**: オニオンアーキテクチャの依存関係ルールを厳守
  - 内側の層（Domain）は外側の層（Presentation、Infrastructure）に依存しない
  - 依存性注入により、具象クラスではなく抽象に依存する

- **Clear Interfaces**: 層間のインターフェースは明確に定義される
  - Domain層: `Protocol` による型安全なインターフェース定義
  - Pydantic による入力/出力の型安全性

### Performance

- **API応答時間**:
  - スクリーニングエンドポイント: 95パーセンタイルで 500ms 以内
  - ヘルスチェックエンドポイント: 95パーセンタイルで 100ms 以内

- **スループット**: 単一インスタンスで 100 req/sec の処理能力

- **起動時間**: アプリケーション起動から初回リクエスト受付まで 5秒以内

### Security

- **入力バリデーション**: Pydantic による自動バリデーション
  - `content` フィールドの必須チェック
  - JSON形式の検証

- **エラーハンドリング**:
  - 内部エラー情報の漏洩防止
  - 適切なHTTPステータスコードの返却

- **認証・認可**: 初期実装では対象外（外部サービスに委ねる）

### Reliability

- **エラーハンドリング**: すべてのエンドポイントで適切なエラーレスポンスを返す
  - バリデーションエラー: 422 Unprocessable Entity
  - サーバーエラー: 500 Internal Server Error
  - エラー詳細を含むJSONレスポンス

- **ログ出力**:
  - リクエスト/レスポンスのログ記録（開発環境）
  - エラー発生時の詳細ログ出力

### Usability

- **API Documentation**:
  - FastAPI 自動生成ドキュメント（`/docs`, `/redoc`）
  - `openapi.yaml` のエクスポート

- **開発体験**:
  - ホットリロード対応の開発サーバー
  - 明確なディレクトリ構造とモジュール分割
  - 型ヒントによるIDE補完サポート

### Testability

- **ユニットテスト**: 各層を独立してテスト可能
  - Domain層: インターフェース定義のテスト
  - Application層: モックを使用したユースケースのテスト
  - Infrastructure層: 実装ロジックのテスト
  - Presentation層: エンドポイントのテスト

- **統合テスト**: FastAPI TestClient を使用したE2Eテスト
  - `/v1/screenings` エンドポイントの統合テスト
  - `/health` エンドポイントの統合テスト

- **テストカバレッジ**: 各層で 80% 以上のコードカバレッジ目標

## Out of Scope (初期実装対象外)

以下の機能は本仕様の対象外とし、将来的な拡張として位置づけます：

- 認証・認可機能（外部サービスに委ねる）
- データベースによる永続化
- 高度なスクリーニングロジック（機械学習モデル、ルールエンジン）
- 非同期処理・バッチ処理
- 監視ダッシュボード
- レート制限
