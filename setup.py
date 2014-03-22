import sys
from setuptools import setup, find_packages

install_requires = ['Flask==0.10.1', 'Fabric==1.8.1']

if sys.version_info < (2, 7):
    install_requires += ['importlib==1.0.2', 'argparse==1.2.1']

setup(
    name='Fabric Remote',
    version='0.0.1',
    long_description=__doc__,
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': {
            'fabric-remote-server = fabric_remote.main:main'
        }
    }
)
