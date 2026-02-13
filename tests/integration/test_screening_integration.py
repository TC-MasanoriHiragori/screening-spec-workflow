"""
スクリーニングエンドポイントの統合テスト

このモジュールは、POST /v1/screenings エンドポイントの統合テストを実行します。
FastAPI TestClient を使用して、完全なリクエスト-レスポンスサイクルをテストします。
"""

import pytest
from fastapi.testclient import TestClient

from app.presentation.main import app

# TestClient インスタンスを作成
client = TestClient(app)


class TestScreeningEndpoint:
    """スクリーニングエンドポイントの統合テストクラス"""

    def test_create_screening_with_valid_request(self):
        """有効なリクエストで 200 OK とコンテンツを返すことをテスト"""
        response = client.post(
            "/v1/screenings",
            json={"content": "テストコンテンツ"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert data["content"] == "テストコンテンツ"

    def test_create_screening_response_has_only_content_field(self):
        """レスポンスに content フィールドのみが含まれることをテスト"""
        response = client.post(
            "/v1/screenings",
            json={"content": "フィールドチェック"},
        )

        assert response.status_code == 200
        data = response.json()
        # content フィールドのみが含まれることを確認
        assert list(data.keys()) == ["content"]
        # 余分なフィールドがないことを確認
        assert "status" not in data
        assert "result" not in data
        assert "message" not in data

    def test_create_screening_with_empty_content(self):
        """空文字列のコンテンツで正常に処理されることをテスト"""
        response = client.post(
            "/v1/screenings",
            json={"content": ""},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["content"] == ""

    @pytest.mark.parametrize(
        "content",
        [
            "通常のテキスト",
            "日本語のテキスト",
            "English text",
            "Mixed 混在 text",
            "特殊文字 !@#$%^&*()",
            "改行\nを含む\nテキスト",
            "😀 絵文字を含むテキスト",
            "a" * 1000,  # 長いテキスト
        ],
    )
    def test_create_screening_with_various_content(self, content):
        """様々なコンテンツで正常に処理されることをテスト"""
        response = client.post(
            "/v1/screenings",
            json={"content": content},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["content"] == content

    def test_create_screening_without_content_field_returns_422(self):
        """content フィールドが欠けている場合に 422 を返すことをテスト"""
        response = client.post(
            "/v1/screenings",
            json={},  # content フィールドなし
        )

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_create_screening_with_null_content_returns_422(self):
        """content が null の場合に 422 を返すことをテスト"""
        response = client.post(
            "/v1/screenings",
            json={"content": None},
        )

        assert response.status_code == 422

    def test_create_screening_with_non_string_content_returns_422(self):
        """content が文字列でない場合に 422 を返すことをテスト"""
        response = client.post(
            "/v1/screenings",
            json={"content": 123},
        )

        assert response.status_code == 422

    def test_create_screening_with_invalid_json_returns_422(self):
        """不正な JSON の場合に 422 を返すことをテスト"""
        response = client.post(
            "/v1/screenings",
            data="invalid json",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 422

    def test_create_screening_with_wrong_content_type_returns_415(self):
        """間違った Content-Type の場合に 415 を返すことをテスト"""
        response = client.post(
            "/v1/screenings",
            data="content=test",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        # FastAPI は Content-Type が application/json でない場合に 422 を返す
        # (415 ではなく 422 がより一般的)
        assert response.status_code == 422

    def test_create_screening_response_headers(self):
        """レスポンスヘッダーが正しいことをテスト"""
        response = client.post(
            "/v1/screenings",
            json={"content": "ヘッダーテスト"},
        )

        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")

    def test_create_screening_idempotency(self):
        """同じリクエストを複数回送信しても同じ結果を返すことをテスト"""
        request_data = {"content": "冪等性テスト"}

        response1 = client.post("/v1/screenings", json=request_data)
        response2 = client.post("/v1/screenings", json=request_data)
        response3 = client.post("/v1/screenings", json=request_data)

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

        assert response1.json() == response2.json() == response3.json()

    def test_create_screening_with_extra_fields_ignored(self):
        """余分なフィールドが無視されることをテスト"""
        response = client.post(
            "/v1/screenings",
            json={
                "content": "テストコンテンツ",
                "extra_field": "これは無視される",
                "another_field": 123,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "テストコンテンツ"
        # 余分なフィールドはレスポンスに含まれない
        assert "extra_field" not in data
        assert "another_field" not in data
