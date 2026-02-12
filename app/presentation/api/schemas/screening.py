"""
スクリーニングAPIのPydanticスキーマ

このモジュールは、スクリーニングAPIのリクエスト/レスポンススキーマを定義します。
Pydantic BaseModelを使用して、データバリデーションとOpenAPIドキュメント生成を行います。
"""

from pydantic import BaseModel, Field


class ScreeningRequest(BaseModel):
    """
    スクリーニングリクエストスキーマ

    POST /v1/screenings エンドポイントへのリクエストボディを表します。

    Attributes:
        content: スクリーニング対象のテキストコンテンツ

    Examples:
        >>> request = ScreeningRequest(content="採用情報テキスト")
        >>> request.content
        '採用情報テキスト'
    """

    content: str = Field(
        ...,
        description="スクリーニング対象のテキストコンテンツ",
        min_length=0,
        examples=["この求人は素晴らしい機会です。"],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [{"content": "この求人は素晴らしい機会です。"}]
        }
    }


class ScreeningResponse(BaseModel):
    """
    スクリーニングレスポンススキーマ

    POST /v1/screenings エンドポイントからのレスポンスボディを表します。

    Attributes:
        content: スクリーニング結果のテキストコンテンツ

    Examples:
        >>> response = ScreeningResponse(content="スクリーニング結果")
        >>> response.content
        'スクリーニング結果'

    Note:
        現在の暫定実装では、入力コンテンツがそのまま返されます。
    """

    content: str = Field(
        ...,
        description="スクリーニング結果のテキストコンテンツ",
        examples=["この求人は素晴らしい機会です。"],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [{"content": "この求人は素晴らしい機会です。"}]
        }
    }


class HealthResponse(BaseModel):
    """
    ヘルスチェックレスポンススキーマ

    GET /health エンドポイントからのレスポンスボディを表します。

    Attributes:
        status: サービスのヘルスステータス（デフォルト: "ok"）

    Examples:
        >>> response = HealthResponse()
        >>> response.status
        'ok'
        >>> response = HealthResponse(status="healthy")
        >>> response.status
        'healthy'
    """

    status: str = Field(
        default="ok",
        description='サービスのヘルスステータス（通常は "ok"）',
        examples=["ok"],
    )

    model_config = {"json_schema_extra": {"examples": [{"status": "ok"}]}}


__all__ = ["ScreeningRequest", "ScreeningResponse", "HealthResponse"]
