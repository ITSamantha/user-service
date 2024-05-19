from typing import List

from fastapi import APIRouter

from src.apps.employees import models
from src.apps.employees.schemas.vacation import Vacation, VacationType, VacationReason, CreateVacationType, \
    CreateVacationReason, CreateVacation
from src.core.database.session_manager import db_manager
from src.utils.handlers import api_handler
from src.utils.repository.crud.base_crud_repository import SqlAlchemyRepository

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
    return vacation_types


@router.post(path="/types", response_model=VacationType)
@api_handler
async def create_vacation_type(data: CreateVacationType):
    """Returns created with the given data vacation type."""

    vacation_type: models.VacationType = await SqlAlchemyRepository(db_manager.get_session,
                                                                    model=models.VacationType).create(data)
    return vacation_type


@router.get(path="/reasons", response_model=List[VacationReason])
@api_handler
async def get_vacation_reasons():
    """Returns the list of vacation reasons."""

    vacation_reasons: List[models.VacationReason] = await SqlAlchemyRepository(db_manager.get_session,
                                                                               model=models.VacationReason).get_multi()
    return vacation_reasons


@router.post(path="/reasons", response_model=VacationReason)
@api_handler
async def create_vacation_reason(data: CreateVacationReason):
    """Returns created with the given data vacation reason."""

    vacation_reason: models.VacationReason = await SqlAlchemyRepository(db_manager.get_session,
                                                                        model=models.VacationReason).create(data)
    return vacation_reason


@router.get(path="", response_model=List[Vacation])
@api_handler
async def get_vacations():
    """Returns the list of vacations."""

    vacations: List[models.Vacation] = await SqlAlchemyRepository(db_manager.get_session,
                                                                  model=models.Vacation).get_multi()
    return vacations


@router.post(path="", response_model=Vacation)
@api_handler
async def create_vacation(data: CreateVacation):
    """Returns created with the given data vacation."""

    vacation: models.Vacation = await SqlAlchemyRepository(db_manager.get_session,
                                                           model=models.Vacation).create(data)
    return vacation
