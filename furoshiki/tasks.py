import json
import logging
from fabric import state
from fabric.tasks import execute
from fabric.main import load_fabfile
from fabric.tasks import WrappedCallableTask

class FabricInterface(object):

    def __init__(self, fabfile_path):
        self.fabfile_path = fabfile_path

    def _load_fabfile(self):
        logging.info("loading fabfile %s" % self.fabfile_path)
        if not state.commands:
            docstring, callables, default = load_fabfile(self.fabfile_path)
            state.commands.update(callables)

    def list_tasks(self):
        self._load_fabfile()
        return state.commands

    def run_task(self, task, *args, **kwargs):
        self._load_fabfile()
        return execute(task, *args, **kwargs)

class FabricEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, WrappedCallableTask):
            return {'name': obj.name, 'description': obj.__doc__ }
        return json.JSONEncoder.default(self, obj)

def dump_fabric_json(resp):
    return json.dumps(resp, cls=FabricEncoder)
