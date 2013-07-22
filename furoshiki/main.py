from tasks import FabricInterface, dump_fabric_json
import json
import importlib
import functools
import logging
from flask import Flask
from flask import request, Response, jsonify, abort

from furoshiki.auth import requires_auth
from furoshiki import executions

app = Flask(__name__)
app.debug = True
app.config.from_object('furoshiki.default_settings')
app.config.from_envvar('FUROSHIKI_SETTINGS', silent=True)

fi = FabricInterface(app.config['FABFILE_PATH'])

@app.route('/tasks', methods=['GET'])
@requires_auth
def get_task():
    return dump_fabric_json(fi.list_tasks())

@app.route('/executions', methods=['POST'])
@requires_auth
def create_execution():
    tasks = request.json
    execution_id = executions.add(tasks, fi.run_tasks(tasks))
    logging.info("creating execution for tasks {0}".format(tasks))
    return jsonify({
        "status": "/executions/{0}/status".format(execution_id), 
        "output": "/executions/{0}/output".format(execution_id) 
    })

@app.route('/executions/<execution_id>/output', methods=['GET'])
@requires_auth
def execution_output(execution_id):
    try:
        ex = executions.get(int(execution_id))
    except KeyError:
        abort(404)

    def generate(ex):
        for line in ex['stream'].output():
            yield str(line)
    return Response(generate(ex), mimetype="text/plain")

@app.route('/executions/<execution_id>/results', methods=['GET'])
@requires_auth
def execution_results(execution_id):
    try:
        ex = executions.get(int(execution_id))
    except KeyError:
        abort(404)

    return jsonify(ex["stream"].results())

if __name__ == '__main__':
    app.run(port=1234, host='0.0.0.0')
