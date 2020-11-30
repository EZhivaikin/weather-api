import os

from fastapi import FastAPI
from omegaconf import DictConfig
from starlette.middleware.cors import CORSMiddleware

from application.adapter.geocoder.client import GeocoderClient
from application.adapter.weather.client import WeatherClient
from application.web.api import api_router
from application.configure.load_config import load_application_configuration
from config.settings import ApiClient, Settings


def _configure_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _load_weather_client_config(app_config) -> ApiClient:
    return ApiClient(
        host=app_config.clients.openweather.host,
        api_key=app_config.clients.openweather.api_key,
        secret_key=app_config.clients.openweather.secret_key,
        prefix=app_config.clients.openweather.prefix
    )


def _load_geocoder_client_config(app_config) -> ApiClient:
    return ApiClient(
        host=config.clients.geocoder.host,
        api_key=config.clients.geocoder.api_key,
        secret_key=config.clients.geocoder.secret_key,
        prefix=config.clients.geocoder.prefix
    )


def load_geocoder_client(geocoder_settings):
    return GeocoderClient(
        host=geocoder_settings.host,
        api_key=geocoder_settings.api_key,
        secret_key=geocoder_settings.secret_key,
        prefix=geocoder_settings.prefix
    )


def load_weather_client(weather_settings):
    return WeatherClient(
        host=weather_settings.host,
        api_key=weather_settings.api_key,
        secret_key=weather_settings.secret_key,
        prefix=weather_settings.prefix
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


_config_profile = os.getenv("CONFIG_PROFILE")
config = load_application_configuration(_config_profile)
settings = load_settings(config)
geocoder_client = load_geocoder_client(settings.geocoder_api)
weather_client = load_weather_client(settings.weather_api)


def init() -> FastAPI:
    app = FastAPI(
        title=settings.app_name
    )
    app.include_router(api_router, prefix=f"/api/v{settings.api_version}")
    _configure_cors_middleware(app)
    return app
