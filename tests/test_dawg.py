# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import tempfile

import pytest
import dawg_python

from .utils import data_path

def test_c_dawg_contains():
    dawg = pytest.importorskip("dawg") #import dawg
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
        return dawg_python.CompletionDAWG().load(data_path('small', 'completion.dawg'))

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

    def test_prefixes(self):
        d = self.dawg()
        assert d.prefixes("foobarz") == ["f", "foo", "foobar"]
        assert d.prefixes("x") == []
        assert d.prefixes("bar") == ["bar"]



#class TestIntDAWG(object):
#
#    def dawg(self):
#        payload = {'foo': 1, 'bar': 5, 'foobar': 3}
#        d = dawg.IntDAWG(payload)
#        return payload, d
#
#    def test_getitem(self):
#        payload, d = self.dawg()
#        for key in payload:
#            assert d[key] == payload[key]
#
#        with pytest.raises(KeyError):
#            d['fo']
#
#
#    def test_dumps_loads(self):
#        payload, d = self.dawg()
#        data = d.tobytes()
#
#        d2 = dawg.IntDAWG()
#        d2.frombytes(data)
#        for key, value in payload.items():
#            assert key in d2
#            assert d2[key] == value
#
#    def test_dump_load(self):
#        payload, _ = self.dawg()
#
#        buf = BytesIO()
#        dawg.IntDAWG(payload).write(buf)
#        buf.seek(0)
#
#        d = dawg.IntDAWG()
#        d.read(buf)
#
#        for key, value in payload.items():
#            assert key in d
#            assert d[key] == value
#
#    def test_pickling(self):
#        payload, d = self.dawg()
#
#        data = pickle.dumps(d)
#        d2 = pickle.loads(data)
#
#        for key, value in payload.items():
#            assert key in d2
#            assert d[key] == value
#
#    def test_int_value_ranges(self):
#        for val in [0, 5, 2**16-1, 2**31-1]:
#            d = dawg.IntDAWG({'f': val})
#            assert d['f'] == val
#
#        with pytest.raises(ValueError):
#            dawg.IntDAWG({'f': -1})
#
#        with pytest.raises(OverflowError):
#            dawg.IntDAWG({'f': 2**32-1})
#
