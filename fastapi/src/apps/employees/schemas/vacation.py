import datetime
from typing import Optional

from src.core.schemas.base import BaseSchemaModel


class CreateVacationReason(BaseSchemaModel):
    title: str


class UpdateVacationReason(BaseSchemaModel):
    title: str


class VacationReason(BaseSchemaModel):
    id: int
    title: str


class CreateVacationType(BaseSchemaModel):
    title: str


class UpdateVacationType(BaseSchemaModel):
    title: str


class VacationType(BaseSchemaModel):
    id: int
    title: str


class CreateVacation(BaseSchemaModel):
    vacation_type_id: int

    employee_id: int

    start_date: datetime.date
    end_date: datetime.date

    reason: str


class UpdateVacation(BaseSchemaModel):
    pass


class Vacation(BaseSchemaModel):
    id: int

    vacation_type: VacationType
    employee: "Employee"

    start_date: datetime.date
    end_date: datetime.date

    vacation_reason: VacationReason

    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]
