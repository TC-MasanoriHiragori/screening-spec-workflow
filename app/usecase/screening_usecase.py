"""
スクリーニングユースケース

このモジュールは、スクリーニング操作のビジネスロジックをオーケストレートします。
依存性注入を使用してDomain層のインターフェースに依存し、外側の層への依存を排除します。
"""

from app.domain.screening_service import ScreeningService


class ScreeningUsecase:
    """
    スクリーニングユースケース

    スクリーニング操作のビジネスロジックをオーケストレートします。
    ScreeningService Protocol に依存し、具体的な実装には依存しません。

    Attributes:
        _service: スクリーニングサービスのインスタンス（Protocol型）

    Examples:
        >>> from app.infrastructure.screening_service_impl import EchoScreeningService
        >>> service = EchoScreeningService()
        >>> usecase = ScreeningUsecase(service)
        >>> result = usecase.execute("テストコンテンツ")
        >>> print(result)
        テストコンテンツ

    Note:
        このクラスはオニオンアーキテクチャのApplication層に位置し、
        Domain層のみに依存します。Infrastructure層やPresentation層への
        依存は持ちません。
    """

    def __init__(self, service: ScreeningService) -> None:
        """
        ScreeningUsecaseを初期化します

        Args:
            service: ScreeningService Protocol に準拠するサービスインスタンス

        Note:
            依存性注入を使用して、ScreeningServiceの実装を外部から注入します。
            これにより、テスト時にモックを使用でき、実装の交換も容易になります。
        """
        self._service = service

    def execute(self, content: str) -> str:
        """
        スクリーニング処理を実行します

        Args:
            content: スクリーニング対象のテキスト

        Returns:
            スクリーニング結果のテキスト

        Examples:
            >>> usecase.execute("入力テキスト")
            'スクリーニング結果'

        Note:
            このメソッドは、ScreeningServiceのscreen()メソッドを
            呼び出してスクリーニング処理を実行します。
            現在の実装では追加のビジネスロジックはありませんが、
            将来的にロギング、バリデーション、前処理・後処理などを
            追加する拡張ポイントとなります。
        """
        return self._service.screen(content)


__all__ = ["ScreeningUsecase"]
