# DAWG-Python

[![Python tests](https://github.com/pymorphy2-fork/DAWG-Python/actions/workflows/python-tests.yml/badge.svg)](https://github.com/pymorphy2-fork/DAWG-Python/actions/workflows/python-tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/pymorphy2-fork/DAWG-Python/badge.svg?branch=master)](https://coveralls.io/github/pymorphy2-fork/DAWG-Python?branch=master)

This pure-python package provides read-only access for files created by
[dawgdic](https://code.google.com/p/dawgdic/) C++ library and
[DAWG](https://github.com/kmike/DAWG) python package.

This package is not capable of creating DAWGs. It works with DAWGs built
by [dawgdic](https://code.google.com/p/dawgdic/) C++ library or
[DAWG](https://github.com/kmike/DAWG) Python extension module. The main
purpose of DAWG-Python is to provide access to DAWGs without
requiring compiled extensions. It is also quite fast under PyPy (see
benchmarks).

# Installation

pip install DAWG-Python

# Usage

The aim of DAWG-Python is to be API- and binary-compatible with
[DAWG](https://github.com/kmike/DAWG) when it is possible.

First, you have to create a dawg using
[DAWG](https://github.com/kmike/DAWG) module:

    import dawg
    d = dawg.DAWG(data)
    d.save('words.dawg')

And then this dawg can be loaded without requiring C extensions:

    import dawg_python
    d = dawg_python.DAWG().load('words.dawg')

Please consult [DAWG](https://github.com/kmike/DAWG) docs for detailed
usage. Some features (like constructor parameters or `save` method) are
intentionally unsupported.

# Benchmarks

Benchmark results (100k unicode words, integer values (lengths of the
words), PyPy 1.9, macbook air i5 1.8 Ghz):

    dict __getitem__ (hits):        11.090M ops/sec
    DAWG __getitem__ (hits):        not supported
    BytesDAWG __getitem__ (hits):   0.493M ops/sec
    RecordDAWG __getitem__ (hits):  0.376M ops/sec

    dict get() (hits):              10.127M ops/sec
    DAWG get() (hits):              not supported
    BytesDAWG get() (hits):         0.481M ops/sec
    RecordDAWG get() (hits):        0.402M ops/sec
    dict get() (misses):            14.885M ops/sec
    DAWG get() (misses):            not supported
    BytesDAWG get() (misses):       1.259M ops/sec
    RecordDAWG get() (misses):      1.337M ops/sec

    dict __contains__ (hits):           11.100M ops/sec
    DAWG __contains__ (hits):           1.317M ops/sec
    BytesDAWG __contains__ (hits):      1.107M ops/sec
    RecordDAWG __contains__ (hits):     1.095M ops/sec

    dict __contains__ (misses):         10.567M ops/sec
    DAWG __contains__ (misses):         1.902M ops/sec
    BytesDAWG __contains__ (misses):    1.873M ops/sec
    RecordDAWG __contains__ (misses):   1.862M ops/sec

    dict items():           44.401 ops/sec
    DAWG items():           not supported
    BytesDAWG items():      3.226 ops/sec
    RecordDAWG items():     2.987 ops/sec
    dict keys():            426.250 ops/sec
    DAWG keys():            not supported
    BytesDAWG keys():       6.050 ops/sec
    RecordDAWG keys():      6.363 ops/sec

    DAWG.prefixes (hits):    0.756M ops/sec
    DAWG.prefixes (mixed):   1.965M ops/sec
    DAWG.prefixes (misses):  1.773M ops/sec

    RecordDAWG.keys(prefix="xxx"), avg_len(res)==415:       1.429K ops/sec
    RecordDAWG.keys(prefix="xxxxx"), avg_len(res)==17:      36.994K ops/sec
    RecordDAWG.keys(prefix="xxxxxxxx"), avg_len(res)==3:    121.897K ops/sec
    RecordDAWG.keys(prefix="xxxxx..xx"), avg_len(res)==1.4: 265.015K ops/sec
    RecordDAWG.keys(prefix="xxx"), NON_EXISTING:            2450.898K ops/sec

Under CPython expect it to be about 50x slower. Memory consumption of
DAWG-Python should be the same as of
[DAWG](https://github.com/kmike/DAWG).

# Current limitations

-   This package is not capable of creating DAWGs;
-   all the limitations of [DAWG](https://github.com/kmike/DAWG) apply.

Contributions are welcome!

# Contributing

Development happens at GitHub: <https://github.com/pymorphy2-fork/DAWG-Python>
Issue tracker: <https://github.com/pymorphy2-fork/DAWG-Python/issues>

Feel free to submit ideas, bugs or pull requests.

## Running tests and benchmarks

Make sure [tox](http://tox.testrun.org) is installed and run

    $ tox

from the source checkout. Tests should pass under python 3.8, 3.9, 3.10, 3.11 and PyPy3 \>= 7.3.

In order to run benchmarks, type

    $ pypy3 -m bench.speed

This runs benchmarks under PyPy (they are about 50x slower under
CPython).

## Authors & Contributors

-   Mikhail Korobov \<<kmike84@gmail.com>\>

The algorithms are from [dawgdic](https://code.google.com/p/dawgdic/)
C++ library by Susumu Yata & contributors.

# License

This package is licensed under MIT License.
