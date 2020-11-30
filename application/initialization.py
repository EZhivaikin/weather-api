import os

from fastapi import FastAPI
from omegaconf import DictConfig
from starlette.middleware.cors import CORSMiddleware

from application.web.api import api_router
from application.configure.load_config import settings, _load_application_configuration
from config.settings import ApiClient, Settings


def _configure_cors_middleware():
    pass


def _load_weather_client_config(config) -> ApiClient:
    return ApiClient(
        host=config.clients.openweather.host,
        api_key=config.clients.openweather.api_key,
        secret_key=config.clients.openweather.secret_key,
        prefix=config.clients.openweather.prefix
    )


def _load_geocoder_client_config(config) -> ApiClient:
    return ApiClient(
        host=config.clients.geocoder.host,
        api_key=config.clients.geocoder.api_key,
        secret_key=config.clients.geocoder.secret_key,
        prefix=config.clients.geocoder.prefix
    )


def load_settings(config: DictConfig) -> Settings:
    weather_api = _load_weather_client_config(config)
    geocoder_api = _load_geocoder_client_config(config)
    return Settings(
        app_name=config.project.name,
        api_version=config.project.api_version,
        weather_api=weather_api,
        geocoder_api=geocoder_api,
    )


def init() -> FastAPI:
    config_profile = os.getenv("CONFIG_PROFILE")
    config = _load_application_configuration(config_profile)
    settings = load_settings(config)
    app = FastAPI(
        title=settings.app_name
    )
    app.include_router(api_router, prefix=f"/api/v{settings.api_version}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
