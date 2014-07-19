import json
import importlib
import functools
from flask import request, Response, jsonify, abort
from . import executions, app
from .auth import requires_auth
from .cors import cors
from .tasks import dump_fabric_json


@app.route('/tasks', methods=['GET', 'OPTIONS'])
@requires_auth
@cors
def get_task():
    return Response(
        dump_fabric_json(app.fi.list_tasks()), mimetype="application/json"
    )


@app.route('/executions', methods=['GET', 'OPTIONS'])
@requires_auth
@cors
def list_executions():
    exs = executions.all()
    return Response(json.dumps(exs), mimetype='application/json')


@app.route('/executions', methods=['POST'])
@requires_auth
@cors
def create_execution():
    tasks = request.get_json(force=True)
    if not tasks:
        abort(400, "Please give a task to execute")
    app.logger.info("got POST with tasks: {0}".format(tasks))
    ps_handle, stream = app.fi.run_tasks(tasks)
    execution_id = executions.add(tasks, ps_handle, stream)
    app.logger.info("creating execution for tasks {0}".format(tasks))
    return jsonify({
        "results": "/executions/{0}/results".format(execution_id),
        "output": "/executions/{0}/output".format(execution_id)
    }), 202


@app.route('/executions/<execution_id>/output', methods=['GET', 'OPTIONS'])
@requires_auth
@cors
def execution_output(execution_id):
    try:
        ex = executions.get(execution_id)
    except KeyError:
        abort(404)

    def generate(ex):
        for line in ex['stream'].output():
            yield str(line)
    # jsonify() is doing something weird to my response.
    return Response(generate(ex), mimetype="text/plain")


@app.route('/executions/<execution_id>/results', methods=['GET', 'OPTIONS'])
@requires_auth
@cors
def execution_results(execution_id):
    try:
        ex = executions.get(execution_id)
    except KeyError:
        abort(404)

    return jsonify(ex["stream"].results())
