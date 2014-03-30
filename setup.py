#!/usr/bin/env python

from distutils.core import setup

setup(
    name="OnionPy",
    version="0.1.0",
    description="Python wrapper for the OnionOO tor status API",
    long_description=open('README.txt').read(),
    author="Lukas Erlacher",
    author_email="tor@lerlacher.de",
    url="http://github.com/duk3luk3/onion-py",
    packages=['onion_py']
    )
