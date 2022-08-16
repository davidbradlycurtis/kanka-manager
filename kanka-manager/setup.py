#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
"""TODO"""
# ---------------------------------------------------------------------------
from setuptools import setup, find_packages

requirements = [
    'dacite==1.6.0',
    'requests==2.27.1',
    'Pyyaml==6.0',
    'coverage==6.4.3',
    'pylint==2.12.2',
    'pytest==6.2.5',
    'tox==3.25.1'
]

setup(
    name='kanka_manager',
    version='1.0.0',
    description="Package to manage Kanka campaigns",
    author="David Curtis",
    packages=[p for p in find_packages() if p.startswith('kanka_manager')],
    package_data={},
    include_package_data=False,
    install_requires=requirements,
)
