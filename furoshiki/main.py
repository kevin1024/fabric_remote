from tasks import FabricInterface
from fabric.tasks import WrappedCallableTask
import json
import importlib
import functools
from flask import Flask
from flask import request

app = Flask(__name__)
app.debug = True
app.config.from_object('furoshiki.default_settings')
app.config.from_envvar('FUROSHIKI_SETTINGS')

fi = FabricInterface(app.config['FABFILE_PATH'])

if 'NOTIFIER_MODULE' in app.config:
    notifier = importlib.import_module(app.config['NOTIFIER_MODULE'])
else:
    notifier = None

class FabricEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, WrappedCallableTask):
            return {'name': obj.name, 'description': obj.__doc__ }
        return json.JSONEncoder.default(self, obj)

def verify_api_key(wrapped):
    @functools.wraps(wrapped)
    def inner(*args, **kwargs):
        if request.form.get('api_key','') != app.config['API_KEY']:
            return 'incorrect api key'
        return wrapped(*args, **kwargs)
    return inner


@app.route('/tasks', methods=['GET'])
@verify_api_key
def get_task():
    return json.dumps(fi.list_tasks(), cls=FabricEncoder)

@app.route('/execute/<tasks>', methods=['POST'])
@verify_api_key
def execute_task(tasks):
    out = ""
    params = request.form.get('params',{})
    for task in tasks.split(","):
        print "running {0}".format(task)
        out += json.dumps(fi.run_task(task, *request.form.get('args',[]), **request.form.get('kwargs',{})))
    if notifier:
        notifier.notify("deployment task {0} finished successfully".format(tasks), app.config)
    return out

if __name__ == '__main__':
    app.run(port=1234, host='0.0.0.0')
