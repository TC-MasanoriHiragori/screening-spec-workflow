"""
Pydantic スキーマのユニットテスト

このモジュールは、Presentation層のPydanticスキーマのバリデーションをテストします。
バリデーション成功と失敗のシナリオを両方カバーします。
"""

import pytest
from pydantic import ValidationError

from app.presentation.api.schemas.screening import (
    HealthResponse,
    ScreeningRequest,
    ScreeningResponse,
)


class TestScreeningRequest:
    """ScreeningRequest スキーマのテストクラス"""

    def test_valid_request_creation(self):
        """有効なリクエストが作成できることをテスト"""
        request = ScreeningRequest(content="テストコンテンツ")
        assert request.content == "テストコンテンツ"

    def test_request_with_empty_string(self):
        """空文字列でリクエストが作成できることをテスト"""
        request = ScreeningRequest(content="")
        assert request.content == ""

    @pytest.mark.parametrize(
        "content",
        [
            "通常のテキスト",
            "日本語テキスト",
            "English text",
            "Mixed 混在 text",
            "123456",
            "!@#$%^&*()",
            "改行\nを含む\nテキスト",
            "タブ\tを含む\tテキスト",
            "😀 絵文字を含むテキスト",
            "a" * 1000,  # 長いテキスト
        ],
    )
    def test_request_with_various_content(self, content):
        """様々なコンテンツでリクエストが作成できることをテスト"""
        request = ScreeningRequest(content=content)
        assert request.content == content

    def test_request_missing_content_field(self):
        """content フィールド欠落時にバリデーションエラーが発生することをテスト"""
        with pytest.raises(ValidationError) as exc_info:
            ScreeningRequest()  # type: ignore

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("content",)
        assert errors[0]["type"] == "missing"

    def test_request_with_non_string_content(self):
        """content が文字列でない場合にバリデーションエラーが発生することをテスト"""
        with pytest.raises(ValidationError) as exc_info:
            ScreeningRequest(content=123)  # type: ignore

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("content",)
        assert errors[0]["type"] == "string_type"

    def test_request_json_serialization(self):
        """リクエストがJSONにシリアライズできることをテスト"""
        request = ScreeningRequest(content="テスト")
        json_data = request.model_dump_json()
        assert isinstance(json_data, str)
        assert "テスト" in json_data

    def test_request_json_deserialization(self):
        """JSONからリクエストがデシリアライズできることをテスト"""
        json_data = '{"content": "デシリアライズテスト"}'
        request = ScreeningRequest.model_validate_json(json_data)
        assert request.content == "デシリアライズテスト"

    def test_request_dict_conversion(self):
        """リクエストが辞書に変換できることをテスト"""
        request = ScreeningRequest(content="辞書変換")
        data = request.model_dump()
        assert data == {"content": "辞書変換"}


class TestScreeningResponse:
    """ScreeningResponse スキーマのテストクラス"""

    def test_valid_response_creation(self):
        """有効なレスポンスが作成できることをテスト"""
        response = ScreeningResponse(content="結果コンテンツ")
        assert response.content == "結果コンテンツ"

    def test_response_with_empty_string(self):
        """空文字列でレスポンスが作成できることをテスト"""
        response = ScreeningResponse(content="")
        assert response.content == ""

    @pytest.mark.parametrize(
        "content",
        [
            "通常の結果",
            "日本語結果",
            "English result",
            "Mixed 混在 result",
            "123456",
            "!@#$%^&*()",
            "改行\nを含む\n結果",
            "😀 絵文字を含む結果",
            "b" * 1000,  # 長いテキスト
        ],
    )
    def test_response_with_various_content(self, content):
        """様々なコンテンツでレスポンスが作成できることをテスト"""
        response = ScreeningResponse(content=content)
        assert response.content == content

    def test_response_missing_content_field(self):
        """content フィールド欠落時にバリデーションエラーが発生することをテスト"""
        with pytest.raises(ValidationError) as exc_info:
            ScreeningResponse()  # type: ignore

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("content",)
        assert errors[0]["type"] == "missing"

    def test_response_with_non_string_content(self):
        """content が文字列でない場合にバリデーションエラーが発生することをテスト"""
        with pytest.raises(ValidationError) as exc_info:
            ScreeningResponse(content=456)  # type: ignore

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("content",)
        assert errors[0]["type"] == "string_type"

    def test_response_json_serialization(self):
        """レスポンスがJSONにシリアライズできることをテスト"""
        response = ScreeningResponse(content="結果")
        json_data = response.model_dump_json()
        assert isinstance(json_data, str)
        assert "結果" in json_data

    def test_response_json_deserialization(self):
        """JSONからレスポンスがデシリアライズできることをテスト"""
        json_data = '{"content": "デシリアライズ結果"}'
        response = ScreeningResponse.model_validate_json(json_data)
        assert response.content == "デシリアライズ結果"

    def test_response_dict_conversion(self):
        """レスポンスが辞書に変換できることをテスト"""
        response = ScreeningResponse(content="辞書変換結果")
        data = response.model_dump()
        assert data == {"content": "辞書変換結果"}


class TestHealthResponse:
    """HealthResponse スキーマのテストクラス"""

    def test_valid_response_with_default_status(self):
        """デフォルトのstatusでレスポンスが作成できることをテスト"""
        response = HealthResponse()
        assert response.status == "ok"

    def test_valid_response_with_custom_status(self):
        """カスタムstatusでレスポンスが作成できることをテスト"""
        response = HealthResponse(status="healthy")
        assert response.status == "healthy"

    @pytest.mark.parametrize(
        "status",
        [
            "ok",
            "healthy",
            "running",
            "active",
            "ready",
            "available",
            "operational",
        ],
    )
    def test_response_with_various_status(self, status):
        """様々なstatusでレスポンスが作成できることをテスト"""
        response = HealthResponse(status=status)
        assert response.status == status

    def test_response_with_non_string_status(self):
        """status が文字列でない場合にバリデーションエラーが発生することをテスト"""
        with pytest.raises(ValidationError) as exc_info:
            HealthResponse(status=123)  # type: ignore

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("status",)
        assert errors[0]["type"] == "string_type"

    def test_response_json_serialization_with_default(self):
        """デフォルトstatusのレスポンスがJSONにシリアライズできることをテスト"""
        response = HealthResponse()
        json_data = response.model_dump_json()
        assert isinstance(json_data, str)
        assert "ok" in json_data

    def test_response_json_serialization_with_custom(self):
        """カスタムstatusのレスポンスがJSONにシリアライズできることをテスト"""
        response = HealthResponse(status="custom")
        json_data = response.model_dump_json()
        assert isinstance(json_data, str)
        assert "custom" in json_data

    def test_response_json_deserialization(self):
        """JSONからレスポンスがデシリアライズできることをテスト"""
        json_data = '{"status": "healthy"}'
        response = HealthResponse.model_validate_json(json_data)
        assert response.status == "healthy"

    def test_response_json_deserialization_missing_status(self):
        """status 欠落時にデフォルト値でデシリアライズできることをテスト"""
        json_data = "{}"
        response = HealthResponse.model_validate_json(json_data)
        assert response.status == "ok"

    def test_response_dict_conversion_with_default(self):
        """デフォルトstatusのレスポンスが辞書に変換できることをテスト"""
        response = HealthResponse()
        data = response.model_dump()
        assert data == {"status": "ok"}

    def test_response_dict_conversion_with_custom(self):
        """カスタムstatusのレスポンスが辞書に変換できることをテスト"""
        response = HealthResponse(status="ready")
        data = response.model_dump()
        assert data == {"status": "ready"}


class TestSchemaIntegration:
    """スキーマ統合テストクラス"""

    def test_request_response_flow(self):
        """リクエスト→レスポンスのフローをテスト"""
        # リクエスト作成
        request = ScreeningRequest(content="統合テスト")

        # リクエストをJSONに変換
        request_json = request.model_dump_json()

        # JSONからリクエストを復元
        restored_request = ScreeningRequest.model_validate_json(request_json)

        # レスポンス作成（同じコンテンツ）
        response = ScreeningResponse(content=restored_request.content)

        # レスポンスの内容を確認
        assert response.content == "統合テスト"

    def test_all_schemas_json_compatibility(self):
        """すべてのスキーマがJSON互換であることをテスト"""
        # ScreeningRequest
        req = ScreeningRequest(content="test")
        req_json = req.model_dump_json()
        req_restored = ScreeningRequest.model_validate_json(req_json)
        assert req.content == req_restored.content

        # ScreeningResponse
        res = ScreeningResponse(content="result")
        res_json = res.model_dump_json()
        res_restored = ScreeningResponse.model_validate_json(res_json)
        assert res.content == res_restored.content

        # HealthResponse
        health = HealthResponse(status="ok")
        health_json = health.model_dump_json()
        health_restored = HealthResponse.model_validate_json(health_json)
        assert health.status == health_restored.status
