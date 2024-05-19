import datetime
from typing import Optional, List

from pydantic import Field

from src.apps.employees.schemas.business_trip import BusinessTrip
from src.apps.employees.schemas.vacation import Vacation
from src.core.schemas.base import BaseSchemaModel


class CreateEmployeePosition(BaseSchemaModel):
    title: str


class UpdateEmployeePosition(CreateEmployeePosition):
    pass


class EmployeePosition(BaseSchemaModel):
    id: int
    title: str


class CreateUnit(BaseSchemaModel):
    title: str

    director_id: Optional[int] = None


class UpdateUnit(BaseSchemaModel):
    # TODO: change
    title: Optional[str] = None
    director_id: Optional[int] = None


class Unit(BaseSchemaModel):
    id: int
    title: str

    director: Optional["Employee"]

    employees: List["Employee"]


class CreateEmployee(BaseSchemaModel):
    last_name: str = Field()
    first_name: str
    patronymic: Optional[str]

    login: str
    password: str
    email: str

    unit_id: int
    position_id: int


class UpdateEmployee(BaseSchemaModel):
    pass


class Employee(BaseSchemaModel):
    id: int

    last_name: str
    first_name: str
    patronymic: str

    login: str
    email: str

    unit: Unit

    position: EmployeePosition

    vacations: List[Vacation]
    business_trips: List[BusinessTrip]

    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]
