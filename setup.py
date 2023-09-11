#! /usr/bin/env python
from setuptools import setup

setup(
    name="DAWG-Python",
    version="0.7.3",
    description="Pure-python reader for DAWGs (DAFSAs) created by dawgdic C++ library or DAWG Python extension.",
    long_description = open('README.rst').read() + "\n\n"+ open('CHANGES.rst').read(),
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',
    url='https://github.com/kmike/DAWG-Python/',
    packages = ['dawg_python'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
    ],
)
