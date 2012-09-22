# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import wrapper

class DAWG(object):
    """
    Base DAWG wrapper.
    """
    def __init__(self):
        self.dct = None

    def __contains__(self, key):
        if not isinstance(key, bytes):
            key = key.encode('utf8')
        return self.dct.contains(key)

    def load(self, path):
        """
        Loads DAWG from a file.
        """
        self.dct = wrapper.Dictionary.load(path)
        return self

    def _similar_keys(self, current_prefix, key, index, replace_chars):

        res = []
        start_pos = len(current_prefix)
        end_pos = len(key)
        word_pos = start_pos

        while word_pos < end_pos:
            b_step = key[word_pos].encode('utf8')

            if b_step in replace_chars:
                next_index = index
                b_replace_char, u_replace_char = replace_chars[b_step]

                next_index = self.dct.follow_bytes(b_replace_char, next_index)

                if next_index is not None:
                    prefix = current_prefix + key[start_pos:word_pos] + u_replace_char
                    extra_keys = self._similar_keys(prefix, key, next_index, replace_chars)
                    res += extra_keys

            index = self.dct.follow_bytes(b_step, index)
            if index is None:
                break
            word_pos += 1

        else:
            if self.dct.has_value(index):
                found_key = current_prefix + key[start_pos:]
                res.insert(0, found_key)

        return res

    def similar_keys(self, key, replaces):
        """
        Returns all variants of ``key`` in this DAWG according to
        ``replaces``.

        ``replaces`` is an object obtained from
        ``DAWG.compile_replaces(mapping)`` where mapping is a dict
        that maps single-char unicode sitrings to another single-char
        unicode strings.

        This may be useful e.g. for handling single-character umlauts.
        """
        return self._similar_keys("", key, self.dct.root(), replaces)

    @classmethod
    def compile_replaces(cls, replaces):

        for k,v in replaces.items():
            if len(k) != 1 or len(v) != 1:
                raise ValueError("Keys and values must be single-char unicode strings.")

        return dict(
            (
                k.encode('utf8'),
                (v.encode('utf8'), v)
            )
            for k, v in replaces.items()
        )


class CompletionDAWG(DAWG):
    """
    DAWG with key completion support.
    """

    def __init__(self):
        super(CompletionDAWG, self).__init__()
        self.guide = None
        self.completer = None

    def keys(self, prefix=""):
        b_prefix = prefix.encode('utf8')
        index = self.dct.root()
        res = []

        index = self.dct.follow_bytes(b_prefix, index)
        if index is None:
            return res

        self.completer.start(index, b_prefix)

        while self.completer.next():
            key = self.completer.key.decode('utf8')
            res.append(key)

        return res

    def load(self, path):
        """
        Loads DAWG from a file.
        """
        self.dct = wrapper.Dictionary()
        self.guide = wrapper.Guide()

        with open(path, 'rb') as f:
            self.dct.read(f)
            self.guide.read(f)

        self.completer = wrapper.Completer(self.dct, self.guide)
        return self

class BytesDAWG(CompletionDAWG):
    def __init__(self):
        raise NotImplementedError

class RecordDAWG(BytesDAWG):
    def __init__(self):
        raise NotImplementedError
