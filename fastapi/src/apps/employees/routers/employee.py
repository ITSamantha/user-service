from typing import List, Union

from fastapi import APIRouter, Depends

from src.apps.employees import models
from src.apps.employees.dependencies import valid_employee_position_id, valid_employee_id, valid_unit_id

from src.apps.employees.schemas.employee import CreateEmployee, CreateEmployeePosition, EmployeePosition, Employee, \
    Unit, CreateUnit
from src.core.database.session_manager import db_manager
from src.utils.handlers import api_handler
from src.utils.repository.crud.base_crud_repository import SqlAlchemyRepository

router: APIRouter = APIRouter(
    prefix="",
    tags=["employees"],
)


@router.get(path="/employee_positions", response_model=List[EmployeePosition])
@api_handler
async def get_employee_positions():
    """Returns the list of employee positions."""

    employee_positions: List[models.EmployeePosition] = await SqlAlchemyRepository(db_manager.get_session,
                                                                                   model=models.EmployeePosition).get_multi()
    return employee_positions


@router.get(path="/employee_positions/{employee_position_id}", response_model=EmployeePosition)
@api_handler
async def get_employee_position_by_id(employee_position: EmployeePosition = Depends(valid_employee_position_id)):
    """Returns employee position with employee_position_id."""

    return employee_position


@router.post(path="/employee_positions", response_model=EmployeePosition)
@api_handler
async def create_employee_position(data: CreateEmployeePosition):
    """Returns created with the given data employee position."""

    employee_position: models.EmployeePosition = await SqlAlchemyRepository(db_manager.get_session,
                                                                            model=models.EmployeePosition).create(data)
    return employee_position


@router.get(path="/units", response_model=List[Unit])
@api_handler
async def get_units():
    """Returns the list of units."""

    units: List[models.Unit] = await SqlAlchemyRepository(db_manager.get_session,
                                                          model=models.Unit).get_multi(unique=True)
    return units


@router.get(path="/units/{unit_id}", response_model=Unit)
@api_handler
async def get_unit_by_id(unit: Unit = Depends(valid_unit_id)):
    """Returns unit with unit_id."""

    return unit


@router.post(path="/units", response_model=Unit)
@api_handler
async def create_unit(data: CreateUnit):
    """Returns created with the given data unit."""

    unit: models.Unit = await SqlAlchemyRepository(db_manager.get_session,
                                                   model=models.Unit).create(data)
    return unit


@router.get(path="/", response_model=List[Employee])
@api_handler
async def get_employees():
    """Returns the list of employees."""

    employees: List[models.Employee] = await SqlAlchemyRepository(db_manager.get_session,
                                                                  model=models.Employee).get_multi()
    return employees


@router.get(path="/{employee_id}", response_model=Employee)
@api_handler
async def get_employee_by_id(employee: Employee = Depends(valid_employee_id)):
    """Returns employee with employee_id."""

    return employee


@router.post(path="/", response_model=Employee)
@api_handler
async def create_employee(data: CreateEmployee):
    """Returns created with the given data employee."""

    employee: models.Employee = await SqlAlchemyRepository(db_manager.get_session,
                                                           model=models.Employee).create(data)
    return employee
