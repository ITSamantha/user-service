from src.apps.tasks import models
from src.apps.tasks.schemas.project import Project
from src.apps.tasks.transformers.task import TaskTransformer
from src.utils.transformer import BaseTransformer


class ProjectTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()
        self.available_includes = [
            "tasks"
        ]
        self.default_includes = []

    def transform(self, project: models.Project):
        return Project(
            id=project.id,
            title=project.title,
            created_at=project.created_at,
            updated_at=project.updated_at,
            deleted_at=project.deleted_at
        )

    def include_tasks(self, project: models.Project):
        return self.collection(project.tasks, TaskTransformer())
