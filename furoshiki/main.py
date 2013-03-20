from tasks import FabricInterface, dump_fabric_json
import json
import importlib
import functools
import logging
from flask import Flask
from flask import request

app = Flask(__name__)
app.debug = True
app.config.from_object('furoshiki.default_settings')
app.config.from_envvar('FUROSHIKI_SETTINGS', silent=True)

fi = FabricInterface(app.config['FABFILE_PATH'])

def get_notifier():
    if app.config.get('NOTIFIER_MODULE'):
        return importlib.import_module(app.config['NOTIFIER_MODULE'])

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
    return dump_fabric_json(fi.list_tasks())

@app.route('/execute/<tasks>', methods=['POST'])
@verify_api_key
def execute_task(tasks):
    out = []
    for task in tasks.split(","):
        logging.info("running {0}".format(task))
        out.append(fi.run_task(task, *request.form.get('args',[]), **request.form.get('kwargs',{})))
    notifier = get_notifier()
    notifier.notify("deployment task {0} finished successfully".format(tasks), app.config)
    return json.dumps(out)

if __name__ == '__main__':
    app.run(port=1234, host='0.0.0.0')
