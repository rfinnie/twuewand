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
import itertools

__version__ = twuewand.__version__


# multiprocessing does not allow for passing class instances, but we
# want to keep persistent state per-worker for EWMA calculations.  This
# requires a global variable, but it's limited to worker children.
child_truerand = None


def worker(bits=8, processes=0):
    if not processes:
        try:
            processes = multiprocessing.cpu_count()
        except NotImplementedError:
            processes = 1
    pool = multiprocessing.Pool(processes, child_init, [bits])
    imap = pool.imap_unordered(child, itertools.repeat(None))
    imap.pool = pool
    return imap


def child(generation=0):
    global child_truerand
    try:
        return child_truerand.next()
    except KeyboardInterrupt:
        return


def child_init(bits=8):
    global child_truerand
    child_truerand = TrueRand(bits=bits)
