"""
EchoScreeningService のユニットテスト

このモジュールは、EchoScreeningService の実装ロジックをテストします。
通常の入力シナリオとエッジケースの両方をカバーします。
"""

import pytest

from app.infrastructure.screening_service_impl import EchoScreeningService


@pytest.fixture
def service():
    """
    テスト用の EchoScreeningService インスタンスを提供

    Returns:
        EchoScreeningService: テスト対象のサービスインスタンス
    """
    return EchoScreeningService()


def test_service_instance_creation():
    """
    EchoScreeningService のインスタンス化をテスト
    """
    service = EchoScreeningService()
    assert service is not None
    assert hasattr(service, "screen")
    assert callable(service.screen)


def test_screen_method_returns_string(service):
    """
    screen メソッドが文字列を返すことをテスト
    """
    result = service.screen("test")
    assert isinstance(result, str)


@pytest.mark.parametrize(
    "input_content,expected_output",
    [
        # 通常のテキスト
        ("Hello, World!", "Hello, World!"),
        ("採用スクリーニング", "採用スクリーニング"),
        ("123456", "123456"),
        # 空文字列
        ("", ""),
        # 単一文字
        ("a", "a"),
        # 改行を含むテキスト
        ("line1\nline2\nline3", "line1\nline2\nline3"),
        # タブを含むテキスト
        ("column1\tcolumn2\tcolumn3", "column1\tcolumn2\tcolumn3"),
        # Unicode文字（絵文字）
        ("😀🎉🚀", "😀🎉🚀"),
        # 特殊文字
        ("!@#$%^&*()_+-=[]{}|;:',.<>?/~`", "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"),
        # HTMLタグを含むテキスト
        ("<div>HTML content</div>", "<div>HTML content</div>"),
        # JSONライクな文字列
        ('{"key": "value"}', '{"key": "value"}'),
        # SQLインジェクション風文字列
        ("'; DROP TABLE users; --", "'; DROP TABLE users; --"),
        # 長いテキスト（100文字）
        ("a" * 100, "a" * 100),
        # 長いテキスト（1000文字）
        ("b" * 1000, "b" * 1000),
        # 日本語の長文
        ("こんにちは" * 50, "こんにちは" * 50),
        # 複数言語混在
        ("Hello こんにちは 你好 مرحبا", "Hello こんにちは 你好 مرحبا"),
        # 連続する空白
        ("   multiple   spaces   ", "   multiple   spaces   "),
        # ゼロ幅文字
        ("zero\u200bwidth\u200bspace", "zero\u200bwidth\u200bspace"),
    ],
)
def test_screen_echoes_input_exactly(service, input_content, expected_output):
    """
    screen メソッドが入力をそのまま返すことをテスト

    Args:
        service: テスト対象のサービスインスタンス
        input_content: 入力文字列
        expected_output: 期待される出力文字列
    """
    result = service.screen(input_content)
    assert result == expected_output
    assert result is not None
    assert type(result) == type(expected_output)


def test_screen_preserves_string_identity(service):
    """
    screen メソッドが文字列の同一性を保持することをテスト
    """
    input_text = "identity test"
    result = service.screen(input_text)
    # 内容が同じであることを確認
    assert result == input_text
    # 型が同じであることを確認
    assert type(result) == str


def test_screen_does_not_modify_input(service):
    """
    screen メソッドが入力を変更しないことをテスト
    """
    input_text = "immutable test"
    original = input_text
    result = service.screen(input_text)
    # 入力が変更されていないことを確認
    assert input_text == original
    assert result == original


def test_screen_with_very_long_text(service):
    """
    screen メソッドが非常に長いテキストを処理できることをテスト
    """
    # 10,000文字のテキスト
    long_text = "x" * 10000
    result = service.screen(long_text)
    assert result == long_text
    assert len(result) == 10000


def test_screen_with_multiline_text(service):
    """
    screen メソッドが複数行テキストを正しく処理することをテスト
    """
    multiline_text = """First line
Second line
Third line
    Indented line
Last line"""
    result = service.screen(multiline_text)
    assert result == multiline_text
    assert result.count("\n") == 4


def test_screen_multiple_calls_same_result(service):
    """
    screen メソッドが同じ入力に対して常に同じ結果を返すことをテスト（冪等性）
    """
    input_text = "consistency test"
    result1 = service.screen(input_text)
    result2 = service.screen(input_text)
    result3 = service.screen(input_text)

    assert result1 == result2 == result3 == input_text


def test_screen_different_instances_same_behavior():
    """
    異なる EchoScreeningService インスタンスが同じ動作をすることをテスト
    """
    service1 = EchoScreeningService()
    service2 = EchoScreeningService()

    input_text = "instance test"
    result1 = service1.screen(input_text)
    result2 = service2.screen(input_text)

    assert result1 == result2 == input_text
