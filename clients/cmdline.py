import argparse
import time
import sys
import logging
import json
import requests


class FabricRemoteClient(object):

    def __init__(self, server_uri, username, password):
        self.server_uri = server_uri
        self.username = username
        self.password = password

    def _get(self, endpoint):
        return requests.get(
            self.server_uri + endpoint,
            auth=(self.username, self.password),
        ).json()

    def execute(self, tasks):
        data = []
        for t in tasks:
            data.append(({'task': t, 'args': [], 'kwargs': {}}))
        resp = requests.post(
            self.server_uri + '/executions',
            auth=(self.username, self.password),
            data=json.dumps(data),
            headers={'Content-type': 'application/json'},
        )
        output = resp.json()
        if 'output' in output:
            r = requests.get(
                self.server_uri + output['output'],
                stream=True,
                auth=(self.username, self.password),
            )
            for content in r.iter_content():
                sys.stdout.write(content)
                sys.stdout.flush()
        if 'results' in output:
            return self._poll(output['results'])

    def _poll(self, results_endpoint):
        while True:
            results = self._get(results_endpoint)
            if results['finished']:
                break
            time.sleep(1)
            sys.stdout.write('.')
            sys.stdout.flush()
        if results['error']:
            logging.error(results['error'])
            return None
        return results['results']


def main(username, password, url, tasks):
    fc = FabricRemoteClient('http://localhost:1234', 'admin', 'secret')
    print fc.execute(tasks)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a remote fabric task')
    parser.add_argument('tasks', nargs='+', help='task to run')
    parser.add_argument('--username', dest='username',
                        required=True, help='Remote server username')
    parser.add_argument('--password', dest='password',
                        required=True, help='Remote server password')
    parser.add_argument('--url', dest='url', required=True,
                        help='Remote server URL')

    args = parser.parse_args()
    main(args.username, args.password, args.url, args.tasks)
