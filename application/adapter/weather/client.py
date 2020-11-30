from typing import Optional

from application.configure.load_config import settings


class WeatherClient:
    def __init__(
            self, host: str, api_key: Optional[str], secret_key: Optional[str], prefix: str, timeout=10
    ):
        self.host = host
        self.timeout = timeout
        self.api_key = api_key
        self.prefix = prefix
        self.secret_key = secret_key

    async def get_weather_forecast(self):
        pass

    async def get_weather_history(self):
        pass


openweather_client = WeatherClient(
    host=settings.openweather_api.host,
    api_key=settings.openweather_api.api_key,
    secret_key=settings.openweather_api.secret_key,
    prefix=settings.openweather_api.prefix
)
