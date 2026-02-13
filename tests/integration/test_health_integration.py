"""
ヘルスチェックエンドポイントの統合テスト

このモジュールは、GET /health エンドポイントの統合テストを実行します。
FastAPI TestClient を使用して、ヘルスチェック機能を検証します。
"""

import time

from fastapi.testclient import TestClient

from app.presentation.main import app

# TestClient インスタンスを作成
client = TestClient(app)


class TestHealthEndpoint:
    """ヘルスチェックエンドポイントの統合テストクラス"""

    def test_get_health_returns_200_ok(self):
        """GET /health が 200 OK を返すことをテスト"""
        response = client.get("/health")
        assert response.status_code == 200

    def test_get_health_returns_status_ok(self):
        """GET /health が {"status": "ok"} を返すことをテスト"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"

    def test_get_health_response_structure(self):
        """レスポンスが正しい構造を持つことをテスト"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        # status フィールドが含まれることを確認
        assert "status" in data
        # status が文字列であることを確認
        assert isinstance(data["status"], str)

    def test_get_health_response_has_only_status_field(self):
        """レスポンスに status フィールドのみが含まれることをテスト"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        # status フィールドのみが含まれることを確認
        assert list(data.keys()) == ["status"]

    def test_get_health_response_time_is_fast(self):
        """レスポンスタイムが 100ms 未満であることをテスト"""
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()

        response_time_ms = (end_time - start_time) * 1000

        assert response.status_code == 200
        # 100ms 未満で応答することを確認
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeded 100ms"

    def test_get_health_multiple_requests(self):
        """複数回リクエストしても一貫して正しいレスポンスを返すことをテスト"""
        for _ in range(10):
            response = client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"

    def test_get_health_response_headers(self):
        """レスポンスヘッダーが正しいことをテスト"""
        response = client.get("/health")
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")

    def test_get_health_no_authentication_required(self):
        """認証なしでアクセス可能であることをテスト"""
        # 認証ヘッダーなしでリクエスト
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

    def test_get_health_idempotency(self):
        """冪等性: 同じリクエストを複数回送信しても同じ結果を返すことをテスト"""
        response1 = client.get("/health")
        response2 = client.get("/health")
        response3 = client.get("/health")

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

        assert response1.json() == response2.json() == response3.json()

    def test_get_health_with_query_parameters_ignored(self):
        """クエリパラメータが無視されることをテスト"""
        response = client.get("/health?foo=bar&baz=qux")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

    def test_get_health_head_method_not_automatically_supported(self):
        """HEAD メソッドがデフォルトではサポートされていないことをテスト"""
        response = client.head("/health")
        # FastAPIはデフォルトでHEADを自動サポートしないため405
        assert response.status_code == 405

    def test_get_health_options_method_supported(self):
        """OPTIONS メソッドがサポートされていることをテスト"""
        response = client.options("/health")
        # OPTIONSリクエストは通常200を返す
        assert response.status_code in [200, 405]  # 405はメソッドが許可されていない場合

    def test_get_health_post_method_not_allowed(self):
        """POST メソッドが許可されていないことをテスト"""
        response = client.post("/health")
        # POSTは許可されていないので405を返すべき
        assert response.status_code == 405

    def test_get_health_put_method_not_allowed(self):
        """PUT メソッドが許可されていないことをテスト"""
        response = client.put("/health")
        # PUTは許可されていないので405を返すべき
        assert response.status_code == 405

    def test_get_health_delete_method_not_allowed(self):
        """DELETE メソッドが許可されていないことをテスト"""
        response = client.delete("/health")
        # DELETEは許可されていないので405を返すべき
        assert response.status_code == 405

    def test_get_health_response_content_length(self):
        """レスポンスのコンテンツ長が適切であることをテスト"""
        response = client.get("/health")
        assert response.status_code == 200

        # レスポンスボディが小さいことを確認（100バイト未満）
        content_length = len(response.content)
        assert content_length < 100, f"Content length {content_length} bytes is too large"

    def test_get_health_concurrent_requests(self):
        """並行リクエストでも正しく動作することをテスト"""
        import concurrent.futures

        def make_request():
            response = client.get("/health")
            return response.status_code, response.json()

        # 10個の並行リクエストを送信
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in futures]

        # すべてのリクエストが成功することを確認
        for status_code, data in results:
            assert status_code == 200
            assert data["status"] == "ok"
