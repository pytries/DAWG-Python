#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division
import os
import sys
import random
import string
import timeit

import dawg_python

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from utils import data_path, words100k

def random_words(num):
    russian = 'абвгдеёжзиклмнопрстуфхцчъыьэюя'
    alphabet = '%s%s' % (russian, string.ascii_letters)
    return [
        "".join([random.choice(alphabet) for x in range(random.randint(1,15))])
        for y in range(num)
    ]

def truncated_words(words):
    return [word[:3] for word in words]

def prefixes1k(words, prefix_len):
    words = [w for w in words if len(w) >= prefix_len]
    every_nth = int(len(words)/1000)
    _words = [w[:prefix_len] for w in words[::every_nth]]
    return _words[:1000]

WORDS100k = words100k()
MIXED_WORDS100k = truncated_words(WORDS100k)
NON_WORDS100k = random_words(100000)
PREFIXES_3_1k = prefixes1k(WORDS100k, 3)
PREFIXES_5_1k = prefixes1k(WORDS100k, 5)
PREFIXES_8_1k = prefixes1k(WORDS100k, 8)
PREFIXES_15_1k = prefixes1k(WORDS100k, 15)


def format_result(key, value):
    print("%55s:    %s" % (key, value))


def bench(name, timer, descr='M ops/sec', op_count=0.1, repeats=3, runs=5):
    try:
        times = []
        for x in range(runs):
            times.append(timer.timeit(repeats))

        def op_time(time):
            return op_count*repeats / time

        val = "%0.3f%s" % (op_time(min(times)), descr)
        format_result(name, val)
    except (AttributeError, TypeError) as e:
        format_result(name, "not supported")
        #print(e)

def load_dawg():
    return dawg_python.DAWG().load(data_path('large', 'dawg.dawg'))

def load_bytes_dawg():
    return dawg_python.BytesDAWG().load(data_path('large', 'bytes_dawg.dawg'))

def load_record_dawg():
    return dawg_python.RecordDAWG(str('<H')).load(data_path('large', 'record_dawg.dawg'))

def load_int_dawg():
    return dawg_python.IntDAWG().load(data_path('large', 'int_dawg.dawg'))

def benchmark():
    print('\n====== Benchmarks (100k unique unicode words) =======\n')

    tests = [
        ('__getitem__ (hits)', "for word in WORDS100k: data[word]", 'M ops/sec', 0.1, 3),
        ('get() (hits)', "for word in WORDS100k: data.get(word)", 'M ops/sec', 0.1, 3),
        ('get() (misses)', "for word in NON_WORDS_10k: data.get(word)", 'M ops/sec', 0.01, 5),
        ('__contains__ (hits)', "for word in WORDS100k: word in data", 'M ops/sec', 0.1, 3),
        ('__contains__ (misses)', "for word in NON_WORDS100k: word in data", 'M ops/sec', 0.1, 3),
        ('items()', 'list(data.items())', ' ops/sec', 1, 1),
        ('keys()', 'list(data.keys())', ' ops/sec', 1, 1),
#        ('values()', 'list(data.values())', ' ops/sec', 1, 1),
    ]

    common_setup = """
from __main__ import load_dawg, load_bytes_dawg, load_record_dawg, load_int_dawg
from __main__ import WORDS100k, NON_WORDS100k, MIXED_WORDS100k
from __main__ import PREFIXES_3_1k, PREFIXES_5_1k, PREFIXES_8_1k, PREFIXES_15_1k
NON_WORDS_10k = NON_WORDS100k[:10000]
NON_WORDS_1k = ['ыва', 'xyz', 'соы', 'Axx', 'avы']*200
"""
    dict_setup = common_setup + 'data = dict((word, len(word)) for word in WORDS100k);'
    dawg_setup = common_setup + 'data = load_dawg();'
    bytes_dawg_setup = common_setup + 'data = load_bytes_dawg();'
    record_dawg_setup = common_setup + 'data = load_record_dawg();'
    int_dawg_setup = common_setup + 'data = load_int_dawg();'

    structures = [
        ('dict', dict_setup),
        ('DAWG', dawg_setup),
        ('BytesDAWG', bytes_dawg_setup),
        ('RecordDAWG', record_dawg_setup),
        ('IntDAWG', int_dawg_setup),
    ]
    for test_name, test, descr, op_count, repeats in tests:
        for name, setup in structures:
            timer = timeit.Timer(test, setup)
            full_test_name = "%s %s" % (name, test_name)
            bench(full_test_name, timer, descr, op_count, repeats)


    # DAWG-specific benchmarks
    for struct_name, setup in structures[1:]:
        _bench_data = [
            ('hits', 'WORDS100k'),
            ('mixed', 'MIXED_WORDS100k'),
            ('misses', 'NON_WORDS100k'),
        ]

        for meth in ['prefixes']:
            for name, data in _bench_data:
                bench(
                    '%s.%s (%s)' % (struct_name, meth, name),
                    timeit.Timer(
                        "for word in %s:\n"
                        "   data.%s(word)" % (data, meth),
                        setup
                    ),
                    runs=3
                )

        _bench_data = [
            ('xxx', 'avg_len(res)==415', 'PREFIXES_3_1k'),
            ('xxxxx', 'avg_len(res)==17', 'PREFIXES_5_1k'),
            ('xxxxxxxx', 'avg_len(res)==3', 'PREFIXES_8_1k'),
            ('xxxxx..xx', 'avg_len(res)==1.4', 'PREFIXES_15_1k'),
            ('xxx', 'NON_EXISTING', 'NON_WORDS_1k'),
        ]
        for xxx, avg, data in _bench_data:
            for meth in ['keys', 'items']:
                bench(
                    '%s.%s(prefix="%s"), %s' % (struct_name, meth, xxx, avg),
                    timeit.Timer(
                        "for word in %s: data.%s(word)" % (data, meth),
                        setup
                    ),
                    'K ops/sec',
                    op_count=1,
                    runs=3
                )

            for meth in ['iterkeys', 'iteritems']:
                bench(
                    '%s.%s(prefix="%s"), %s' % (struct_name, meth, xxx, avg),
                    timeit.Timer(
                        "for word in %s: list(data.%s(word))" % (data, meth),
                        setup
                    ),
                    'K ops/sec',
                    op_count=1,
                    runs=3
                )

if __name__ == '__main__':
    benchmark()
    #profiling()
    print('\n~~~~~~~~~~~~~~\n')