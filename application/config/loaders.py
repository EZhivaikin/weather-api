import os

from omegaconf import OmegaConf, DictConfig

from config.application_config import APPLICATION_CONFIGS_ROOT, ApiClient, Settings


def load_application_configuration(profile: str) -> DictConfig:
    config_folder = APPLICATION_CONFIGS_ROOT / "profiles" / profile
    config_params = config_folder / "params.yaml"
    return OmegaConf.load(str(config_params))


def _load_weather_client_config(weather_config) -> ApiClient:
    return ApiClient(
        host=weather_config.host,
        api_key=weather_config.api_key,
        secret_key=weather_config.secret_key,
        prefix=weather_config.prefix
    )


def _load_geocoder_client_config(geocoder_config) -> ApiClient:
    return ApiClient(
        host=geocoder_config.host,
        api_key=geocoder_config.api_key,
        secret_key=geocoder_config.secret_key,
        prefix=geocoder_config.prefix
    )


def load_settings() -> Settings:
    config_profile = os.getenv("CONFIG_PROFILE")
    app_config = load_application_configuration(config_profile)
    weather_api = _load_weather_client_config(app_config.clients.weather)
    geocoder_api = _load_geocoder_client_config(app_config.clients.geocoder)
    return Settings(
        app_name=app_config.project.name,
        api_version=app_config.project.api_version,
        weather_api=weather_api,
        geocoder_api=geocoder_api,
    )


