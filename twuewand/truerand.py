#!/usr/bin/env python3

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

from __future__ import division
import signal


__all__ = ['TrueRand']


class TrueRand():
    '''Generate true random numbers by measuring variances between the
    CPU and the RTC.

    This class generates bits by setting an alarm for a short time in
    the future, and flipping a bit (or technically, incrementing an
    integer) continuously until the alarm is reached.  The bit state is
    then recorded, and the process is repeated until the desired number
    of bits are returned.

    The interval between bits is continually evaluated and updated using
    a modified moving average, attempting to reach a target number of
    flips per bit (40000 by default).

    The TrueRand class instance is an iterable, and may be used in a
    loop to generate a continual stream of random integers.
    '''
    def __init__(self, bits=8, target_flips=40000):
        '''TrueRand constructor.

        Arguments, all optional:

        bits : Number of bits to generate per get_int().  While this can
        be any size, precision may be lost at larger sizes.  It is
        recommended to limit the size to 32 bits, and call get_int()
        multiple times if more random bits are needed.  default: 8

        target_flips : Target number of flips per bit.  The interval
        between bits is automatically adjusted up or down to attempt to
        reach this target.  default: 40000
        '''
        if not hasattr(signal, 'SIGALRM'):
            raise OSError('Platform does not support SIGALRM')

        self.bits = bits
        self.target_flips = target_flips
        self.interval = 0.02
        self.bits_collected = 0

    def __iter__(self):
        return self

    def _sigalrm_handler(self, signum, frame):
        '''SIGALRM handler.'''
        if self._flips:
            self._int = (self._int << 1) + (self._flips & 1)
            self._int_bits += 1
            self.bits_collected += 1
            ideal_interval = (self.target_flips / self._flips) * self.interval
            self.interval = ((self.bits_collected * self.interval) + ideal_interval) / (self.bits_collected + 1)
        self._flips = 0
        if self._int_bits < self.bits:
            signal.setitimer(signal.ITIMER_REAL, self.interval)

    def get_int(self):
        '''Return a random integer.

        Generates a number of bits, as specified in the constructor, and
        returns an integer representation of the bits.
        '''
        self._int_bits = 0
        self._int = 0
        self._flips = 0
        previous_sigalrm = signal.signal(
            signal.SIGALRM,
            self._sigalrm_handler,
        )
        signal.setitimer(signal.ITIMER_REAL, self.interval)
        while self._int_bits < self.bits:
            self._flips += 1
        signal.signal(signal.SIGALRM, previous_sigalrm)
        return self._int

    def __next__(self):
        return self.get_int()

    def next(self):
        return self.__next__()
