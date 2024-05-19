from fastapi import FastAPI

from src.apps.employees.routers.employee import router as employee_router
from src.apps.employees.routers.vacation import router as vacation_router


def create_app_routers(app: FastAPI):
    """Includes all nested routers into base."""

    app.include_router(employee_router)
    app.include_router(vacation_router)
    return app
