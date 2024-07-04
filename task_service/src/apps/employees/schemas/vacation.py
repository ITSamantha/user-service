import datetime
from typing import Optional

from pydantic import Field

from src.core.schemas.base import BaseSchemaModel, BaseResponseSchemaModel


class CreateVacationReason(BaseSchemaModel):
    title: str = Field(min_length=2)


class UpdateVacationReason(CreateVacationReason):
    pass


class VacationReason(BaseSchemaModel):
    id: int
    title: str


class CreateVacationType(BaseSchemaModel):
    title: str = Field(min_length=2)


class UpdateVacationType(CreateVacationType):
    pass


class VacationType(BaseSchemaModel):
    id: int
    title: str


class CreateVacation(BaseSchemaModel):
    vacation_type_id: int
    vacation_reason_id: int

    employee_id: int

    start_date: datetime.date
    end_date: datetime.date

    comment: Optional[str] = Field(min_length=2, default=None)


class UpdateVacation(BaseSchemaModel):
    vacation_type_id: int
    vacation_reason_id: int

    start_date: datetime.date
    end_date: datetime.date

    comment: Optional[str] = Field(min_length=2, default=None)


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
