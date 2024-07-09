"""TASK"""
from src.apps.tasks import models
from src.core.dependencies import valid_id
from src.utils.handlers import api_handler


@api_handler
async def valid_task_id(task_id: int) -> models.Task:
    return await valid_id(task_id, models.Task, "Task")
