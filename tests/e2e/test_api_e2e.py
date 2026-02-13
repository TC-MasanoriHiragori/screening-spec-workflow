"""
スクリーニングAPIのEnd-to-Endテスト

このモジュールは、スクリーニングAPIの主要なユーザーシナリオを
エンドツーエンドでテストします。実際のユーザーワークフローを再現します。
"""

from fastapi.testclient import TestClient

from app.presentation.main import app

# TestClient インスタンスを作成
client = TestClient(app)


class TestAPIEndToEnd:
    """APIのE2Eテストクラス"""

    def test_complete_screening_workflow(self):
        """
        完全なスクリーニングワークフローをテスト

        シナリオ:
        1. ヘルスチェックでAPIが稼働していることを確認
        2. スクリーニングリクエストを送信
        3. 正常なレスポンスを受け取る
        """
        # Step 1: ヘルスチェック
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "ok"

        # Step 2: スクリーニングリクエストを送信
        screening_request = {
            "content": "この求人は素晴らしい機会です。給与は競争力があり、福利厚生も充実しています。"
        }
        screening_response = client.post("/v1/screenings", json=screening_request)

        # Step 3: レスポンスを検証
        assert screening_response.status_code == 200
        result = screening_response.json()
        assert "content" in result
        assert result["content"] == screening_request["content"]

    def test_multiple_screenings_in_sequence(self):
        """
        複数のスクリーニングを順番に実行するワークフローをテスト

        シナリオ:
        1. 複数の異なるコンテンツをスクリーニング
        2. 各リクエストが独立して正しく処理されることを確認
        """
        contents = [
            "一つ目の求人情報です。",
            "二つ目の求人情報です。",
            "三つ目の求人情報です。",
        ]

        for content in contents:
            response = client.post("/v1/screenings", json={"content": content})
            assert response.status_code == 200
            result = response.json()
            assert result["content"] == content

    def test_health_check_screening_health_workflow(self):
        """
        ヘルスチェック → スクリーニング → ヘルスチェックのワークフローをテスト

        シナリオ:
        1. 初期ヘルスチェック
        2. スクリーニング実行
        3. 最終ヘルスチェック（APIが安定していることを確認）
        """
        # 初期ヘルスチェック
        health1 = client.get("/health")
        assert health1.status_code == 200
        assert health1.json()["status"] == "ok"

        # スクリーニング実行
        screening_response = client.post(
            "/v1/screenings",
            json={"content": "テストコンテンツ"},
        )
        assert screening_response.status_code == 200

        # 最終ヘルスチェック
        health2 = client.get("/health")
        assert health2.status_code == 200
        assert health2.json()["status"] == "ok"

    def test_error_recovery_workflow(self):
        """
        エラーからの回復ワークフローをテスト

        シナリオ:
        1. 無効なリクエストを送信（エラー）
        2. 有効なリクエストを送信（成功）
        3. APIが正常に回復することを確認
        """
        # 無効なリクエスト（contentフィールドなし）
        invalid_response = client.post("/v1/screenings", json={})
        assert invalid_response.status_code == 422

        # 有効なリクエスト（APIは正常に動作する）
        valid_response = client.post(
            "/v1/screenings",
            json={"content": "有効なコンテンツ"},
        )
        assert valid_response.status_code == 200
        assert valid_response.json()["content"] == "有効なコンテンツ"

    def test_long_content_screening_workflow(self):
        """
        長いコンテンツのスクリーニングワークフローをテスト

        シナリオ:
        1. 長い求人情報をスクリーニング
        2. 正常に処理されることを確認
        """
        long_content = "求人情報。" * 500  # 約5000文字

        response = client.post("/v1/screenings", json={"content": long_content})
        assert response.status_code == 200
        result = response.json()
        assert result["content"] == long_content

    def test_empty_content_screening_workflow(self):
        """
        空のコンテンツのスクリーニングワークフローをテスト

        シナリオ:
        1. 空文字列をスクリーニング
        2. 正常に処理されることを確認
        """
        response = client.post("/v1/screenings", json={"content": ""})
        assert response.status_code == 200
        result = response.json()
        assert result["content"] == ""

    def test_special_characters_screening_workflow(self):
        """
        特殊文字を含むコンテンツのスクリーニングワークフローをテスト

        シナリオ:
        1. 特殊文字、改行、絵文字を含むコンテンツをスクリーニング
        2. 正常に処理されることを確認
        """
        special_content = """
        求人情報 🎉
        - 年収: 500-800万円 💰
        - 勤務地: 東京都渋谷区
        - 福利厚生: 充実 ✨

        特殊文字テスト: !@#$%^&*()_+-=[]{}|;:',.<>?/~`
        """

        response = client.post("/v1/screenings", json={"content": special_content})
        assert response.status_code == 200
        result = response.json()
        assert result["content"] == special_content

    def test_api_endpoints_independence(self):
        """
        エンドポイントの独立性をテスト

        シナリオ:
        1. ヘルスチェックとスクリーニングを交互に実行
        2. エンドポイントが互いに影響しないことを確認
        """
        # ヘルスチェック
        health1 = client.get("/health")
        assert health1.status_code == 200

        # スクリーニング
        screening1 = client.post("/v1/screenings", json={"content": "テスト1"})
        assert screening1.status_code == 200

        # ヘルスチェック
        health2 = client.get("/health")
        assert health2.status_code == 200

        # スクリーニング
        screening2 = client.post("/v1/screenings", json={"content": "テスト2"})
        assert screening2.status_code == 200

        # すべてのレスポンスが独立していることを確認
        assert health1.json() == health2.json()
        assert screening1.json()["content"] == "テスト1"
        assert screening2.json()["content"] == "テスト2"

    def test_concurrent_user_scenario(self):
        """
        複数ユーザーの同時利用シナリオをテスト

        シナリオ:
        1. 複数のユーザーが同時にスクリーニングを実行
        2. 各リクエストが正しく処理されることを確認
        """
        import concurrent.futures

        def user_workflow(user_id: int):
            # ヘルスチェック
            health = client.get("/health")
            assert health.status_code == 200

            # スクリーニング
            content = f"ユーザー{user_id}の求人情報です。"
            screening = client.post("/v1/screenings", json={"content": content})
            assert screening.status_code == 200
            assert screening.json()["content"] == content

            return True

        # 5人のユーザーが同時にアクセス
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(user_workflow, i) for i in range(5)]
            results = [future.result() for future in futures]

        # すべてのユーザーのワークフローが成功
        assert all(results)

    def test_error_handling_across_requests(self):
        """
        複数リクエスト間でのエラーハンドリングをテスト

        シナリオ:
        1. 成功 → エラー → 成功のパターンでリクエスト
        2. エラーが後続のリクエストに影響しないことを確認
        """
        # 成功
        response1 = client.post("/v1/screenings", json={"content": "成功1"})
        assert response1.status_code == 200

        # エラー
        response2 = client.post("/v1/screenings", json={})
        assert response2.status_code == 422

        # 成功（エラーの影響を受けない）
        response3 = client.post("/v1/screenings", json={"content": "成功2"})
        assert response3.status_code == 200
        assert response3.json()["content"] == "成功2"

    def test_openapi_documentation_available(self):
        """
        OpenAPIドキュメントが利用可能であることをテスト

        シナリオ:
        1. /openapi.json にアクセス
        2. 有効なOpenAPI仕様が返されることを確認
        """
        response = client.get("/openapi.json")
        assert response.status_code == 200

        openapi_spec = response.json()
        assert "openapi" in openapi_spec
        assert "info" in openapi_spec
        assert "paths" in openapi_spec

        # エンドポイントが定義されていることを確認
        assert "/v1/screenings" in openapi_spec["paths"]
        assert "/health" in openapi_spec["paths"]

    def test_api_metadata(self):
        """
        APIメタデータが正しく設定されていることをテスト

        シナリオ:
        1. OpenAPI仕様を取得
        2. タイトル、バージョン、説明が正しいことを確認
        """
        response = client.get("/openapi.json")
        assert response.status_code == 200

        openapi_spec = response.json()
        info = openapi_spec["info"]

        assert info["title"] == "Screening API"
        assert info["version"] == "1.0.0"
        assert "description" in info
