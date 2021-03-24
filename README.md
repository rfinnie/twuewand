# twuewand - A TrueRand algorithm for generating entropy

## About

twuewand is software that creates hardware-generated random data.
It accomplishes this by exploiting the fact that the CPU clock and the RTC (real-time clock) are physically separate, and that time and work are not linked.

## Installation

twuewand requires Python 3.
In addition, the pycrypto package is optional, but highly recommended.

To install:

    sudo python3 setup.py install

On Linux systems, a small C program is also available called rndaddentropy.
This is a wrapper for the RNDADDENTROPY ioctl, and is used for directly adding entropy to the Linux primary pool.
Please see its manpage for more details.

    sudo make -C rndaddentropy install

## Usage

Please see the twuewand manpage for invocation options.

## License

twuewand - A TrueRand algorithm for generating entropy

Copyright (C) 2015-2021 [Ryan Finnie](https://www.finnie.org/)

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
