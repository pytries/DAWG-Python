DAWG-python
===========

This pure-python package provides read-only access for files
created by `dawgdic`_ C++ library and `DAWG`_ python package.

.. _dawgdic: https://code.google.com/p/dawgdic/
.. _DAWG: https://github.com/kmike/DAWG

This package is not capable of creating DAWGs. It works with DAWGs built by
`dawgdic`_ C++ library or `DAWG`_ Python extension module. The main purpose
of DAWG-Python is to provide an access to DAWGs without requiring compiled
extensions. It is also quite fast under PyPy (see benchmarks).

Installation
============

pip install DAWG-Python

Usage
=====

The aim of DAWG-Python is to be API- and binary-compatible
with `DAWG`_ when it is possible.

First, you have to create a dawg using DAWG_ module::

    import dawg
    d = dawg.DAWG(data)
    d.save('words.dawg')

And then this dawg can be loaded without requiring C extensions::

    import dawg_python
    d = dawg_python.DAWG().load('words.dawg')

Please consult `DAWG`_ docs for detailed usage. Some features
(like constructor parameters or ``save`` method) are intentionally
unsupported.

Benchmarks
==========

Benchmark results (100k unicode words, integer values (lenghts of the words),
PyPy 1.9, macbook air i5 1.8 Ghz)::

    dict __getitem__ (hits):        10.978M ops/sec
    DAWG __getitem__ (hits):        not supported
    BytesDAWG __getitem__ (hits):   0.423M ops/sec
    RecordDAWG __getitem__ (hits):  0.348M ops/sec

    dict get() (hits):              10.127M ops/sec
    DAWG get() (hits):              not supported
    BytesDAWG get() (hits):         0.438M ops/sec
    RecordDAWG get() (hits):        0.363M ops/sec
    dict get() (misses):            14.885M ops/sec
    DAWG get() (misses):            not supported
    BytesDAWG get() (misses):       1.228M ops/sec
    RecordDAWG get() (misses):      1.239M ops/sec

    dict __contains__ (hits):           10.341M ops/sec
    DAWG __contains__ (hits):           1.086M ops/sec
    BytesDAWG __contains__ (hits):      0.904M ops/sec
    RecordDAWG __contains__ (hits):     0.886M ops/sec

    dict __contains__ (misses):         9.823M ops/sec
    DAWG __contains__ (misses):         1.491M ops/sec
    BytesDAWG __contains__ (misses):    1.451M ops/sec
    RecordDAWG __contains__ (misses):   1.437M ops/sec

    dict items():           44.401 ops/sec
    DAWG items():           not supported
    BytesDAWG items():      3.437 ops/sec
    RecordDAWG items():     3.210 ops/sec
    dict keys():            426.250 ops/sec
    DAWG keys():            not supported
    BytesDAWG keys():       6.347 ops/sec
    RecordDAWG keys():      6.428 ops/sec


    RecordDAWG.keys(prefix="xxx"), avg_len(res)==415:       1.531K ops/sec
    RecordDAWG.keys(prefix="xxxxx"), avg_len(res)==17:      39.823K ops/sec
    RecordDAWG.keys(prefix="xxxxxxxx"), avg_len(res)==3:    165.236K ops/sec
    RecordDAWG.keys(prefix="xxxxx..xx"), avg_len(res)==1.4: 237.831K ops/sec
    RecordDAWG.keys(prefix="xxx"), NON_EXISTING:            4183.149K ops/sec

Under CPython expect it to be about 50x slower.

I think these results are quite good for pure-Python package. For example,
under PyPy it has faster lookups and uses 2.5x less memory than `marisa-trie`_
under Python 3.2 (`marisa-trie`_ is much slower/doesn't work under PyPy).

It is several times slower under PyPy than Cython-based `DAWG`_ under CPython
though, so `DAWG`_ + CPython > DAWG-Python + PyPy.

Memory consumption of DAWG-Python should be the same as of `DAWG`_.

.. _marisa-trie: https://github.com/kmike/marisa-trie

Current limitations
===================

* This package is not capable of creating DAWGs;
* ``IntDAWG`` is not implemented;
* all the limitations of `DAWG`_ apply.

Contributions are welcome!


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

from the source checkout. Tests should pass under python 2.6, 2.7, 3.2, 3.3
and PyPy >= 1.9.

In order to run benchmarks, type

::

    $ tox -c bench.ini -e pypy

This runs benchmarks under PyPy (they are about 50x slower under CPython).

.. _tox: http://tox.testrun.org

Authors & Contributors
----------------------

* Mikhail Korobov <kmike84@gmail.com>

The algorithms are from `dawgdic`_ C++ library by Susumu Yata & contributors.

License
=======

This package is licensed under MIT License.
