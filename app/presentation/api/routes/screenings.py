"""
スクリーニングAPIルーター

このモジュールは、スクリーニング操作のためのREST APIエンドポイントを提供します。
POST /v1/screenings エンドポイントでスクリーニングリクエストを受け付けます。
"""

from fastapi import APIRouter, Depends

from app.presentation.api.dependencies import get_screening_usecase
from app.presentation.api.schemas.screening import (
    ScreeningRequest,
    ScreeningResponse,
)
from app.usecase.screening_usecase import ScreeningUsecase

router = APIRouter(
    prefix="/v1/screenings",
    tags=["screenings"],
)


@router.post(
    "",
    response_model=ScreeningResponse,
    summary="スクリーニング実行",
    description="提供されたコンテンツに対してスクリーニング処理を非同期で実行します。",
)
async def create_screening(
    request: ScreeningRequest,
    usecase: ScreeningUsecase = Depends(get_screening_usecase),
) -> ScreeningResponse:
    """
    スクリーニング処理を非同期で実行するエンドポイント

    このエンドポイントは、リクエストボディで提供されたコンテンツに対して
    スクリーニング処理を非同期で実行し、結果を返します。

    Args:
        request: スクリーニングリクエスト（content フィールドを含む）
        usecase: ScreeningUsecase インスタンス（依存性注入）

    Returns:
        ScreeningResponse: スクリーニング結果（content フィールドを含む）

    Raises:
        422: リクエストボディのバリデーションエラー（FastAPI自動処理）
        415: 不正な Content-Type（FastAPI自動処理）

    Examples:
        リクエスト:
        ```json
        {
            "content": "この求人は素晴らしい機会です。"
        }
        ```

        レスポンス:
        ```json
        {
            "content": "この求人は素晴らしい機会です。"
        }
        ```

    Note:
        非同期実行により、外部APIやデータベースアクセスを含む
        スクリーニングロジックでも効率的に処理できます。
        現在の実装では、入力コンテンツをそのまま返す暫定的な動作です。
    """
    # ユースケースを非同期で実行してスクリーニング処理を行う
    result_content = await usecase.execute(request.content)

    # レスポンスを作成して返す
    return ScreeningResponse(content=result_content)


__all__ = ["router"]
