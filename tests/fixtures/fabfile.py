import os
from fabric.api import task, run, local, env
import time

@task
def host_type():
    """
    test description
    """
    local('uname -a')
    local('ls -l /usr/lib')
    local('echo blah')
    time.sleep(4)
    local('echo blah')
    local('echo blah')
    local('echo blah')
    env['foo'] = 'bar'
    return "shit worked"

@task
def check_foo():
    return env['foo']
