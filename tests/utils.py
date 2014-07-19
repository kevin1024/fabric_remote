import base64


def open_with_auth(client, url, method, data=None):
    username = 'admin'
    password = 'secret'
    return client.open(
        url,
        method=method,
        data=data,
        headers={
            'Authorization': 'Basic ' + base64.b64encode(username +
                                                         ":" + password)
        }
    )


def get_with_auth(client, url):
    return open_with_auth(client, url, 'get')


def post_with_auth(client, url, data=None):
    return open_with_auth(client, url, 'post', data)
