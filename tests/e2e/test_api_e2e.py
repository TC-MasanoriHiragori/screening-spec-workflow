"""
エンドツーエンドテスト: screening-api-core

APIの主要なユーザーシナリオをE2Eでテストします。
実際のユーザーワークフローを模倣して、システム全体の統合動作を検証します。
"""

import pytest
from fastapi.testclient import TestClient

from app.presentation.main import app


@pytest.fixture
def client():
    """TestClient フィクスチャ"""
    return TestClient(app)


class TestAPIEndToEnd:
    """APIのエンドツーエンドテスト"""

    def test_complete_screening_workflow(self, client):
        """
        完全なスクリーニングワークフロー
        1. ヘルスチェックでサービス稼働確認
        2. スクリーニングリクエスト送信
        3. レスポンスの検証
        """
        # Step 1: ヘルスチェック
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json() == {"status": "ok"}

        # Step 2: スクリーニング実行
        screening_request = {"content": "応募者のテキスト情報"}
        screening_response = client.post(
            "/v1/screenings",
            json=screening_request,
        )

        # Step 3: レスポンス検証
        assert screening_response.status_code == 200
        assert screening_response.json() == {"content": "応募者のテキスト情報"}

    def test_health_check_before_screening(self, client):
        """
        ヘルスチェック後にスクリーニングを実行するシナリオ
        """
        # まずヘルスチェック
        health = client.get("/health")
        assert health.status_code == 200

        # ヘルスチェック成功後、スクリーニング実行
        screening = client.post(
            "/v1/screenings",
            json={"content": "健全なサービスでスクリーニング"},
        )
        assert screening.status_code == 200
        assert screening.json()["content"] == "健全なサービスでスクリーニング"

    def test_multiple_screenings_in_sequence(self, client):
        """
        複数のスクリーニングを連続で実行するシナリオ
        """
        test_cases = [
            "応募者A の情報",
            "応募者B の情報",
            "応募者C の情報",
        ]

        for content in test_cases:
            response = client.post(
                "/v1/screenings",
                json={"content": content},
            )
            assert response.status_code == 200
            assert response.json()["content"] == content

    def test_error_recovery_workflow(self, client):
        """
        エラー発生後の回復ワークフロー
        1. 無効なリクエストでエラー
        2. 有効なリクエストで正常化
        """
        # Step 1: 無効なリクエスト
        invalid_response = client.post(
            "/v1/screenings",
            json={"invalid_field": "value"},
        )
        assert invalid_response.status_code == 422

        # Step 2: 有効なリクエストで回復
        valid_response = client.post(
            "/v1/screenings",
            json={"content": "有効なコンテンツ"},
        )
        assert valid_response.status_code == 200
        assert valid_response.json()["content"] == "有効なコンテンツ"

    def test_api_documentation_endpoints(self, client):
        """
        API ドキュメントエンドポイントの動作確認
        """
        # OpenAPI JSON
        openapi_response = client.get("/openapi.json")
        assert openapi_response.status_code == 200
        openapi_data = openapi_response.json()
        assert "openapi" in openapi_data
        assert "paths" in openapi_data

        # Swagger UI
        docs_response = client.get("/docs")
        assert docs_response.status_code == 200

        # ReDoc
        redoc_response = client.get("/redoc")
        assert redoc_response.status_code == 200

    def test_screening_with_various_content_types(self, client):
        """
        様々なコンテンツタイプでのスクリーニングワークフロー
        """
        test_contents = [
            "短いテキスト",
            "非常に長いテキスト" * 100,
            "日本語のテキスト",
            "English text",
            "混在 Mixed テキスト",
            "特殊文字 !@#$%^&*()",
            "",  # 空文字列
        ]

        for content in test_contents:
            response = client.post(
                "/v1/screenings",
                json={"content": content},
            )
            assert response.status_code == 200
            assert response.json()["content"] == content

    def test_concurrent_health_checks_and_screenings(self, client):
        """
        ヘルスチェックとスクリーニングの並行実行シナリオ
        """
        # ヘルスチェック
        health1 = client.get("/health")
        assert health1.status_code == 200

        # スクリーニング1
        screening1 = client.post(
            "/v1/screenings",
            json={"content": "並行処理1"},
        )
        assert screening1.status_code == 200

        # 再度ヘルスチェック
        health2 = client.get("/health")
        assert health2.status_code == 200

        # スクリーニング2
        screening2 = client.post(
            "/v1/screenings",
            json={"content": "並行処理2"},
        )
        assert screening2.status_code == 200

    def test_error_handling_across_endpoints(self, client):
        """
        複数のエンドポイント間でのエラーハンドリング
        """
        # ヘルスチェックは常に成功
        health = client.get("/health")
        assert health.status_code == 200

        # スクリーニングで無効なリクエスト
        invalid_screening = client.post(
            "/v1/screenings",
            json={},  # content フィールドなし
        )
        assert invalid_screening.status_code == 422

        # ヘルスチェックは引き続き正常
        health2 = client.get("/health")
        assert health2.status_code == 200

    def test_api_response_consistency(self, client):
        """
        APIレスポンスの一貫性を検証
        """
        # 同じリクエストを複数回送信
        request_data = {"content": "一貫性テスト"}
        responses = [
            client.post("/v1/screenings", json=request_data)
            for _ in range(3)
        ]

        # すべてのレスポンスが一貫していることを確認
        for response in responses:
            assert response.status_code == 200
            assert response.json() == {"content": "一貫性テスト"}

    def test_full_api_coverage(self, client):
        """
        全エンドポイントの包括的なテスト
        """
        # GET /health
        health = client.get("/health")
        assert health.status_code == 200
        assert "status" in health.json()

        # POST /v1/screenings (正常)
        screening_success = client.post(
            "/v1/screenings",
            json={"content": "包括テスト"},
        )
        assert screening_success.status_code == 200
        assert "content" in screening_success.json()

        # POST /v1/screenings (エラー)
        screening_error = client.post(
            "/v1/screenings",
            json={},
        )
        assert screening_error.status_code == 422

        # GET /openapi.json
        openapi = client.get("/openapi.json")
        assert openapi.status_code == 200

    def test_empty_and_whitespace_content_handling(self, client):
        """
        空文字列と空白文字の処理を検証
        """
        test_cases = [
            "",
            " ",
            "   ",
            "\n",
            "\t",
            "\n\t  \n",
        ]

        for content in test_cases:
            response = client.post(
                "/v1/screenings",
                json={"content": content},
            )
            assert response.status_code == 200
            assert response.json()["content"] == content
