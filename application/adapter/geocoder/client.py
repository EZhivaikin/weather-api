from application.adapter.async_request import async_request
from application.configure.load_config import settings
from config.settings import ApiClient


class GeocoderClient:
    def __init__(self, host: str, api_key: str, secret_key, prefix: str, timeout=10):
        self._host = host
        self._timeout = timeout
        self._api_key = api_key
        self._secret_key = secret_key
        self._prefix = prefix

    async def get_coords_by_city_name(self, city_name: str):
        headers = self._prepare_headers()
        params = self._prepare_params(city_name)
        url = self._prepare_url()
        result = await async_request(
            url=url,
            method="POST",
            headers=headers,
            params=params,
            timeout=self._timeout
        )
        return result

    def _prepare_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Token {self._api_key}",
            "X-Secret": self._secret_key
        }

    def _prepare_url(self) -> str:
        return f"https://{self._host}{self._prefix}"

    def _prepare_params(self, city_name: str) -> dict:
        return dict(
            format="json",
            apikey=self._api_key,
            geocode=city_name
        )


def load_geocoder_client(geocoder_settings: ApiClient):
    return GeocoderClient(
        host=geocoder_settings.host,
        api_key=geocoder_settings.api_key,
        secret_key=geocoder_settings.secret_key,
        prefix=geocoder_settings.prefix
    )


geocoder_client = load_geocoder_client(settings.geocoder_api)
