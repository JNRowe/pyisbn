PYFILES := $(filter-out setup.py, $(wildcard *.py))

PACKAGE_NAME := pyisbn
SNAPSHOT_DATE := $(shell date -I)

.PHONY: ChangeLog MANIFEST .hg_version check clean dist snapshot

all: html/index.html README.html

html/index.html: $(PYFILES)
	epydoc $(PYFILES)

README.html: README
	rst2html.py $< $@

check:
	for i in $(PYFILES); do echo ">>> $$i"; ./$$i; done

clean:
	rm -rf .hg_version ChangeLog MANIFEST README.html html \
		$(patsubst %.py, %.pyc, $(PYFILES))
	./setup.py clean --all

dist: check ChangeLog MANIFEST .hg_version
	./setup.py sdist

.hg_version:
	hg identify >$@

ChangeLog:
	hg log --style changelog >$@

MANIFEST: html/index.html
	hg manifest >$@
	echo $@ >>$@
	echo ChangeLog >>$@
	echo "README.html" >>$@
	echo ".hg_version" >>$@
	find html -not -type d >>$@

snapshot: check ChangeLog
	rm -rf $(PACKAGE_NAME)-$(SNAPSHOT_DATE) \
		dist/$(PACKAGE_NAME)-$(SNAPSHOT_DATE).tar.bz2
	hg archive dist/$(PACKAGE_NAME)-$(SNAPSHOT_DATE)
	cp ChangeLog dist/$(PACKAGE_NAME)-$(SNAPSHOT_DATE)
	
	cd dist; \
		tar --create --bzip2 --file=$(PACKAGE_NAME)-$(SNAPSHOT_DATE).tar.bz2 \
		$(PACKAGE_NAME)-$(SNAPSHOT_DATE)
	
	rm -rf dist/$(PACKAGE_NAME)-$(SNAPSHOT_DATE)

