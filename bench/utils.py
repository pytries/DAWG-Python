import zipfile
from pathlib import Path

DEV_DATA_PATH = Path(__file__).parent.parent / "dev_data"


def data_path(*args):
    """
    Returns a path to dev data
    """
    return DEV_DATA_PATH.joinpath(*args)


def words100k():
    zip_name = data_path('words100k.txt.zip')
    zf = zipfile.ZipFile(zip_name)
    txt = zf.open(zf.namelist()[0]).read().decode('utf8')
    return txt.splitlines()
