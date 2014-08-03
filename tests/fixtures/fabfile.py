import os
from fabric.api import task, run, local, env
import time
env.hosts = [os.environ.get("TEST_HOST")]

@task
def host_type():
    """
    test description
    """
    run('uname -a')
    run('ls -l /usr/lib')
    run('echo blah')
    time.sleep(4)
    run('echo blah')
    time.sleep(4)
    run('echo blah')
    time.sleep(4)
    run('echo blah')
    env['foo'] = 'bar'
    return "shit worked"

@task
def check_foo():
    return env['foo']
