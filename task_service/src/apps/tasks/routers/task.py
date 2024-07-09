from typing import List

from fastapi import APIRouter, Depends

from src.apps.tasks import models
from src.apps.tasks.dependencies import valid_task_id
from src.apps.tasks.schemas.task import Task, CreateTask
from src.apps.tasks.transformers.task import TaskTransformer
from src.core.database.session_manager import db_manager
from src.utils.handlers import api_handler
from src.utils.repository.crud.base_crud_repository import SqlAlchemyRepository
from src.utils.transformer import transform

router: APIRouter = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

"""TASK"""


@router.get(path="", response_model=List[Task], tags=["tasks"])
@api_handler
async def get_tasks():
    """Returns the list of all tasks."""

    tasks: List[models.Task] = await SqlAlchemyRepository(db_manager.get_session,
                                                          model=models.Task).get_multi()
    return transform(tasks, TaskTransformer().include(["project"]))


@router.get(path="/{task_id}", response_model=Task, tags=["tasks"])
@api_handler
async def get_task_by_id(task: models.Task = Depends(valid_task_id)):
    """Returns task with id=task_id."""

    return transform(task, TaskTransformer().include(["project"]))


@router.post(path="", response_model=Task, tags=["tasks"])
@api_handler
async def create_task(data: CreateTask):
    """Returns created with the given data task."""

    task: models.Task = await SqlAlchemyRepository(db_manager.get_session,
                                                   model=models.Task).create(data=data)
    return transform(task, TaskTransformer())
