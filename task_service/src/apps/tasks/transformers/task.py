from src.apps.tasks import models
from src.apps.tasks.schemas.task import Task
from src.apps.tasks.transformers.project import ProjectTransformer
from src.utils.transformer import BaseTransformer


class TaskTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()
        self.available_includes = [
            "project"
        ]
        self.default_includes = []

    def transform(self, task: models.Task):
        return Task(
            id=task.id,
            title=task.title,
            description=task.description,
            assigned_employee_id=task.assigned_employee_id,
            created_at=task.created_at,
            updated_at=task.updated_at,
            deleted_at=task.deleted_at
        )

    def include_project(self, task: models.Task):
        return self.item(task.project, ProjectTransformer())
