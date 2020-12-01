from typing import List

from pydantic import BaseModel


class WeatherCastBaseSchema(BaseModel):
    date: str
    temperature: str


class WeatherCastSchema(WeatherCastBaseSchema):
    pass


class WeatherCastListSchema(BaseModel):
    weather: List[WeatherCastSchema]
