"""
API ルーターパッケージ

このパッケージは、FastAPI のルーターを含みます。
"""

from app.presentation.api.routes.screenings import router as screenings_router

__all__ = ["screenings_router"]
