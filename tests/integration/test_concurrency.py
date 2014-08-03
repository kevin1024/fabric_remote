import os
import signal
import json
import threading
import Queue
import requests
import pytest
from fabric_remote import app
from fabric_remote.tasks import FabricInterface, dump_fabric_json

dir = os.path.dirname(__file__)
fixture_path = os.path.join(dir, '../fixtures/')


@pytest.yield_fixture()
def server():
    PORT = 12345
    pid = os.fork()
    if pid == 0:
        os.chdir(fixture_path)
        app.fi = FabricInterface('fabfile')
        app.config['PASSWORD'] = 'secret'
        app.run(port=PORT, debug=True, use_reloader=False)
    else:
        while True:
            try:
                requests.get('http://localhost:{0}'.format(PORT))
                break
            except requests.ConnectionError:
                continue
    yield 'http://localhost:{0}'.format(PORT)
    os.kill(pid, signal.SIGKILL)

def _start_streaming_output(server, q):
    resp = requests.post(server + '/executions', data=json.dumps([{"task": "host_type", "args": [], "kwargs": {}}]), auth=('', 'secret'))
    q.put(requests.get(server + resp.json()['output'], auth=('','secret')))

def test_concurrent_request(server):
    """
    Should be able to fetch results and stuff even while output is streaming in
    another connection
    """ 
    q = Queue.Queue()
    t = threading.Thread(target=_start_streaming_output, args=[server, q])
    t.start()
    resp = requests.post(server + '/executions', data=json.dumps([{"task": "host_type", "args": [], "kwargs": {}}]), auth=('', 'secret'))
    urls = resp.json()
    assert requests.get(server + urls['results'], auth=('', 'secret'))
    resp2 = q.get()
    t.join()
    assert resp and resp2
    
