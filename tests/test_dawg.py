# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import pickle
import tempfile

import pytest
import dawg_python

from .utils import data_path


def test_c_dawg_contains():
    dawg = pytest.importorskip("dawg")  # import dawg
    bin_dawg = dawg.IntDAWG({'foo': 1, 'bar': 2, 'foobar': 3})

    d = dawg_python.Dictionary()

    fd, path = tempfile.mkstemp()
    bin_dawg.save(path)

    with open(path, 'rb') as f:
        d.read(f)

    assert d.contains(b'foo')
    assert not d.contains(b'x')
    assert d.contains(b'foobar')
    assert d.contains(b'bar')


class TestCompletionDAWG(object):
    keys = ['f', 'bar', 'foo', 'foobar']

    def dawg(self):
        return dawg_python.CompletionDAWG().load(data_path('small',
                                                           'completion.dawg'))

    def test_contains(self):
        d = self.dawg()
        for key in self.keys:
            assert key in d

    def test_contains_bytes(self):
        d = self.dawg()
        for key in self.keys:
            assert key.encode('utf8') in d

    def test_keys(self):
        d = self.dawg()
        assert d.keys() == sorted(self.keys)

    def test_children(self):
        d = self.dawg()
        assert d.children() == [('b', False), ('f', True)]
        assert d.children('b') == [('ba', False)]
        assert d.children('fo') == [('foo', True)]
        assert d.children('foobar') == []

    def test_iterkeys(self):
        d = self.dawg()
        assert list(d.iterkeys()) == d.keys()

    def test_iter_children(self):
        d = self.dawg()
        assert list(d.iterchildren()) == [('b', False), ('f', True)]
        assert list(d.iterchildren('b')) == [('ba', False)]
        assert list(d.children('fo')) == [('foo', True)]
        assert list(d.children('foobar')) == []

    def test_completion(self):
        d = self.dawg()

        assert d.keys('z') == []
        assert d.keys('b') == ['bar']
        assert d.keys('foo') == ['foo', 'foobar']

    def test_no_segfaults_on_invalid_file(self):
        d = self.dawg()
        fd, path = tempfile.mkstemp()
        with open(path, 'w') as f:
            f.write('foo')

        with pytest.raises(Exception) as e:
            d.load(path)

    def test_empty_dawg(self):
        d = dawg_python.CompletionDAWG().load(data_path('small', 'completion-empty.dawg'))
        assert d.keys() == []

    def test_prefixes(self):
        d = self.dawg()
        assert d.prefixes("foobarz") == ["f", "foo", "foobar"]
        assert d.prefixes("x") == []
        assert d.prefixes("bar") == ["bar"]


class TestIntDAWG(object):
    payload = {'foo': 1, 'bar': 5, 'foobar': 30}

    def dawg(self):
        return dawg_python.IntDAWG().load(data_path('small', 'int_dawg.dawg'))

    def test_getitem(self):
        d = self.dawg()
        for key in self.payload:
            assert d[key] == self.payload[key]

        with pytest.raises(KeyError):
            d['fo']

    def test_pickling(self):
        d = self.dawg()

        data = pickle.dumps(d)
        d2 = pickle.loads(data)

        for key, value in self.payload.items():
            assert key in d2
            assert d[key] == value


class TestIntCompletionDawg(TestIntDAWG):
    def dawg(self):
        return dawg_python.IntCompletionDAWG().load(data_path('small', 'int_completion_dawg.dawg'))

    def test_completion_keys(self):
        assert self.dawg().keys() == sorted(self.payload.keys())

    def test_completion_keys_with_prefix(self):
        assert self.dawg().keys('fo') == ['foo', 'foobar']
        assert self.dawg().keys('foo') == ['foo', 'foobar']
        assert self.dawg().keys('foob') == ['foobar']
        assert self.dawg().keys('z') == []
        assert self.dawg().keys('b') == ['bar']

    def test_completion_items(self):
        assert self.dawg().items() == sorted(self.payload.items(), key=lambda r: r[0])

    def test_completion_children(self):
        assert self.dawg().children('ba') == [('bar', True)]
        assert self.dawg().children('foob') == [('fooba', False)]
        assert self.dawg().children('fooba') == [('foobar', True)]
        assert self.dawg().children('foobar') == []

    def test_completion_iterchildren(self):
        assert list(self.dawg().iterchildren('ba')) == [('bar', True)]
        assert list(self.dawg().iterchildren('foob')) == [('fooba', False)]
        assert list(self.dawg().iterchildren('fooba')) == [('foobar', True)]
        assert list(self.dawg().iterchildren('foobar')) == []

    def test_completion_children_data(self):
        assert self.dawg().children_data('ba') == [('bar', 5)]
        assert self.dawg().children_data('foob') == [('fooba', None)]
        assert self.dawg().children_data('fooba') == [('foobar', 30)]
        assert self.dawg().children_data('foobar') == []

    def test_completion_iterchildren_data(self):
        assert list(self.dawg().iterchildren_data('ba')) == [('bar', 5)]
        assert list(self.dawg().iterchildren_data('foob')) == [('fooba', None)]
        assert list(self.dawg().iterchildren_data('fooba')) == [('foobar', 30)]
        assert list(self.dawg().iterchildren_data('foobar')) == []
