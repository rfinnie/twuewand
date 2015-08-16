% RNDADDENTROPY(1) | rndaddentropy
% Ryan Finnie
# NAME

rndaddentropy - An RNDADDENTROPY ioctl wrapper

# SYNOPSIS

$ENTROPY_GENERATOR | rndaddentropy

# DESCRIPTION

`rndaddentropy` is used to pipe entropy directly into Linux's primary entropy pool.
This requires superuser privileges.

Adding entropy directly to the primary entropy pool can be very dangerous, a predictable entropy increases the predictability of resulting data from /dev/random and /dev/urandom.
Be sure the entropy is generated from a truly random source, and is properly debiased.

# OPTIONS

--help
:   Display version and usage information.

# BUGS

None known, many assumed.

# SEE ALSO

* `twuewand(8)`, a TrueRand implementation.
