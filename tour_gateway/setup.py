#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='tour-gateway',
    version='0.0.1',
    description='Gateway for Tour',
    packages=find_packages(exclude=['test', 'test.*']),
    zip_safe=True
)
