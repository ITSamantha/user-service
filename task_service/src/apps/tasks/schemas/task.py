import datetime
from typing import Optional

from pydantic import Field

from src.core.schemas.base import BaseResponseSchemaModel, BaseSchemaModel


class Task(BaseResponseSchemaModel):
    id: int

    title: str = Field(min_length=1, max_length=128)
    description: Optional[str] = Field(default=None, min_length=1)

    assigned_employee_id: Optional[int] = Field(default=None)

    # project: Project

    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]


class CreateTask(BaseSchemaModel):
    title: str = Field(min_length=1, max_length=128)
    description: Optional[str] = Field(default=None, min_length=1)

    assigned_employee_id: Optional[int] = Field(default=None)

    project_id: int


class UpdateTask(BaseSchemaModel):
    title: str = Field(min_length=1, max_length=128)
    description: Optional[str] = Field(default=None, min_length=1)

    project_id: int


class AssignEmployeeTask(BaseSchemaModel):
    assigned_employee_id: Optional[int] = Field(default=None)
