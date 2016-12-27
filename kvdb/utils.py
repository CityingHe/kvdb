# -*- coding: utf-8 -*-

"""
kvdb.utils
~~~~~~~~~~~~

Author: Citying
"""

import sys

__all__ = ['args', 'colored', 'exit_after_echo']

def exit_after_echo(msg, color='red'):
    if color == 'red':
        print(colored.red(msg))
    else:
        print(msg)
    exit(1)



class Args(object):
    """A simple customed args parser for `kvdb`."""

    def __init__(self, arg=None):
        self._args = sys.argv[1:]
        self._argc = len(self)
        self._key = None
        self._value = None

    def __repr__(self):
        return '<args {}>'.format(repr(self._args))

    def __len__(self):
        return len(self._args)

    @property
    def all(self):
        return self._args

    def get(self, idx):
        try:
            return self.all[idx]
        except IndexError:
            return None

    @property
    def kvdb(self):
        return self.get(0)

    @property
    def key(self):
        if self._key is None:
            self._key = self.get(2)
        return self._key

    @property
    def value(self):
        if self._value is None:
            self._value = self.get(3)
        return self._value

    @property
    def is_asking_for_help(self):
        arg = self.get(0)
        if arg in ('-h', '--help'):
            return True
        return False

    @property
    def is_set_key(self):
        arg = self.get(1)
        if arg in ('set','SET'):
            self._key = self.get(2)
            self._value = self.get(3)
            return True
        return False

    @property
    def is_get_key(self):
        arg = self.get(1)
        if arg in ('get','GET'):
            self._key = self.get(2)
            return True
        return False

    @property
    def is_del_key(self):
        arg = self.get(1)
        if arg in ('del','DEL'):
            self._key = self.get(2)
            return True
        return False

    @property
    def is_closed(self):
        arg = self.get(1)
        if arg in ('close','CLOSE'):
            return True
        return False

class Colored(object):

    """Keep it simple, only use `red` and `green` color."""

    RED = '\033[91m'
    GREEN = '\033[92m'

    #: no color
    RESET = '\033[0m'

    def _color_str(self, color, s):
        return '{}{}{}'.format(
            getattr(self, color),
            s,
            self.RESET
        )

    def red(self, s):
        return self._color_str('RED', s)

    def green(self, s):
        return self._color_str('GREEN', s)

args = Args()
colored = Colored()