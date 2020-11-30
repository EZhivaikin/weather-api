from typing import List

from pydantic import BaseModel


class WeatherCastBase(BaseModel):
    date: str
    temperature: str


class WeatherCast(WeatherCastBase):
    pass


class WeatherCastList(BaseModel):
    weather: List[WeatherCast]
