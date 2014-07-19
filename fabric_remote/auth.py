from functools import wraps
from flask import request, Response
from . import app
from .cors import cors


def _secure_compare(x, y):
    """
    Compare 2 strings securely in order to avoid
    a timing attack
    """
    if len(x) != len(y):
        return False
    result = 0
    for a, b in zip(x, y):
        result |= ord(a) ^ ord(b)
    return result == 0


def check_auth(username, password):
    """
    This function is called to check if a username /
    password combination is valid.
    """
    return _secure_compare(password, app.config['PASSWORD'])


@cors
def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if (not auth or not check_auth(auth.username, auth.password)) and not request.method == 'OPTIONS':
            return authenticate()
        return f(*args, **kwargs)
    return decorated
