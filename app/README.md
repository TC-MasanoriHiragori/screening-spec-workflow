# アプリケーションコード構造

このディレクトリには、screening-api-coreのアプリケーションコードが含まれています。オニオンアーキテクチャの4層構造で構成されています。

## ディレクトリ構成

```
app/
├── domain/                  # Domain層（ドメイン層）
│   ├── __init__.py
│   └── screening_service.py  # ScreeningService Protocol
├── usecase/                 # Application層（アプリケーション層）
│   ├── __init__.py
│   └── screening_usecase.py  # ScreeningUsecase
├── infrastructure/          # Infrastructure層（インフラストラクチャ層）
│   ├── __init__.py
│   └── screening_service_impl.py  # EchoScreeningService
└── presentation/            # Presentation層（プレゼンテーション層）
    ├── __init__.py
    ├── main.py              # FastAPIアプリケーション
    └── api/
        ├── __init__.py
        ├── dependencies.py   # 依存性注入設定
        ├── schemas/          # Pydanticスキーマ
        │   ├── __init__.py
        │   └── screening.py  # ScreeningRequest/Response、HealthResponse
        └── routes/           # APIルーター
            ├── __init__.py
            ├── screenings.py # POST /v1/screenings
            └── health.py     # GET /health
```

## 層の詳細

### Domain層 (`domain/`)

**責務**: ビジネスロジックのインターフェース定義

- **外部依存なし**: Pure Pythonのみを使用
- **Protocol使用**: typing.Protocolによる構造的部分型付け
- **ビジネスルール**: 核となるビジネスルールとインターフェースを定義

#### 主要ファイル

- **`screening_service.py`**
  - `ScreeningService` Protocol: スクリーニングサービスのインターフェース
  - `screen(content: str) -> str`: スクリーニングメソッドのシグネチャ定義

**例:**
```python
from typing import Protocol

class ScreeningService(Protocol):
    def screen(self, content: str) -> str:
        """スクリーニング処理を実行します"""
        ...
```

### Application層 (`usecase/`)

**責務**: ユースケースのオーケストレーション

- **Domain層のみに依存**: インターフェースを通じてビジネスロジックを呼び出す
- **ビジネスフローの調整**: 複数のドメインサービスを組み合わせる
- **トランザクション管理**: 将来的にトランザクション制御を追加可能

#### 主要ファイル

- **`screening_usecase.py`**
  - `ScreeningUsecase`: スクリーニング操作のユースケース
  - 依存性注入により`ScreeningService`を受け取る
  - `execute(content: str) -> str`: スクリーニング実行メソッド

**例:**
```python
from app.domain.screening_service import ScreeningService

class ScreeningUsecase:
    def __init__(self, service: ScreeningService) -> None:
        self._service = service

    def execute(self, content: str) -> str:
        return self._service.screen(content)
```

### Infrastructure層 (`infrastructure/`)

**責務**: Domain層のインターフェースの具体的実装

- **Domain層のインターフェース実装**: Protocolに準拠した実装
- **外部サービス連携**: データベース、外部API等との連携（将来拡張）
- **技術的詳細**: 具体的な実装技術に依存

#### 主要ファイル

- **`screening_service_impl.py`**
  - `EchoScreeningService`: ScreeningServiceの暫定実装
  - 入力をそのまま返すエコー実装
  - 将来的に実際のスクリーニングロジックに置き換え可能

**例:**
```python
class EchoScreeningService:
    def screen(self, content: str) -> str:
        """入力コンテンツをそのまま返す"""
        return content
```

### Presentation層 (`presentation/`)

**責務**: REST APIエンドポイントの提供

- **FastAPI使用**: REST APIフレームワーク
- **Pydanticスキーマ**: リクエスト/レスポンスのバリデーション
- **依存性注入**: Application層とInfrastructure層を疎結合に接続
- **OpenAPI自動生成**: APIドキュメントの自動生成

#### 主要ファイル

##### `main.py`
FastAPIアプリケーションのエントリーポイント

```python
from fastapi import FastAPI

app = FastAPI(
    title="Screening API",
    version="1.0.0",
)

app.include_router(screenings_router)
app.include_router(health_router)
```

##### `api/dependencies.py`
依存性注入の設定

```python
from fastapi import Depends

def get_screening_service() -> ScreeningService:
    return EchoScreeningService()

def get_screening_usecase(
    service: ScreeningService = Depends(get_screening_service),
) -> ScreeningUsecase:
    return ScreeningUsecase(service)
```

##### `api/schemas/screening.py`
Pydanticスキーマの定義

- `ScreeningRequest`: POST /v1/screenings のリクエストボディ
- `ScreeningResponse`: POST /v1/screenings のレスポンスボディ
- `HealthResponse`: GET /health のレスポンスボディ

##### `api/routes/screenings.py`
スクリーニングAPIルーター

```python
@router.post("", response_model=ScreeningResponse)
def create_screening(
    request: ScreeningRequest,
    usecase: ScreeningUsecase = Depends(get_screening_usecase),
) -> ScreeningResponse:
    result_content = usecase.execute(request.content)
    return ScreeningResponse(content=result_content)
```

##### `api/routes/health.py`
ヘルスチェックAPIルーター

```python
@router.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return HealthResponse()
```

## 依存関係の方向

オニオンアーキテクチャでは、依存関係は**外側から内側**に向かいます：

```
Presentation → Application → Domain ← Infrastructure
```

- **Presentation層**: Application層に依存
- **Application層**: Domain層に依存
- **Infrastructure層**: Domain層に依存
- **Domain層**: どの層にも依存しない（Pure Python）

この依存方向により：
- ビジネスロジック（Domain層）が独立
- 実装の交換が容易（Infrastructure層の差し替え）
- テストが容易（モックを使用した単体テスト）

## コーディング規約

### 命名規則

- **モジュール/パッケージ**: `snake_case`
- **クラス**: `PascalCase`
- **関数/メソッド**: `snake_case`
- **定数**: `UPPER_CASE`

### 型ヒント

すべての関数/メソッドに型ヒントを付与：

```python
def screen(self, content: str) -> str:
    ...
```

### Docstring

Google/NumPyスタイルのdocstringを使用：

```python
def execute(self, content: str) -> str:
    """
    スクリーニング処理を実行します

    Args:
        content: スクリーニング対象のテキスト

    Returns:
        スクリーニング結果のテキスト
    """
    ...
```

### エクスポート

各モジュールで`__all__`を定義：

```python
__all__ = ["ScreeningService"]
```

## 将来の拡張

### Infrastructure層の拡張

実際のスクリーニングロジックを実装する際：

1. 新しい実装クラスを作成（例: `MLScreeningService`）
2. `ScreeningService` Protocolに準拠
3. `dependencies.py`で実装を切り替え

```python
def get_screening_service() -> ScreeningService:
    # 環境変数等で切り替え可能
    return MLScreeningService()  # または EchoScreeningService()
```

### Application層の拡張

複雑なビジネスロジックを追加する際：

1. 新しいユースケースクラスを作成
2. 必要なDomain層インターフェースを注入
3. Presentation層でルーターを追加

### Presentation層の拡張

新しいエンドポイントを追加する際：

1. 新しいPydanticスキーマを定義
2. 新しいルーターを作成
3. `main.py`でルーターを登録

---

詳細なテスト方法については [../tests/README.md](../tests/README.md) を参照してください。
