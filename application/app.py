from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from application.web.api import api_router
from config.application_config import Settings


def configure_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.app_name
    )
    app.include_router(api_router, prefix=f"/api/v{settings.api_version}")
    configure_cors_middleware(app)
    return app
