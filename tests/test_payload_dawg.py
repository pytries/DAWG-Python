# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import pytest
import dawg_python
from .utils import data_path

class TestBytesDAWG(object):

    DATA = (
        ('foo', b'data1'),
        ('bar', b'data2'),
        ('foo', b'data3'),
        ('foobar', b'data4')
    )

    def dawg(self):
        return dawg_python.BytesDAWG().load(data_path("small", "bytes.dawg"))

    def test_contains(self):
        d = self.dawg()
        for key, val in self.DATA:
            assert key in d

        assert 'food' not in d
        assert 'x' not in d
        assert 'fo' not in d


    def test_getitem(self):
        d = self.dawg()

        assert d['foo'] == [b'data1', b'data3']
        assert d['bar'] == [b'data2']
        assert d['foobar'] == [b'data4']


    def test_getitem_missing(self):
        d = self.dawg()

        with pytest.raises(KeyError):
            d['x']

        with pytest.raises(KeyError):
            d['food']

        with pytest.raises(KeyError):
            d['foobarz']

        with pytest.raises(KeyError):
            d['f']

    def test_keys(self):
        d = self.dawg()
        assert d.keys() == ['bar', 'foo', 'foo', 'foobar']

    def test_iterkeys(self):
        d = self.dawg()
        assert list(d.iterkeys()) == d.keys()

    def test_edges(self):
        d = self.dawg()
        assert d.edges('foob') == [('fooba', False)]
        assert d.edges('fooba') == [('foobar', True)]
        assert d.edges('fo') == [('foo', True)]

    def test_iteredges(self):
        d = self.dawg()
        assert list(d.iteredges('foob')) == [('fooba', False)]
        assert list(d.iteredges('fooba')) == [('foobar', True)]
        assert list(d.iteredges('fo')) == [('foo', True)]

    def test_edges_data(self):
        d = self.dawg()
        assert d.edges_data('foob') == [('fooba', None)]
        assert d.edges_data('fooba') == [('foobar', b'data4')]
        assert d.edges_data('fo') == [('foo', b'data1'), ('foo', b'data3')]

    def test_iteredges_data(self):
        d = self.dawg()
        assert list(d.iteredges_data('foob')) == [('fooba', None)]
        assert list(d.iteredges_data('fooba')) == [('foobar', b'data4')]
        assert list(d.iteredges_data('fo')) == \
               [('foo', b'data1'), ('foo', b'data3')]

    def test_key_completion(self):
        d = self.dawg()
        assert d.keys('fo') == ['foo', 'foo', 'foobar']

    def test_items(self):
        d = self.dawg()
        assert d.items() == sorted(self.DATA)
        assert d.items('not a real key') == []

    def test_iteritems(self):
        d = self.dawg()
        assert list(d.iteritems('xxx')) == []
        assert list(d.iteritems('fo')) == d.items('fo')
        assert list(d.iteritems()) == d.items()

    def test_items_completion(self):
        d = self.dawg()
        assert d.items('foob') == [('foobar', b'data4')]
        assert d.items('foo') == [('foo', b'data1'), ('foo', b'data3'),
                                  ('foobar', b'data4')]

    def test_prefixes(self):
        d = self.dawg()
        assert d.prefixes("foobarz") == ["foo", "foobar"]
        assert d.prefixes("x") == []
        assert d.prefixes("bar") == ["bar"]


class TestRecordDAWG(object):

    STRUCTURED_DATA = (
        ('foo',     (3, 2, 256)),
        ('bar',     (3, 1, 0)),
        ('foo',     (3, 2, 1)),
        ('foobar',  (6, 3, 0))
    )

    def dawg(self):
        path = data_path("small", "record.dawg")
        return dawg_python.RecordDAWG(">3H").load(path)

    def test_getitem(self):
        d = self.dawg()
        assert d['foo'] == [(3, 2, 1), (3, 2, 256)]
        assert d['bar'] == [(3, 1, 0)]
        assert d['foobar'] == [(6, 3, 0)]

    def test_getitem_missing(self):
        d = self.dawg()

        with pytest.raises(KeyError):
            d['x']

        with pytest.raises(KeyError):
            d['food']

        with pytest.raises(KeyError):
            d['foobarz']

        with pytest.raises(KeyError):
            d['f']

    def test_record_items(self):
        d = self.dawg()
        assert d.items() == sorted(self.STRUCTURED_DATA)

    def test_edges_data(self):
        d = self.dawg()
        assert d.edges_data('foob') == [('fooba', None)]
        assert d.edges_data('fooba') == [('foobar', (6, 3, 0))]
        assert d.edges_data('fo') == [('foo', (3, 2, 1)), ('foo', (3, 2, 256))]

    def test_iteredges_data(self):
        d = self.dawg()
        assert list(d.iteredges_data('foob')) == [('fooba', None)]
        assert list(d.iteredges_data('fooba')) == [('foobar', (6, 3, 0))]
        assert list(d.iteredges_data('fo')) == [('foo', (3, 2, 1)),
                                                ('foo', (3, 2, 256))]

    def test_record_keys(self):
        d = self.dawg()
        assert d.keys() == ['bar', 'foo', 'foo', 'foobar',]

    def test_record_keys_prefix(self):
        d = self.dawg()
        assert d.keys('fo') == ['foo', 'foo', 'foobar']
        assert d.keys('bar') == ['bar']
        assert d.keys('barz') == []

    def test_prefixes(self):
        d = self.dawg()
        assert d.prefixes("foobarz") == ["foo", "foobar"]
        assert d.prefixes("x") == []
        assert d.prefixes("bar") == ["bar"]
