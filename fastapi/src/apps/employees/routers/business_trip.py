from typing import List

from fastapi import APIRouter, Depends

from src.apps.employees import models
from src.apps.employees.dependencies import valid_business_trip_id, valid_employee_business_trip, existing_business_trip
from src.apps.employees.schemas.business_trip import BusinessTrip, CreateBusinessTrip, UpdateBusinessTrip
from src.apps.employees.transformers.business_trip import BusinessTripTransformer
from src.core.database.session_manager import db_manager
from src.core.schemas.base import BaseDeleteSchema
from src.utils.handlers import api_handler
from src.utils.repository.crud.base_crud_repository import SqlAlchemyRepository
from src.utils.transformer import transform

router: APIRouter = APIRouter(
    prefix="/business_trips",
    tags=["business_trips"],
)

""" BUSINESS TRIPS """


@router.get(path="", response_model=List[BusinessTrip], tags=["business_trips"])
@api_handler
async def get_business_trips() -> List[BusinessTrip]:
    """Returns the list of business trips."""

    business_trips: List[models.BusinessTrip] = await SqlAlchemyRepository(db_manager.get_session,
                                                                           model=models.BusinessTrip).get_multi(
        unique=True)
    return transform(business_trips, BusinessTripTransformer().include(["employee"]))


@router.get(path="/{business_trip_id}", response_model=List[BusinessTrip], tags=["business_trips"])
@api_handler
async def get_business_trip_by_id(business_trip: BusinessTrip = Depends(valid_business_trip_id)) -> List[BusinessTrip]:
    """Returns the business trip with the given id."""

    return transform(business_trip, BusinessTripTransformer().include(["employee"]))


@router.post(path="", response_model=BusinessTrip, tags=["business_trips"])
@api_handler
async def create_business_trip(data: CreateBusinessTrip = Depends(valid_employee_business_trip)) -> BusinessTrip:
    """Returns created with the given data business trip."""

    business_trip: models.BusinessTrip = await SqlAlchemyRepository(db_manager.get_session,
                                                                    model=models.BusinessTrip).create(data)
    return transform(business_trip, BusinessTripTransformer())


@router.patch(path="/{business_trip_id}", response_model=BusinessTrip, tags=["business_trips"])
@api_handler
async def update_business_trip_by_id(data: UpdateBusinessTrip,
                                     business_trip: models.BusinessTrip = Depends(
                                         existing_business_trip)) -> BusinessTrip:
    """Returns updated with given data business trip."""

    business_trip: models.BusinessTrip = await SqlAlchemyRepository(db_manager.get_session,
                                                                    model=models.BusinessTrip).update(
        data=data,
        id=business_trip.id)
    return transform(business_trip, BusinessTripTransformer())


@router.delete(path="/{business_trip_id}", response_model=BusinessTrip, tags=["business_trips"])
@api_handler
async def delete_business_trip(business_trip: models.BusinessTrip = Depends(existing_business_trip)) -> BusinessTrip:
    """Returns deleted business trip."""

    business_trip: models.BusinessTrip = await SqlAlchemyRepository(db_manager.get_session,
                                                                    model=models.BusinessTrip).update(
        data=BaseDeleteSchema(),
        id=business_trip.id)
    return transform(business_trip, BusinessTripTransformer())
