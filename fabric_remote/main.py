import os
import argparse
from . import app
from .tasks import FabricInterface


def main():
    parser = argparse.ArgumentParser(
        description='Run the Fabric Remote REST API server'
    )
    parser.add_argument(
        '--password', type=str, default=os.environ.get('PASSWORD', 'secret')
    )
    parser.add_argument(
        '--port', type=int, default=os.environ.get('PORT', '1234')
    )
    parser.add_argument(
        '--bind', type=str, default=os.environ.get('BIND', '0.0.0.0')
    )
    parser.add_argument(
        '--cors-hosts', type=str, default=os.environ.get('CORS_HOSTS', '')
    )
    parser.add_argument(
        '--fabfile-path',
        type=str,
        default=os.environ.get('FABFILE_PATH', 'fabfile')
    )
    parser.add_argument(
        '--debug', action='store_true', default=os.environ.get('DEBUG', False)
    )
    args = parser.parse_args()
    app.debug = args.debug
    app.config['PASSWORD'] = args.password
    app.config['CORS_HOSTS'] = [h.strip() for h in args.cors_hosts.split(',')] if args.cors_hosts else None
    app.fi = FabricInterface(args.fabfile_path)
    app.run(port=args.port, host=args.bind, threaded=True)

if __name__ == '__main__':
    main()
