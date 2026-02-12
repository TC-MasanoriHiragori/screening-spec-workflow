"""
ScreeningService Protocol のユニットテスト

このモジュールは、ScreeningService Protocol が正しく定義されており、
実装クラスがそのインターフェースに準拠できることをテストします。
"""

from app.domain.screening_service import ScreeningService


class MockScreeningService:
    """
    ScreeningService Protocol に準拠するモック実装

    このクラスは Protocol から明示的に継承せず、
    構造的部分型付けにより暗黙的に準拠することをテストします。
    """

    def screen(self, content: str) -> str:
        """
        モックスクリーニング実装

        Args:
            content: 入力テキスト

        Returns:
            固定の文字列 "mocked"
        """
        return "mocked"


def test_protocol_has_screen_method():
    """
    ScreeningService Protocol が screen メソッドを定義していることを確認
    """
    # Protocol のメソッドシグネチャが存在することを確認
    assert hasattr(ScreeningService, "screen")


def test_mock_implementation_conforms_to_protocol():
    """
    モック実装が ScreeningService Protocol に準拠することを確認
    """
    # モック実装のインスタンスを作成
    mock_service = MockScreeningService()

    # screen メソッドが存在することを確認
    assert hasattr(mock_service, "screen")
    assert callable(mock_service.screen)


def test_mock_implementation_screen_method_signature():
    """
    モック実装の screen メソッドが正しいシグネチャを持つことを確認
    """
    mock_service = MockScreeningService()

    # screen メソッドが文字列を受け取り、文字列を返すことを確認
    result = mock_service.screen("test input")
    assert isinstance(result, str)


def test_mock_implementation_can_be_used_as_protocol():
    """
    モック実装が Protocol 型として使用できることを確認

    型チェッカー（mypy等）がこのコードを許可することを期待します。
    """

    def process_with_service(service: ScreeningService, content: str) -> str:
        """
        ScreeningService Protocol を受け取る関数

        Args:
            service: ScreeningService Protocol に準拠する実装
            content: スクリーニング対象のコンテンツ

        Returns:
            スクリーニング結果
        """
        return service.screen(content)

    # モック実装を Protocol 型として渡す
    mock_service = MockScreeningService()
    result = process_with_service(mock_service, "test content")

    # 結果が文字列であることを確認
    assert isinstance(result, str)
    assert result == "mocked"


def test_protocol_conformance_with_different_implementation():
    """
    異なる実装でも Protocol に準拠できることを確認
    """

    class AnotherMockService:
        """別のモック実装"""

        def screen(self, content: str) -> str:
            return f"processed: {content}"

    # 別の実装も Protocol に準拠する
    another_service = AnotherMockService()
    result = another_service.screen("input")

    assert isinstance(result, str)
    assert result == "processed: input"
