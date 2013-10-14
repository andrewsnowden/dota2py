#!/usr/bin/env python
"""
=========
 dota2py
=========

dota2py contains both a replay parser and a thin wrapper for the Dota 2 WebAPI.

Installation
============

Install via pip::

    $ pip install dota2py

or, install via easy_install::

    $ easy_install dota2py

Documentation
=============

See the `github <http://github.com/andrewsnowden/dota2py>`_ repository for full
documentation
"""

from distutils.core import setup

setup(name='dota2py',
    version='0.1.3',
    description='Python tools for Dota 2',
    long_description=__doc__,
    author='Andrew Snowden',
    author_email="andrew.snowden@gmail.com",
    download_url="https://github.com/andrewsnowden/dota2py",
    url='https://github.com/andrewsnowden/dota2py',
    packages=['dota2py', 'dota2py.proto', 'dota2py.twisted',
        'dota2py.funtests'],
    package_data={"dota2py": ["data/*.json"]},
    scripts=["scripts/dota2py_parser"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
    ],
    )
