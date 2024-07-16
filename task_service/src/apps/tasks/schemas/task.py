import datetime
from typing import Optional

from pydantic import Field

from src.apps.tasks import models
from src.core.schemas.base import BaseResponseSchemaModel, BaseSchemaModel

""" TASK STATUS """


class TaskStatus(BaseResponseSchemaModel):
    id: int

    title: str = Field(min_length=1, max_length=128)


class CreateTaskStatus(BaseSchemaModel):
    title: str = Field(min_length=1, max_length=128)


class UpdateTaskStatus(CreateTaskStatus):
    pass


""" TASK """


class Task(BaseResponseSchemaModel):
    id: int

    title: str = Field(min_length=1, max_length=128)
    description: Optional[str] = Field(default=None, min_length=1)

    assigned_employee_id: Optional[int] = Field(default=None)

    expected_completion_date: datetime.datetime
    actual_completion_date: Optional[datetime.datetime]

    hours_spent: Optional[int]

    # project: Project
    # task_status: TaskStatus

    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]


class CreateTask(BaseSchemaModel):
    title: str = Field(min_length=1, max_length=128)
    description: Optional[str] = Field(default=None, min_length=1)

    expected_completion_date: datetime.datetime
    actual_completion_date: Optional[datetime.datetime] = Field(default=None)

    task_status_id: int = Field(default=models.TaskStatus.IN_PROCESS)

    hours_spent: int = Field(default=0)

    assigned_employee_id: Optional[int] = Field(default=None)

    project_id: int


class UpdateTask(BaseSchemaModel):
    title: str = Field(min_length=1, max_length=128)
    description: Optional[str] = Field(default=None, min_length=1)

    task_status_id: int = Field(default=models.TaskStatus.IN_PROCESS)

    hours_spent: int = Field(default=0)

    expected_completion_date: datetime.datetime
    actual_completion_date: Optional[datetime.datetime] = Field(default=None)

    project_id: int


class AssignEmployeeTask(BaseSchemaModel):
    assigned_employee_id: Optional[int] = Field(default=None)


class AssignableEmployee(BaseResponseSchemaModel):
    is_employee_assignable: bool
