
from typing import Optional

from common.struct import TaskStruct

from .context import SQLiteContext
from .declarative import TaskDeclarative


class TaskDatabase:

    def __init__(self) -> None:
        self.database_context = SQLiteContext()

    def _get_all_tasks_with_database(self) -> list[TaskDeclarative]:
        with self.database_context as cursor:
            result = cursor.query(TaskDeclarative).all()
            cursor.expunge_all()
        return result

    def _get_tasks_with_database(self, task_id: int) -> Optional[TaskDeclarative]:
        with self.database_context as cursor:
            result = cursor.query(TaskDeclarative).filter(
                TaskDeclarative.id == task_id
            ).one_or_none()
            cursor.expunge_all()
        return result

    def _insert_task_with_database(self, task: TaskDeclarative) -> int:
        with self.database_context as cursor:
            cursor.add(task)
            cursor.commit()
            cursor.refresh(task)
            return task.id

    def _update_task_with_database(self, task: TaskDeclarative):
        with self.database_context as cursor:
            result = cursor.query(TaskDeclarative).filter(
                TaskDeclarative.id == task.id
            ).one_or_none()
            result.name = task.name
            result.status = task.status

    def _delete_task_with_database(self, task: TaskDeclarative):
        with self.database_context as cursor:
            cursor.delete(task)

    def get_task(self, task_id: int) -> Optional[TaskDeclarative]:
        return self._get_tasks_with_database(task_id)

    def get_all_task(self) -> list[TaskDeclarative]:
        return self._get_all_tasks_with_database()

    def add_task(self, task: TaskStruct) -> int:
        return self._insert_task_with_database(
            TaskDeclarative(**task.dict())
        )

    def update_task(self, task: TaskDeclarative) -> TaskDeclarative:
        self._update_task_with_database(task)
        result = self._get_tasks_with_database(task.id)
        if result:
            return result
        raise ValueError('Task not found.') 

    def delete_task(self, task: TaskDeclarative):
        self._delete_task_with_database(task)
