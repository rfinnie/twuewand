PREFIX := /usr/local

all: rndaddentropy

rndaddentropy: rndaddentropy.c
	$(CC) $(CPPFLAGS) -Wall -Werror -Wextra $(CFLAGS) $(LDFLAGS) -o $@ $<

install: rndaddentropy
	install -d -m 0755 $(DESTDIR)$(PREFIX)/sbin
	install -m 0755 rndaddentropy $(DESTDIR)$(PREFIX)/sbin

distclean: clean

clean:
	rm -f rndaddentropy
