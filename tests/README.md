# テストコード構造

このディレクトリには、screening-api-coreの包括的なテストスイートが含まれています。**合計146テスト**で、すべての層とシナリオをカバーしています。

## テストの種類と構成

```
tests/
├── unit/                           # ユニットテスト（98テスト）
│   ├── domain/                     # Domain層のテスト（5テスト）
│   │   └── test_screening_service.py
│   ├── infrastructure/             # Infrastructure層のテスト（26テスト）
│   │   └── test_screening_service_impl.py
│   ├── usecase/                    # Application層のテスト（16テスト）
│   │   └── test_screening_usecase.py
│   └── presentation/               # Presentation層のテスト（51テスト）
│       └── test_schemas.py
├── integration/                    # 統合テスト（36テスト）
│   ├── test_screening_integration.py  # スクリーニングエンドポイント（19テスト）
│   └── test_health_integration.py     # ヘルスチェックエンドポイント（17テスト）
└── e2e/                            # E2Eテスト（12テスト）
    └── test_api_e2e.py             # エンドツーエンドワークフロー
```

## テストの実行

### すべてのテストを実行

```bash
uv run pytest
```

**期待される結果**: 146 passed

### テストタイプ別に実行

```bash
# ユニットテストのみ（98テスト）
uv run pytest tests/unit/

# 統合テストのみ（36テスト）
uv run pytest tests/integration/

# E2Eテストのみ（12テスト）
uv run pytest tests/e2e/
```

### 層別にテストを実行

```bash
# Domain層のテスト（5テスト）
uv run pytest tests/unit/domain/

# Infrastructure層のテスト（26テスト）
uv run pytest tests/unit/infrastructure/

# Application層のテスト（16テスト）
uv run pytest tests/unit/usecase/

# Presentation層のテスト（51テスト）
uv run pytest tests/unit/presentation/
```

### 詳細な出力

```bash
# 詳細モード
uv run pytest -v

# より詳細なモード（テスト名とdocstring表示）
uv run pytest -vv

# 失敗時のみ詳細表示
uv run pytest --tb=short
```

### カバレッジレポート

```bash
# カバレッジ付きで実行
uv run pytest --cov=app --cov-report=html

# HTMLレポートを開く
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## テストの詳細

### 1. ユニットテスト（98テスト）

各層のコンポーネントを独立してテストします。外部依存はモック化されています。

#### Domain層テスト（5テスト）

**ファイル**: `tests/unit/domain/test_screening_service.py`

- **テスト対象**: `ScreeningService` Protocol
- **テスト内容**:
  - Protocolの構造的部分型チェック
  - 準拠クラスと非準拠クラスの検証
  - ダックタイピングの動作確認

**主要テスト**:
- `test_screening_service_protocol_structure`: Protocol構造の検証
- `test_conforming_class_implements_protocol`: 準拠クラスの検証
- `test_protocol_duck_typing_with_callable`: ダックタイピングの検証

#### Infrastructure層テスト（26テスト）

**ファイル**: `tests/unit/infrastructure/test_screening_service_impl.py`

- **テスト対象**: `EchoScreeningService`
- **テスト内容**:
  - エコー機能の正常動作
  - 空文字列、Unicode、特殊文字の処理
  - 大量データの処理
  - エッジケースの網羅的テスト

**主要テスト**:
- `test_echo_screening_service_basic`: 基本的なエコー動作
- `test_screen_method_with_various_inputs`: パラメータ化された多様な入力テスト
- `test_screen_method_with_special_cases`: 特殊ケースのテスト

**使用技術**:
- `pytest.mark.parametrize`: 多様な入力パターンのテスト
- エッジケース: 空文字列、空白文字、非ASCII文字、絵文字、改行等

#### Application層テスト（16テスト）

**ファイル**: `tests/unit/usecase/test_screening_usecase.py`

- **テスト対象**: `ScreeningUsecase`
- **テスト内容**:
  - ユースケースのオーケストレーション
  - サービス呼び出しの検証
  - 依存性注入の動作確認
  - エラーハンドリング

**主要テスト**:
- `test_screening_usecase_execute_calls_service`: サービス呼び出しの検証
- `test_execute_with_various_inputs`: 多様な入力でのテスト
- `test_execute_with_service_exception`: 例外伝播のテスト

**使用技術**:
- `unittest.mock.Mock`: サービスのモック化
- `assert_called_once_with`: 呼び出し検証
- 依存性注入パターンのテスト

#### Presentation層テスト（51テスト）

**ファイル**: `tests/unit/presentation/test_schemas.py`

- **テスト対象**: Pydanticスキーマ（`ScreeningRequest`, `ScreeningResponse`, `HealthResponse`）
- **テスト内容**:
  - バリデーション動作の検証
  - 正常系・異常系のテスト
  - JSONシリアライゼーション
  - スキーマ生成の検証

**主要テスト**:
- `test_screening_request_valid_data`: 正常なリクエストのバリデーション
- `test_screening_request_invalid_type`: 型エラーのバリデーション
- `test_screening_request_empty_content`: 空文字列の受け入れ検証
- `test_health_response_schema`: ヘルスレスポンスのスキーマ検証

**使用技術**:
- Pydantic V2 API
- `model_validate`: バリデーション
- `model_dump`: シリアライゼーション
- `model_json_schema`: スキーマ生成

### 2. 統合テスト（36テスト）

エンドポイント単位で、複数の層を統合してテストします。FastAPIのTestClientを使用します。

#### スクリーニングエンドポイントテスト（19テスト）

**ファイル**: `tests/integration/test_screening_integration.py`

- **テスト対象**: `POST /v1/screenings`
- **テスト内容**:
  - 正常系: 有効なリクエストの処理
  - 異常系: バリデーションエラー、不正な形式
  - HTTPメソッド: GET, PUT, DELETE等の非対応メソッド
  - エッジケース: 空文字列、特殊文字、大量データ

**主要テスト**:
- `test_create_screening_success`: 正常なスクリーニング実行
- `test_create_screening_with_various_content`: 多様なコンテンツのテスト
- `test_create_screening_invalid_content_type`: 型エラーのテスト
- `test_create_screening_method_not_allowed`: 非対応メソッドのテスト

#### ヘルスチェックエンドポイントテスト（17テスト）

**ファイル**: `tests/integration/test_health_integration.py`

- **テスト対象**: `GET /health`
- **テスト内容**:
  - 正常系: ヘルスチェックのレスポンス
  - 冪等性: 複数回呼び出しの検証
  - HTTPメソッド: POST, PUT, DELETE等の非対応メソッド
  - エラーケース: クエリパラメータ、リクエストボディの無視

**主要テスト**:
- `test_health_check_success`: 正常なヘルスチェック
- `test_health_check_idempotency`: 冪等性の検証
- `test_health_check_method_not_allowed`: 非対応メソッドのテスト

**使用技術**:
- `TestClient`: FastAPIのテストクライアント
- HTTPステータスコードの検証
- JSONレスポンスのバリデーション

### 3. E2Eテスト（12テスト）

実際のユーザーワークフローを模倣した、エンドツーエンドのテストです。

**ファイル**: `tests/e2e/test_api_e2e.py`

- **テスト対象**: 全体のAPIワークフロー
- **テスト内容**:
  - 完全なユーザーシナリオ
  - 複数エンドポイントの組み合わせ
  - 実際のユースケースの検証
  - OpenAPI仕様との整合性

**主要テスト**:
- `test_complete_screening_workflow`: スクリーニングの完全なワークフロー
- `test_health_check_before_screening`: ヘルスチェック後のスクリーニング
- `test_multiple_screenings_in_sequence`: 連続スクリーニング
- `test_api_documentation_endpoints`: OpenAPIドキュメントの検証

**シナリオ例**:
1. ヘルスチェックでサービス稼働確認
2. スクリーニングリクエスト送信
3. レスポンスの検証
4. 複数回のスクリーニング実行
5. OpenAPIドキュメントの取得

## テスト規約

### テスト関数の命名

```python
# 良い例
def test_screening_request_valid_data(): ...
def test_execute_with_empty_string(): ...
def test_health_check_success(): ...

# 悪い例
def test_1(): ...
def test_it_works(): ...
```

### Arrange-Act-Assert パターン

すべてのテストは AAA パターンに従います：

```python
def test_example():
    # Arrange: テストデータとモックの準備
    request_data = {"content": "test"}

    # Act: テスト対象の実行
    response = client.post("/v1/screenings", json=request_data)

    # Assert: 結果の検証
    assert response.status_code == 200
    assert response.json() == {"content": "test"}
```

### パラメータ化テスト

繰り返しパターンは `pytest.mark.parametrize` を使用：

```python
@pytest.mark.parametrize(
    "content,expected",
    [
        ("hello", "hello"),
        ("", ""),
        ("日本語", "日本語"),
    ],
)
def test_with_various_inputs(content: str, expected: str):
    result = service.screen(content)
    assert result == expected
```

### フィクスチャの使用

共通のセットアップは `conftest.py` でフィクスチャとして定義：

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.presentation.main import app

@pytest.fixture
def client():
    return TestClient(app)
```

## カバレッジ目標

- **全体カバレッジ**: 90%以上
- **Domain層**: 100%（Pure Pythonで依存なし）
- **Infrastructure層**: 95%以上
- **Application層**: 95%以上
- **Presentation層**: 90%以上

## テスト実行時の注意事項

### テストの独立性

各テストは独立して実行可能で、他のテストの実行順序や結果に依存しません。

### モックの使用

ユニットテストでは外部依存をモック化し、テストを高速かつ信頼性の高いものにします。

### TestClient の動作

FastAPIの`TestClient`は実際のHTTPリクエストを送信せず、ASGI アプリケーションを直接呼び出します。これにより高速なテストが可能です。

## トラブルシューティング

### テストが失敗する

```bash
# 詳細な失敗情報を表示
uv run pytest -vv --tb=long

# 特定のテストのみ実行
uv run pytest tests/unit/domain/test_screening_service.py::test_screening_service_protocol_structure
```

### カバレッジが表示されない

```bash
# pytest-covをインストール
uv add --dev pytest-cov

# カバレッジ付きで再実行
uv run pytest --cov=app --cov-report=term-missing
```

### テストが遅い

```bash
# 並列実行（pytest-xdist使用）
uv add --dev pytest-xdist
uv run pytest -n auto
```

## 今後の拡張

### パフォーマンステスト

```bash
# locustなどのツールで負荷テスト
uv add --dev locust
```

### セキュリティテスト

```bash
# banditでセキュリティスキャン
uv add --dev bandit
uv run bandit -r app/
```

### ミューテーションテスト

```bash
# mutmutでテストの質を検証
uv add --dev mutmut
uv run mutmut run
```

---

詳細なアプリケーション構造については [../app/README.md](../app/README.md) を参照してください。
