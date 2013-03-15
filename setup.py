from setuptools import setup

setup(
    name='Furoshiki',
    version='0.0.1',
    long_description=__doc__,
    packages=['furoshiki'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask==0.9.0','Fabric==1.6.0'],
)
