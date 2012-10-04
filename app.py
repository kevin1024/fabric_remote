from tasks import list_tasks, run_task
from fabric.tasks import WrappedCallableTask
import json
from flask import Flask, url_for
from flask.views import MethodView

class FabricEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, WrappedCallableTask):
            return obj.name
        return json.JSONEncoder.default(self, obj)

app = Flask(__name__)

@app.route('/tasks/')
def get_task():
    task_list = list_tasks()
    return json.dumps(task_list, cls=FabricEncoder)

@app.route('/execute/<task_name>')
def execute_task(task_name):
    return json.dumps(run_task(task_name))
    

if __name__ == '__main__':
    app.debug = True
    app.run()
