#!/bin/bash
# to install: $ ln -s ../../pre-commit-check.sh .git/hooks/pre-commit

echo '====== Running tests ========='
bin/nosetests -s --with-coverage --cover-package=trolasi --cover-tests

echo '====== Running PyFlakes ======'
pyflakes trolasi

echo '====== Running pep8 =========='
pep8 trolasi
pep8 setup.py

exit 0
