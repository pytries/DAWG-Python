# -*- coding: utf-8 -*-
"""
Script for building test DAWGs.
"""
from __future__ import absolute_import, unicode_literals
import dawg
import os
import sys
import struct

sys.path.insert(0, os.path.dirname(__file__))

from bench.utils import words100k
from tests.test_prediction import TestPrediction

def create_dawg():
    words = words100k()
    return dawg.DAWG(words)

def create_bytes_dawg():
    words = words100k()
    values = [struct.pack(str('<H'), len(word)) for word in words]
    return dawg.BytesDAWG(zip(words, values))

def create_record_dawg():
    words = words100k()
    values = [ [len(word)] for word in words]
    return dawg.RecordDAWG(str('<H'), zip(words, values))

def create_int_dawg():
    words = words100k()
    values = [len(word) for word in words]
    return dawg.IntDAWG(zip(words, values))

def build_test_data():

    dawg.CompletionDAWG(['f', 'bar', 'foo', 'foobar']).save('dev_data/small/completion.dawg')
    dawg.CompletionDAWG([]).save('dev_data/small/completion-empty.dawg')

    bytes_data =  (
        ('foo', b'data1'),
        ('bar', b'data2'),
        ('foo', b'data3'),
        ('foobar', b'data4')
    )
    dawg.BytesDAWG(bytes_data).save('dev_data/small/bytes.dawg')

    record_data = (
        ('foo',     (3, 2, 256)),
        ('bar',     (3, 1, 0)),
        ('foo',     (3, 2, 1)),
        ('foobar',  (6, 3, 0))
    )
    dawg.RecordDAWG(str(">3H"), record_data).save('dev_data/small/record.dawg')

    dawg.DAWG(TestPrediction.DATA).save('dev_data/small/prediction.dawg')
    dawg.RecordDAWG(str("=H"), [(k, (len(k),)) for k in TestPrediction.DATA]).save('dev_data/small/prediction-record.dawg')

    create_dawg().save('dev_data/large/dawg.dawg')
    create_bytes_dawg().save('dev_data/large/bytes_dawg.dawg')
    create_record_dawg().save('dev_data/large/record_dawg.dawg')
    create_int_dawg().save('dev_data/large/int_dawg.dawg')


if __name__ == '__main__':
    build_test_data()
