from fastapi import FastAPI

from application.api.api import api_router
from application.configure.load_config import settings


def set_cors_middleware():
    pass


def init() -> FastAPI:
    app = FastAPI(
        title=settings.app_name
    )
    app.include_router(api_router, prefix=f"/api/v{settings.api_version}")
    return app
