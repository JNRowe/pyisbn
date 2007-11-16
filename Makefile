#
# vim: set sw=4 sts=4 tw=80 fileencoding=utf-8:
#
# pyisbn - A module for working with 10- and 13-digit ISBNs
# Copyright (C) 2007  James Rowe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

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
	echo ">>> README"
	python -c "import doctest, sys; sys.exit(doctest.testfile('README')[0])"

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

