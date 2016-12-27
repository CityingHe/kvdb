import os

from kvdb.interface import KVDB


__all__ = ['KVDB', 'connect']

DB = 'data'

def connect(dbname):
    try:
        path = os.path.dirname(__file__)
        os.chdir(path)
        dbname = '%s/%s.db' % (DB, dbname)
        f = open(dbname, 'r+b')
    except IOError:
        fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b')
    return KVDB(f)
