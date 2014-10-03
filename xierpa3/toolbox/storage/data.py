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
#   data.py
#
class Data(object):
    u"""Generic data instance, answered by every adapter query."""
    def __init__(self, **kargs):
        self.fields = set() # Attribute names, besides self.fields and self.items
        self.items = [] # Make sure that self.items can always be iterated.
        for key, item in kargs.items():
            self[key] = item
            
    def __getattr__(self, key):
        return self.__dict__.get(key)
    
    def __repr__(self):
        return '[Data] %s' % `self.__dict__`

    def __setitem__(self, key, item):
        self.fields.add(key)
        setattr(self, key, item)
        
    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        return None

