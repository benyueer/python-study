from time import time
from typing import Optional
from fastapi import FastAPI, Request
from .exception import setup_exception
from fastapi.staticfiles import StaticFiles
from app.routers import setup_routers


def create_application():
    app = FastAPI()

    # 挂载静态文件 
    app.mount(path='/static', app=StaticFiles(directory='./static'))

    setup_routers(app)
    setup_exception(app)

    @app.middleware('http')
    async def add_process_time_header(request: Request, call_next):
        start = time()
        response = await call_next(request)
        process_time = time() - start
        response.headers['X-Procress-Time'] = str(process_time)
        return response

    return app
