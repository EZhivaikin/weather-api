from pydantic import BaseSettings

from application.configs import APPLICATION_CONFIGS_ROOT
from omegaconf import OmegaConf


class Settings(BaseSettings):
    app_name: str
    open_weather_api_key: str
    geo_coder_api_key: str


def _load_application_configuration(profile: str):
    config_folder = APPLICATION_CONFIGS_ROOT / "profiles" / profile
    config_params = config_folder / "params.yaml"
    return OmegaConf.load(str(config_params))


def load_settings(profile: str):
    config = _load_application_configuration(profile)
    return Settings(
        app_name=config.project.name,
        open_weather_api_key=config.clients.openweather.api_key,
        geo_coder_api_key=config.clients.geocoder.api_key,
    )


settings = load_settings("default")
