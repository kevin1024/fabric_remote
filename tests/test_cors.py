import mock
import fabric_remote
import pytest
import json
from StringIO import StringIO
from utils import get_with_auth, post_with_auth


@pytest.fixture
def execution():
    '''
    Runs a test execution and returns the two endpoints as a tuple
    '''
    fabric_remote.app.testing = True
    fabric_remote.app.fi = mock.Mock()
    fabric_remote.app.fi.list_tasks.return_value = []
    fabric_remote.app.fi.run_tasks.return_value = (
        (mock.Mock(is_alive=mock.Mock(return_value=False))), 'bar')
    fabric_remote.app.config['PASSWORD'] = 'secret'
    client = fabric_remote.app.test_client()
    response = post_with_auth(
        client,
        '/executions',
        json.dumps({"task": "test"})
    )
    response = json.loads(response.data)
    return response['output'], response['results']


def setup_module():
    fabric_remote.app.testing = True
    fabric_remote.app.config['CORS_HOSTS'] = 'http://localhost:1234'


def test_execute_options_header():
    fabric_remote.app.fi = mock.Mock()
    fabric_remote.app.fi.list_tasks.return_value = []
    fabric_remote.app.fi.run_tasks.return_value = ('foo', 'bar')
    client = fabric_remote.app.test_client()
    response = client.options('/executions')
    assert response.headers['Access-Control-Allow-Origin'] == 'http://localhost:1234'


def test_output_options_header(execution):
    output_endpoint, results_endpoint = execution
    client = fabric_remote.app.test_client()
    response = client.options(output_endpoint)
    assert response.headers.get('Access-Control-Allow-Origin') == 'http://localhost:1234'


def test_result_options_header(execution):
    output_endpoint, results_endpoint = execution
    client = fabric_remote.app.test_client()
    response = client.options(results_endpoint)
    assert response.headers.get('Access-Control-Allow-Origin') == 'http://localhost:1234'
