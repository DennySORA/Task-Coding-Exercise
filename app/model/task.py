
from typing import Optional

from database.task import TaskDatabase
from common.struct import TaskStruct

from common.logs import error_gather


class Task:

    def __init__(self):
        self.task_database = TaskDatabase()

    @error_gather
    def get_task(self, task_id:int) -> Optional[TaskStruct]:
        task_with_declarative = self.task_database.get_task(task_id)
        if task_with_declarative is None:
            return None
        return TaskStruct.from_orm(task_with_declarative)

    @error_gather
    def get_all_tasks(self, is_dict=True) -> list[TaskStruct | dict]:
        task_with_declarative = self.task_database.get_all_task()
        task_with_struct = [TaskStruct.from_orm(
            i) for i in task_with_declarative]
        if is_dict:
            return [i.dict() for i in task_with_struct]
        return task_with_struct

    @error_gather
    def add_task(self, task_with_struct: TaskStruct) -> TaskStruct:
        task_with_struct.id = self.task_database.add_task(task_with_struct)
        return task_with_struct

    @error_gather
    def update_task(self, task_id: int, task_with_struct: TaskStruct) -> Optional[TaskStruct]:
        task_with_declarative = self.task_database.get_task(task_id)
        if task_with_declarative is None:
            return None
        task_with_declarative.name = task_with_struct.name
        task_with_declarative.status = task_with_struct.status
        task_update_result_with_declarative = self.task_database.update_task(task_with_declarative)
        return TaskStruct.from_orm(task_update_result_with_declarative)

    @error_gather
    def delete_task(self, task_id: int):
        task_with_declarative = self.task_database.get_task(task_id)
        if task_with_declarative is None:
            return None
        self.task_database.delete_task(task_with_declarative)
