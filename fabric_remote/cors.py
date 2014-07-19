from functools import wraps
from flask_cors import cross_origin
from . import app


def cors(fun):
    @wraps(fun)
    def inner(*args, **kwargs):
        if not app.config.get('CORS_HOSTS'):
            return fun(*args, **kwargs)
        return cross_origin(
            headers=['Authorization', 'Content-Type'],
            supports_credentials=True,
            origins=app.config['CORS_HOSTS'],
        )(fun)(*args, **kwargs)
    return inner
