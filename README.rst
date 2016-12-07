Simple webapp for Ljubljana bus traffic info (LPP).

Part of http://www.opendata.si project.

INSTALL
=======

::

    $ virtualenv .
    $ bin/pip install -r requirements.txt
    $ bin/python trolasi/__init__.py

TESTS
=====

::

    $ bin/pip install nose
    $ bin/nosetests

API
===

http://trolasi.readthedocs.org/en/latest/

TODO
====

* sometimes site will return "Prišlo je do napake"

* fix tests (include mimerender support for functionaltests)
* autocomplete stations
* show nearest 5 stations (info, map)
* tell people to use google maps for distance times
* list: Stations
* Map of stations and routes
