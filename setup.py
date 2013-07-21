from setuptools import setup

install_requires = ['Flask==0.10.1', 'Fabric==1.6.1']

#We need importlib on 2.6 but not 2.7
try:
    import importlib
except ImportError:
    install_requires.append('importlib==1.0.2')

setup(
    name='Furoshiki',
    version='0.0.1',
    long_description=__doc__,
    packages=['furoshiki'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
)

