from src.apps.employees import models
from src.core.dependencies import valid_id
from src.utils.handlers import api_handler


@api_handler
async def valid_vacation_id(vacation_id: int) -> models.Vacation:
    return await valid_id(vacation_id, models.Vacation, "Vacation")


@api_handler
async def valid_vacation_reason_id(vacation_reason_id: int) -> models.VacationReason:
    return await valid_id(vacation_reason_id, models.VacationReason, "Vacation reason")


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
