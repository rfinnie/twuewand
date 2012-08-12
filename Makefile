PREFIX := /usr/local

all: rndaddentropy

rndaddentropy: rndaddentropy.c
	$(CC) $(CPPFLAGS) -Wall -Werror -Wextra $(CFLAGS) $(LDFLAGS) -o rndaddentropy rndaddentropy.c

test:
	@perl -MGetopt::Long -e 'print "Getopt::Long is installed.\n";'
	@perl -MPod::Usage -e 'print "Pod::Usage is installed.\n";'
	@perl -MTime::HiRes -e 'print "Time::HiRes is installed.\n";'
	@perl -MModule::Load::Conditional -e 'print "Module::Load::Conditional is installed.\n";'
	@perl -MDigest::SHA -e 'print "Digest::SHA is installed.\n";' 2>/dev/null || echo 'Digest::SHA is not installed (but optional).'
	@perl -MDigest::MD5 -e 'print "Digest::MD5 is installed.\n";' 2>/dev/null || echo 'Digest::MD5 is not installed (but optional).'
	@perl -MCrypt::Scrypt -e 'print "Crypt::Scrypt is installed.\n";' 2>/dev/null || echo 'Crypt::Scrypt is not installed (but optional).'
	@perl -MCrypt::Rijndael -e 'print "Crypt::Rijndael is installed.\n";' 2>/dev/null || echo 'Crypt::Rijndael is not installed (but optional).'
	@echo 'All tests complete.'

install: all
	install -d -m 0755 $(DESTDIR)$(PREFIX)/bin
	install -d -m 0755 $(DESTDIR)$(PREFIX)/sbin
	install -m 0755 twuewand $(DESTDIR)$(PREFIX)/bin
	install -m 0755 rndaddentropy $(DESTDIR)$(PREFIX)/sbin

distclean: clean

clean:
	rm -f rndaddentropy
