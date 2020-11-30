class ApplicationError(Exception):
    pass


class GeocoderClientError(ApplicationError):
    pass


class WeatherClientError(ApplicationError):
    pass
