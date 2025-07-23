from fastapi import APIRouter

from app.api.v1.routes.daily_prices import router as daily_prices_router
from app.api.v1.routes.securities import router as securities_router

api_router = APIRouter()

api_router.include_router(securities_router)
api_router.include_router(daily_prices_router) 