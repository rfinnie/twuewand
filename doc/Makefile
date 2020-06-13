PANDOC := pandoc

MARKDOWN=twuewand.md rndaddentropy.md
MAN=$(patsubst %.md,%.1,$(MARKDOWN))

all: man
man: ${MAN}

clean:
	rm -f ${MAN}

%.1: %.md
	$(PANDOC) -s -t man -o $@ $<
