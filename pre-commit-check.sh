#!/bin/sh
# to install: $ ln -s ../../pre-commit-check.sh .git/hooks/pre-commit

echo '====== Running tests ========='
nosetests -s --with-coverage --cover-package=trolasi --cover-tests

echo '====== Running pep8 =========='
pep8 trolasi
