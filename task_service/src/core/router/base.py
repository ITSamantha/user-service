from fastapi import FastAPI

from src.apps.employees.routers.base import router as tasks_router


def create_app_routers(app: FastAPI):
    """Includes all nested routers into base."""

    app.include_router(tasks_router)
    return app
