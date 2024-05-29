from typing import List, Union

from fastapi import APIRouter, Depends

from src.apps.employees import models
from src.apps.employees.dependencies import valid_employee_position_id, valid_employee_id, valid_unit_id
from src.apps.employees.schemas.business_trip import BusinessTrip

from src.apps.employees.schemas.employee import CreateEmployee, CreateEmployeePosition, EmployeePosition, Employee, \
    Unit, CreateUnit, SearchEmployee, UpdateEmployeePosition, UpdateUnit, UpdateEmployee
from src.apps.employees.schemas.vacation import Vacation
from src.apps.employees.transformers.business_trip import BusinessTripTransformer
from src.apps.employees.transformers.employee import EmployeePositionTransformer, UnitTransformer, EmployeeTransformer
from src.apps.employees.transformers.vacation import VacationTransformer
from src.core.database.session_manager import db_manager
from src.utils.handlers import api_handler
from src.utils.repository.crud.base_crud_repository import SqlAlchemyRepository
from src.utils.transformer import transform

router: APIRouter = APIRouter(
    prefix="",
    tags=["employees"],
)

""" EMPLOYEE POSITION """


@router.get(path="/positions", response_model=List[EmployeePosition], tags=["employee_positions"])
@api_handler
async def get_employee_positions():
    """Returns the list of employee positions."""

    employee_positions: List[models.EmployeePosition] = await SqlAlchemyRepository(db_manager.get_session,
                                                                                   model=models.EmployeePosition).get_multi()
    return transform(employee_positions, EmployeePositionTransformer())


@router.get(path="/positions/{employee_position_id}", response_model=EmployeePosition, tags=["employee_positions"])
@api_handler
async def get_employee_position_by_id(employee_position: EmployeePosition = Depends(valid_employee_position_id)):
    """Returns employee position with id=employee_position_id."""

    return transform(employee_position, EmployeePositionTransformer())


@router.post(path="/positions", response_model=EmployeePosition, tags=["employee_positions"])
@api_handler
async def create_employee_position(data: CreateEmployeePosition):
    """Returns created with the given data employee position."""

    employee_position: models.EmployeePosition = await SqlAlchemyRepository(db_manager.get_session,
                                                                            model=models.EmployeePosition).create(data)
    return transform(employee_position, EmployeePositionTransformer())


@router.patch(path="/positions/{employee_position_id}", response_model=EmployeePosition, tags=["employee_positions"])
@api_handler
async def update_employee_position_by_id(data: UpdateEmployeePosition,
                                         employee_position: models.EmployeePosition = Depends(
                                             valid_employee_position_id)):
    """Returns updated with given data employee position."""

    employee_position: models.EmployeePosition = await SqlAlchemyRepository(db_manager.get_session,
                                                                            model=models.EmployeePosition).update(
        data=data,
        id=employee_position.id)
    return transform(employee_position, EmployeePositionTransformer())


""" UNIT """


@router.get(path="/units", response_model=List[Unit], tags=["units"])
@api_handler
async def get_units():
    """Returns the list of units."""

    units: List[models.Unit] = await SqlAlchemyRepository(db_manager.get_session,
                                                          model=models.Unit).get_multi(unique=True)
    return transform(units,
                     UnitTransformer().include(["director", "employees"]))


@router.get(path="/units/{unit_id}", response_model=Unit, tags=["units"])
@api_handler
async def get_unit_by_id(unit: Unit = Depends(valid_unit_id)):
    """Returns unit with id=unit_id."""

    return transform(unit, UnitTransformer().include(["director", "employees"]))


@router.post(path="/units", response_model=Unit, tags=["units"])
@api_handler
async def create_unit(data: CreateUnit):
    """Returns created with the given data unit."""

    unit: models.Unit = await SqlAlchemyRepository(db_manager.get_session,
                                                   model=models.Unit).create(data)
    return transform(unit, UnitTransformer())


@router.patch(path="/units/{unit_id}", response_model=Unit, tags=["units"])
@api_handler
async def update_unit_by_id(data: UpdateUnit,
                            unit: models.Unit = Depends(valid_unit_id)):
    """Returns updated with given data unit."""

    unit: models.Unit = await SqlAlchemyRepository(db_manager.get_session,
                                                   model=models.Unit).update(
        data=data,
        id=unit.id)
    return transform(unit, UnitTransformer())


""" EMPLOYEE """


@router.get(path="/", response_model=List[Employee], tags=["employees"])
@api_handler
async def get_employees():
    """Returns the list of employees."""

    employees: List[models.Employee] = await SqlAlchemyRepository(db_manager.get_session,
                                                                  model=models.Employee).get_multi(unique=True)
    return transform(employees, EmployeeTransformer().include(["unit"]))


@router.get(path="/search", response_model=List[Employee], tags=["employees"])
@api_handler
async def search_employees(data: SearchEmployee):
    """Returns the list of employees."""
    info = data.model_dump(exclude_unset=True)
    employees: List[models.Employee] = await SqlAlchemyRepository(db_manager.get_session,
                                                                  model=models.Employee).get_multi(unique=True)
    return transform(employees, EmployeeTransformer().include(["unit"]))


@router.get(path="/{employee_id}", response_model=Employee, tags=["employees"])
@api_handler
async def get_employee_by_id(employee: Employee = Depends(valid_employee_id)):
    """Returns employee with employee_id."""

    return transform(employee, EmployeeTransformer().include(["unit", "vacations", "business_trips"]))


@router.post(path="/", response_model=Employee, tags=["employees"])
@api_handler
async def create_employee(data: CreateEmployee):
    """Returns created with the given data employee."""

    employee: models.Employee = await SqlAlchemyRepository(db_manager.get_session,
                                                           model=models.Employee).create(data)
    return transform(employee, EmployeeTransformer())


@router.patch(path="/{employee_id}", response_model=Employee, tags=["employees"])
@api_handler
async def update_employee_by_id(data: UpdateEmployee,
                                employee: models.Employee = Depends(valid_employee_id)):
    """Returns updated with given data employee."""

    employee: models.Employee = await SqlAlchemyRepository(db_manager.get_session,
                                                           model=models.Employee).update(
        data=data,
        id=employee.id)
    return transform(employee, EmployeeTransformer())


@router.get(path="/{employee_id}/business_trips", response_model=List[BusinessTrip], tags=["employees"])
@api_handler
async def get_employee_business_trips(employee_id: int):
    business_trips: List[models.BusinessTrip] = await SqlAlchemyRepository(db_manager.get_session,
                                                                           model=models.BusinessTrip).get_multi(
        unique=True, employee_id=employee_id)
    return transform(business_trips, BusinessTripTransformer())


@router.get(path="/{employee_id}/vacations", response_model=List[Vacation], tags=["employees"])
@api_handler
async def get_employee_vacations(employee_id: int):
    vacations: List[models.Vacation] = await SqlAlchemyRepository(db_manager.get_session,
                                                                  model=models.Vacation).get_multi(
        unique=True, employee_id=employee_id)
    return transform(vacations, VacationTransformer())
