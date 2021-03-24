# twuewand random number generator
# Copyright (C) 2015-2021 Ryan Finnie
# SPDX-License-Identifier: MPL-2.0

from __future__ import division, print_function
import sys
import argparse
import time
import hashlib
from . import __version__
from .worker import worker

try:
    from Crypto.Cipher import AES
    HAS_AES = True
except ImportError:
    HAS_AES = False


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
        # Start time, for time period calculations
        self.start_time = time.time()

        # Support raw buffers on both Python 2 / 3
        if hasattr(sys.stdout, 'buffer'):
            self.stdout = getattr(sys.stdout, 'buffer')
        else:
            self.stdout = sys.stdout

        # Build the worker children
        self.worker = worker(bits=self.worker_round_bits)

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
        # Every 32 bytes of Von Neumann data, AES encrypt
        while len(self.vn_byte_queue) >= 32:
            # All raw bits are fed to the SHA256 hash
            self.kaminsky_hash.update(bytes(self.raw_byte_queue))
            self.raw_byte_queue = bytearray()

            key = self.kaminsky_hash.copy().digest()
            a = AES.new(key, AES.MODE_ECB)
            self.output_queue.extend(a.encrypt(bytes(self.vn_byte_queue[0:32])))
            self.vn_byte_queue = self.vn_byte_queue[32:]

    def process_sha256(self):
        # Further whiten Von Neumann data with SHA256
        while len(self.vn_byte_queue) >= 32:
            self.raw_byte_queue = bytearray()

            h = hashlib.sha256()
            h.update(bytes(self.vn_byte_queue[0:32]))
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
        out = self.output_queue
        self.output_queue = bytearray()
        if self.args.bytes:
            if (self.bytes_written + len(out)) > self.args.bytes:
                out = out[0:(self.args.bytes-self.bytes_written)]
        self.bytes_written += len(out)
        self.stdout.write(bytes(out))
        self.stdout.flush()

    def print_stderr(self, value=None, end='\n'):
        print(value, file=sys.stderr, end=end)

    def finish(self):
        self.print_stderr('')

    def report_progress(self):
        if self.args.quiet:
            return

        self.print_stderr('{}Generated {:d} bits ({:0.02f} bps), output {:d} bytes        '.format(
            chr(13),
            self.bits_generated,
            self.bits_generated / (time.time() - self.start_time),
            self.bytes_written,
        ), end='')

    def loop(self):
        for n in self.worker:
            if n is None:
                return self.finish()
            self.incoming_bytes.extend([(n >> (i*8)) % 256 for i in range(int(self.worker_round_bits / 8))])
            self.process()
            self.output()
            self.report_progress()
            if self.args.bytes and (self.bytes_written == self.args.bytes):
                return self.finish()
            if self.args.seconds and (time.time() >= (self.start_time + self.args.seconds)):
                return self.finish()

    def run(self):
        if self.args.verbose:
            self.print_stderr('twuewand %s' % __version__)
            self.print_stderr('Copyright 2015 Ryan Finnie')
            self.print_stderr('')
            if self.args.no_debias:
                self.print_stderr('No debiasing will be performed.')
                self.print_stderr('')
            elif not HAS_AES:
                self.print_stderr('pycrypto not found, please consider installing for Kaminsky (AES) debiasing.')
                self.print_stderr('')
        try:
            self.loop()
        except KeyboardInterrupt:
            self.finish()


def main():
    args = parse_args()
    t = TwueWand(args)
    t.run()

if __name__ == '__main__':
    sys.exit(main())
