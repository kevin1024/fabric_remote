import json
import importlib
import functools
from flask import request, Response, jsonify, abort
from furoshiki.auth import requires_auth
from furoshiki import executions, app
from furoshiki.tasks import dump_fabric_json


@app.route('/tasks', methods=['GET'])
@requires_auth
def get_task():
    return Response(dump_fabric_json(app.fi.list_tasks()), mimetype="application/json")

@app.route('/executions', methods=['POST'])
@requires_auth
def create_execution():
    tasks = request.json
    app.logger.info("got POST with tasks: {0}".format(tasks))
    ps_handle, stream = app.fi.run_tasks(tasks)
    execution_id = executions.add(tasks, ps_handle, stream)
    app.logger.info("creating execution for tasks {0}".format(tasks))
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

