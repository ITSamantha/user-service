import os
from typing import List

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Depends

from src.apps.tasks import models
from src.apps.tasks.dependencies import valid_task_id, existing_task, existing_project
from src.apps.tasks.repository.task_repository import TaskRepository
from src.apps.tasks.schemas.task import Task, CreateTask, UpdateTask, AssignEmployeeTask, AssignableEmployee
from src.apps.tasks.transformers.task import TaskTransformer
from src.core.database.session_manager import db_manager
from src.core.schemas.base import BaseDeleteSchema
from src.utils.handlers import api_handler
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

    tasks: List[models.Task] = await TaskRepository(db_manager.get_session,
                                                    model=models.Task).get_multi()
    return transform(tasks, TaskTransformer().include(["project", "task_status"]))


@router.get(path="/search", response_model=List[Task], tags=["tasks", "search"])
@api_handler
async def search_tasks(title: str = None, description: str = None) -> List[Task]:
    """Returns the list of tasks."""

    tasks: List[models.Task] = await TaskRepository(db_manager.get_session,
                                                    model=models.Task).search(title=title,
                                                                              description=description,
                                                                              unique=True)
    return transform(tasks, TaskTransformer().include(["project", "task_status"]))


@router.get(path="/{task_id}", response_model=Task, tags=["tasks"])
@api_handler
async def get_task_by_id(task: models.Task = Depends(valid_task_id)):
    """Returns task with id=task_id."""

    return transform(task, TaskTransformer().include(["project", "task_status"]))


@router.post(path="", response_model=Task, tags=["tasks"])
@api_handler
async def create_task(data: CreateTask):
    """Returns created with the given data task."""

    await existing_project(project_id=data.project_id)

    task: models.Task = await TaskRepository(db_manager.get_session,
                                             model=models.Task).create(data=data)
    return transform(task, TaskTransformer())


@router.patch(path="/{task_id}", response_model=Task, tags=["tasks"])
@api_handler
async def update_task_by_id(task_id: int, data: UpdateTask) -> Task:
    """Returns updated with given data task."""

    # await existing_project(project_id=data.project_id)

    task: models.Task = await TaskRepository(db_manager.get_session,
                                             model=models.Task).update(
        data=data,
        id=task_id)
    return transform(task, TaskTransformer())


@router.delete(path="/{task_id}", response_model=Task, tags=["tasks"])
@api_handler
async def delete_task(task: models.Task = Depends(existing_task)) -> Task:
    """Returns deleted task."""

    task: models.Task = await TaskRepository(db_manager.get_session,
                                             model=models.Task).update(
        data=BaseDeleteSchema(),
        id=task.id)
    return transform(task, TaskTransformer())


@router.patch(path="/{task_id}/assign", response_model=Task, tags=["tasks"])
@api_handler
async def assign_task(data: AssignEmployeeTask, task: models.Task = Depends(existing_task)) -> Task:
    """Returns updated with assignment task."""

    params = {
        "director_id": 1
    }

    load_dotenv()

    if data.assigned_employee_id:
        host: str = os.getenv("USERSERVICE_HOST")
        port: str = os.getenv("USERSERVICE_PORT")

        try:
            response = requests.get(f'http://{host}:{port}/employees/{data.assigned_employee_id}/assignable',
                                    params=params)
        except Exception as e:
            raise Exception("Произошла ошибка.")

        response_data = response.json()

        if response.status_code == 200:

            is_employee_assignable: bool = response_data["is_employee_assignable"]

            if not is_employee_assignable:
                raise Exception("Условия назначения сотрудника не выполнены. "
                                "Возможно, вы пытаетесь назначить сотрудника не своего отдела на задачу.")
        else:
            raise Exception(response_data["detail"])

    task: models.Task = await TaskRepository(db_manager.get_session,
                                             model=models.Task).update(
        data=data,
        id=task.id)
    return transform(task, TaskTransformer())
