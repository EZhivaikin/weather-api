from fastapi import APIRouter

from application.api.endpoints import weather

api_router = APIRouter()

api_router.include_router(weather.router, prefix="/weather", tags=["weather"])
