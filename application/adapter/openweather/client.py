class OpenWeatherClient:
    def __init__(self, host: str, timeout=10):
        self.host = host
        self.timeout = timeout

    async def get_weather_forecast(self):
        pass

    async def get_weather_history(self):
        pass
