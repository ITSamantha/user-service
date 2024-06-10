from fastapi import APIRouter

from src.apps.employees.routers.employee import router as employee_router
from src.apps.employees.routers.vacation import router as vacation_router
from src.apps.employees.routers.business_trip import router as business_trips_router

router: APIRouter = APIRouter(
    prefix="/employees",
    tags=["employees"],
)
router.include_router(vacation_router)
router.include_router(business_trips_router)
router.include_router(employee_router)
