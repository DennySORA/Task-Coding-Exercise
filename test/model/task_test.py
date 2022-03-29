
import pytest

from app.database.declarative import drop_all_table, create_table
from app.common.struct import TaskStruct
from app.model.task import Task


def test_insert_get_all_task():
    task = Task()
    drop_all_table(task.task_database.database_context.engine)
    create_table(task.task_database.database_context.engine)
    for i in [("買晚餐", 0), ("買早餐", 1), ("不想吃飯", 0)]:
        Task().add_task(TaskStruct(name=i[0], status=i[1]))
    assert len(Task().get_all_tasks(is_dict=True)) == 3


@pytest.mark.parametrize('name, status', [
    ("買晚餐", 0),
    ("買早餐", 1),
    ("不想吃飯", 0),
])
def test_insert_get_task(name: str, status: int):
    task = TaskStruct(name=name, status=status)
    task.id = Task().add_task(task).id
    assert task.id is not None
    assert Task().get_task(task.id) == task


@pytest.mark.parametrize('name, status', [
    ("買晚餐", 0),
    ("買早餐", 1),
    ("不想吃飯", 0),
])
def test_insert_delete_task(name: str, status: int):
    task = TaskStruct(name=name, status=status)
    task.id = Task().add_task(task).id
    assert task.id is not None
    assert Task().get_task(task.id) == task
    Task().delete_task(task.id)
    assert Task().get_task(task.id) is None


@pytest.mark.parametrize('name, status, new_name, new_status', [
    ("買晚餐", 0, "晚餐", 0),
    ("買早餐", 1, "買早餐", 0),
    ("不想吃飯", 0, "不吃飯", 1),
    ("不吃飯", 0, "不吃飯", 0),
])
def test_insert_update_task(name: str, status: int, new_name: str, new_status: int):
    task = TaskStruct(name=name, status=status)
    task.id = Task().add_task(task).id
    assert task.id is not None
    assert Task().get_task(task.id) == task

    new_task = TaskStruct(id=task.id, name=new_name, status=new_status)
    Task().update_task(task.id, new_task)
    assert Task().get_task(task.id) == new_task
