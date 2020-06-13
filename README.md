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

Copyright (C) 2015 [Ryan Finnie](http://www.finnie.org/)

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
02110-1301, USA.
