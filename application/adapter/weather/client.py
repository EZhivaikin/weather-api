import asyncio
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, List
from urllib.parse import urljoin

from application.adapter.async_request import async_request
from application.config.application import settings
from application.domain.geocode import Geocode
from application.domain.weather import WeatherCastInformation
from application.errors import WeatherClientError
from config.application_config import ApiClient


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
        path = 'onecall'
        url = self._prepare_url(path)
        params = self._prepare_params_forecast(geocode)
        try:
            result = await self._make_request(url, params)
        except Exception:
            raise WeatherClientError()

        weather_cast = self._convert_from_forecast_to_weathercast(result)
        return weather_cast

    async def get_weather_history(self, geocode):
        path = 'onecall/timemachine'
        url = self._prepare_url(path)
        timestamps = self._get_previous_five_days_timestamp()

        history_params: List[dict] = [
            self._prepare_params_history(geocode, timestamp) for timestamp in timestamps
        ]
        futures = [
            self._make_request(url=url, params=params) for params in history_params
        ]

        casts: List[WeatherCastInformation] = []
        for future in asyncio.as_completed(futures):
            response = await future
            weather_cast_information = self._convert_from_previous_to_weathercast(response)
            casts.append(weather_cast_information)

        casts.sort(key=lambda x: x.date, reverse=True)
        return casts

    def _prepare_url(self, path) -> str:
        return urljoin(self._host, f"{self._prefix}/{path}")

    def _prepare_params_forecast(self, geocode: Geocode) -> dict:
        return dict(
            lat=geocode.lat,
            lon=geocode.lon,
            units='metric',
            exclude=','.join(['current', 'minutely', 'hourly', 'alerts']),
            appid=self._api_key,
        )

    def _prepare_params_history(self, geocode, timestamp):
        return dict(
            lat=geocode.lat,
            lon=geocode.lon,
            units='metric',
            dt=timestamp,
            appid=self._api_key,
        )

    async def _make_request(self, url, params):
        return await async_request(
            url=url,
            method="GET",
            params=params,
            timeout=self._timeout
        )

    def _get_previous_five_days_timestamp(self):
        today = datetime.today()
        return [
            int(datetime.timestamp(today - timedelta(i)))
            for i in range(5)
        ]

    def _convert_from_forecast_to_weathercast(self, response: dict):
        daily_casts = response.get('daily')
        weather_casts: List[WeatherCastInformation] = []
        for daily_cast in daily_casts:
            timestamp = daily_cast.get('dt')
            date = datetime.fromtimestamp(timestamp)
            min_temp = Decimal(daily_cast.get('temp').get('min'))
            max_temp = Decimal(daily_cast.get('temp').get('max'))
            avg_temp = ((min_temp + max_temp) / 2).quantize(Decimal(".01"))
            weather_cast = WeatherCastInformation(
                date=date,
                temperature=avg_temp
            )
            weather_casts.append(weather_cast)
        return weather_casts

    def _convert_from_previous_to_weathercast(self, response: dict):
        current_day = response.get('current')
        date = datetime.fromtimestamp(current_day.get('dt'))
        temp = Decimal(current_day.get('temp')).quantize(Decimal(".01"))
        weather_cast = WeatherCastInformation(
            date=date,
            temperature=temp
        )
        return weather_cast


def load_weather_client(weather_settings: ApiClient):
    return WeatherClient(
        host=weather_settings.host,
        api_key=weather_settings.api_key,
        secret_key=weather_settings.secret_key,
        prefix=weather_settings.prefix
    )


weather_client = load_weather_client(settings.weather_api)
