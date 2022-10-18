from fastapi import APIRouter

from .city import router as city_router

def setup_routers(app):
    router = APIRouter(prefix='/v1')

    router.include_router(city_router)

    app.include_router(router)