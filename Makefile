###
# build, install, and uninstall

# Write permission is required in installation directories, probably
#   /usr/local/lib/python2.7/dist-packages/
#   /usr/local/bin/
# so usually install and uninstall as root.

.PHONY:	build release install uninstall

build:
	python setup.py sdist

release:
	python setup.py sdist upload

install:
	pip install $(shell ls -tr dist/*)

uninstall:
	pip uninstall scsi_pt
