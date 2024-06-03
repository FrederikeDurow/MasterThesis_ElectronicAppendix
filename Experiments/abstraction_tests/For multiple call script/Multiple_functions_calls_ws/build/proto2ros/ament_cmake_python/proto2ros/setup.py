from setuptools import find_packages
from setuptools import setup

setup(
    name='proto2ros',
    version='0.1.0',
    packages=find_packages(
        include=('proto2ros', 'proto2ros.*')),
)
