from fastapi import HTTPException
from fastapi.responses import JSONResponse


def setup_exception(app):
    @app.exception_handler(HTTPException)
    async def general_http_exception_handler(
        request,
        exc: HTTPException
    ):
        return JSONResponse(
            status_code=500, content='error'
        )