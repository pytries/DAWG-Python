# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import struct
import array

from . import units

class Dictionary(object):
    """
    Dictionary class for retrieval and binary I/O.
    """
    def __init__(self):
        self._units = array.array(str("I"))

    def root(self):
        "Root index"
        return 0

    def has_value(self, index):
        "Checks if a given index is related to the end of a key."
        return units.has_leaf(self._units[index])

    def value(self, index):
        "Gets a value from a given index."
        offset = units.offset(self._units[index])
        value_index = (index ^ offset) & units.PRECISION_MASK
        return units.value(self._units[value_index])

    def read(self, fp):
        "Reads a dictionary from an input stream."
        base_size = struct.unpack(str("=I"), fp.read(4))[0]
        self._units.fromfile(fp, base_size)

    def contains(self, key):
        "Exact matching."
        index = self.follow_bytes(key, self.root())
        if index is None:
            return False
        return self.has_value(index)

    def find(self, key):
        "Exact matching (returns value)"
        index = self.follow_bytes(key, self.root())
        if index is None:
            return -1
        if not self.has_value(index):
            return -1
        return self.value(index)

    def follow_char(self, label, index):
        "Follows a transition"
        offset = units.offset(self._units[index])
        next_index = (index ^ offset ^ label) & units.PRECISION_MASK

        if units.label(self._units[next_index]) != label:
            return None

        return next_index

    def follow_bytes(self, s, index):
        "Follows transitions."
        for ch in bytearray(s):
            index = self.follow_char(ch, index)
            if index is None:
                return None

        return index

    @classmethod
    def load(cls, path):
        dawg = cls()
        with open(path, 'rb') as f:
            dawg.read(f)
        return dawg
