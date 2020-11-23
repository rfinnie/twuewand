#!/usr/bin/env python3

import os
from setuptools import setup
import twuewand


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='twuewand',
    description='twuewand random number generator',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    version=twuewand.__version__,
    license='GPLv2+',
    platforms=['Unix'],
    author='Ryan Finnie',
    author_email='ryan@finnie.org',
    url='http://www.finnie.org/software/twuewand/',
    download_url='http://www.finnie.org/software/twuewand/',
    packages=['twuewand'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    extras_require={
        'AES':  ['pycrypto'],
    },
    entry_points={
        'console_scripts': [
            'twuewand = twuewand.cli:main',
        ],
    },
)
