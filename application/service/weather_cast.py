from typing import List

from application.adapter.geocoder.client import geocoder_client
from application.adapter.weather.client import weather_client
from application.domain.geocode import Geocode
from application.domain.weather import WeatherCastInformation
from application.schemas.weather_cast import WeatherCastSchema, WeatherCastListSchema


class WeatherService:
    async def get_weather_forecast(self, city_name) -> WeatherCastListSchema:
        coords: Geocode = await geocoder_client.get_coords_by_city_name(city_name)
        casts_information: List[WeatherCastInformation] = await weather_client.get_weather_forecast(coords)
        weather_casts = [
            WeatherCastSchema(
                date=cast.date.strftime("%Y-%m-%d"),
                temperature=f"{cast.temperature}°С",
            )
            for cast in casts_information
        ]
        return WeatherCastListSchema(weather_casts=weather_casts)


weather_service = WeatherService()