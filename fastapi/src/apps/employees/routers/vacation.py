from typing import List

from fastapi import APIRouter, Depends

from src.apps.employees import models
from src.apps.employees.dependencies import valid_vacation_id, valid_vacation_reason_id
from src.apps.employees.schemas.vacation import Vacation, VacationType, VacationReason, CreateVacationType, \
    CreateVacationReason, CreateVacation
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


@router.get(path="/types", response_model=List[VacationType])
@api_handler
async def get_vacation_types():
    """Returns the list of vacation types."""

    vacation_types: List[models.VacationType] = await SqlAlchemyRepository(db_manager.get_session,
                                                                           model=models.VacationType).get_multi()
    return transform(vacation_types, VacationTypeTransformer())


@router.post(path="/types", response_model=VacationType)
@api_handler
async def create_vacation_type(data: CreateVacationType):
    """Returns created with the given data vacation type."""

    vacation_type: models.VacationType = await SqlAlchemyRepository(db_manager.get_session,
                                                                    model=models.VacationType).create(data)
    return transform(vacation_type, VacationTypeTransformer())


@router.get(path="/reasons", response_model=List[VacationReason])
@api_handler
async def get_vacation_reasons():
    """Returns the list of vacation reasons."""

    vacation_reasons: List[models.VacationReason] = await SqlAlchemyRepository(db_manager.get_session,
                                                                               model=models.VacationReason).get_multi()
    return transform(vacation_reasons, VacationReasonTransformer())


@router.get(path="/reasons/{vacation_reason_id}", response_model=VacationReason)
@api_handler
async def get_vacation_reason_by_id(vacation_reason: Vacation = Depends(valid_vacation_reason_id)):
    """Returns employee position with employee_position_id."""

    return transform(vacation_reason, VacationReasonTransformer())


@router.post(path="/reasons", response_model=VacationReason)
@api_handler
async def create_vacation_reason(data: CreateVacationReason):
    """Returns created with the given data vacation reason."""

    vacation_reason: models.VacationReason = await SqlAlchemyRepository(db_manager.get_session,
                                                                        model=models.VacationReason).create(data)
    return transform(vacation_reason, VacationReasonTransformer())


@router.get(path="", response_model=List[Vacation])
@api_handler
async def get_vacations():
    """Returns the list of vacations."""

    vacations: List[models.Vacation] = await SqlAlchemyRepository(db_manager.get_session,
                                                                  model=models.Vacation).get_multi(unique=True)
    return transform(vacations, VacationTransformer().include(["employee", "vacation_type", "vacation_reason"]))


@router.get(path="/{vacation_id}", response_model=Vacation)
@api_handler
async def get_vacation_by_id(vacation: Vacation = Depends(valid_vacation_id)):
    """Returns employee position with employee_position_id."""

    return transform(vacation, VacationTransformer().include(["employee", "vacation_type", "vacation_reason"]))


@router.post(path="", response_model=Vacation)
@api_handler
async def create_vacation(data: CreateVacation):
    """Returns created with the given data vacation."""

    vacation: models.Vacation = await SqlAlchemyRepository(db_manager.get_session,
                                                           model=models.Vacation).create(data)
    return transform(vacation, VacationTransformer().include(["vacation_type", "vacation_reason"]))
