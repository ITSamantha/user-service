import datetime
from typing import Optional

from pydantic import Field

from src.core.schemas.base import BaseSchemaModel, BaseResponseSchemaModel


class CreateBusinessTrip(BaseSchemaModel):
    employee_id: int

    start_date: datetime.date
    end_date: datetime.date

    purpose: str = Field(min_length=2)

    destination: str = Field(min_length=2)

    comment: Optional[str] = Field(min_length=2, default=None)


class UpdateBusinessTrip(BaseSchemaModel):
    start_date: datetime.date
    end_date: datetime.date

    purpose: str = Field(min_length=2)

    destination: str = Field(min_length=2)

    comment: Optional[str] = Field(min_length=2, default=None)


class BusinessTrip(BaseResponseSchemaModel):
    id: int

    start_date: datetime.date
    end_date: datetime.date

    purpose: str
    destination: str

    comment: Optional[str] = None

    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]
