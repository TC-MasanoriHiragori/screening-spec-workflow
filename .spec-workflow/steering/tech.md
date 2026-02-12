# Technology Stack

## Project Type

RESTful API バックエンドサービス。採用情報のスクリーニングを行うHTTP APIを提供します。

## Core Technologies

### Primary Language(s)

- **Language**: Python 3.12
- **Runtime**: CPython 3.12.x
- **Language-specific tools**:
  - `uv`: モダンなPythonパッケージマネージャー（高速依存関係解決とプロジェクト管理）
  - `ruff`: 高速なLinter/Formatter（Rustベース）

### Key Dependencies/Libraries

- **FastAPI**: 最新バージョン - 高性能な非同期Webフレームワーク、自動OpenAPI生成機能
- **pytest**: 最新バージョン - Pythonの標準的なテストフレームワーク
- **pydantic**: FastAPIに含まれる - データバリデーションとシリアライゼーション

### Application Architecture

**オニオンアーキテクチャ** + **ドメイン駆動設計（DDD）** を採用：

```
┌─────────────────────────────────────────┐
│     Presentation Layer (FastAPI)        │ ← HTTPエンドポイント、リクエスト/レスポンス処理
├─────────────────────────────────────────┤
│      Application Layer (Use Cases)      │ ← ビジネスロジックのオーケストレーション
├─────────────────────────────────────────┤
│       Domain Layer (Core Business)      │ ← エンティティ、バリューオブジェクト、ドメインサービス
├─────────────────────────────────────────┤
│   Infrastructure Layer (Persistence)    │ ← データアクセス、外部システム連携
└─────────────────────────────────────────┘
```

**依存関係のルール**:
- 外側の層は内側の層に依存できる
- 内側の層は外側の層に依存してはいけない（依存性逆転の原則）
- ドメイン層はフレームワークに依存しない純粋なビジネスロジック

### Data Storage (if applicable)

初期実装では永続化層は不要：

- **Primary storage**: なし（暫定実装では固定レスポンスを返すため、データ保存不要）
- **Caching**: なし（初期実装対象外）
- **Data formats**: JSON（API入出力形式）

将来的には以下を検討：
- SQLiteまたはPostgreSQLによる評価結果の保存
- Redisによるキャッシング

### External Integrations (if applicable)

初期実装では外部連携なし：

- **APIs**: なし（初期実装対象外）
- **Protocols**: HTTP/REST のみ
- **Authentication**: なし（認証・認可は外部サービスに委ねる設計）

将来的には以下を検討：
- 機械学習APIとの連携（スクリーニングロジックの高度化）
- 認証サービス（Auth0、Firebase Auth等）との統合

### Monitoring & Dashboard Technologies (if applicable)

専用ダッシュボードは提供しない：

- **Dashboard Framework**: なし
- **Real-time Communication**: なし
- **Visualization Libraries**: なし
- **State Management**: なし

運用監視は外部APMツール（Datadog、New Relic等）やログ集約システム（ELK、CloudWatch Logs等）の利用を想定。

## Development Environment

### Build & Development Tools

- **Build System**: `uv` による依存関係管理とビルド
- **Package Management**: `uv` - pyproject.toml ベースの管理
- **Development workflow**:
  - `uv run fastapi dev` - 開発サーバー起動（ホットリロード対応）
  - `uv run pytest` - テスト実行

### Code Quality Tools

- **Static Analysis**: `ruff check` - 高速Linter（Flake8、isort、pyupgrade等の機能を統合）
- **Formatting**: `ruff format` - 高速Formatter（Black互換）
- **Testing Framework**: `pytest` - ユニットテスト、統合テスト
- **Documentation**: FastAPIの自動OpenAPI生成（/docs、/redoc エンドポイント）、`openapi.yaml` 出力

### Version Control & Collaboration

- **VCS**: Git
- **Branching Strategy**: GitHub Flow（主要ブランチ：main、フィーチャーブランチから直接マージ）
- **Code Review Process**:
  - プルリクエストベースのレビュー
  - 1つのIssueに対して1つのPRを作成
  - GitHub CLIを活用した自動化

### Dashboard Development (if applicable)

該当なし（専用ダッシュボードは提供しない）

## Deployment & Distribution (if applicable)

- **Target Platform(s)**: Linuxサーバー、コンテナ環境（Docker/Kubernetes想定）
- **Distribution Method**:
  - Dockerイメージとして配布
  - または `uv` による直接インストール
- **Installation Requirements**:
  - Python 3.12以上
  - `uv` パッケージマネージャー
- **Update Mechanism**:
  - コンテナイメージの更新
  - または `uv sync` による依存関係更新

## Technical Requirements & Constraints

### Performance Requirements

- **API応答時間**: 95パーセンタイルで500ms以内
- **スループット**: 初期目標 100 req/sec（単一インスタンス）
- **メモリ使用量**: 512MB以内（コンテナ環境想定）
- **起動時間**: 5秒以内

### Compatibility Requirements

- **Platform Support**: Linux（Ubuntu 22.04以降推奨）、macOS（開発環境のみ）
- **Dependency Versions**:
  - Python 3.12以上
  - FastAPI最新安定版
- **Standards Compliance**:
  - OpenAPI 3.1仕様準拠
  - RESTful API設計原則

### Security & Compliance

- **Security Requirements**:
  - 初期実装では認証・認可なし（外部サービスに委ねる）
  - HTTPS通信（リバースプロキシ層で実装）
  - 入力バリデーション（Pydanticによる自動バリデーション）
- **Compliance Standards**: なし（初期実装対象外）
- **Threat Model**:
  - インジェクション攻撃対策（Pydanticバリデーション）
  - DoS攻撃対策（レートリミットは外部ゲートウェイに委ねる）

### Scalability & Reliability

- **Expected Load**: 初期段階では小～中規模（〜1000 req/sec）
- **Availability Requirements**: 99%以上の稼働率目標
- **Growth Projections**: 水平スケーリング可能なステートレス設計

## Technical Decisions & Rationale

### Decision Log

1. **Python 3.12 + FastAPI**:
   - **選定理由**: 高速な開発サイクル、優れたOpenAPI自動生成、Pydanticによる型安全性
   - **代替案**: Go（より高速だが開発速度で劣る）、Node.js（JavaScript生態系、型安全性で劣る）

2. **オニオンアーキテクチャ + DDD**:
   - **選定理由**: ビジネスロジックとインフラ層の分離、テスタビリティ向上、将来の機能拡張に対応
   - **トレードオフ**: 初期の開発コストは増加するが、長期的な保守性を優先

3. **uv パッケージマネージャー**:
   - **選定理由**: pip/poetryより高速、pyproject.toml標準準拠、モダンな依存関係解決
   - **代替案**: poetry（成熟しているが速度で劣る）、pip + pip-tools（従来型、機能不足）

4. **ruff Linter/Formatter**:
   - **選定理由**: 従来ツール（Black, Flake8, isort等）の10〜100倍高速、オールインワンツール
   - **代替案**: Black + Flake8（複数ツールの組み合わせ、速度で劣る）

5. **認証・認可の除外**:
   - **選定理由**: 初期実装ではスクリーニングロジックに集中、認証は外部サービス（APIゲートウェイ、Auth0等）に委ねる
   - **トレードオフ**: 独立したAPIとして機能しないが、アーキテクチャがシンプルになる

## Known Limitations

初期実装における技術的制約：

- **暫定スクリーニングロジック**: 固定レスポンスを返すのみ。機械学習モデルやルールエンジンは将来実装
- **認証・認可なし**: 外部システムでの実装を前提とし、API単体では認証機能を持たない
- **永続化層なし**: 初期実装ではデータ保存を行わない。将来的にはデータベース統合が必要
- **非同期処理なし**: 大量データの一括処理には非対応。将来的にはCelery等のタスクキューを検討
- **監視機能なし**: 専用ダッシュボードなし。外部APM/ログツールとの連携を想定
