import shortuuid
from .stream import ExecutionStream

# This is a crappy in-memory database. Maybe replace this with a real database
# someday. Also, expire old ones (memory leak) - backported python3.3 lru?
# how about pluggable DB backends?  yes.. yes yes.
executions = {}


def _serialize(execution):
    return {
        "tasks": execution['tasks'],
        "stream": execution['stream'].results(),
    }


def add(tasks, ps_handle, output_stream):
    global executions
    execution_id = shortuuid.uuid()
    executions[execution_id] = {
        "tasks": tasks,
        "stream": ExecutionStream(ps_handle, output_stream),
    }
    return execution_id


def get(execution_id):
    return executions[execution_id]


def all():
    return [_serialize(e) for e in executions.values()]
