import time
import requests
import logging
import json
import sys

class FuroshikiClient(object):
    def __init__(self, server_uri, username, password):
        self.server_uri = server_uri
        self.username = username
        self.password = password

    def _get(self, endpoint):
        return requests.get(
            self.server_uri + endpoint, 
            auth=(self.username, self.password),
        ).json()

    def execute(self, command, *args, **kwargs):
        data = {
            command: {"args": list(args), "kwargs": kwargs},
        }
        resp = requests.post(
            self.server_uri + '/executions', 
            auth=(self.username, self.password),
            data=json.dumps(data),
	    headers={'Content-type':'application/json'},
        )
        output = resp.json()
        return self._poll(output['results'])

    def _poll(self, results_endpoint):
        while True:
            results = self._get(results_endpoint)
	    if results['finished']:
                break
            time.sleep(1)
	    sys.stdout.write('.')
	    sys.stdout.flush()
        return results['results']


if __name__ == '__main__':
    fc = FuroshikiClient('http://localhost:1234', 'admin', 'secret')
    print fc.execute('host_type')
     
