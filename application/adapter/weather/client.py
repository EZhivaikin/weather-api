from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from application.adapter.async_request import async_request
from application.configure.load_config import settings
from application.domain.geocode import Geocode
from application.errors import WeatherClientError
from application.schemas.weather_cast import WeatherCastList, WeatherCast
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

    async def get_weather_forecast(self, geocode: Geocode):
        path = '/onecall'
        url = self._prepare_url(path)
        params = self._prepare_params(geocode)
        try:
            result = await async_request(
                url=url,
                method="GET",
                params=params,
                timeout=self._timeout
            )
        except Exception:
            raise WeatherClientError()

        weather_cast = self._convert_to_weathercast(result)
        return weather_cast

    async def get_weather_history(self):
        pass

    def _prepare_url(self, path) -> str:
        return f"https://{self._host}{self._prefix}{path}"

    def _prepare_params(self, geocode: Geocode) -> dict:
        return dict(
            lat=geocode.lat,
            lon=geocode.lon,
            units='metric',
            exclude=','.join(['current', 'minutely', 'hourly', 'alerts']),
            appid=self._api_key,
        )

    def _convert_to_weathercast(self, response: dict):
        casts = response.get('daily')
        weather_casts: List[WeatherCast] = []
        for cast in casts:
            timestamp = cast.get('dt')
            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            min_temp = Decimal(cast.get('temp').get('min'))
            max_temp = Decimal(cast.get('temp').get('max'))
            avg_temp = ((min_temp + max_temp) / 2).quantize(Decimal(".01"))
            weather_cast = WeatherCast(
                date=date,
                temperature=f"{avg_temp}°С"
            )
            weather_casts.append(weather_cast)
        return WeatherCastList(weather=weather_casts)


def load_weather_client(weather_settings: ApiClient):
    return WeatherClient(
        host=weather_settings.host,
        api_key=weather_settings.api_key,
        secret_key=weather_settings.secret_key,
        prefix=weather_settings.prefix
    )


weather_client = load_weather_client(settings.weather_api)
