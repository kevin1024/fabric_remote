from tasks import FabricInterface, dump_fabric_json
import json
import importlib
import functools
import logging
from flask import Flask
from flask import request

from furoshiki.auth import requires_auth

app = Flask(__name__)
app.debug = True
app.config.from_object('furoshiki.default_settings')
app.config.from_envvar('FUROSHIKI_SETTINGS', silent=True)

fi = FabricInterface(app.config['FABFILE_PATH'])

def get_notifier():
    if app.config.get('NOTIFIER_MODULE'):
        return importlib.import_module(app.config['NOTIFIER_MODULE'])

@app.route('/tasks', methods=['GET'])
@requires_auth
def get_task():
    return dump_fabric_json(fi.list_tasks())

@app.route('/execute/<tasks>', methods=['POST'])
@requires_auth
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
