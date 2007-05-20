PYFILES := $(wildcard *.py)

PACKAGE_NAME := pyisbn
SNAPSHOT_DATE := $(shell date -I)

.PHONY: check clean snapshot

all: html/index.html README.html

html/index.html: $(PYFILES)
	epydoc $(PYFILES)

README.html: README
	rst2html.py $< $@

check:
	for i in $(filter-out setup.py, $(PYFILES)); do echo ">>> $$i"; ./$$i; done

clean:
	rm -rf README.html html $(patsubst %.py, %.pyc, $(PYFILES))

snapshot: check
	rm -rf $(PACKAGE_NAME)-$(SNAPSHOT_DATE) \
		$(PACKAGE_NAME)-$(SNAPSHOT_DATE).tar.bz2
	hg archive $(PACKAGE_NAME)-$(SNAPSHOT_DATE)
	
	cd $(PACKAGE_NAME)-$(SNAPSHOT_DATE); \
	$(MAKE); \
	rm *.pyc
	
	tar --create --bzip2 --file=$(PACKAGE_NAME)-$(SNAPSHOT_DATE).tar.bz2 \
		$(PACKAGE_NAME)-$(SNAPSHOT_DATE)
	
	rm -rf $(PACKAGE_NAME)-$(SNAPSHOT_DATE)

