import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

install_requires = [
    'Flask==0.10.1',
    'Fabric==1.8.1',
    'shortuuid==0.4',
    'Flask-Cors==1.2.1',
]


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

if sys.version_info < (2, 7):
    install_requires += ['importlib==1.0.2', 'argparse==1.2.1']

setup(
    name='fabric_remote',
    version='0.0.2',
    long_description=__doc__,
    description='REST API for Fabric',
    url='https://github.com/kevin1024/fabric_remote/',
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=['mock', 'pytest', 'requests'],
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': [
            'fabric-remote-server=fabric_remote.main:main'
        ]
    }
)
