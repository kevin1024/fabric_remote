import time
import json
import logging
import sys
import multiprocessing
import Queue
from fabric import state
from fabric.tasks import execute
from fabric.main import load_fabfile
from fabric.tasks import WrappedCallableTask
from StringIO import StringIO

class Poo(object):
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
        logging.info("loading fabfile %s" % self.fabfile_path)
        if not state.commands:
            docstring, callables, default = load_fabfile(self.fabfile_path)
            state.commands.update(callables)
        state.env.abort_on_prompts = True #Don't prompt me bro

    def list_tasks(self):
        self._load_fabfile()
        return state.commands

    def _execute(self, tasks, queue):
        sys.stdout = Poo(queue)
        sys.stderr = Poo(queue)
        try:
            self._load_fabfile()
            for task, args in tasks.iteritems():
                results = execute(task, *args.get('args',[]), **args.get('kwargs',{}))
                queue.put({"results": results})
        except Exception as e:
            queue.put({"error": str(e)})

    def run_tasks(self, tasks):
        # Join whatever children are still sitting around 
        multiprocessing.active_children()

        queue = multiprocessing.Queue()
        execute_ps = multiprocessing.Process(target=self._execute, args=[tasks, queue])
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

        return generate_response(execute_ps, queue)

        #results['output'] = captured_output.getvalue()


class FabricEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, WrappedCallableTask):
            return {'name': obj.name, 'description': obj.__doc__ }
        return json.JSONEncoder.default(self, obj)

def dump_fabric_json(resp):
    return json.dumps(resp, cls=FabricEncoder)
