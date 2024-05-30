from typing import List, Optional

from fastapi import APIRouter, Depends, Request

from src.apps.employees import models
from src.apps.employees.dependencies import valid_vacation_id, valid_vacation_reason_id, valid_vacation_type_id, \
    valid_employee_business_trip, valid_employee_vacation
from src.apps.employees.schemas.vacation import Vacation, VacationType, VacationReason, CreateVacationType, \
    CreateVacationReason, CreateVacation, UpdateVacationType, UpdateVacationReason, UpdateVacation
from src.apps.employees.transformers.vacation import VacationTypeTransformer, VacationReasonTransformer, \
    VacationTransformer
from src.core.database.session_manager import db_manager
from src.utils.handlers import api_handler
from src.utils.repository.crud.base_crud_repository import SqlAlchemyRepository
from src.utils.transformer import transform

router: APIRouter = APIRouter(
    prefix="/vacations",
    tags=["vacations"],
)

""" VACATION TYPE """


@router.get(path="/types", response_model=List[VacationType], tags=["vacation_types"])
@api_handler
async def get_vacation_types():
    """Returns the list of vacation types."""

    vacation_types: List[models.VacationType] = await SqlAlchemyRepository(db_manager.get_session,
                                                                           model=models.VacationType).get_multi()
    return transform(vacation_types, VacationTypeTransformer())


@router.get(path="/types/{vacation_type_id}", response_model=VacationType, tags=["vacation_types"])
@api_handler
async def get_vacation_type_by_id(vacation_type: models.VacationType = Depends(valid_vacation_type_id)):
    """Returns vacation type with id=vacation_type_id."""

    return transform(vacation_type, VacationTypeTransformer())


@router.post(path="/types", response_model=VacationType, tags=["vacation_types"])
@api_handler
async def create_vacation_type(data: CreateVacationType):
    """Returns created with the given data vacation type."""

    vacation_type: models.VacationType = await SqlAlchemyRepository(db_manager.get_session,
                                                                    model=models.VacationType).create(data=data)
    return transform(vacation_type, VacationTypeTransformer())


@router.patch(path="/types/{vacation_type_id}", response_model=VacationType, tags=["vacation_types"])
@api_handler
async def update_vacation_type_by_id(data: UpdateVacationType,
                                     vacation_type: models.VacationType = Depends(valid_vacation_type_id)):
    """Returns updated with given data vacation type."""

    vacation_type: models.VacationType = await SqlAlchemyRepository(db_manager.get_session,
                                                                    model=models.VacationType).update(data=data,
                                                                                                      id=vacation_type.id)
    return transform(vacation_type, VacationTypeTransformer())


""" VACATION REASON """


@router.get(path="/reasons", response_model=List[VacationReason], tags=["vacation_reasons"])
@api_handler
async def get_vacation_reasons():
    """Returns the list of vacation reasons."""

    vacation_reasons: List[models.VacationReason] = await SqlAlchemyRepository(db_manager.get_session,
                                                                               model=models.VacationReason).get_multi()
    return transform(vacation_reasons, VacationReasonTransformer())


@router.get(path="/reasons/{vacation_reason_id}", response_model=VacationReason, tags=["vacation_reasons"])
@api_handler
async def get_vacation_reason_by_id(vacation_reason: Vacation = Depends(valid_vacation_reason_id)):
    """Returns vacation reason with id=vacation_reason_id."""

    return transform(vacation_reason, VacationReasonTransformer())


@router.patch(path="/reasons/{vacation_reason_id}", response_model=VacationReason, tags=["vacation_reasons"])
@api_handler
async def update_vacation_reason_by_id(data: UpdateVacationReason,
                                       vacation_reason: models.VacationReason = Depends(valid_vacation_reason_id)):
    """Returns updated with given data vacation reason."""

    vacation_reason: models.VacationReason = await SqlAlchemyRepository(db_manager.get_session,
                                                                        model=models.VacationReason).update(data=data,
                                                                                                            id=vacation_reason.id)
    return transform(vacation_reason, VacationReasonTransformer())


@router.post(path="/reasons", response_model=VacationReason, tags=["vacation_reasons"])
@api_handler
async def create_vacation_reason(data: CreateVacationReason):
    """Returns created with the given data vacation reason."""

    vacation_reason: models.VacationReason = await SqlAlchemyRepository(db_manager.get_session,
                                                                        model=models.VacationReason).create(data=data)
    return transform(vacation_reason, VacationReasonTransformer())


""" VACATION """


@router.get(path="", response_model=List[Vacation], tags=["vacation"])
@api_handler
async def get_vacations():
    """Returns the list of vacations."""

    vacations: List[models.Vacation] = await SqlAlchemyRepository(db_manager.get_session,
                                                                  model=models.Vacation).get_multi(unique=True)
    return transform(vacations, VacationTransformer().include(["employee", "vacation_type", "vacation_reason"]))


@router.get(path="/{vacation_id}", response_model=Vacation, tags=["vacation"])
@api_handler
async def get_vacation_by_id(vacation: Vacation = Depends(valid_vacation_id)):
    """Returns vacation with vacation_id."""

    return transform(vacation, VacationTransformer().include(["employee", "vacation_type", "vacation_reason"]))


# TODO: ДИАНА ДОДЕЛАТЬ
@router.patch(path="/{vacation_id}", response_model=Vacation, tags=["vacation"])
@api_handler
async def update_vacation_by_id(data: UpdateVacation, vacation: models.Vacation = Depends(valid_vacation_id)):
    """Returns updated with given data vacation."""

    vacation: models.Vacation = await SqlAlchemyRepository(db_manager.get_session,
                                                           model=models.Vacation).update(data=data,
                                                                                         exclude_unset=True,
                                                                                         exclude_none=False,
                                                                                         id=vacation.id)
    return transform(vacation, VacationTransformer().include(["vacation_type", "vacation_reason"]))


@router.post(path="", response_model=Vacation, tags=["vacation"])
@api_handler
async def create_vacation(data: CreateVacation = Depends(valid_employee_vacation)):
    """Returns created with the given data vacation."""

    vacation: models.Vacation = await SqlAlchemyRepository(db_manager.get_session,
                                                           model=models.Vacation).create(data=data)
    return transform(vacation, VacationTransformer().include(["vacation_type", "vacation_reason"]))
