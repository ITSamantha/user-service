from src.apps.tasks.models import TaskStatus
from src.core.database.seeders.generic_seeder import GenericSeeder


class TaskStatusSeeder(GenericSeeder):
    def __init__(self):
        super().__init__()
        self.initial_data = {
            TaskStatus: {
                TaskStatus.DONE: {"title": "Выполнена"},
                TaskStatus.IN_PROCESS: {"title": "Не выполнена (в процессе)"}
            }
        }
