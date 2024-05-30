from src.apps.employees import models
from src.apps.employees.schemas.business_trip import CreateBusinessTrip
from src.apps.employees.schemas.vacation import CreateVacation
from src.core.dependencies import valid_id, valid_dates
from src.utils.handlers import api_handler


@api_handler
async def valid_vacation_id(vacation_id: int) -> models.Vacation:
    return await valid_id(vacation_id, models.Vacation, "Vacation")


@api_handler
async def valid_vacation_reason_id(vacation_reason_id: int) -> models.VacationReason:
    return await valid_id(vacation_reason_id, models.VacationReason, "Vacation reason")


@api_handler
async def valid_vacation_type_id(vacation_type_id: int) -> models.VacationType:
    return await valid_id(vacation_type_id, models.VacationReason, "Vacation type")


@api_handler
async def valid_employee_id(employee_id: int) -> models.Employee:
    return await valid_id(employee_id, models.Employee, "Employee")


@api_handler
async def valid_unit_id(unit_id: int) -> models.Unit:
    return await valid_id(unit_id, models.Unit, "Unit")


@api_handler
async def valid_employee_position_id(employee_position_id: int) -> models.EmployeePosition:
    return await valid_id(employee_position_id, models.EmployeePosition, "Employee position")


@api_handler
async def valid_business_trip_id(business_trip_id: int) -> models.BusinessTrip:
    return await valid_id(business_trip_id, models.BusinessTrip, "Business trip")


@api_handler
async def valid_employee_business_trip(data: CreateBusinessTrip):
    return await valid_dates(data)


@api_handler
async def valid_employee_vacation(data: CreateVacation):
    return await valid_dates(data)
