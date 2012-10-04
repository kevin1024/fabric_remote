from fabric import api, state
from fabric.tasks import execute
from fabric.main import load_fabfile

class FabricInterface(object):

    def __init__(self, fabfile_path):
        self.fabfile_path = fabfile_path

    def _load_fabfile(self):
        if not state.commands:
            docstring, callables, default = load_fabfile(self.fabfile_path)
            state.commands.update(callables)

    def list_tasks(self):
        self._load_fabfile()
        return state.commands

    def run_task(self, task, *args, **kwargs):
        self._load_fabfile()
        return execute(task, *args, **kwargs)
