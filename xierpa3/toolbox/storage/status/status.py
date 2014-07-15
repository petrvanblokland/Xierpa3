# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     xierpa server
#     (c) 2006-2013  buro@petr.com, www.petr.com, www.xierpa.com, www.xierpad.com
#
#     X I E R P A 3
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     status.py
#
from xierpa3.constants.constants import Constants

class Status(object):
    u"""
    The <code>Status</code> class offers a “lazy” storage of basic values, that can be
    stored with JSON in the <code>StatusField</code> field of a database record.
    It can contain an arbitrary set of attributes and getting an attribute that does
    not exist, simply answers <code>None</code>, so in general they don't need to be
    initialized if the default value is <code>False</code>.<br/>
    Note that this is an easy, simple, flat storage device. If storage in a tree is
    required, then use <code>Node<code>, <code>Tree</code> or <code>State</code> classes.
    """
    C = Constants
    
    USE_BASECLASSONLY     = True

    def __init__(self, **args):
        for key, value in args.items():
            if getattr(self, key) is None and self.isAllowedValueType(value):
                setattr(self, key, value)

    @classmethod
    def fromDict(cls, d):
        return cls(**d)

    def __repr__(self):
        return `self.getValues()`

    def __getattr__(self, key):
        return self.__dict__.get(key)

    def __setattr__(self, key, value):
        assert not self.USE_BASECLASSONLY or self.isAllowedValueType(value)
        self.__dict__[key] = value

    __getitem__ = __getattr__
    __setitem__ = __setattr__

    def _get(self, key):
        return self[key]

    def _set(self, key, value):
        self[key] = value

    def _items(self):
        return self.getValues().items()

    def _keys(self):
        return self.getValues().keys()

    def getValues(self,):
        d = {}
        for key, value in self.__dict__.items():
            if self.isAllowedValueType(value):
                d[key] = value
        return d

    def isAllowedValueType(self, value):
        return not self.USE_BASECLASSONLY or value is None or isinstance(value, (bool, int, float, long, basestring, list, tuple, dict))

class XXXData(Status):
    u"""Data is identical to Status, except that it allows non-isAllowedValueType values as storage.
    (Which makes the instances more flexible, but they cannot be stored automatically as JSON or plist)."""
    USE_BASECLASSONLY = False

if __name__ == '__main__':
    s = Status()
    s.abcd = 1234
    print s.abcd
    print s.xyz

    s = Status(aaa=123, bbb=234)
    print s
    print s.aaa

    s = Status.fromDict(dict(aaa=123, bbb=234))
    print s
    print s.aaa, s.bbb

