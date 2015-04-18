
Changes
=======

0.7.2 (2015-04-18)
------------------

- minor speedup;
- bitbucket mirror is no longer maintained.

0.7.1 (2014-06-05)
------------------

- Switch to setuptools;
- upload wheel tp pypi;
- check Python 3.4 compatibility.

0.7 (2013-10-13)
----------------

IntDAWG and IntCompletionDAWG are implemented.

0.6 (2013-03-23)
----------------

Use less shared state internally. This should fix thread-safety bugs and
make iterkeys/iteritems reenterant.

0.5.1 (2013-03-01)
------------------

Internal tweaks: memory usage is reduced; something is a bit faster,
something is a bit slower.

0.5 (2012-10-08)
----------------

Storage scheme is updated to match DAWG==0.5. This enables
the alphabetical ordering of ``BytesDAWG`` and ``RecordDAWG`` items.

In order to read ``BytesDAWG`` or ``RecordDAWG`` created with
versions of DAWG < 0.5 use ``payload_separator`` constructor argument::

    >>> BytesDAWG(payload_separator=b'\xff').load('old.dawg')


0.3.1 (2012-10-01)
------------------

Bug with empty DAWGs is fixed.

0.3 (2012-09-26)
----------------

- ``iterkeys`` and ``iteritems`` methods.

0.2 (2012-09-24)
----------------

``prefixes`` support.

0.1 (2012-09-20)
----------------

Initial release.
