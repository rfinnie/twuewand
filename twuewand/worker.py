#!/usr/bin/env python

# twuewand random number generator
# Copyright (C) 2015 Ryan Finnie
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import __init__ as twuewand
from truerand import TrueRand
import multiprocessing

__version__ = twuewand.__version__


# multiprocessing does not allow for passing class instances, but we
# want to keep persistent state per-worker for EWMA calculations.  This
# requires a global variable, but it's limited to worker children.
worker_global = {}


class FakePool():
    def __init__(self, processes=1, initializer=None, initargs=None):
        if initargs is None:
            initargs = []
        if initializer:
            initializer(*initargs)

    class imap():
        def __init__(self, func, iterable, chunksize=1):
            self.func = func
            self.iterable = iterable

        def __iter__(self):
            return self

        def next(self):
            return self.func(self.iterable.next())

    imap_unordered = imap


def pool(processes=0, initializer=None, initargs=None):
    if not processes:
        try:
            processes = multiprocessing.cpu_count()
        except NotImplementedError:
            processes = 1
    if initargs is None:
        initargs = []

    if processes > 1:
        return multiprocessing.Pool(processes, initializer, initargs)
    else:
        return FakePool(processes, initializer, initargs)


def worker(generation=0):
    global worker_obj
    if 'truerand_obj' not in worker_global:
        worker_global['truerand_obj'] = TrueRand()
        if worker_global['bits']:
            worker_global['truerand_obj'].bits = worker_global['bits']
    try:
        return worker_global['truerand_obj'].next()
    except KeyboardInterrupt:
        return


def worker_init(config):
    global worker_obj
    for k, v in config.items():
        worker_global[k] = v
