"""
ヘルスチェックAPIルーター

このモジュールは、サービスのヘルスステータスを確認するための
シンプルなヘルスチェックエンドポイントを提供します。
"""

from fastapi import APIRouter

from app.presentation.api.schemas.screening import HealthResponse

router = APIRouter(
    tags=["health"],
)


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="ヘルスチェック",
    description="APIサービスのヘルスステータスを確認します。",
)
def get_health() -> HealthResponse:
    """
    ヘルスチェックエンドポイント

    このエンドポイントは、APIサービスが正常に動作していることを確認するための
    シンプルなヘルスチェックを提供します。認証不要で、非常に高速に応答します。

    Returns:
        HealthResponse: ヘルスステータス（status: "ok"）

    Examples:
        レスポンス:
        ```json
        {
            "status": "ok"
        }
        ```

    Note:
        - このエンドポイントは認証を必要としません
        - 応答時間は 100ms 未満を目標としています
        - ロードバランサーやモニタリングシステムからの定期的な呼び出しを想定
        - 現在の実装では常に "ok" を返しますが、将来的には
          データベース接続や外部サービスの状態チェックを追加できます
    """
    return HealthResponse()


__all__ = ["router"]
