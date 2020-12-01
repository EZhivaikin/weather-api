from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class WeatherCastInformation:
    date: datetime
    temperature: Decimal