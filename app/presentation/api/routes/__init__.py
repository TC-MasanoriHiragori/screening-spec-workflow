"""
API ルーターパッケージ

このパッケージは、FastAPI のルーターを含みます。
"""

from app.presentation.api.routes.health import router as health_router
from app.presentation.api.routes.screenings import router as screenings_router

__all__ = ["screenings_router", "health_router"]
