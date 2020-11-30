from application.adapter.geocoder.client import geocoder_client
from application.adapter.weather.client import weather_client
from application.domain.geocode import Geocode


class WeatherService:
    async def get_weather_forecast(self, city_name):
        coords: Geocode = await geocoder_client.get_coords_by_city_name(city_name)
        weather = await weather_client.get_weather_forecast(coords)
        return weather


weather_service = WeatherService()