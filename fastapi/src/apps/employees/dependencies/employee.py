from typing import Mapping

from src.apps.employees import models
from src.core.database.session_manager import db_manager
from src.utils.handlers import api_handler
from src.utils.repository.crud.base_crud_repository import SqlAlchemyRepository


@api_handler
async def valid_employee_id(employee_id: int) -> models.Employee:
    employee: models.Employee = await SqlAlchemyRepository(db_manager.get_session,
                                                           model=models.Employee).get_single(id=employee_id)

    if not employee:
        raise Exception("Employee with this data does not exist.")

    return employee


@api_handler
async def valid_employee_position_id(employee_position_id: int) -> models.EmployeePosition:
    employee_position: models.EmployeePosition = await SqlAlchemyRepository(db_manager.get_session,
                                                                            model=models.EmployeePosition).get_single(
        id=employee_position_id)

    if not employee_position:
        raise Exception("Employee position with this data does not exist.")

    return employee_position
