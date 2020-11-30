import json

from application.adapter.async_request import async_request
from application.configure.load_config import settings


class GeoCoderClient:
    def __init__(self, host: str, api_key: str, secret_key, prefix: str, timeout=10):
        self.host = host
        self.timeout = timeout
        self.api_key = api_key
        self.secret_key = secret_key
        self.prefix = prefix

    async def get_coords_by_city_name(self, city_name: str):
        headers = self._prepare_headers()
        params = self._prepare_params(city_name)
        url = self._prepare_url()
        result = await async_request(
            url=url,
            method="POST",
            headers=headers,
            params=params,
            timeout=self.timeout
        )
        return result

    def _prepare_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.api_key}",
            "X-Secret": self.secret_key
        }

    def _prepare_url(self) -> str:
        return f"https://{self.host}{self.prefix}"

    def _prepare_params(self, city_name: str) -> dict:
        return dict(
            format="json",
            apikey=self.api_key,
            geocode=city_name
        )


geocoder_client = GeoCoderClient(
    host=settings.geocoder_api.host,
    api_key=settings.geocoder_api.api_key,
    secret_key=settings.geocoder_api.secret_key,
    prefix=settings.geocoder_api.prefix
)
