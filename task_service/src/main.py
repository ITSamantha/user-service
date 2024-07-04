import uvicorn
from fastapi import FastAPI

from src.config.app import settings_app
from src.config.uvicorn import settings_uvicorn
from src.core.router.base import create_app_routers


def get_application() -> FastAPI:
    """Creates FastAPI application."""

    application = FastAPI(
        title=settings_app.APP_NAME,
        debug=settings_app.DEBUG,
        version=settings_app.APP_VERSION
    )

    create_app_routers(application)

    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run(
        app=settings_uvicorn.UVICORN_APP_NAME,
        host=settings_uvicorn.UVICORN_HOST,
        port=settings_uvicorn.UVICORN_PORT,
        reload=settings_uvicorn.UVICORN_RELOAD
    )
