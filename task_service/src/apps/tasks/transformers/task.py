from src.apps.tasks import models
from src.apps.tasks.schemas.task import Task, TaskStatus
from src.apps.tasks.transformers.project import ProjectTransformer
from src.utils.transformer import BaseTransformer


class TaskStatusTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()
        self.available_includes = []
        self.default_includes = []

    def transform(self, task_status: models.TaskStatus):
        return TaskStatus(
            id=task_status.id,
            title=task_status.title
        )


class TaskTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()
        self.available_includes = [
            "project",
            "task_status"
        ]
        self.default_includes = []

    def transform(self, task: models.Task):
        return Task(
            id=task.id,
            title=task.title,
            description=task.description,
            assigned_employee_id=task.assigned_employee_id,
            expected_completion_date=task.expected_completion_date,
            actual_completion_date=task.actual_completion_date,
            hours_spent=task.hours_spent,
            created_at=task.created_at,
            updated_at=task.updated_at,
            deleted_at=task.deleted_at
        )

    def include_project(self, task: models.Task):
        return self.item(task.project, ProjectTransformer())

    def include_task_status(self, task: models.Task):
        return self.item(task.task_status, TaskStatusTransformer())
