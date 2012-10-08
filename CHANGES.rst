
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