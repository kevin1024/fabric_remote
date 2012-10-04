from fabric import api, state
from fabric.tasks import execute
from fabric.main import load_fabfile

TEST_FABFILE = '/home/kevin/work/server_config/fabfile'

def list_tasks():
    fabfile = TEST_FABFILE
    docstring, callables, default = load_fabfile(fabfile)
    state.commands.update(callables)
    return state.commands

def run_task(task, *args, **kwargs):
    return execute(task, *args, **kwargs)
    

