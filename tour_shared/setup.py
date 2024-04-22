#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='tour_shared',
    version='0.0.1',
    description='Tour Shared library',
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=True,
    install_requires=[
        'sqlalchemy~=1.4.36',
        'nameko==3.0.0-rc11',
        'marshmallow~=3.19.0',
    ],
    extras_require={
        'dev': [
            'pytest~=6.2.0',
            'coverage~=5.5.0',
            'flake8~=3.9.0',
        ],
    },
)
