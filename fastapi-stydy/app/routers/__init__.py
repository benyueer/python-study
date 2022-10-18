from fastapi import APIRouter
from .v1 import setup_routers as setup_v1_routers

def setup_routers(app):
    setup_v1_routers(app)

    router = APIRouter(prefix='/-')
    app.include_router(router)