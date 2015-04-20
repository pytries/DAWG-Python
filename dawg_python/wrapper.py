# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import struct
import array

from . import units
from .compat import int_from_byte

class Dictionary(object):
    """
    Dictionary class for retrieval and binary I/O.
    """
    def __init__(self):
        self._units = array.array(str("I"))

    ROOT = 0
    "Root index"

    def has_value(self, index):
        #Checks if a given index is related to the end of a key.
        return units.has_leaf(self._units[index])

    def value(self, index):
        #Gets a value from a given index.
        offset = units.offset(self._units[index])
        value_index = (index ^ offset) & units.PRECISION_MASK
        return units.value(self._units[value_index])

    def read(self, fp):
        #Reads a dictionary from an input stream.
        base_size = struct.unpack(str("=I"), fp.read(4))[0]
        self._units.fromfile(fp, base_size)

    def contains(self, key):
        #Exact matching.
        index = self.follow_bytes(key, self.ROOT)
        if index is None:
            return False
        return self.has_value(index)

    def find(self, key):
        #Exact matching (returns value)
        index = self.follow_bytes(key, self.ROOT)
        if index is None:
            return -1
        if not self.has_value(index):
            return -1
        return self.value(index)

    def follow_char(self, label, index):
        #Follows a transition
        offset = units.offset(self._units[index])
        next_index = (index ^ offset ^ label) & units.PRECISION_MASK

        if units.label(self._units[next_index]) != label:
            return None

        return next_index

    def follow_bytes(self, s, index):
        #Follows transitions.
        for ch in s:
            index = self.follow_char(int_from_byte(ch), index)
            if index is None:
                return None

        return index

    @classmethod
    def load(cls, path):
        dawg = cls()
        with open(path, 'rb') as f:
            dawg.read(f)
        return dawg


class Guide(object):

    ROOT = 0

    def __init__(self):
        self._units = array.array(str("B"))

    def child(self, index):
        return self._units[index*2]

    def sibling(self, index):
        return self._units[index*2 + 1]

    def read(self, fp):
        base_size = struct.unpack(str("=I"), fp.read(4))[0]
        self._units.fromfile(fp, base_size*2)

    def size(self):
        return len(self._units)


class EdgeFollower(object):
    def __init__(self, dic=None, guide=None, payload_separator=b'\x01'):
        self._payload_separator = ord(payload_separator)
        self._dic = dic
        self._guide = guide

    def value(self):
        "provides list of values at current index"

        if self._dic.has_value(self._cur_index):
            return self._dic.value(self._cur_index)
        return None

    def has_value(self):
        "boolean telling whether or not cur_index has a value"
        if self._dic.has_value(self._cur_index):
            return True
        return False

    def start(self, index, prefix=b""):
        """initial setup for the next() action on some prefix. If there's a
        child for this prefix, we add that as the one item on the index_stack.
        Otherwise, leave the stack empty, so next() fails"""

        self.key = bytearray(prefix)
        self.base_key_len = len(self.key)
        self._parent_index = index
        self._sib_index = None
        self._cur_index = None
        if self._guide.size():
            child_label = self._guide.child(index) # UCharType

            if child_label:
                # Follows a transition to the first child.
                next_index = self._dic.follow_char(child_label, index)
                if index is not None:
                    self._sib_index = next_index
                    self._cur_index = self._sib_index
                    #skip if the child is \x01 (the divider char)
                    if child_label == self._payload_separator:
                        return self.next()
                    else:
                        self.key.append(child_label)
                        self.decoded_key = self.key.decode('utf8')
                        return True

    def next(self):
        "Gets the next edge (not necessarily a terminal)"

        if not self._sib_index:
            return False

        sibling_label = self._guide.sibling(self._sib_index)
        self._sib_index = self._dic.follow_char(sibling_label,
                                                self._parent_index)
        self._cur_index = self._sib_index
        if not self._sib_index:
            return False
        if sibling_label == self._payload_separator:
            return self.next()
        self.key = self.key[:self.base_key_len]
        self.key.append(sibling_label)
        try:
            self.decoded_key = self.key.decode('utf8')
        except UnicodeDecodeError:
            #this sibling is a multibyte char. keep following its children til
            #something is decodable
            while True:
                child_label = self._guide.child(self._sib_index)
                self._cur_index = self._dic.follow_char(child_label,
                                                        self._cur_index)
                if not self._cur_index:
                    return False
                self.key.append(child_label)
                try:
                    self.decoded_key = self.key.decode('utf8')
                    break
                except UnicodeDecodeError:
                    pass
        return True

    def get_cur_edge(self):
        """helper method for getting the decoded key along with whether or not
        it is a terminal"""

        return (self.decoded_key, self._dic.has_value(self._cur_index))


class Completer(object):

    def __init__(self, dic=None, guide=None):
        self._dic = dic
        self._guide = guide

    def value(self):
        "provides list of values at current index"

        return self._dic.value(self._last_index)

    def start(self, index, prefix=b""):
        "initial setup for a completer next() action on some prefix"

        self.key = bytearray(prefix)

        if self._guide.size():
            self._index_stack = [index]
            self._last_index = self._dic.ROOT
        else:
            self._index_stack = []

    def next(self):
        "Gets the next key"

        if not self._index_stack:
            return False

        index = self._index_stack[-1]

        if self._last_index != self._dic.ROOT:

            child_label = self._guide.child(index) # UCharType

            if child_label:
                # Follows a transition to the first child.
                index = self._follow(child_label, index)
                if index is None:
                    return False
            else:
                while True:
                    sibling_label = self._guide.sibling(index)
                    # Moves to the previous node.
                    if len(self.key) > 0:
                        self.key.pop()
                        #self.key[-1] = 0

                    self._index_stack.pop()
                    if not self._index_stack:
                        return False

                    index = self._index_stack[-1]
                    if sibling_label:
                        # Follows a transition to the next sibling.
                        index = self._follow(sibling_label, index)
                        if index is None:
                            return False
                        break

        return self._find_terminal(index)

    def _follow(self, label, index):
        next_index = self._dic.follow_char(label, index)
        if next_index is None:
            return None

        self.key.append(label)
        self._index_stack.append(next_index)
        return next_index

    def _find_terminal(self, index):
        while not self._dic.has_value(index):
            label = self._guide.child(index)

            index = self._dic.follow_char(label, index)
            if index is None:
                return False

            self.key.append(label)
            self._index_stack.append(index)

        self._last_index = index
        return True
