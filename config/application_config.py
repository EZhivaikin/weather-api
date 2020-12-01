from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings

APPLICATION_ROOT = Path(__file__).absolute().parent.parent
APPLICATION_CONFIGS_ROOT = APPLICATION_ROOT / "config"


@dataclass
class ApiClient:
    host: str
    api_key: Optional[str]
    secret_key: Optional[str]
    prefix: Optional[str]


class Settings(BaseSettings):
    app_name: str
    api_version: str
    weather_api: ApiClient
    geocoder_api: ApiClient
