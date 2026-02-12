"""
ScreeningUsecase のユニットテスト

このモジュールは、ScreeningUsecase のオーケストレーションロジックをテストします。
ScreeningServiceをモック化して、ユースケースの動作を実装から分離してテストします。
"""

from unittest.mock import MagicMock

import pytest

from app.usecase.screening_usecase import ScreeningUsecase


@pytest.fixture
def mock_service():
    """
    モック化された ScreeningService を提供

    Returns:
        MagicMock: ScreeningService のモックインスタンス
    """
    return MagicMock()


@pytest.fixture
def usecase(mock_service):
    """
    テスト用の ScreeningUsecase インスタンスを提供

    Args:
        mock_service: モック化された ScreeningService

    Returns:
        ScreeningUsecase: テスト対象のユースケースインスタンス
    """
    return ScreeningUsecase(mock_service)


def test_usecase_initialization_with_service(mock_service):
    """
    ScreeningUsecase がサービスを受け取って初期化できることをテスト
    """
    usecase = ScreeningUsecase(mock_service)
    assert usecase is not None
    assert hasattr(usecase, "_service")
    assert usecase._service is mock_service


def test_usecase_has_execute_method(usecase):
    """
    ScreeningUsecase が execute メソッドを持つことをテスト
    """
    assert hasattr(usecase, "execute")
    assert callable(usecase.execute)


def test_execute_calls_service_screen(mock_service, usecase):
    """
    execute() が service.screen() を呼び出すことをテスト
    """
    # モックの戻り値を設定
    mock_service.screen.return_value = "mocked result"

    # execute を呼び出す
    input_content = "test input"
    result = usecase.execute(input_content)

    # service.screen() が呼び出されたことを確認
    mock_service.screen.assert_called_once_with(input_content)
    assert result == "mocked result"


def test_execute_returns_service_result(mock_service, usecase):
    """
    execute() が service.screen() の結果を返すことをテスト
    """
    # モックの戻り値を設定
    expected_result = "screening result"
    mock_service.screen.return_value = expected_result

    # execute を呼び出す
    result = usecase.execute("any content")

    # 結果が service.screen() の戻り値と一致することを確認
    assert result == expected_result


def test_execute_passes_content_to_service(mock_service, usecase):
    """
    execute() が正しいコンテンツを service.screen() に渡すことをテスト
    """
    test_content = "specific test content"
    mock_service.screen.return_value = "result"

    usecase.execute(test_content)

    # 正しい引数で呼び出されたことを確認
    mock_service.screen.assert_called_with(test_content)


@pytest.mark.parametrize(
    "input_content,mock_return",
    [
        ("simple text", "simple text"),
        ("", ""),
        ("日本語テキスト", "日本語テキスト"),
        ("very long text" * 100, "very long text" * 100),
        ("special chars !@#$%", "special chars !@#$%"),
    ],
)
def test_execute_with_various_inputs(mock_service, input_content, mock_return):
    """
    execute() が様々な入力に対して正しく動作することをテスト

    Args:
        mock_service: モック化された ScreeningService
        input_content: テスト用の入力コンテンツ
        mock_return: モックの戻り値
    """
    mock_service.screen.return_value = mock_return
    usecase = ScreeningUsecase(mock_service)

    result = usecase.execute(input_content)

    mock_service.screen.assert_called_once_with(input_content)
    assert result == mock_return


def test_execute_called_multiple_times(mock_service, usecase):
    """
    execute() が複数回呼び出せることをテスト
    """
    mock_service.screen.side_effect = ["result1", "result2", "result3"]

    result1 = usecase.execute("content1")
    result2 = usecase.execute("content2")
    result3 = usecase.execute("content3")

    assert result1 == "result1"
    assert result2 == "result2"
    assert result3 == "result3"
    assert mock_service.screen.call_count == 3


def test_execute_with_different_service_implementations():
    """
    異なるサービス実装で ScreeningUsecase が動作することをテスト
    """
    # 最初のモック
    mock_service1 = MagicMock()
    mock_service1.screen.return_value = "result from service1"
    usecase1 = ScreeningUsecase(mock_service1)

    # 2番目のモック
    mock_service2 = MagicMock()
    mock_service2.screen.return_value = "result from service2"
    usecase2 = ScreeningUsecase(mock_service2)

    # それぞれのユースケースが独立して動作することを確認
    result1 = usecase1.execute("content")
    result2 = usecase2.execute("content")

    assert result1 == "result from service1"
    assert result2 == "result from service2"


def test_usecase_does_not_modify_input(mock_service, usecase):
    """
    ユースケースが入力を変更しないことをテスト
    """
    original_content = "original content"
    test_content = original_content
    mock_service.screen.return_value = "result"

    usecase.execute(test_content)

    # 入力が変更されていないことを確認
    assert test_content == original_content


def test_service_screen_called_with_correct_signature(mock_service):
    """
    service.screen() が正しいシグネチャで呼び出されることをテスト
    """
    usecase = ScreeningUsecase(mock_service)
    mock_service.screen.return_value = "result"

    usecase.execute("test")

    # screen() が1つの引数（文字列）で呼び出されたことを確認
    args, kwargs = mock_service.screen.call_args
    assert len(args) == 1
    assert isinstance(args[0], str)
    assert len(kwargs) == 0


def test_usecase_delegation_pattern(mock_service, usecase):
    """
    ユースケースが委譲パターンを実装していることをテスト
    """
    # モックの戻り値を設定
    mock_service.screen.return_value = "delegated result"

    # execute は単純に service.screen に委譲する
    result = usecase.execute("input")

    # 委譲が正しく行われていることを確認
    mock_service.screen.assert_called_once()
    assert result == mock_service.screen.return_value


def test_usecase_maintains_service_reference(mock_service):
    """
    ユースケースがサービスへの参照を保持することをテスト
    """
    usecase = ScreeningUsecase(mock_service)

    # 初回の呼び出し
    mock_service.screen.return_value = "result1"
    usecase.execute("content1")

    # 2回目の呼び出し（同じサービスインスタンスが使用される）
    mock_service.screen.return_value = "result2"
    usecase.execute("content2")

    # 同じモックサービスが使用されたことを確認
    assert mock_service.screen.call_count == 2
