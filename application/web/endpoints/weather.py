from fastapi import APIRouter, HTTPException
from starlette import status

from application.errors import GeocoderClientError, WeatherClientError
from application.schemas.weather_cast import WeatherCastList
from application.service.weather_cast import weather_service

router = APIRouter()


@router.get("/cast/forecast/city/{city_name}", response_model=WeatherCastList)
async def get_forecast(city_name: str):
    try:
        geocode = await weather_service.get_weather_forecast(city_name)
    except GeocoderClientError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Geocoder client unavailable"
        )

    except WeatherClientError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Weather client unavailable"
        )
    return geocode


@router.get("/history")
async def get_weather_history():
    pass
