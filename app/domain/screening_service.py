"""
スクリーニングサービスのインターフェース定義

このモジュールは、スクリーニング操作の契約を定義するProtocolを提供します。
フレームワークに依存しない純粋なビジネスロジックのインターフェースです。
"""

from typing import Protocol


class ScreeningService(Protocol):
    """
    スクリーニングサービスのインターフェース

    このProtocolは構造的部分型付け（Structural Subtyping）を使用して、
    スクリーニングサービスの実装が満たすべき契約を定義します。

    実装クラスは明示的にこのProtocolを継承する必要はなく、
    必要なメソッドシグネチャを持っていれば自動的に準拠します。
    """

    def screen(self, content: str) -> str:
        """
        スクリーニング処理を実行します

        Args:
            content: スクリーニング対象のテキスト

        Returns:
            スクリーニング結果のテキスト

        Note:
            このメソッドは副作用を持たず、純粋関数として実装されるべきです。
        """
        ...


__all__ = ["ScreeningService"]
