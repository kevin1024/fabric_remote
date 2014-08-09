import time
import json
import sys
import multiprocessing
import Queue
from fabric import state
from fabric.tasks import execute
from fabric.main import load_fabfile
from fabric.tasks import WrappedCallableTask
from . import app
from .util import threadsafe_iter

class FabricException(Exception):
    pass


class QueueIO(object):

    def __init__(self, queue):
        self.queue = queue

    def write(self, data):
        self.queue.put({'output': data})

    def isatty(self):
        return False

    def flush(self, *args, **kwargs):
        pass


class FabricInterface(object):

    def __init__(self, fabfile_path):
        self.fabfile_path = fabfile_path

    def _load_fabfile(self):
        app.logger.info("loading fabfile %s" % self.fabfile_path)
        if not state.commands:
            docstring, callables, default = load_fabfile(self.fabfile_path)
            state.commands.update(callables)
            app.logger.info(
                "loaded {0} tasks from fabfile".format(
                    len(state.commands)
                )
            )
        # Don't prompt me bro
        state.env.abort_on_prompts = True
        # Let us capture exceptions
        state.env.abort_exception = FabricException

    def list_tasks(self):
        self._load_fabfile()
        return state.commands

    def _execute(self, tasks, queue):
        sys.stdout = QueueIO(queue)
        sys.stderr = sys.stdout
        try:
            self._load_fabfile()
            for task in tasks:
                results = execute(
                    task['task'],
                    *task.get('args', []),
                    **task.get('kwargs', {})
                )
                queue.put({"results": (task, results)})
        except FabricException as e:
            queue.put({"error": str(e)})

    def run_tasks(self, tasks):
        # Join whatever children are still sitting around
        multiprocessing.active_children()

        queue = multiprocessing.Queue()
        execute_ps = multiprocessing.Process(
            target=self._execute, args=[tasks, queue]
        )
        execute_ps.start()

        def generate_response(execute_ps, queue):
            while execute_ps.is_alive():
                try:
                    data = queue.get_nowait()
                    yield data
                except Queue.Empty:
                    time.sleep(1)

            execute_ps.join()

            # suck the last goodness out of the queue before moving on
            while True:
                try:
                    data = queue.get_nowait()
                    yield data
                except Queue.Empty:
                    break

        return execute_ps, threadsafe_iter(generate_response(execute_ps, queue))


class FabricEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, WrappedCallableTask):
            return {
                'name': obj.name,
                'description': obj.__doc__.strip() if obj.__doc__ else None
            }
        return json.JSONEncoder.default(self, obj)


def dump_fabric_json(resp):
    return json.dumps(resp, cls=FabricEncoder)
