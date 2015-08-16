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

import sys
import argparse
import time
import hashlib
import __init__ as twuewand
import worker

try:
    from Crypto.Cipher import AES
    HAS_AES = True
except ImportError:
    HAS_AES = False

__version__ = twuewand.__version__


def parse_args():
    parser = argparse.ArgumentParser(
        description='twuewand random number generator (%s)' % __version__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '--version', action='version',
        version=__version__,
        help='report the program version',
    )
    parser.add_argument(
        '--bytes', '-b', type=int, default=0, dest='bytes_opt', metavar='BYTES',
        help='number of bytes to generate',
    )
    parser.add_argument(
        'bytes', type=int, default=0, nargs='?',
        help='number of bytes to generate',
    )
    parser.add_argument(
        '--seconds', '-s', type=float, default=0.0,
        help='number of seconds to generate bytes',
    )
    parser.add_argument(
        '--no-debias', action='store_true',
        help='do not debias generated data',
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='output extra information',
    )
    parser.add_argument(
        '--quiet', '-q', action='store_true',
        help='do not output any extra information',
    )

    # Legacy ignored options
    for opt in ('--no-md5', '--no-sha', '--no-aes'):
        parser.add_argument(
            opt, action='store_true',
            help=argparse.SUPPRESS,
        )
    parser.add_argument(
        '--interval', '-i', type=float, default=0.0,
        help=argparse.SUPPRESS,
    )

    p = parser.parse_args()
    if p.bytes_opt:
        p.bytes = p.bytes_opt
    return p


class TwueWand():
    def __init__(self, args):
        self.args = args

        # Number of bits to generate per worker round
        self.worker_round_bits = 32
        # List of bytes as they come from the worker children
        self.incoming_bytes = bytearray()
        # Full bytes which have passed Von Neumann
        self.vn_byte_queue = bytearray()
        # Von Neumann produces single bits, so hold it here until a full
        # byte is produced
        self.vn_partial_byte = 0
        self.vn_partial_byte_bits = 0
        # Bytes which have or have not passed Von Neumann, for the
        # Kaminsky hash
        self.raw_byte_queue = bytearray()
        # Bytes which are ready to be output
        self.output_queue = bytearray()
        # SHA256 of all bits, used for AES encryption
        self.kaminsky_hash = hashlib.sha256()
        # Number of bits which probably will be output, used for progress
        # display to the user
        self.bits_generated = 0
        # Number of bytes which have actually been written to stdout
        self.bytes_written = 0
        # Whether to enter shutdown mode
        self.complete = False
        # Start time, for time period calculations
        self.start_time = time.time()

        # Build the worker children
        self.worker = worker.worker(bits=self.worker_round_bits)

    def process_von_neumann(self):
        # Apply Von Neumann to incoming bits
        self.raw_byte_queue.extend(self.incoming_bytes)
        for byte in self.incoming_bytes:
            for i in (0, 2, 4, 6):
                bit1 = (byte >> i) & 1
                bit2 = (byte >> (i + 1)) & 1
                if bit1 == bit2:
                    continue
                self.vn_partial_byte = (self.vn_partial_byte << 1) + bit1
                self.vn_partial_byte_bits += 1
                self.bits_generated += 1
                if self.vn_partial_byte_bits == 8:
                    self.vn_byte_queue.append(self.vn_partial_byte)
                    self.vn_partial_byte = 0
                    self.vn_partial_byte_bits = 0
        self.incoming_bytes = bytearray()

    def process_kaminsky(self):
        # Every 16 bytes of Von Neumann data, AES encrypt
        while len(self.vn_byte_queue) >= 16:
            # All raw bits are fed to the SHA256 hash
            self.kaminsky_hash.update(str(self.raw_byte_queue))
            self.raw_byte_queue = bytearray()

            key = self.kaminsky_hash.copy().digest()
            a = AES.new(key, AES.MODE_ECB)
            self.output_queue.extend(a.encrypt(str(self.vn_byte_queue[0:16])))
            self.vn_byte_queue = self.vn_byte_queue[16:]

    def process_sha256(self):
        # Further whiten Von Neumann data with SHA256
        while len(self.vn_byte_queue) >= 32:
            self.raw_byte_queue = bytearray()

            h = hashlib.sha256()
            h.update(str(self.vn_byte_queue[0:32]))
            self.output_queue.extend(h.digest())
            self.vn_byte_queue = self.vn_byte_queue[32:]

    def process_raw(self):
        # No debiasing whatsoever
        if not self.incoming_bytes:
            return
        self.output_queue.extend(self.incoming_bytes)
        self.bits_generated += (len(self.incoming_bytes) * 8)
        self.incoming_bytes = bytearray()

    def process(self):
        if self.args.no_debias:
            self.process_raw()
        elif HAS_AES:
            self.process_von_neumann()
            self.process_kaminsky()
        else:
            self.process_von_neumann()
            self.process_sha256()

    def output(self):
        if not self.output_queue:
            return
        out = str(self.output_queue)
        self.output_queue = bytearray()
        if self.args.bytes:
            if (self.bytes_written + len(out)) > self.args.bytes:
                out = out[0:(self.args.bytes-self.bytes_written)]
        self.bytes_written += len(out)
        sys.stdout.write(out)
        sys.stdout.flush()

    def finish(self):
        print >> sys.stderr

    def report_progress(self):
        if self.args.quiet:
            return

        print >> sys.stderr, '%sGenerated %0.01f bytes, output %d' % (
            chr(13),
            (self.bits_generated / 8.0),
            self.bytes_written,
        ),

    def loop(self):
        for n in self.worker:
            if n is None:
                self.complete = True
                return self.finish()
            self.incoming_bytes.extend([(n >> (i*8)) % 256 for i in range(self.worker_round_bits / 8)])
            self.process()
            self.output()
            self.report_progress()
            if self.args.bytes and (self.bytes_written == self.args.bytes):
                self.complete = True
            if self.args.seconds and (time.time() >= (self.start_time + self.args.seconds)):
                self.complete = True
            if self.complete:
                return self.finish()

    def run(self):
        if self.args.verbose:
            print >> sys.stderr, 'twuewand %s' % __version__
            print >> sys.stderr, 'Copyright 2015 Ryan Finnie'
            print >> sys.stderr
            if self.args.no_debias:
                print >> sys.stderr, 'No debiasing will be performed.'
            elif not HAS_AES:
                print >> sys.stderr, 'pycrypto not found, please consider installing for Kaminsky (AES) debiasing.'
                print >> sys.stderr
        try:
            self.loop()
        except KeyboardInterrupt:
            self.complete = True
            self.finish()


def main():
    args = parse_args()
    t = TwueWand(args)
    t.run()

if __name__ == '__main__':
    sys.exit(main())
