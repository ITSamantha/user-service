from src.apps.tasks import models
from src.core.dependencies import valid_id, is_deleted_model
from src.utils.handlers import api_handler

"""TASK"""


@api_handler
async def valid_task_id(task_id: int) -> models.Task:
    return await valid_id(task_id, models.Task, "Task")


@api_handler
async def existing_task(task_id: int) -> models.Task:
    return await is_deleted_model(task_id, models.Task, "Task")


"""PROJECT"""


@api_handler
async def valid_project_id(project_id: int) -> models.Project:
    return await valid_id(project_id, models.Project, "Project")


@api_handler
async def existing_project(project_id: int) -> models.Project:
    return await is_deleted_model(project_id, models.Project, "Project")
