import base64
import mock
import fabric_remote
import json
from utils import get_with_auth, post_with_auth


def setup_module():
    fabric_remote.app.config['PASSWORD'] = 'secret'


def test_unauthorized_list_tasks():
    client = fabric_remote.app.test_client()
    response = client.get('/tasks')
    assert response.status_code == 401


def test_list_tasks():
    fabric_remote.app.testing = True
    fabric_remote.app.fi = mock.Mock()
    fabric_remote.app.fi.list_tasks.return_value = []
    client = fabric_remote.app.test_client()
    response = get_with_auth(client, '/tasks')
    assert response.status_code == 200


def test_unauthorized_create_execution():
    client = fabric_remote.app.test_client()
    response = client.post('/executions')
    assert response.status_code == 401


def test_create_execution_with_missing_task():
    fabric_remote.app.testing = True
    fabric_remote.app.fi = mock.Mock()
    fabric_remote.app.fi.list_tasks.return_value = []
    client = fabric_remote.app.test_client()
    response = post_with_auth(client, '/executions')
    assert response.status_code == 400


def test_create_execution():
    fabric_remote.app.testing = True
    fabric_remote.app.fi = mock.Mock()
    fabric_remote.app.fi.list_tasks.return_value = []
    fabric_remote.app.fi.run_tasks.return_value = ('foo', 'bar')
    client = fabric_remote.app.test_client()
    response = post_with_auth(
        client,
        '/executions',
        json.dumps({"task": "test"})
    )
    assert response.status_code == 202
