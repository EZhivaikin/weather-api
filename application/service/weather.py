from application.adapter.geocoder.client import geocoder_client


class WeatherService:
    def get_weather_forecast(self, city_name):
        geocoder_client.get_coords_by_city_name(city_name)


weather_service = WeatherService()