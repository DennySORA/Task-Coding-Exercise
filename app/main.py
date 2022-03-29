
from flask import Flask, request

from model.task import Task
from common.struct import TaskStruct

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.get('/tasks')
def get_tasks():
    try:
        result = Task().get_all_tasks(is_dict=True)
        return {"result": result}
    except:
        return {"result": 'Task Get Failed.'}, 500


@app.post('/task')
def post_task():
    body = request.get_json()
    if body is None:
        return {"result": 'Need json body'}, 400

    try:
        task_with_struct = TaskStruct(**body, status=0)
    except:
        return {"result": 'Key name not exist.'}, 400

    try:
        result_task_with_struct = Task().add_task(task_with_struct)
        return {"result": result_task_with_struct.dict()}
    except:
        return {"result": 'Task Add Failed.'}, 500


@app.put('/task/<task_id>')
def put_task(task_id: str):
    body = request.get_json()
    if body is None:
        return {"result": 'Need json body'}, 400

    try:
        task_with_struct = TaskStruct(**body)
    except:
        return {"result": 'Data incomplete.'}, 400

    try:
        result_task_with_struct = Task().update_task(int(task_id), task_with_struct)
        if result_task_with_struct is None:
            return {"result": 'Task task id not exist'}, 400
        return {"result": result_task_with_struct.dict()}
    except:
        return {"result": 'Task Update Failed.'}, 500


@app.delete('/task/<task_id>')
def delete_task(task_id: str):
    try:
        Task().delete_task(int(task_id))
        return ''
    except:
        return {"result": 'Task Delete Failed.'}, 500
