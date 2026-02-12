# Project Structure

## Directory Organization

オニオンアーキテクチャに基づいた階層構造を採用します。依存関係は外側から内側へ向かい、内側の層は外側の層に依存しません。

```text
screening-spec-workflow/
├── src/
│   └── screening_api/                 # メインアプリケーションパッケージ
│       ├── domain/                    # ドメイン層（最内層・依存ゼロ）
│       │   ├── entities/             # エンティティ
│       │   ├── value_objects/        # 値オブジェクト
│       │   ├── repositories/         # リポジトリインターフェース（抽象）
│       │   └── services/             # ドメインサービス
│       ├── application/               # アプリケーション層（ユースケース）
│       │   ├── use_cases/            # ユースケース実装
│       │   ├── dtos/                 # データ転送オブジェクト
│       │   └── interfaces/           # アプリケーション層のインターフェース
│       ├── infrastructure/            # インフラストラクチャ層
│       │   ├── repositories/         # リポジトリ実装（将来的に使用）
│       │   ├── external/             # 外部API連携（将来的に使用）
│       │   └── config/               # 設定管理
│       └── presentation/              # プレゼンテーション層（最外層）
│           ├── api/                  # FastAPI エンドポイント
│           │   ├── routes/           # ルーター定義
│           │   ├── schemas/          # Pydantic リクエスト/レスポンススキーマ
│           │   └── dependencies/     # FastAPI 依存性注入
│           └── main.py               # FastAPIアプリケーションエントリーポイント
├── tests/                             # テストディレクトリ
│   ├── unit/                         # ユニットテスト（層ごとに分離）
│   │   ├── domain/                   # ドメイン層のテスト
│   │   ├── application/              # アプリケーション層のテスト
│   │   └── infrastructure/           # インフラ層のテスト
│   ├── integration/                  # 統合テスト
│   └── e2e/                          # End-to-End テスト（API レベル）
├── openapi.yaml                       # OpenAPI 仕様書（自動生成または手動管理）
├── pyproject.toml                     # プロジェクト設定（uv管理）
├── uv.lock                            # 依存関係ロックファイル
├── ruff.toml                          # Ruff Linter/Formatter 設定
├── .spec-workflow/                    # 仕様駆動開発ワークフローディレクトリ
│   ├── specs/                        # 機能仕様書
│   ├── steering/                     # ステアリングドキュメント
│   └── templates/                    # テンプレート
└── README.md                          # プロジェクト概要
```

## Naming Conventions

### Files

Pythonの標準的な命名規則に従います：

- **モジュール/パッケージ**: `snake_case`（例: `screening_service.py`, `use_cases/`）
- **クラス定義ファイル**: クラス名と一致させる（例: `ScreeningRequest` クラス → `screening_request.py`）
- **テストファイル**: `test_[対象ファイル名].py`（例: `test_screening_service.py`）
- **設定ファイル**: `snake_case`（例: `app_config.py`）

### Code

Python標準のPEP 8に準拠：

- **Classes/Types**: `PascalCase`（例: `ScreeningRequest`, `CandidateEntity`）
- **Functions/Methods**: `snake_case`（例: `screen_candidate()`, `get_result()`）
- **Constants**: `UPPER_SNAKE_CASE`（例: `MAX_TEXT_LENGTH`, `DEFAULT_RESPONSE`）
- **Variables**: `snake_case`（例: `candidate_data`, `result_list`）
- **Private members**: アンダースコア接頭辞（例: `_internal_method()`, `_private_var`）

## Import Patterns

### Import Order

Ruff（isort互換）による自動整形に従います：

1. **標準ライブラリ**: `import os`, `from typing import ...`
2. **サードパーティ**: `from fastapi import ...`, `import pydantic`
3. **ファーストパーティ（自プロジェクト）**: `from screening_api.domain import ...`
4. **相対インポート**: `from . import ...`, `from .. import ...`

各グループ間には空行を挿入します。

### Module/Package Organization

```python
# 標準ライブラリ
from typing import Optional
from datetime import datetime

# サードパーティ
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# 自プロジェクト（絶対インポート推奨）
from screening_api.domain.entities import CandidateEntity
from screening_api.application.use_cases import ScreeningUseCase
from screening_api.presentation.api.schemas import ScreeningRequest

# 相対インポート（同一モジュール内のみ）
from .dependencies import get_screening_service
```

**依存関係のルール**:
- プレゼンテーション層 → アプリケーション層、ドメイン層
- アプリケーション層 → ドメイン層
- インフラストラクチャ層 → ドメイン層（インターフェース実装）
- ドメイン層 → **依存なし**（純粋なビジネスロジック）

## Code Structure Patterns

### Module/Class Organization

ファイル内の標準的な構成順序：

```python
"""
モジュールのDocstring（目的と責務を記述）
"""

# 1. Imports（上記のImport Order に従う）
from typing import Protocol

# 2. Constants（モジュールレベル定数）
MAX_CANDIDATE_TEXT_LENGTH = 5000

# 3. Type/Interface Definitions（プロトコル、型エイリアス）
class ScreeningRepository(Protocol):
    """リポジトリインターフェース"""
    def save(self, data: dict) -> None: ...

# 4. Main Implementation（クラス、関数）
class ScreeningService:
    """スクリーニングサービス実装"""

    def __init__(self, repository: ScreeningRepository) -> None:
        self._repository = repository

    def screen(self, text: str) -> dict:
        """スクリーニング実行"""
        # 実装...

# 5. Helper/Utility Functions（プライベート関数）
def _validate_text(text: str) -> bool:
    """内部バリデーション"""
    return len(text) <= MAX_CANDIDATE_TEXT_LENGTH

# 6. Exports（__all__ による公開API定義）
__all__ = ["ScreeningService", "MAX_CANDIDATE_TEXT_LENGTH"]
```

### Function/Method Organization

関数内部の推奨構成：

```python
def screen_candidate(candidate_text: str) -> dict:
    """候補者のスクリーニングを実行"""

    # 1. Input validation（入力検証）
    if not candidate_text:
        raise ValueError("Candidate text is required")

    if len(candidate_text) > MAX_TEXT_LENGTH:
        raise ValueError("Text too long")

    # 2. Core logic（コアロジック）
    result = _perform_screening(candidate_text)

    # 3. Return（明確な戻り値）
    return {
        "status": "processed",
        "result": result,
        "timestamp": datetime.now().isoformat()
    }
```

### File Organization Principles

- **1ファイル1クラス原則**: 大きなクラスは1ファイルに1つ。小さな関連クラスは同一ファイルに配置可
- **Public API優先**: 公開クラス/関数を先に、プライベート実装を後に配置
- **責務の明確化**: 各ファイルは単一の責務を持つ（例: `screening_service.py` はスクリーニングロジックのみ）

## Code Organization Principles

1. **Single Responsibility（単一責任の原則）**: 各モジュール、クラス、関数は1つの明確な責務のみを持つ
2. **Dependency Inversion（依存性逆転の原則）**: 具象ではなく抽象（Protocol）に依存する
3. **Testability（テスト容易性）**: 依存性注入を活用し、モックによるテストを可能にする
4. **Consistency（一貫性）**: プロジェクト全体で命名規則、構造パターンを統一

## Module Boundaries

各層間の境界と依存関係のルール：

### 依存関係の方向

```text
Presentation Layer
       ↓ (depends on)
  Application Layer
       ↓ (depends on)
    Domain Layer ← Infrastructure Layer (implements interfaces)
```

### 層ごとの責務

- **Domain Layer（ドメイン層）**:
  - ビジネスロジックとルールの定義
  - フレームワーク非依存
  - 外部ライブラリへの依存を最小化
  - 他の層に依存してはいけない

- **Application Layer（アプリケーション層）**:
  - ユースケースのオーケストレーション
  - ドメイン層のみに依存
  - トランザクション管理
  - ビジネスフローの調整

- **Infrastructure Layer（インフラストラクチャ層）**:
  - ドメイン層のインターフェース実装
  - データベース、外部API、ファイルシステムとの連携
  - フレームワーク固有の実装

- **Presentation Layer（プレゼンテーション層）**:
  - HTTP APIエンドポイント
  - リクエスト/レスポンスの変換
  - 認証・認可（将来実装）
  - エラーハンドリング

### 境界の強制

- **型チェック**: mypyまたはPyright（将来導入検討）で依存関係を静的チェック
- **Import制御**: Ruffのルールでドメイン層からの不正なインポートを禁止
- **テスト**: 各層のユニットテストで依存関係を検証

## Code Size Guidelines

コード品質を保つためのガイドライン：

- **File size（ファイルサイズ）**: 300行以内を推奨、500行を超えたら分割を検討
- **Function/Method size（関数サイズ）**: 50行以内を推奨、100行を超える場合は分割
- **Class complexity（クラス複雑度）**: メソッド数10以内、フィールド数5以内を推奨
- **Nesting depth（ネスト深度）**: 4レベル以内（深すぎる場合はヘルパー関数に抽出）

Ruffによる自動チェック：
- 行長: 88文字（Black互換）
- 複雑度: McCabe複雑度 10以下（Ruff C901ルール）

## Dashboard/Monitoring Structure (if applicable)

初期実装では専用ダッシュボードは提供しません。

将来的に管理ダッシュボードを追加する場合の推奨構造：

```text
src/
└── screening_api/
    └── dashboard/           # 独立したダッシュボードモジュール
        ├── server.py       # ダッシュボード専用サーバー
        ├── static/         # 静的ファイル（HTML, CSS, JS）
        └── templates/      # テンプレートファイル
```

**分離の原則**:
- ダッシュボードはコアAPIから独立
- 別のエントリーポイントで起動可能
- コアビジネスロジックに依存しない

## Documentation Standards

ドキュメンテーションのルール：

- **Docstrings**: すべての公開クラス、関数に必須（Google Styleまたは NumPy Style）
- **型ヒント**: すべての関数シグネチャに型ヒントを付与（PEP 484）
- **インラインコメント**: 複雑なロジックには簡潔な説明を追加
- **README**: 各主要モジュール（domain, application等）にREADME.mdを配置
- **OpenAPI**: FastAPIによる自動生成、`openapi.yaml` として出力

### Docstring 例

```python
def screen_candidate(candidate_text: str, threshold: float = 0.5) -> dict:
    """
    候補者情報をスクリーニングします。

    Args:
        candidate_text: 候補者のテキスト情報
        threshold: スクリーニング閾値（0.0〜1.0）

    Returns:
        スクリーニング結果を含む辞書
            - status: 処理ステータス
            - score: スコア
            - recommendation: 推奨アクション

    Raises:
        ValueError: テキストが空または長すぎる場合
    """
    # 実装...
```

## Testing Structure

テストディレクトリの構成原則：

- **テストはsrc構造を反映**: `tests/unit/domain/` は `src/screening_api/domain/` に対応
- **テストの独立性**: 各テストは他のテストに依存せず実行可能
- **Fixture活用**: `conftest.py` で共通Fixtureを定義
- **命名規則**: `test_<対象機能>_<条件>_<期待結果>()`（例: `test_screen_candidate_with_valid_text_returns_success()`）

### テスト構成例

```text
tests/
├── conftest.py                      # 共通Fixture定義
├── unit/
│   ├── domain/
│   │   └── test_screening_service.py
│   ├── application/
│   │   └── test_screening_use_case.py
│   └── infrastructure/
│       └── test_candidate_repository.py
├── integration/
│   └── test_api_integration.py
└── e2e/
    └── test_screening_endpoint.py
```

## Configuration Management

設定管理の方針：

- **環境変数**: 環境依存の設定（デプロイ先URL、ポート等）は環境変数で管理
- **設定ファイル**: `src/screening_api/infrastructure/config/settings.py` に集約
- **Pydantic Settings**: `pydantic-settings` で型安全な設定管理
- **シークレット管理**: `.env` ファイル（`.gitignore`対象）または外部シークレット管理サービス

### 設定例

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """アプリケーション設定"""
    app_name: str = "Screening API"
    api_version: str = "v1"
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```
