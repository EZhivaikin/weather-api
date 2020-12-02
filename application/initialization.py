from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from application.config.application import settings
from application.web.api import api_router

app = FastAPI(
    title=settings.app_name
)
app.include_router(api_router, prefix=f"/api/v{settings.api_version}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
