# -*- coding: utf-8 -*-

"""
kvdb.core
~~~~~~~~~~~~

Author: Citying
"""

import sys
import traceback
import kvdb

from .utils import args, exit_after_echo

def usage():
    pass

def cli():
    """Usage:
    kvdb DBNAME SET key value
    kvdb DBNAME GET key
    kvdb DBNAME DEL key
    kvdb DBNAME CLOSE
    """
    if args.is_asking_for_help:
        exit_after_echo(cli.__doc__,color=None)

    try:

        db = kvdb.connect(args.kvdb)

        if args.is_set_key:
            # print args.__dict__
            db[args.key] = args.value
            db.commit()
        elif args.is_get_key:
            sys.stdout.write(db[args.key])
            print
        elif args.is_del_key:
            del db[args.key]
            db.commit()
        elif args.is_closed:
            db.close()
        else:
            exit_after_echo(cli.__doc__,color=None)
    except Exception as e:
        print('Err: %s' % e)
        # traceback.print_exc()
        exit_after_echo(cli.__doc__,color=None)

    
