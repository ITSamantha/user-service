from typing import List, Union

from fastapi import APIRouter

from src.apps.employees import models
from src.apps.employees.schemas.employee import CreateEmployee, CreateEmployeePosition, EmployeePosition
from src.core.database.session_manager import db_manager
from src.utils.handlers import api_handler
from src.utils.repository.crud.base_crud_repository import SqlAlchemyRepository

router: APIRouter = APIRouter(
    prefix="/employees",
    tags=["employees"],
)


@router.get(path="/employee_positions", response_model=List[EmployeePosition])
@api_handler
async def get_employee_positions():
    """Returns the list of employee positions."""

    employee_positions: List[models.EmployeePosition] = await SqlAlchemyRepository(db_manager.get_session,
                                                                                   model=models.EmployeePosition).get_multi()
    return employee_positions


@router.post(path="/employee_positions", response_model=EmployeePosition)
@api_handler
async def create_employee_positions(data: CreateEmployeePosition):
    """Returns created with the given data employee position."""

    employee_position: models.EmployeePosition = await SqlAlchemyRepository(db_manager.get_session,
                                                                            model=models.EmployeePosition).create(data)
    return employee_position


@router.get(path="")
@api_handler
async def get_employees():
    """Returns the list of employees."""

    employees: List[models.Employee] = await SqlAlchemyRepository(db_manager.get_session,
                                                                  model=models.Employee).get_multi(deleted_at=None)
    return employees
