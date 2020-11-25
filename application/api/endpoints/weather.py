from fastapi import APIRouter

from application.adapter.geocoder.client import geocoder_client

router = APIRouter()


@router.get("/forecast/{city_name}")
async def get_forecast(city_name: str):
    r = await geocoder_client.get_coords_by_city_name(city_name)
    return r


@router.get("/history")
async def get_last_5_days_weather():
    pass
