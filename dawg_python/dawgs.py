# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .wrapper import Dictionary

class DAWG(object):
    """
    Base DAWG wrapper.
    """
    def __init__(self):
        self.dct = None

    def __contains__(self, key):
        if isinstance(key, unicode):
            key = key.encode('utf8')
        return self.dct.contains(key)

    def load(self, path):
        """
        Loads DAWG from a file.
        """
        self.dct = Dictionary.load(path)
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