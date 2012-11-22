#!/usr/bin/env python

from distutils.core import setup

setup(name='Distutils',
      version='1.1',
      description='Python tools for Dota 2',
      author='Andrew Snowden',
      url='https://github.com/andrewsnowden/dota2py',
      packages=['dota2py', 'dota2py.proto'],
      package_data={"dota2py":["data/*.json"]},
      scripts=["scripts/dota2py_parser","scripts/dota2py_summary"]
      )
