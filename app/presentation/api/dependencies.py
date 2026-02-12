"""
FastAPI 依存性注入設定

このモジュールは、FastAPIの依存性注入パターンを使用して、
アプリケーション層とインフラストラクチャ層のインスタンスを提供します。
"""

from fastapi import Depends

from app.domain.screening_service import ScreeningService
from app.infrastructure.screening_service_impl import EchoScreeningService
from app.usecase.screening_usecase import ScreeningUsecase


def get_screening_service() -> ScreeningService:
    """
    ScreeningService の実装を提供する依存性注入ファクトリ

    FastAPI の Depends で使用され、EchoScreeningService の
    インスタンスを返します。Protocol 型を返すことで、
    具体的な実装に依存しないインターフェースを提供します。

    Returns:
        ScreeningService: ScreeningService Protocol に準拠する実装

    Examples:
        >>> from fastapi import Depends
        >>> def my_endpoint(service: ScreeningService = Depends(get_screening_service)):
        ...     result = service.screen("test")
        ...     return {"result": result}

    Note:
        現在の実装では EchoScreeningService を返しますが、
        将来的には設定ファイルや環境変数に基づいて
        異なる実装を返すように拡張できます。
    """
    return EchoScreeningService()


def get_screening_usecase(
    service: ScreeningService = Depends(get_screening_service),
) -> ScreeningUsecase:
    """
    ScreeningUsecase のインスタンスを提供する依存性注入ファクトリ

    FastAPI の Depends で使用され、ScreeningService を注入した
    ScreeningUsecase のインスタンスを返します。

    Args:
        service: ScreeningService の実装（Depends で自動注入）

    Returns:
        ScreeningUsecase: ScreeningUsecase のインスタンス

    Examples:
        >>> from fastapi import Depends
        >>> def my_endpoint(usecase: ScreeningUsecase = Depends(get_screening_usecase)):
        ...     result = usecase.execute("test content")
        ...     return {"result": result}

    Note:
        この関数は get_screening_service に依存しており、
        FastAPI が自動的に依存関係を解決してサービスを注入します。
        これにより、層間の疎結合が実現されます。
    """
    return ScreeningUsecase(service)


__all__ = ["get_screening_service", "get_screening_usecase"]
