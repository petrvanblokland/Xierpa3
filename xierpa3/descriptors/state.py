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
import copy

class State(object):

    def __init__(self, **kwargs):
        self._docs = {}
        self._items = {}
        for key, value in kwargs.items():
            self[key] = value

    def copy(self):
        state = self.__class__(**self.__dict__)
        state.doc = copy.copy(self.doc) # Make a deep copy of the documentation. New entries may be added.
        return state
    
    @classmethod
    def fromDict(cls, d):
        return cls(d)
    
    def getDoc(self, key):
        u"""Answer the doc string of <b>key</b> if it exists. Answer <b>None</b> otherwise."""
        return self._docs.get('doc_' + key)
    
    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name or self.id or 'Untitled')

    def __setitem__(self, key, value):
        if key.startswith('doc_'):
            self._docs[key] = value
        else:
            self._items[key] = value

    def __getitem__(self, key):
        if key.startswith('doc_'):
            return self._docs.get(key)
        return self._items.get(key)

    def __getattr__(self, key):
        if key.startswith('doc_'):
            return self._docs.get(key)
        if self._docs.has_key(key):
            return self._docs[key]
        return self.__dict__.get(key)

    def items(self):
        return self._items.items()

    def keys(self):
        return self._items.keys()
    
    def has_key(self, key):
        return self._items.has_key(key)
    
    def docs(self):
        return self._docs.items()
    