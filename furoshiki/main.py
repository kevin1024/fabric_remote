import os
import json
import importlib
import functools
import argparse
from flask import Flask
from flask import request, Response, jsonify, abort

from furoshiki.tasks import FabricInterface, dump_fabric_json
from furoshiki.auth import requires_auth
from furoshiki import executions

app = Flask(__name__)
fi = None

@app.route('/tasks', methods=['GET'])
@requires_auth
def get_task():
    return Response(dump_fabric_json(fi.list_tasks()), mimetype="application/json")

@app.route('/executions', methods=['POST'])
@requires_auth
def create_execution():
    tasks = request.json
    ps_handle, stream = fi.run_tasks(tasks)
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

def main():
    parser = argparse.ArgumentParser(description='Run the Furoshiki Fabric REST API server')
    parser.add_argument('--password', type=str, default=os.environ.get('PASSWORD','secret'))
    parser.add_argument('--port', type=int, default=os.environ.get('PORT','1234'))
    parser.add_argument('--bind', type=str, default=os.environ.get('BIND','0.0.0.0'))
    parser.add_argument('--fabfile_path', type=str, default=os.environ.get('FABFILE_PATH','Fabfile'))
    parser.add_argument('--debug', action='store_true', default=os.environ.get('DEBUG', False))
    args = parser.parse_args()
    app.debug = args.debug
    fi = FabricInterface(args.fabfile_path)
    app.run(port=args.port, host=args.bind)

if __name__ == '__main__':
    main()
