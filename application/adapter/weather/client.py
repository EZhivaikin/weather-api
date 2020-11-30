from typing import Optional

from application.configure.load_config import settings
from config.settings import ApiClient


class WeatherClient:
    def __init__(
            self, host: str, api_key: Optional[str], secret_key: Optional[str], prefix: str, timeout=10
    ):
        self._host = host
        self._timeout = timeout
        self._api_key = api_key
        self._prefix = prefix
        self._secret_key = secret_key

    async def get_weather_forecast(self):
        pass

    async def get_weather_history(self):
        pass


def load_weather_client(weather_settings: ApiClient):
    return WeatherClient(
        host=weather_settings.host,
        api_key=weather_settings.api_key,
        secret_key=weather_settings.secret_key,
        prefix=weather_settings.prefix
    )


weather_client = load_weather_client(settings.weather_api)
