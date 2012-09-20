# -*- coding: utf-8 -*-
"""
Unit of a dictionary
"""
from __future__ import absolute_import

PRECISION_MASK = 0xFFFFFFFF

OFFSET_MAX = 1 << 21
IS_LEAF_BIT = 1 << 31
HAS_LEAF_BIT = 1 << 8
EXTENSION_BIT = 1 << 9

def has_leaf(base):
    " Checks if a unit has a leaf as a child or not."
    return bool(base & HAS_LEAF_BIT & PRECISION_MASK)

def value(base):
    "Checks if a unit corresponds to a leaf or not."
    return base & ~IS_LEAF_BIT & PRECISION_MASK

def label(base):
    "Reads a label with a leaf flag from a non-leaf unit."
    return base & (IS_LEAF_BIT | 0xFF) & PRECISION_MASK

def offset(base):
    "Reads an offset to child units from a non-leaf unit."
    return ((base >> 10) << ((base & EXTENSION_BIT) >> 6)) & PRECISION_MASK
