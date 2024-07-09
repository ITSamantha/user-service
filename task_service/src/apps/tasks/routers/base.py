from fastapi import APIRouter

from src.apps.tasks.routers.task import router as task_router
from src.apps.tasks.routers.project import router as project_router
from src.apps.employees.routers.business_trip import router as business_trips_router

router: APIRouter = APIRouter(
    prefix=""
)

router.include_router(project_router)
router.include_router(task_router)
