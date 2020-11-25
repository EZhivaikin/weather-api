from dataclasses import dataclass
from typing import Optional

from pydantic import BaseSettings

from application.configs import APPLICATION_CONFIGS_ROOT
from omegaconf import OmegaConf

@dataclass
class ApiClient:
    host: str
    api_key: Optional[str]
    secret_key: Optional[str]
    prefix: Optional[str]


class Settings(BaseSettings):
    app_name: str
    api_version: str
    weather_api: ApiClient
    geocoder_api: ApiClient




def _load_application_configuration(profile: str):
    config_folder = APPLICATION_CONFIGS_ROOT / "profiles" / profile
    config_params = config_folder / "params.yaml"
    return OmegaConf.load(str(config_params))


def load_settings(profile: str) -> Settings:
    config = _load_application_configuration(profile)
    weather_api = ApiClient(
        host=config.clients.openweather.host,
        api_key=config.clients.openweather.api_key,
        secret_key=config.clients.openweather.secret_key,
        prefix=config.clients.openweather.prefix
    )
    geocoder_api = ApiClient(
        host=config.clients.geocoder.host,
        api_key=config.clients.geocoder.api_key,
        secret_key=config.clients.geocoder.secret_key,
        prefix=config.clients.geocoder.prefix
    )

    return Settings(
        app_name=config.project.name,
        api_version=config.project.api_version,
        weather_api=weather_api,
        geocoder_api=geocoder_api,
    )


settings = load_settings("default")
