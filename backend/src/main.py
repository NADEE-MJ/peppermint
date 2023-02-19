from fastapi import FastAPI
from src.api.api_v1.api import api_router
from src.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_VERSION_STR}/openapi.json")

app.include_router(api_router, prefix=settings.API_VERSION_STR)
