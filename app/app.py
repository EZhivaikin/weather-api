from fastapi import FastAPI


def set_cors_middleware():
    pass


def _load_application_configuration():
    pass


def init() -> FastAPI:
    app = FastAPI(
        title="weather-api"
    )
    return app
