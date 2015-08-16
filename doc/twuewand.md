% TWUEWAND(1) | twuewand
% Ryan Finnie
# NAME

twuewand - A TrueRand algorithm for generating entropy

# SYNOPSIS

twuewand [*options*] [*bytes*]

# DESCRIPTION

`twuewand` is software that creates hardware-generated random data.
It accomplishes this by exploiting the fact that the CPU clock and the RTC (real-time clock) are physically separate, and that time and work are not linked.

twuewand schedules a SIGALRM for a short time in the future, then begins flipping a bit as fast as possible.
When the alarm is delivered, the bit's state is recorded.
Von Neumann debiasing is (by default) performed on bit pairs, throwing out matching bit pairs, and using the first bit for non-matching bit pairs.
This reduces bias, at the expense of wasted bits.

This process is performed multiple times until the number of desired bytes have been generated.
The data is then (by default) either run through a SHA256 cryptographic hash digest, or encrypted with a hashed key (Kaminsky debiasing) to further debias the data before being output.

twuewand is based on the TrueRand algorithm, by D. P. Mitchell in 1995.
The output of twuewand may be used for random data directly (as long as debiasing is not disabled), but its primary purpose is for seeding a PRNG, when a saved PRNG state is not available (on a LiveCD or diskless workstation, for example), or when insufficient initial entropy is not available (in a virtual machine, for example).
An example use in Linux is:

    twuewand $(($(cat /proc/sys/kernel/random/poolsize)/8)) | rndaddentropy

(This example is specific to Linux 2.6 and later.  poolsize in Linux 2.6 is represented in bits, while 2.4 and earlier is bytes.)

`rndaddentropy` is a helper utility to send data to the RNDADDENTROPY ioctl.
This can be dangerous without a good source of entropy (such as a hardware key or twuewand with sufficient debiasing); see `rndaddentropy(8)` for details.

You may also send twuewand output to /dev/random or /dev/urandom, but this merely "stirs the pot", and does not directly add entropy to the pool.

Unless specifically disabled (see below), twuewand will try to use a variety of debiasing techniques, The most comprehensive method will be chosen, depending on what Python modules are available.  They include:

* Von Neumann simple debiasing.
* Output hashing with SHA256.
* Kaminsky debiasing, an extension of Von Neumann.  This requires pycrypto.

# OPTIONS

--bytes=*bytes*, -b *bytes*
:   The number of bytes to generate.
    If both --bytes and --seconds are set, twuewand will exit when either condition is satisfied first.

--seconds=*seconds*, -s *seconds*
:   The number of seconds to generate bytes.
    This can be a fraction of a second.
    If both --bytes and --seconds are set, twuewand will exit when either condition is satisfied first.

--quiet, -q
:   Do not print status information to STDERR.

--verbose, -v
:   Print additional information to STDERR.

--no-debias
:   Do not perform any sort of debiasing on the output returned from the TrueRand procedure.

# BUGS

None known, many assumed.

# SEE ALSO

* `rndaddentropy(1)`
* [Introducing twuewand](http://www.finnie.org/2011/09/25/introducing-twuewand/)
* [/dev/random - Wikipedia](http://en.wikipedia.org/wiki//dev/random)
* [Hardware random number generator - Wikipedia](http://en.wikipedia.org/wiki/Hardware_random_number_generator)
* [Analysis of the Linux Random Number Generator](http://eprint.iacr.org/2006/086.pdf)
* [Re: `Random' seed.](http://www.atomicfrog.com/knowledge/security/misc/truerand.c)
