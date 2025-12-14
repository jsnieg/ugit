#!/usr/bin/env python

from setuptools import setup

setup(name='ugit',
       version='1.0',
       packages=['ugit'],
       # exec calls the main() func in cli.py once invoked.
       entry_points = {
           'console_scripts' : [
               'ugit = ugit.cli:main'
           ]
    })