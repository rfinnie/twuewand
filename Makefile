PREFIX := /usr/local
UNAME := $(shell uname)

ifeq ($(UNAME), Linux)
ALLTARGETS := twuewand rndaddentropy
INSTALLTARGETS := install-twuewand install-rndaddentropy
DOCTARGETS := twuewand.8 twuewand.8.html rndaddentropy.8 rndaddentropy.8.html
else
ALLTARGETS := twuewand
INSTALLTARGETS := install-twuewand
DOCTARGETS := twuewand.8 twuewand.8.html
endif

all: $(ALLTARGETS)

twuewand: src/twuewand.pl
	perl -pe 's%#EXTRAVERSION#%$(EXTRAVERSION)%g' $< >$@
	chmod 0755 $@

rndaddentropy: src/rndaddentropy.c
	$(CC) $(CPPFLAGS) -Wall -Werror -Wextra $(CFLAGS) $(LDFLAGS) -o $@ $<

test:
	@perl -MGetopt::Long -e 'print "Getopt::Long is installed.\n";'
	@perl -MPod::Usage -e 'print "Pod::Usage is installed.\n";'
	@perl -MTime::HiRes -e 'print "Time::HiRes is installed.\n";'
	@perl -MModule::Load::Conditional -e 'print "Module::Load::Conditional is installed.\n";'
	@perl -MDigest::SHA -e 'print "Digest::SHA is installed.\n";' 2>/dev/null || echo 'Digest::SHA is not installed (but optional).'
	@perl -MDigest::MD5 -e 'print "Digest::MD5 is installed.\n";' 2>/dev/null || echo 'Digest::MD5 is not installed (but optional).'
	@perl -MCrypt::Rijndael -e 'print "Crypt::Rijndael is installed.\n";' 2>/dev/null || echo 'Crypt::Rijndael is not installed (but optional).'
	@echo 'All tests complete.'

install: $(ALLTARGETS) $(INSTALLTARGETS)

install-twuewand:
	install -d -m 0755 $(DESTDIR)$(PREFIX)/bin
	install -m 0755 twuewand $(DESTDIR)$(PREFIX)/bin

install-rndaddentropy:
	install -d -m 0755 $(DESTDIR)$(PREFIX)/sbin
	install -m 0755 rndaddentropy $(DESTDIR)$(PREFIX)/sbin

distclean: clean

clean:
	rm -f twuewand rndaddentropy

# Docs are shipped pre-compiled
doc: $(DOCTARGETS)

twuewand.8: twuewand
	pod2man -c '' -r '' -s 8 $< >$@

twuewand.8.html: twuewand
	pod2html $< >$@
	rm -f pod2htmd.tmp pod2htmi.tmp

rndaddentropy.8: src/rndaddentropy.pod
	pod2man -c '' -r '' -s 8 $< >$@

rndaddentropy.8.html: src/rndaddentropy.pod
	pod2html $< >$@
	rm -f pod2htmd.tmp pod2htmi.tmp

doc-clean:
	rm -f twuewand.8 twuewand.8.html rndaddentropy.8 rndaddentropy.8.html
