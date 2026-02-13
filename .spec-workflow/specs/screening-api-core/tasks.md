# Tasks Document - screening-api-core

## Phase 1: プロジェクトセットアップ

- [x] 1. プロジェクト基盤の構築
  - Files: `pyproject.toml`, `ruff.toml`, `.gitignore`, `README.md`
  - Purpose: uv によるプロジェクト管理基盤を構築し、ruff による Lint/Format 設定を行う
  - _Leverage: なし（新規プロジェクト）_
  - _Requirements: REQ-5 (EARS-15, EARS-17)_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: モダンなPythonツールとプロジェクトセットアップに特化したPython DevOpsエンジニア

    タスク: 要件 REQ-5 (EARS-15, EARS-17) に従って、screening-api-core のプロジェクト基盤を構築してください。uv パッケージマネージャーを使用してPython 3.12プロジェクトを初期化し、ruff によるリント・フォーマット設定を行い、基本的なプロジェクトファイルをセットアップしてください。

    制約事項:
    - poetry、pip、その他のパッケージマネージャーを使用しないこと
    - すべての依存関係管理に uv を使用すること
    - 初期セットアップに不要な依存関係を含めないこと
    - structure.md の命名規則に従うこと

    活用するもの:
    - なし（新規プロジェクト）

    要件:
    - REQ-5 (EARS-15): uv による依存関係管理、pyproject.toml、uv.lock
    - REQ-5 (EARS-17): ruff による Lint/Format 設定

    成功条件:
    - Python 3.12 要件を含む pyproject.toml が作成されている
    - uv.lock ファイルが生成されている
    - ruff.toml が Black 互換設定で構成されている（行長88文字、McCabe複雑度10）
    - .gitignore に Python 標準の除外設定が含まれている
    - プロジェクト概要を記載した README.md がある
    - `uv sync` でプロジェクトを初期化できる

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. タスクを実装する
    3. 完了後: log-implementation ツールを使用して、artifacts（成果物情報）を含む実装詳細を記録する
    4. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```

- [x] 2. ディレクトリ構造の作成
  - Files: `app/domain/`, `app/usecase/`, `app/infrastructure/`, `app/presentation/api/routes/`, `app/presentation/api/schemas/`, `tests/unit/domain/`, `tests/unit/usecase/`, `tests/unit/infrastructure/`, `tests/unit/presentation/`, `tests/integration/`, `tests/e2e/`
  - Purpose: オニオンアーキテクチャに基づいた4層構造のディレクトリを作成する
  - _Leverage: structure.md のディレクトリ定義_
  - _Requirements: REQ-3 (EARS-11)_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: クリーンアーキテクチャとプロジェクト構造に特化したソフトウェアアーキテクト

    タスク: 要件 REQ-3 (EARS-11) と structure.md に従って、screening-api-core のディレクトリ構造を作成してください。適切に分離された4層のオニオンアーキテクチャを実装してください：Domain層、Application層（usecase）、Infrastructure層、Presentation層。

    制約事項:
    - design.md で定義された正確なディレクトリ構造に従うこと
    - 不要にネストしたディレクトリを作成しないこと
    - オニオンアーキテクチャの原則から逸脱しないこと
    - 各層のディレクトリに __init__.py ファイルを含めること

    活用するもの:
    - .spec-workflow/steering/structure.md（ディレクトリ構成）
    - .spec-workflow/specs/screening-api-core/design.md（アーキテクチャ図）

    要件:
    - REQ-3 (EARS-11): 4層構造のディレクトリ作成

    成功条件:
    - すべての層のディレクトリが作成されている（domain、usecase、infrastructure、presentation）
    - Presentation層のサブディレクトリが作成されている（api/routes/、api/schemas/）
    - すべてのテストディレクトリが作成されている（unit/domain/、unit/usecase/、unit/infrastructure/、unit/presentation/、integration/、e2e/）
    - すべてのディレクトリに __init__.py ファイルが含まれている
    - 構造が design.md の仕様に一致している

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. タスクを実装する
    3. 完了後: log-implementation ツールを使用して、artifacts を含む実装詳細を記録する
    4. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```

## Phase 2: Domain層の実装

- [x] 3. ScreeningService インターフェースの定義
  - File: `app/domain/screening_service.py`
  - Purpose: スクリーニングサービスのインターフェースを Protocol で定義する
  - _Leverage: typing.Protocol_
  - _Requirements: REQ-3 (EARS-10), design.md Component 4_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: Python インターフェースとプロトコルに特化したドメイン駆動設計エキスパート

    タスク: 要件 REQ-3 (EARS-10) と design.md Component 4 に従って、typing.Protocol を使用して ScreeningService インターフェースを定義してください。スクリーニング操作の契約を定義する、フレームワークに依存しないインターフェースを作成してください。

    制約事項:
    - typing.Protocol を使用すること（抽象基底クラスは使用しない）
    - FastAPI やその他の外部フレームワークに依存しないこと
    - 実装の詳細を含めないこと
    - インターフェースを最小限に保ち、焦点を絞ること（単一責任の原則）
    - structure.md の docstring 規約に従うこと

    活用するもの:
    - typing.Protocol（構造的部分型付け）
    - .spec-workflow/steering/structure.md（docstring の例）

    要件:
    - REQ-3 (EARS-10): Domain層でインターフェースを定義

    成功条件:
    - screen(content: str) -> str メソッドを持つ ScreeningService Protocol が定義されている
    - 型ヒントが完全かつ正確である
    - docstring が Google/NumPy スタイルに従っている
    - 外部依存がない（Pure Python）
    - __all__ でエクスポートが定義されている

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. タスクを実装する
    3. 完了後: log-implementation ツールを使用して、artifacts（classes）を含む実装詳細を記録する
    4. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```

- [x] 4. Domain層のユニットテスト
  - File: `tests/unit/domain/test_screening_service.py`
  - Purpose: ScreeningService Protocol の型チェックと準拠性をテストする
  - _Leverage: pytest, typing.Protocol_
  - _Requirements: REQ-3 (EARS-10), design.md Testing Strategy_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: Python ユニットテストと型システムに精通したQAエンジニア

    タスク: 要件 REQ-3 (EARS-10) と design.md Testing Strategy に従って、ScreeningService Protocol のユニットテストを作成してください。Protocol が正しく定義されており、実装がそれに準拠できることを検証してください。

    制約事項:
    - 実装の詳細をテストしないこと（インターフェース契約のみをテスト）
    - テストフレームワークとして pytest を使用すること
    - structure.md のテスト命名規則に従うこと
    - FastAPI やインフラストラクチャコードをインポートしないこと

    活用するもの:
    - pytest フレームワーク
    - app/domain/screening_service.py（Protocol 定義）
    - .spec-workflow/steering/structure.md（テスト命名規則）

    要件:
    - REQ-3 (EARS-10): Domain層のテスト
    - Design.md: Domain層ユニットテスト

    成功条件:
    - 適切な命名でテストファイルが作成されている（test_screening_service.py）
    - テストが Protocol の構造（メソッドシグネチャ）を検証している
    - テストがモック実装を作成して Protocol 準拠を検証している
    - すべてのテストが pytest で合格する
    - テストが structure.md の命名規則に従っている（test_<function>_<condition>_<expected>）

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. タスクを実装する
    3. 完了後: log-implementation ツールを使用して、artifacts（functions）を含む実装詳細を記録する
    4. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```

## Phase 3: Infrastructure層の実装

- [x] 5. EchoScreeningService 実装
  - File: `app/infrastructure/screening_service_impl.py`
  - Purpose: 入力値をそのまま返す暫定的なスクリーニング実装を作成する
  - _Leverage: app/domain/screening_service.py_
  - _Requirements: REQ-1 (EARS-01), REQ-3 (EARS-10), design.md Component 5_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: サービスパターンとクリーンアーキテクチャの実装に精通したバックエンド開発者

    タスク: 要件 REQ-1 (EARS-01)、REQ-3 (EARS-10)、および design.md Component 5 に従って、ScreeningService Protocol に準拠する EchoScreeningService を実装してください。入力コンテンツをそのまま返すシンプルな実装を作成してください。

    制約事項:
    - ScreeningService Protocol を実装すること（構造的部分型付け）
    - Protocol から明示的に継承しないこと（暗黙的準拠）
    - 実装をシンプルに保つこと（複雑なロジックは不要）
    - 外部サービスへの依存を追加しないこと
    - structure.md のコード構成に従うこと

    活用するもの:
    - app/domain/screening_service.py（ScreeningService Protocol）
    - .spec-workflow/steering/structure.md（コード構成パターン）

    要件:
    - REQ-1 (EARS-01): 入力値をそのまま返す実装
    - REQ-3 (EARS-10): Infrastructure層でインターフェースを実装

    成功条件:
    - screen(content: str) -> str メソッドを持つ EchoScreeningService クラスが定義されている
    - メソッドが入力コンテンツを変更せずに返す
    - 型ヒントが完全である
    - docstring が Google/NumPy スタイルに従っている
    - ScreeningService Protocol に暗黙的に準拠している
    - __all__ でエクスポートが定義されている

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. タスクを実装する
    3. 完了後: log-implementation ツールを使用して、artifacts（classes）を含む実装詳細を記録する
    4. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```

- [x] 6. Infrastructure層のユニットテスト
  - File: `tests/unit/infrastructure/test_screening_service_impl.py`
  - Purpose: EchoScreeningService の実装ロジックをテストする
  - _Leverage: pytest, app/infrastructure/screening_service_impl.py_
  - _Requirements: REQ-1 (EARS-01), design.md Testing Strategy_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: ユニットテストとテスト駆動開発に精通したQAエンジニア

    タスク: 要件 REQ-1 (EARS-01) と design.md Testing Strategy に従って、EchoScreeningService のユニットテストを作成してください。エッジケースを含むさまざまな入力でエコー実装をテストしてください。

    制約事項:
    - 実装の動作をテストすること（インターフェースだけでなく）
    - 複数のシナリオのためにパラメータ化されたテストで pytest を使用すること
    - structure.md のテスト命名規則に従うこと
    - エッジケースをテストすること（空文字列、長文テキスト、特殊文字）

    活用するもの:
    - pytest フレームワーク（parametrize 付き）
    - app/infrastructure/screening_service_impl.py（EchoScreeningService）
    - .spec-workflow/steering/structure.md（テスト規約）

    要件:
    - REQ-1 (EARS-01): エコー実装のテスト
    - Design.md: Infrastructure層ユニットテスト

    成功条件:
    - 適切な命名でテストファイルが作成されている
    - テストが通常の入力シナリオをカバーしている
    - テストがエッジケース（空文字列、長文テキスト、Unicode）をカバーしている
    - すべてのテストが pytest で合格する
    - EchoScreeningService のテストカバレッジが80%以上である

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. タスクを実装する
    3. 完了後: log-implementation ツールを使用して、artifacts（functions）を含む実装詳細を記録する
    4. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```

## Phase 4: Application層の実装

- [x] 7. ScreeningUsecase 実装
  - File: `app/usecase/screening_usecase.py`
  - Purpose: スクリーニングユースケースのオーケストレーションを実装する
  - _Leverage: app/domain/screening_service.py_
  - _Requirements: REQ-3 (EARS-09, EARS-10), design.md Component 3_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: ユースケース設計と依存性注入に特化したアプリケーションアーキテクト

    タスク: 要件 REQ-3 (EARS-09, EARS-10) と design.md Component 3 に従って、スクリーニング操作をオーケストレートする ScreeningUsecase を実装してください。依存性注入を使用して ScreeningService 実装を受け取ってください。

    制約事項:
    - Domain層（ScreeningService Protocol）のみに依存すること
    - Infrastructure層や Presentation層に依存しないこと
    - FastAPI や具体的な実装をインポートしないこと
    - 依存関係にコンストラクタ注入を使用すること
    - structure.md のコード構成に従うこと

    活用するもの:
    - app/domain/screening_service.py（ScreeningService Protocol）
    - .spec-workflow/steering/structure.md（依存性注入パターン）

    要件:
    - REQ-3 (EARS-09): Application層はDomain層のみに依存
    - REQ-3 (EARS-10): Usecase層がDomain層インターフェースを呼び出す

    成功条件:
    - execute(content: str) -> str メソッドを持つ ScreeningUsecase クラスが定義されている
    - コンストラクタが ScreeningService を受け取る（Protocol 型ヒント）
    - execute() が service.screen() を呼び出して結果を返す
    - 型ヒントが完全である
    - docstring が Google/NumPy スタイルに従っている
    - 外側の層への依存がない
    - __all__ でエクスポートが定義されている

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. タスクを実装する
    3. 完了後: log-implementation ツールを使用して、artifacts（classes）を含む実装詳細を記録する
    4. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```

- [x] 8. Application層のユニットテスト
  - File: `tests/unit/usecase/test_screening_usecase.py`
  - Purpose: ScreeningUsecase のオーケストレーションロジックをモックでテストする
  - _Leverage: pytest, unittest.mock, app/usecase/screening_usecase.py_
  - _Requirements: REQ-3 (EARS-10), design.md Testing Strategy_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: ユニットテストとモックフレームワークに精通したQAエンジニア

    タスク: 要件 REQ-3 (EARS-10) と design.md Testing Strategy に従って、ScreeningUsecase のユニットテストを作成してください。モックを使用してユースケースをサービス実装から分離してください。

    制約事項:
    - ScreeningService をモック化すること（実装を使用しない）
    - unittest.mock または pytest-mock を使用すること
    - ユースケースのオーケストレーションロジックのみをテストすること
    - structure.md のテスト命名規則に従うこと

    活用するもの:
    - pytest フレームワーク
    - unittest.mock.MagicMock（ScreeningService のモック化）
    - app/usecase/screening_usecase.py（ScreeningUsecase）
    - .spec-workflow/steering/structure.md（テスト規約）

    要件:
    - REQ-3 (EARS-10): Application層のテスト
    - Design.md: Application層ユニットテスト

    成功条件:
    - 適切な命名でテストファイルが作成されている
    - ScreeningService が適切にモック化されている
    - テストが execute() が正しい引数で service.screen() を呼び出すことを検証している
    - テストが execute() が service.screen() の結果を返すことを検証している
    - すべてのテストが pytest で合格する
    - ScreeningUsecase のテストカバレッジが80%以上である

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. タスクを実装する
    3. 完了後: log-implementation ツールを使用して、artifacts（functions）を含む実装詳細を記録する
    4. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```

## Phase 5: Presentation層の実装

- [x] 9. Pydantic スキーマの定義
  - File: `app/presentation/api/schemas/screening.py`
  - Purpose: リクエスト/レスポンスのPydanticスキーマを定義する
  - _Leverage: pydantic.BaseModel_
  - _Requirements: REQ-1 (EARS-01, EARS-02), REQ-2 (EARS-05), design.md Component 2_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: データバリデーションとPydanticスキーマに特化したAPI設計者

    タスク: 要件 REQ-1 (EARS-01, EARS-02)、REQ-2 (EARS-05)、および design.md Component 2 に従って、スクリーニングAPIのPydanticスキーマを定義してください。ScreeningRequest、ScreeningResponse、HealthResponse モデルを作成してください。

    制約事項:
    - Pydantic BaseModel を使用すること
    - 要件からの正確なフィールド名に従うこと（content、status）
    - OpenAPI ドキュメント用に Field の説明を追加すること
    - 例を含む json_schema_extra を含めること
    - structure.md のコード構成に従うこと

    活用するもの:
    - pydantic.BaseModel、pydantic.Field
    - .spec-workflow/steering/structure.md（コード構成）
    - .spec-workflow/specs/screening-api-core/design.md（データモデル）

    要件:
    - REQ-1 (EARS-01): content フィールドを持つ ScreeningRequest
    - REQ-1 (EARS-01): content フィールドのみを持つ ScreeningResponse
    - REQ-2 (EARS-05): status フィールドを持つ HealthResponse

    成功条件:
    - content: str フィールドを持つ ScreeningRequest が定義されている
    - content: str フィールドのみを持つ ScreeningResponse が定義されている（他のフィールドなし）
    - status: str フィールド（default="ok"）を持つ HealthResponse が定義されている
    - すべてのフィールドに Field の説明がある
    - json_schema_extra にドキュメント用の例が含まれている
    - 型ヒントが完全である
    - docstring が Google/NumPy スタイルに従っている
    - __all__ でエクスポートが定義されている

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. タスクを実装する
    3. 完了後: log-implementation ツールを使用して、artifacts（classes）を含む実装詳細を記録する
    4. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```

- [x] 10. Presentation層スキーマのユニットテスト
  - File: `tests/unit/presentation/test_schemas.py`
  - Purpose: Pydantic スキーマのバリデーションをテストする
  - _Leverage: pytest, app/presentation/api/schemas/screening.py_
  - _Requirements: REQ-1 (EARS-02), design.md Testing Strategy_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: データバリデーションとスキーマテストに精通したQAエンジニア

    タスク: 要件 REQ-1 (EARS-02) と design.md Testing Strategy に従って、Pydantic スキーマのユニットテストを作成してください。バリデーション成功と失敗のシナリオをテストしてください。

    制約事項:
    - 有効なデータと無効なデータの両方をテストすること
    - パラメータ化されたテストで pytest を使用すること
    - Pydantic ValidationError シナリオをテストすること
    - structure.md のテスト命名規則に従うこと

    活用するもの:
    - pytest フレームワーク（parametrize 付き）
    - pydantic.ValidationError
    - app/presentation/api/schemas/screening.py（スキーマ）
    - .spec-workflow/steering/structure.md（テスト規約）

    要件:
    - REQ-1 (EARS-02): バリデーションエラーのテスト
    - Design.md: Presentation層ユニットテスト

    成功条件:
    - 適切な命名でテストファイルが作成されている
    - テストが有効なデータで ScreeningRequest のバリデーションが成功することを検証している
    - テストが content フィールドが欠けている ScreeningRequest のバリデーションが失敗することを検証している
    - テストが ScreeningResponse の構造を検証している
    - テストが HealthResponse のデフォルト値を検証している
    - すべてのテストが pytest で合格する
    - スキーマのテストカバレッジが80%以上である

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. タスクを実装する
    3. 完了後: log-implementation ツールを使用して、artifacts（functions）を含む実装詳細を記録する
    4. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```

- [x] 11. 依存性注入の設定
  - File: `app/presentation/api/dependencies.py`
  - Purpose: FastAPI の Depends で Infrastructure層の実装を注入する設定を作成する
  - _Leverage: FastAPI Depends, app/domain/screening_service.py, app/infrastructure/screening_service_impl.py, app/usecase/screening_usecase.py_
  - _Requirements: REQ-3 (EARS-09), design.md Deployment Considerations_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: FastAPI 依存性注入に精通したバックエンド開発者

    タスク: 要件 REQ-3 (EARS-09) と design.md Deployment Considerations に従って、FastAPI の依存性注入設定を作成してください。ScreeningService と ScreeningUsecase を注入するファクトリ関数をセットアップしてください。

    制約事項:
    - FastAPI Depends パターンを使用すること
    - 可能な場合は Protocol 型ヒントを返すこと（具体型ではなく）
    - 依存関係をシンプルに保つこと（複雑な初期化なし）
    - structure.md のコード構成に従うこと

    活用するもの:
    - FastAPI Depends
    - app/domain/screening_service.py（ScreeningService Protocol）
    - app/infrastructure/screening_service_impl.py（EchoScreeningService）
    - app/usecase/screening_usecase.py（ScreeningUsecase）
    - .spec-workflow/steering/structure.md（依存性注入パターン）

    要件:
    - REQ-3 (EARS-09): 依存性注入による層間の疎結合

    成功条件:
    - get_screening_service() 関数が EchoScreeningService を返す
    - get_screening_usecase() 関数が Depends(get_screening_service) を使用する
    - 型ヒントが該当する場合に Protocol 型を使用している
    - 関数が適切に型付けされている
    - docstring が依存性注入の目的を説明している
    - __all__ でエクスポートが定義されている

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. タスクを実装する
    3. 完了後: log-implementation ツールを使用して、artifacts（functions、integrations）を含む実装詳細を記録する
    4. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```

- [x] 12. スクリーニングルーターの実装
  - File: `app/presentation/api/routes/screenings.py`
  - Purpose: POST /v1/screenings エンドポイントを実装する
  - _Leverage: FastAPI APIRouter, app/presentation/api/schemas/screening.py, app/presentation/api/dependencies.py_
  - _Requirements: REQ-1 (EARS-01, EARS-02, EARS-03, EARS-04), design.md Component 1_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: FastAPI と RESTful 設計に特化したバックエンドAPI開発者

    タスク: 要件 REQ-1 (EARS-01〜04) と design.md Component 1 に従って、POST /v1/screenings エンドポイントを持つスクリーニングルーターを実装してください。依存性注入を使用して ScreeningUsecase を受け取ってください。

    制約事項:
    - FastAPI APIRouter を使用すること
    - エンドポイントパスは正確に "/v1/screenings" でなければならない
    - ScreeningUsecase の注入に Depends を使用すること
    - レスポンスには "content" フィールドのみを含めること（status、result 等なし）
    - structure.md のコード構成に従うこと

    活用するもの:
    - FastAPI APIRouter、Depends
    - app/presentation/api/schemas/screening.py（ScreeningRequest、ScreeningResponse）
    - app/presentation/api/dependencies.py（get_screening_usecase）
    - .spec-workflow/steering/structure.md（ルーターパターン）

    要件:
    - REQ-1 (EARS-01): {"content": "..."} を返す POST /v1/screenings エンドポイント
    - REQ-1 (EARS-02): FastAPI 自動422バリデーション
    - REQ-1 (EARS-03): FastAPI 自動415 Content-Type ハンドリング
    - REQ-1 (EARS-04): 応答時間 <500ms（実装は高速であるべき）

    成功条件:
    - prefix と tags を持つ APIRouter が作成されている
    - response_model=ScreeningResponse で POST /v1/screenings エンドポイントが定義されている
    - エンドポイントが ScreeningRequest を受け取り、Depends 経由で ScreeningUsecase を使用する
    - エンドポイントが usecase.execute() を呼び出し、ScreeningResponse を返す
    - レスポンスに content フィールドのみが含まれている
    - OpenAPI ドキュメントが正しく自動生成される
    - __all__ でルーターがエクスポートされている

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. タスクを実装する
    3. 完了後: log-implementation ツールを使用して、artifacts（apiEndpoints、functions、integrations）を含む実装詳細を記録する
    4. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```

- [x] 13. ヘルスチェックルーターの実装
  - File: `app/presentation/api/routes/health.py`
  - Purpose: GET /health エンドポイントを実装する
  - _Leverage: FastAPI APIRouter, app/presentation/api/schemas/screening.py_
  - _Requirements: REQ-2 (EARS-05, EARS-06, EARS-07), design.md Component 1_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: FastAPI とヘルスチェックエンドポイントに特化したバックエンドAPI開発者

    タスク: 要件 REQ-2 (EARS-05〜07) と design.md Component 1 に従って、GET /health エンドポイントを持つヘルスチェックルーターを実装してください。ヘルスステータスを返すシンプルなエンドポイントを作成してください。

    制約事項:
    - FastAPI APIRouter を使用すること
    - エンドポイントパスは正確に "/health" でなければならない
    - 認証を要求してはいけない
    - 非常に高速でなければならない（<100ms）
    - structure.md のコード構成に従うこと

    活用するもの:
    - FastAPI APIRouter
    - app/presentation/api/schemas/screening.py（HealthResponse）
    - .spec-workflow/steering/structure.md（ルーターパターン）

    要件:
    - REQ-2 (EARS-05): {"status": "ok"} を返す GET /health
    - REQ-2 (EARS-06): 応答時間 <100ms
    - REQ-2 (EARS-07): 認証不要

    成功条件:
    - 適切な tags を持つ APIRouter が作成されている
    - response_model=HealthResponse で GET /health エンドポイントが定義されている
    - エンドポイントが HealthResponse(status="ok") を返す
    - 依存関係や複雑なロジックがない（高速レスポンス）
    - OpenAPI ドキュメントが正しく自動生成される
    - __all__ でルーターがエクスポートされている

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. タスクを実装する
    3. 完了後: log-implementation ツールを使用して、artifacts（apiEndpoints、functions）を含む実装詳細を記録する
    4. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```

- [x] 14. FastAPIアプリケーションのエントリーポイント実装
  - File: `app/presentation/main.py`
  - Purpose: FastAPI アプリケーションを作成し、ルーターを登録する
  - _Leverage: FastAPI, app/presentation/api/routes/screenings.py, app/presentation/api/routes/health.py_
  - _Requirements: REQ-5 (EARS-18), design.md Component 6_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: FastAPI アプリケーションセットアップに精通したバックエンド開発者

    タスク: 要件 REQ-5 (EARS-18) と design.md Component 6 に従って、FastAPI アプリケーションのエントリーポイントを作成してください。スクリーニングとヘルスルーターを登録し、OpenAPI 用にアプリメタデータを設定してください。

    制約事項:
    - 適切なメタデータ（title、version）で FastAPI インスタンスを作成すること
    - 両方のルーター（screenings、health）を含めること
    - 設定をシンプルに保つこと（今のところ複雑なミドルウェアなし）
    - structure.md のコード構成に従うこと

    活用するもの:
    - FastAPI
    - app/presentation/api/routes/screenings.py（screenings_router）
    - app/presentation/api/routes/health.py（health_router）
    - .spec-workflow/steering/structure.md（main.py パターン）

    要件:
    - REQ-5 (EARS-18): `uv run fastapi dev` で FastAPI 開発サーバーを起動可能

    成功条件:
    - title="Screening API" と version="1.0.0" で FastAPI アプリインスタンスが作成されている
    - Screenings ルーターが含まれている
    - Health ルーターが含まれている
    - `uv run fastapi dev app/presentation/main.py` でアプリを起動できる
    - OpenAPI ドキュメントが /docs と /redoc でアクセス可能
    - /openapi.json エンドポイントが正しい仕様を生成する

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. タスクを実装する
    3. 完了後: log-implementation ツールを使用して、artifacts（integrations）を含む実装詳細を記録する
    4. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```

## Phase 6: 統合テスト

- [x] 15. スクリーニングエンドポイントの統合テスト
  - File: `tests/integration/test_screening_integration.py`
  - Purpose: /v1/screenings エンドポイントの統合テストを実装する
  - _Leverage: FastAPI TestClient, app/presentation/main.py_
  - _Requirements: REQ-1 (EARS-01, EARS-02, EARS-03), design.md Testing Strategy_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: API 統合テストと FastAPI TestClient に精通したQAエンジニア

    タスク: 要件 REQ-1 (EARS-01〜03) と design.md Testing Strategy に従って、/v1/screenings エンドポイントの統合テストを作成してください。完全なリクエスト-レスポンスサイクルをテストしてください。

    制約事項:
    - FastAPI TestClient を使用すること（実際のHTTPクライアントではなく）
    - 実際のアプリに対してテストすること（モックなし）
    - 成功とエラーのシナリオをカバーすること
    - structure.md のテスト命名規則に従うこと

    活用するもの:
    - FastAPI TestClient
    - app/presentation/main.py（FastAPI app）
    - .spec-workflow/steering/structure.md（テスト規約）

    要件:
    - REQ-1 (EARS-01): POST /v1/screenings が content フィールドを返すことをテスト
    - REQ-1 (EARS-02): content フィールドが欠けていると 422 を返すことをテスト
    - REQ-1 (EARS-03): 間違った Content-Type で 415 を返すことをテスト

    成功条件:
    - 適切な命名でテストファイルが作成されている
    - テストが有効なリクエストを送信し、content フィールドを持つ 200 レスポンスを検証する
    - テストがレスポンスに content フィールドのみが含まれることを検証する（余分なフィールドなし）
    - テストが content フィールドなしでリクエストを送信し、422 エラーを検証する
    - テストが間違った Content-Type でリクエストを送信し、415 エラーを検証する
    - すべてのテストが pytest で合格する
    - テストが TestClient を正しく使用している

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. タスクを実装する
    3. 完了後: log-implementation ツールを使用して、artifacts（functions）を含む実装詳細を記録する
    4. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```

- [x] 16. ヘルスチェックエンドポイントの統合テスト
  - File: `tests/integration/test_health_integration.py`
  - Purpose: /health エンドポイントの統合テストを実装する
  - _Leverage: FastAPI TestClient, app/presentation/main.py_
  - _Requirements: REQ-2 (EARS-05, EARS-06), design.md Testing Strategy_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: API 統合テストに精通したQAエンジニア

    タスク: 要件 REQ-2 (EARS-05, EARS-06) と design.md Testing Strategy に従って、/health エンドポイントの統合テストを作成してください。ヘルスチェック機能を検証してください。

    制約事項:
    - FastAPI TestClient を使用すること
    - 実際のアプリに対してテストすること（モックなし）
    - レスポンス構造とステータスを検証すること
    - structure.md のテスト命名規則に従うこと

    活用するもの:
    - FastAPI TestClient
    - app/presentation/main.py（FastAPI app）
    - .spec-workflow/steering/structure.md（テスト規約）

    要件:
    - REQ-2 (EARS-05): GET /health が {"status": "ok"} を返すことをテスト
    - REQ-2 (EARS-06): 高速レスポンスタイムを検証

    成功条件:
    - 適切な命名でテストファイルが作成されている
    - テストが GET /health リクエストを送信し、200 レスポンスを検証する
    - テストがレスポンスに {"status": "ok"} が含まれることを検証する
    - テストがレスポンスタイムを測定する（非常に高速であるべき）
    - すべてのテストが pytest で合格する

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. タスクを実装する
    3. 完了後: log-implementation ツールを使用して、artifacts（functions）を含む実装詳細を記録する
    4. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```

## Phase 7: End-to-End テストとOpenAPI出力

- [-] 17. End-to-Endテストの実装
  - File: `tests/e2e/test_api_e2e.py`
  - Purpose: APIの主要なユーザーシナリオをE2Eでテストする
  - _Leverage: FastAPI TestClient または httpx, app/presentation/main.py_
  - _Requirements: 全要件, design.md Testing Strategy_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: エンドツーエンドテストに精通したQA自動化エンジニア

    タスク: 全要件と design.md Testing Strategy に従って、スクリーニングAPIのエンドツーエンドテストを作成してください。両方のエンドポイントにわたる現実的なユーザーシナリオをテストしてください。

    制約事項:
    - TestClient または実際のHTTPクライアント（httpx）を使用できる
    - 現実的なユーザーワークフローをテストすること
    - ハッピーパスとエラーシナリオをカバーすること
    - structure.md のテスト命名規則に従うこと

    活用するもの:
    - FastAPI TestClient または httpx
    - app/presentation/main.py（FastAPI app）
    - .spec-workflow/steering/structure.md（テスト規約）

    要件:
    - 全要件（REQ-1、REQ-2）
    - Design.md: E2E テスト戦略

    成功条件:
    - 適切な命名でテストファイルが作成されている
    - テストシナリオ：ヘルスチェック → スクリーニング送信 → レスポンス検証
    - テストが完全なユーザーワークフローを検証する
    - テストがエラーシナリオ（無効な入力）を含む
    - すべてのテストが pytest で合格する
    - テストがエンドツーエンドの機能を検証する

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. タスクを実装する
    3. 完了後: log-implementation ツールを使用して、artifacts（functions）を含む実装詳細を記録する
    4. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```

- [x] 18. OpenAPI仕様書の出力
  - File: `openapi.yaml`, `scripts/export_openapi.py`
  - Purpose: OpenAPI 3.0仕様書をYAML形式でエクスポートする
  - _Leverage: FastAPI openapi() method, PyYAML_
  - _Requirements: REQ-4 (EARS-12, EARS-13, EARS-14), design.md Deployment Considerations_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: API ドキュメントと OpenAPI 仕様に精通した DevOps エンジニア

    タスク: 要件 REQ-4 (EARS-12〜14) と design.md Deployment Considerations に従って、OpenAPI 仕様をエクスポートするスクリプトを作成してください。FastAPI アプリから openapi.yaml を生成してください。

    制約事項:
    - FastAPI の app.openapi() メソッドを使用すること
    - 出力は有効な YAML 形式でなければならない
    - PyYAML ライブラリを使用すること
    - スクリプトは `uv run` で実行可能でなければならない
    - structure.md のコード構成に従うこと

    活用するもの:
    - FastAPI app.openapi() メソッド
    - PyYAML ライブラリ（YAML 出力用）
    - app/presentation/main.py（FastAPI app）
    - .spec-workflow/steering/structure.md（スクリプトパターン）

    要件:
    - REQ-4 (EARS-12): プロジェクトルートに openapi.yaml を出力
    - REQ-4 (EARS-13): OpenAPI 3.0+ 形式
    - REQ-4 (EARS-14): すべてのエンドポイントとスキーマを含む

    成功条件:
    - scripts/export_openapi.py が作成されている
    - スクリプトが app.presentation.main から app をインポートする
    - スクリプトが app.openapi() を呼び出し、openapi.yaml にエクスポートする
    - openapi.yaml が有効な OpenAPI 3.0+ 仕様である
    - YAML に /v1/screenings と /health エンドポイントが含まれている
    - YAML に ScreeningRequest、ScreeningResponse、HealthResponse スキーマが含まれている
    - スクリプトを `uv run python scripts/export_openapi.py` で実行できる
    - PyYAML が pyproject.toml の依存関係に追加されている

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. タスクを実装する
    3. 完了後: log-implementation ツールを使用して、artifacts（functions）を含む実装詳細を記録する
    4. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```

## Phase 8: 最終統合と文書化

- [-] 19. プロジェクト文書の作成
  - File: `README.md`, `app/README.md`, `tests/README.md`
  - Purpose: プロジェクトの概要、セットアップ手順、使用方法を文書化する
  - _Leverage: design.md, requirements.md_
  - _Requirements: 全要件, structure.md Documentation Standards_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: API ドキュメントに精通したテクニカルライター

    タスク: 全要件と structure.md Documentation Standards に従って、README ファイルを含む包括的なプロジェクトドキュメントを作成してください。セットアップ、使用方法、アーキテクチャを文書化してください。

    制約事項:
    - uv を使用したセットアップ手順を含めること
    - すべての使用可能なコマンドを文書化すること
    - アーキテクチャ層を説明すること
    - structure.md のドキュメント標準に従うこと

    活用するもの:
    - .spec-workflow/specs/screening-api-core/design.md（アーキテクチャ概要）
    - .spec-workflow/specs/screening-api-core/requirements.md（機能説明）
    - .spec-workflow/steering/structure.md（ドキュメント標準）

    要件:
    - 全要件（包括的なドキュメント）
    - Structure.md: ドキュメント標準

    成功条件:
    - ルート README.md にプロジェクト概要、セットアップ、使用方法、アーキテクチャが含まれている
    - README に uv のインストールとプロジェクトセットアップが文書化されている
    - README に API リクエストの例（curl 例）が含まれている
    - README にオニオンアーキテクチャ層が説明されている
    - app/README.md にコード構造が説明されている
    - tests/README.md にテスト構造とテスト実行方法が説明されている
    - すべてのコマンドが文書化されている（開発サーバー、テスト、リント、OpenAPI エクスポート）

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. タスクを実装する
    3. 完了後: log-implementation ツールを使用して、artifacts を含む実装詳細を記録する
    4. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```

- [ ] 20. 最終統合確認とクリーンアップ
  - Files: 全プロジェクトファイル
  - Purpose: 全機能が統合され、要件を満たしていることを確認し、コードをクリーンアップする
  - _Leverage: ruff, pytest, design.md_
  - _Requirements: 全要件_
  - _Prompt:

    ```text
    spec screening-api-core のタスクを実装してください。最初に spec-workflow-guide を実行してワークフローガイドを取得してから、タスクを実装してください。

    役割: コード品質とシステム統合に精通したシニアソフトウェアエンジニア

    タスク: 全要件をカバーする screening-api-core の最終統合検証とコードクリーンアップを実施してください。すべてのコンポーネントが正しく連携し、コード品質基準を満たしていることを確認してください。

    制約事項:
    - 既存の機能を壊さないこと
    - すべてのテストを実行し、合格を確認すること
    - ruff check と ruff format を実行すること
    - OpenAPI 仕様が正しいことを検証すること
    - structure.md のコード品質ガイドラインに従うこと

    活用するもの:
    - ruff check と ruff format
    - pytest（すべてのテストスイート）
    - FastAPI app（手動テスト）
    - .spec-workflow/specs/screening-api-core/design.md（アーキテクチャ検証）
    - .spec-workflow/specs/screening-api-core/requirements.md（要件チェックリスト）
    - .spec-workflow/steering/structure.md（コード品質ガイドライン）

    要件:
    - 全要件（REQ-1 から REQ-5）

    成功条件:
    - すべてのユニットテストが合格する（pytest tests/unit/）
    - すべての統合テストが合格する（pytest tests/integration/）
    - すべての E2E テストが合格する（pytest tests/e2e/）
    - ruff check がエラーなしで合格する
    - ruff format がすべてのコードに適用されている
    - FastAPI 開発サーバーが正常に起動する
    - /v1/screenings エンドポイントが正しく動作する（手動テスト）
    - /health エンドポイントが正しく動作する（手動テスト）
    - /docs と /redoc が正しくレンダリングされる
    - openapi.yaml が生成され、有効である
    - requirements.md のすべての要件が満たされている
    - アーキテクチャが design.md の仕様に一致している
    - コードが structure.md のガイドラインに従っている

    手順:
    1. 開始前: .spec-workflow/specs/screening-api-core/tasks.md を編集し、このタスクのステータスを [ ] から [-] に変更する
    2. すべての要件を体系的に検証する
    3. すべての品質チェックとテストを実行する
    4. 見つかった問題を修正する
    5. 完了後: log-implementation ツールを使用して、最終検証結果を記録する
    6. ログ記録後: tasks.md を編集し、このタスクのステータスを [-] から [x] に変更する
    ```
