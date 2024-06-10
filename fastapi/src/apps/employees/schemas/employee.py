import datetime
from typing import Optional

from pydantic import Field, EmailStr

from src.core.schemas.base import BaseSchemaModel, BaseResponseSchemaModel


class CreateEmployeePosition(BaseSchemaModel):
    title: str = Field(max_length=256)


class UpdateEmployeePosition(CreateEmployeePosition):
    pass


class EmployeePosition(BaseResponseSchemaModel):
    id: int
    title: str


class CreateUnit(BaseSchemaModel):
    title: str

    director_id: Optional[int] = None


class UpdateUnit(BaseSchemaModel):
    title: str

    director_id: Optional[int] = None


class Unit(BaseResponseSchemaModel):
    id: int
    title: str

    # director: Optional["Employee"] = Field( default=None)
    # employees: Optional[List["Employee"]] = Field(exclude=True, default=None)


class CreateEmployee(BaseSchemaModel):
    last_name: str = Field()
    first_name: str
    patronymic: Optional[str] = None

    login: str
    password: str = Field(max_length=16, min_length=8)
    email: EmailStr

    unit_id: int
    position_id: int


class UpdateEmployee(BaseSchemaModel):
    last_name: str
    first_name: str
    patronymic: Optional[str] = None

    login: str

    email: EmailStr

    unit_id: int
    position_id: int


class Employee(BaseResponseSchemaModel):
    id: int

    last_name: str
    first_name: str
    patronymic: Optional[str] = None

    login: str
    email: EmailStr

    # unit: Optional[Unit]

    # position: Optional[EmployeePosition]

    # vacations: Optional[List[Vacation]]
    # business_trips: Optional[List[BusinessTrip]]

    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]
