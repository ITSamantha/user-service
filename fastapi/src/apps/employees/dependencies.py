from typing import TypeVar

from fastapi import Depends

from src.apps.employees import models
from src.apps.employees.schemas.business_trip import CreateBusinessTrip, UpdateBusinessTrip
from src.apps.employees.schemas.vacation import CreateVacation, UpdateVacation
from src.core.dependencies import valid_id, valid_dates, is_deleted_model
from src.core.schemas.base import BaseSchemaModel
from src.utils.handlers import api_handler

"""VACATION"""


@api_handler
async def valid_vacation_id(vacation_id: int) -> models.Vacation:
    return await valid_id(vacation_id, models.Vacation, "Vacation")


@api_handler
async def existing_vacation(vacation_id: int) -> models.Vacation:
    return await is_deleted_model(vacation_id, models.Vacation, "Vacation")


"""VACATION REASON"""


@api_handler
async def valid_vacation_reason_id(vacation_reason_id: int) -> models.VacationReason:
    return await valid_id(vacation_reason_id, models.VacationReason, "Vacation reason")


"""VACATION TYPE"""


@api_handler
async def valid_vacation_type_id(vacation_type_id: int) -> models.VacationType:
    return await valid_id(vacation_type_id, models.VacationType, "Vacation type")


"""BUSINESS TRIP"""


@api_handler
async def valid_business_trip_id(business_trip_id: int) -> models.BusinessTrip:
    return await valid_id(business_trip_id, models.BusinessTrip, "Business trip")


@api_handler
async def existing_business_trip(business_trip_id: int) -> models.BusinessTrip:
    return await is_deleted_model(business_trip_id, models.BusinessTrip, "Business trip")


"""EMPLOYEE"""


@api_handler
async def valid_employee_id(employee_id: int) -> models.Employee:
    return await valid_id(employee_id, models.Employee, "Employee")


@api_handler
async def existing_employee(employee_id: int) -> models.Employee:
    return await is_deleted_model(employee_id, models.Employee, "Employee")


@api_handler
async def valid_create_employee_business_trip(data: CreateBusinessTrip | UpdateBusinessTrip):
    return await valid_dates(data, employee_id=data.employee_id, object_id=None)


@api_handler
async def valid_create_employee_vacation(data: CreateBusinessTrip):
    return await valid_dates(data, employee_id=data.employee_id, object_id=None)


@api_handler
async def valid_update_employee_business_trip(data: UpdateBusinessTrip, business_trip_id: int,
                                              business_trip: models.BusinessTrip = Depends(
                                                  existing_business_trip)):
    return await valid_dates(data, employee_id=business_trip.employee_id, object_id=business_trip_id)


@api_handler
async def valid_create_employee_vacation(data: CreateVacation):
    return await valid_dates(data, employee_id=data.employee_id, object_id=None)


@api_handler
async def valid_update_employee_vacation(data: UpdateVacation, vacation_id: int,
                                         vacation: models.Vacation = Depends(
                                             existing_vacation)):
    return await valid_dates(data, employee_id=vacation.employee_id, object_id=vacation_id)


"""UNIT"""


@api_handler
async def valid_unit_id(unit_id: int) -> models.Unit:
    return await valid_id(unit_id, models.Unit, "Unit")


"""EMPLOYEE POSITION"""


@api_handler
async def valid_employee_position_id(employee_position_id: int) -> models.EmployeePosition:
    return await valid_id(employee_position_id, models.EmployeePosition, "Employee position")
