class GeoCoderClient:
    def __init__(self, host: str, api_key: str, timeout=10):
        self.host = host
        self.timeout = timeout
        self.api_key = api_key

    async def get_coords_by_city_name(self, city_name: str):
        pass
