from fastapi import APIRouter

from api.routes import alerts

api_router = APIRouter()
api_router.include_router(alerts.router)
