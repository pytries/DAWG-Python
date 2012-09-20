DAWG-python
===========

This pure-python package provides read-only access for files
created by `dawgdic`_ C++ library and `DAWG`_ python package.

.. _dawgdic: https://code.google.com/p/dawgdic/
.. _DAWG: https://github.com/kmike/DAWG

This package is not capable of creating DAWGs. It works with DAWGs built by
`dawgdic`_ C++ library or `DAWG`_ Python extension module. The main purpose
of DAWG-Python is to provide an access to DAWGs without requiring compiled
extensions. It is also quite fast under pypy.

Installation
============

pip install DAWG-Python

Usage
=====

The aim of DAWG-Python is to be API- and binary-compatible
with `DAWG`_ when it is possible.

First, you have to create a dawg using DAWG_ module::

::

    import dawg
    d = dawg.DAWG(data)
    d.save('words.dawg')

And then this dawg can be loaded without requiring C extensions::

    import dawg_python
    d = dawg_python.DAWG().load('words.dawg')

Please consult `DAWG`_ docs for detailed usage. Some features
(like constructor parameters or ``save`` method) are intentionally
unsupported.

Contributing
============

Development happens at github and bitbucket:

* https://github.com/kmike/DAWG-Python
* https://bitbucket.org/kmike/DAWG-Python

The main issue tracker is at github: https://github.com/kmike/DAWG-Python/issues

Feel free to submit ideas, bugs, pull requests (git or hg) or
regular patches.

Running tests and benchmarks
----------------------------

Make sure `tox`_ is installed and run

::

    $ tox

from the source checkout. Tests should pass under python 2.6, 2.7, 3.2 and 3.3.

In order to run benchmarks, type

::

    $ tox -c bench.ini

.. _tox: http://tox.testrun.org

Authors & Contributors
----------------------

* Mikhail Korobov <kmike84@gmail.com>

The algorithms are from `dawgdic`_ C++ library by Susumu Yata & contributors.

License
=======

This package is licensed under MIT License.
