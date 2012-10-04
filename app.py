from tasks import FabricInterface
from fabric.tasks import WrappedCallableTask
import json
from flask import Flask, url_for
from flask.views import MethodView

app = Flask(__name__)
app.debug = True
app.config.from_object('default_settings')

fi = FabricInterface(app.config['FABFILE_PATH'])

class FabricEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, WrappedCallableTask):
            return obj.name
        return json.JSONEncoder.default(self, obj)


@app.route('/tasks/')
def get_task():
    return json.dumps(fi.list_tasks(), cls=FabricEncoder)

@app.route('/execute/<task_name>')
def execute_task(task_name):
    return json.dumps(fi.run_task(task_name))
    

if __name__ == '__main__':
    app.run()
