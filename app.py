from tasks import FabricInterface
from fabric.tasks import WrappedCallableTask
from fabric.utils import indent
import json
from flask import Flask, url_for
from flask.views import MethodView
from flask import request

app = Flask(__name__)
app.debug = True
app.config.from_object('default_settings')

fi = FabricInterface(app.config['FABFILE_PATH'])

class FabricEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, WrappedCallableTask):
            return {'name': obj.name, 'description': obj.__doc__ }
        return json.JSONEncoder.default(self, obj)


@app.route('/tasks', methods=['GET'])
def get_task():
    return json.dumps(fi.list_tasks(), cls=FabricEncoder)

@app.route('/execute/<task_name>', methods=['POST'])
def execute_task(task_name):
    params = request.form.get('params',[])
    print "running {0}".format(task_name)
    return json.dumps(fi.run_task(task_name, *request.form.get('args',[]), **request.form.get('kwargs',{})))
    

if __name__ == '__main__':
    app.run(port=1234, host='0.0.0.0')
