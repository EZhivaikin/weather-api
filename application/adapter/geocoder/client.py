from typing import Optional
from urllib.parse import urljoin

from application.adapter.async_request import async_request
from application.config.application import settings
from application.domain.geocode import Geocode
from application.errors import GeocoderClientError, CityNotFound
from config.application_config import ApiClient


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
        try:
            result = await self._make_request(url, params, headers)
        except Exception as e:
            raise GeocoderClientError()

        geocode = self._convert_to_geocode(result)
        if not geocode:
            raise CityNotFound()

        return geocode

    def _prepare_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Token {self._api_key}",
            "X-Secret": self._secret_key
        }

    async def _make_request(self, url, params, headers):
        return await async_request(
            url=url,
            method="GET",
            params=params,
            timeout=self._timeout,
            headers=headers
        )

    def _prepare_url(self) -> str:
        return urljoin(self._host, self._prefix)

    def _prepare_params(self, city_name: str) -> dict:
        return dict(
            format="json",
            apikey=self._api_key,
            geocode=city_name
        )

    def _convert_to_geocode(self, response: dict) -> Optional[Geocode]:
        geo_objects = (
            response
                .get('response')
                .get('GeoObjectCollection')
                .get('featureMember')
        )
        if geo_objects is None or len(geo_objects) == 0:
            return None

        geo_object = geo_objects[0].get('GeoObject')
        position = geo_object.get('Point').get('pos')
        lon, lat = position.split()

        return Geocode(
            lat=lat,
            lon=lon
        )


def load_geocoder_client(geocoder_settings: ApiClient):
    return GeocoderClient(
        host=geocoder_settings.host,
        api_key=geocoder_settings.api_key,
        secret_key=geocoder_settings.secret_key,
        prefix=geocoder_settings.prefix
    )


geocoder_client = load_geocoder_client(settings.geocoder_api)
