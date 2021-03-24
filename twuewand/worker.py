# twuewand random number generator
# Copyright (C) 2015-2021 Ryan Finnie
# SPDX-License-Identifier: MPL-2.0

from .truerand import TrueRand
import multiprocessing
import itertools


# multiprocessing does not allow for passing class instances, but we
# want to keep persistent state per-worker for EWMA calculations.  This
# requires a global variable, but it's limited to worker children.
child_truerand = None


def worker(bits=8, processes=None):
    pool = multiprocessing.Pool(processes, child_init, [bits])
    imap = pool.imap_unordered(child, itertools.repeat(None))
    imap.pool = pool
    return imap


def child(unused=None):
    global child_truerand
    try:
        return child_truerand.next()
    except KeyboardInterrupt:
        return


def child_init(bits=8):
    global child_truerand
    child_truerand = TrueRand(bits=bits)
