"""
統合テスト: ヘルスチェックエンドポイント

GET /health エンドポイントの統合テストを実装します。
実際のアプリケーションに対してテストを実行し、ヘルスチェック機能を検証します。
"""

import time

import pytest
from fastapi.testclient import TestClient

from app.presentation.main import app


@pytest.fixture
def client():
    """TestClient フィクスチャ"""
    return TestClient(app)


class TestHealthEndpoint:
    """ヘルスチェックエンドポイントの統合テスト"""

    def test_health_check_returns_200(self, client):
        """GET /health が 200 を返すことをテスト"""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_returns_ok_status(self, client):
        """GET /health が {"status": "ok"} を返すことをテスト"""
        response = client.get("/health")
        assert response.json() == {"status": "ok"}

    def test_health_check_response_structure(self, client):
        """ヘルスチェックレスポンスの構造を検証"""
        response = client.get("/health")
        data = response.json()

        assert "status" in data
        assert isinstance(data["status"], str)
        assert len(data) == 1  # status フィールドのみ

    def test_health_check_content_type(self, client):
        """Content-Type が application/json であることを検証"""
        response = client.get("/health")
        assert "application/json" in response.headers["content-type"]

    def test_health_check_fast_response(self, client):
        """ヘルスチェックが高速にレスポンスを返すことを検証"""
        start_time = time.time()
        response = client.get("/health")
        elapsed_time = time.time() - start_time

        assert response.status_code == 200
        assert elapsed_time < 0.1  # 100ms以内にレスポンス

    def test_health_check_multiple_calls(self, client):
        """複数回呼び出しても一貫した結果を返すことを検証"""
        responses = [client.get("/health") for _ in range(5)]

        for response in responses:
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}

    def test_health_check_idempotency(self, client):
        """ヘルスチェックが冪等であることを検証"""
        response1 = client.get("/health")
        response2 = client.get("/health")

        assert response1.status_code == response2.status_code
        assert response1.json() == response2.json()

    def test_health_check_with_query_params_ignored(self, client):
        """クエリパラメータを送信しても無視されることを検証"""
        response = client.get("/health?param=value")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_health_check_method_post_not_allowed(self, client):
        """POST メソッドが許可されていないことを検証"""
        response = client.post("/health")
        assert response.status_code == 405  # Method Not Allowed

    def test_health_check_method_put_not_allowed(self, client):
        """PUT メソッドが許可されていないことを検証"""
        response = client.put("/health")
        assert response.status_code == 405  # Method Not Allowed

    def test_health_check_method_delete_not_allowed(self, client):
        """DELETE メソッドが許可されていないことを検証"""
        response = client.delete("/health")
        assert response.status_code == 405  # Method Not Allowed

    def test_health_check_method_patch_not_allowed(self, client):
        """PATCH メソッドが許可されていないことを検証"""
        response = client.patch("/health")
        assert response.status_code == 405  # Method Not Allowed

    def test_health_check_method_head_not_allowed(self, client):
        """HEAD メソッドの動作を検証"""
        response = client.head("/health")
        # FastAPI は HEAD を自動サポートしないため 405 を返す
        assert response.status_code == 405

    def test_health_check_response_headers(self, client):
        """レスポンスヘッダーが適切であることを検証"""
        response = client.get("/health")

        assert "content-type" in response.headers
        assert "application/json" in response.headers["content-type"]

    def test_health_check_no_authentication_required(self, client):
        """認証なしでアクセスできることを検証"""
        # 認証ヘッダーなしでリクエスト
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_benchmark(self, client):
        """ヘルスチェックのベンチマークテスト"""
        num_requests = 10
        times = []

        for _ in range(num_requests):
            start_time = time.time()
            response = client.get("/health")
            elapsed_time = time.time() - start_time

            assert response.status_code == 200
            times.append(elapsed_time)

        avg_time = sum(times) / len(times)
        assert avg_time < 0.05  # 平均50ms以内
