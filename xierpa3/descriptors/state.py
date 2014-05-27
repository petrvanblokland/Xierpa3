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
from copy import deepcopy

class State(object):

    def __init__(self, **kwargs):
        self._doc = {} # If key is of format "doc_fontsize" then keep documentation string here.
        for key, value in kwargs.items():
            if key.startswith('doc_'):
                self._doc[key] = value
            else:
                self[key] = value

    def copy(self):
        return deepcopy(self)

    @classmethod
    def fromDict(cls, d):
        return cls(d)

    def getDoc(self, key):
        u"""Answer the doc string of <b>key</b> if it exists. Answer <b>None</b> otherwise."""
        return self._doc.get('doc_' + key)

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

