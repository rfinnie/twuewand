PYTHON := python3

all: build

build:
	$(PYTHON) setup.py build

test: build
	$(PYTHON) setup.py test

install: build
	$(PYTHON) setup.py install

clean:
	$(PYTHON) setup.py clean
	$(RM) -r build MANIFEST

rndaddentropy:
	$(MAKE) -C rndaddentropy

doc:
	$(MAKE) -C doc
