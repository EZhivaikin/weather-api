
from fastapi import FastAPI
# Press the green button in the gutter to run the script.

def set_cors_middleware():


def init() -> FastAPI:
    app = FastAPI(
        title="weather-api"
    )
    return app
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
