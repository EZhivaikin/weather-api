class OpenWeatherClient:
    def __init__(self, host: str, api_key: str, timeout=10):
        self.host = host
        self.timeout = timeout
        self.api_key = api_key

    async def get_weather_forecast(self):
        pass

    async def get_weather_history(self):
        pass
