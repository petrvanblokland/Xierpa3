# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#    state.py
#
class State(object):
    u"""
    Attributes
    self.parent        Get/set the parent of this Floq or FloqValue (stored as weakref)
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self[key] = value

    @classmethod
    def fromDict(cls, d):
        return cls(d)

    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name or self.id or 'Untitled')

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __getattr__(self, key):
        return self.__dict__.get(key)

    def items(self):
        return self.__dict__.items()

