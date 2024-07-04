from fastapi import FastAPI

from src.apps.employees.routers.base import router as employees_router


def create_app_routers(app: FastAPI):
    """Includes all nested routers into base."""

    app.include_router(employees_router)
    return app
