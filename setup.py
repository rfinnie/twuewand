#!/usr/bin/env python

import os
from setuptools import setup
import twuewand


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='twuewand',
    description='twuewand random number generator',
    long_description=read('README'),
    version=twuewand.__version__,
    license='GPLv2+',
    platforms=['Unix'],
    author='Ryan Finnie',
    author_email='ryan@finnie.org',
    url='http://www.finnie.org/software/twuewand/',
    download_url='http://www.finnie.org/software/twuewand/',
    packages=['twuewand'],
    classifiers=[],
    entry_points={
        'console_scripts': [
            'twuewand = twuewand.cli:main',
        ],
    }
)
