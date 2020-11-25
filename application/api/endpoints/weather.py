from fastapi import APIRouter

router = APIRouter()

@router.get("/forecast")
def get_forecast():
    pass

@router.get("/last-days")
def get_last_5_days_weather():
    pass
