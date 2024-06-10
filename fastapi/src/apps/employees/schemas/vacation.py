import datetime
from typing import Optional, Annotated

from pydantic import Field

from src.core.schemas.base import BaseSchemaModel, BaseResponseSchemaModel


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
    vacation_reason_id: int

    employee_id: int

    start_date: datetime.date
    end_date: datetime.date

    comment: Optional[str] = None


class UpdateVacation(BaseSchemaModel):
    vacation_type_id: int
    vacation_reason_id: int

    start_date: datetime.date
    end_date: datetime.date

    comment: Optional[str] = None


class Vacation(BaseResponseSchemaModel):
    id: int

    # vacation_type: VacationType
    # employee: "Employee"
    # vacation_reason: VacationReason

    start_date: datetime.date
    end_date: datetime.date

    comment: Optional[str]

    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]
