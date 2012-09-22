# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import zipfile

DEV_DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    '..',
    'dev_data',
)

def data_path(*args):
    """
    Returns a path to dev data
    """
    return os.path.join(DEV_DATA_PATH, *args)

def words100k():
    zip_name = data_path('words100k.txt.zip')
    zf = zipfile.ZipFile(zip_name)
    txt = zf.open(zf.namelist()[0]).read().decode('utf8')
    return txt.splitlines()
