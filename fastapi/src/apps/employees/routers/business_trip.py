from typing import List

from fastapi import APIRouter

from src.apps.employees import models
from src.apps.employees.schemas.business_trip import BusinessTrip, CreateBusinessTrip
from src.core.database.session_manager import db_manager
from src.utils.handlers import api_handler
from src.utils.repository.crud.base_crud_repository import SqlAlchemyRepository

router: APIRouter = APIRouter(
    prefix="/business_trips",
    tags=["business_trips"],
)


@router.get(path="", response_model=List[BusinessTrip])
@api_handler
async def get_business_trips():
    """Returns the list of business trips."""

    business_trips: List[models.BusinessTrip] = await SqlAlchemyRepository(db_manager.get_session,
                                                                           model=models.BusinessTrip).get_multi()
    return business_trips


@router.get(path="/{employee_id}")
@api_handler
async def get_business_trip(business_trip_id: int):
    """Returns the list of employees."""

    business_trip: models.BusinessTrip = await SqlAlchemyRepository(db_manager.get_session,
                                                                    model=models.BusinessTrip).get_single(
        id=business_trip_id)

    if not business_trip:
        raise Exception("Business trip with this data does not exist.")

    return business_trip


@router.post(path="", response_model=BusinessTrip)
@api_handler
async def create_business_trip(data: CreateBusinessTrip):
    """Returns created with the given data business trip."""

    business_trip: models.BusinessTrip = await SqlAlchemyRepository(db_manager.get_session,
                                                                    model=models.BusinessTrip).create(data)
    return business_trip
