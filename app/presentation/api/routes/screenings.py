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
    description="提供されたコンテンツに対してスクリーニング処理を実行します。",
)
def create_screening(
    request: ScreeningRequest,
    usecase: ScreeningUsecase = Depends(get_screening_usecase),
) -> ScreeningResponse:
    """
    スクリーニング処理を実行するエンドポイント

    このエンドポイントは、リクエストボディで提供されたコンテンツに対して
    スクリーニング処理を実行し、結果を返します。

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
        現在の実装では、入力コンテンツをそのまま返す暫定的な動作です。
        将来的には実際のスクリーニングロジックが実装される予定です。
    """
    # ユースケースを実行してスクリーニング処理を行う
    result_content = usecase.execute(request.content)

    # レスポンスを作成して返す
    return ScreeningResponse(content=result_content)


__all__ = ["router"]
