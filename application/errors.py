class ApplicationError(Exception):
    pass


class GeocoderClientError(ApplicationError):
    pass


class CityNotFound(GeocoderClientError):
    pass


class WeatherClientError(ApplicationError):
    pass
