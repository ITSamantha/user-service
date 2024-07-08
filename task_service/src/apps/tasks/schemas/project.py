import datetime
from typing import Optional

from pydantic import Field

from src.core.schemas.base import BaseResponseSchemaModel, BaseSchemaModel


class Project(BaseResponseSchemaModel):
    id: int

    title: str = Field(min_length=2, max_length=128)

    # tasks: List[Task]

    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]


class CreateProject(BaseSchemaModel):
    title: str = Field(min_length=2, max_length=128)


class UpdateProject(CreateProject):
    pass
