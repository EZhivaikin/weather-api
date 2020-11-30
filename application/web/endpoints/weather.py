from fastapi import APIRouter

from application.service.weather import weather_service

router = APIRouter()


@router.get("/forecast/{city_name}")
async def get_forecast(city_name: str):
    weather_service.get_weather_forecast(city_name)
    return None


@router.get("/history")
async def get_last_5_days_weather():
    pass
