"""
Screening API - FastAPIアプリケーションエントリーポイント

このモジュールは、採用スクリーニングAPIのFastAPIアプリケーションを定義します。
オニオンアーキテクチャに基づき、スクリーニング機能とヘルスチェックを提供します。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.presentation.api.routes import health_router, screenings_router

# FastAPIアプリケーションインスタンスを作成
app = FastAPI(
    title="Screening API",
    version="1.0.0",
    description="""
採用スクリーニングAPIは、採用情報のコンテンツをスクリーニングするための
RESTful APIバックエンドサービスです。

## 主な機能

* **スクリーニング処理**: POST /v1/screenings で採用コンテンツをスクリーニング
* **ヘルスチェック**: GET /health でサービスの稼働状況を確認

## アーキテクチャ

このAPIはオニオンアーキテクチャとドメイン駆動設計（DDD）に基づいて構築されており、
以下の4層で構成されています:

- **Domain層**: ビジネスロジックのインターフェース定義
- **Application層**: ユースケースのオーケストレーション
- **Infrastructure層**: 具体的な実装（暫定的なエコー実装）
- **Presentation層**: REST APIエンドポイント
    """,
    contact={
        "name": "Screening API Team",
    },
    license_info={
        "name": "Internal Use",
    },
)

# CORS設定
# フロントエンドからのアクセスを許可するためのCORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # 開発環境のフロントエンド
        "http://localhost:5173",  # Vite開発サーバー
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        # 本番環境では適切なオリジンを設定してください
    ],
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可
)

# スクリーニングルーターを登録
app.include_router(screenings_router)

# ヘルスチェックルーターを登録
app.include_router(health_router)


# アプリケーション起動時のイベントハンドラー（オプション）
@app.on_event("startup")
async def startup_event():
    """
    アプリケーション起動時に実行されるイベントハンドラー

    将来的には、データベース接続の初期化や
    外部サービスの接続確認などを行うことができます。
    """
    pass


# アプリケーション終了時のイベントハンドラー（オプション）
@app.on_event("shutdown")
async def shutdown_event():
    """
    アプリケーション終了時に実行されるイベントハンドラー

    将来的には、データベース接続のクローズや
    リソースのクリーンアップを行うことができます。
    """
    pass
