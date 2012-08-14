Simple webapp for Ljubljana bus traffic info (LPP).

INSTALL
=======

::

    $ python bootstrap.py
    $ bin/buildout
    $ bin/python trolasi/__init__.py

TESTS
=====

::

    $ bin/nosetests

TODO
====

* upload api to readthedocs
* update opendata.si
* sometimes site will return "Prišlo je do napake"
* travis-ci

* fix tests (include mimerender support for functionaltests)
* autocomplete stations
* show nearest 5 stations (info, map)
* tell people to use google maps for distance times
* list: Stations
* Map of stations and routes
