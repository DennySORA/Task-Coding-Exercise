
import pytest

from app.database.task import TaskDatabase
from app.database.declarative import drop_all_table,create_table
from app.common.struct import TaskStruct

def test_insert_get_all_task():
    task_database = TaskDatabase()
    drop_all_table(task_database.database_context.engine)
    create_table(task_database.database_context.engine)
    for i in [("買晚餐", 0),("買早餐", 1),("不想吃飯", 0)]:
        task = TaskStruct(name=i[0], status=i[1])
        task_database.add_task(task)
    assert len(task_database.get_all_task()) == 3

@pytest.mark.parametrize('name, status', [
    ("買晚餐", 0),
    ("買早餐", 1),
    ("不想吃飯", 0),
])
def test_insert_get_task(name: str, status: int):
    task_database = TaskDatabase()
    task = TaskStruct(name=name, status=status)
    uid = task_database.add_task(task)
    task.id = uid
    assert TaskStruct.from_orm(task_database.get_task(uid)) == task

@pytest.mark.parametrize('name, status', [
    ("買晚餐", 0),
    ("買早餐", 1),
    ("不想吃飯", 0),
])
def test_insert_delete_task(name: str, status: int):
    task_database = TaskDatabase()
    task = TaskStruct(name=name, status=status)
    uid = task_database.add_task(task)
    task_in_database = task_database.get_task(uid)
    if not task_in_database:
        raise Exception('Task not found')
    task_database.delete_task(task_in_database)
    assert task_database.get_task(uid) is None

@pytest.mark.parametrize('name, status, new_name, new_status', [
    ("買晚餐", 0,"晚餐",0),
    ("買早餐", 1,"買早餐",0),
    ("不想吃飯", 0,"不吃飯",1),
    ("不吃飯", 0,"不吃飯",0),
])
def test_insert_update_task(name: str, status: int,new_name: str, new_status: int):
    task_database = TaskDatabase()
    task = TaskStruct(name=name, status=status)
    uid = task_database.add_task(task)
    task_in_database = task_database.get_task(uid)
    assert task_in_database is not None
    task.id = uid
    assert TaskStruct.from_orm(task_in_database) == task

    new_task = TaskStruct(name=new_name, status=new_status)
    task_in_database.name = new_task.name
    task_in_database.status = new_task.status
    task_database.update_task(task_in_database)
    new_task_in_database = task_database.get_task(uid)
    new_task.id = uid
    assert TaskStruct.from_orm(new_task_in_database) == new_task