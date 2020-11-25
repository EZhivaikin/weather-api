from typing import Optional

from pydantic import BaseSettings

from application.configs import APPLICATION_CONFIGS_ROOT
from omegaconf import OmegaConf


class Settings(BaseSettings):
    app_name: str
    api_version: str
    open_weather_api_key: Optional[str]
    geo_coder_api_key: Optional[str]


def _load_application_configuration(profile: str):
    config_folder = APPLICATION_CONFIGS_ROOT / "profiles" / profile
    config_params = config_folder / "params.yaml"
    return OmegaConf.load(str(config_params))


def load_settings(profile: str) -> Settings:
    config = _load_application_configuration(profile)
    return Settings(
        app_name=config.project.name,
        api_version=config.project.api_version,
        open_weather_api_key=config.clients.openweather.api_key,
        geo_coder_api_key=config.clients.geocoder.api_key,
    )


settings = load_settings("default")
