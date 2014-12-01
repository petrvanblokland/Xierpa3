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
    u"""Generic data instance, answered by every adapter query. The attributes of the *Data* instance
    can be accessed as dictionary key and as attribute.
        >>> data = Data(a=1, b=2, c=3)
        >>> data.a
        1
        >>> data['b']
        2
    """
    def __init__(self, **kargs):
        self.fields = set() # Attribute names, besides self.fields and self.items
        self._data = [] # Make sure that self.items can always be iterated.
        for key, item in kargs.items():
            self[key] = item
            
    def __getattr__(self, key):
        u"""Answer the list of all attribute names.
            >>> data = Data(a=1, b=2, c=3)
            >>> data.b
            2
        """
        return self.__dict__.get(key)
    
    def __repr__(self):
        u"""
            >>> data = Data(a=1, b=2, c=3)
            >>> data
            [Data a, b, c]
        """
        return '[%s %s]' % (self.__class__.__name__, ', '.join(sorted(self.fields)))

    def __setitem__(self, key, item):
        u"""
            >>> data = Data(a=1, b=2, c=3)
            >>> data['d'] = 10
            >>> data.d
            10
            >>> data.d = 20
            >>> data.d
            20
        """
        self.fields.add(key)
        setattr(self, key, item)
        
    def __getitem__(self, key):
        u"""
            >>> data = Data(a=1, b=2, c=3)
            >>> data.d = 10
            >>> data['d']
            10
        """
        if hasattr(self, key):
            return getattr(self, key)
        return None

    def items(self):
        u"""
            >>> data = Data(a=1, b=2, c=3)
            >>> data.items()
            [('a', 1), ('b', 2), ('c', 3)]
        """
        items = []
        for key in self.keys():
            items.append((key, self[key]))
        return items

    def keys(self):
        u"""Answer the list of all attribute names.
            >>> data = Data(a=1, b=2, c=3)
            >>> data.keys()
            ['a', 'b', 'c']
        """
        return sorted(self.fields)

