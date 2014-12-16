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
#       formdict.py
#

class FormDict(object):

    """
        >>> d = FormDict("a-12/b-13")
        >>> d
        {'a': ['12'], 'b': ['13']}
        >>> d = FormDict("a-12/a-13/b-13")
        >>> d
        {'a': ['12', '13'], 'b': ['13']}
        >>> d = FormDict({'a': ['12'], 'b': ['13']})
        >>> d
        {'a': ['12'], 'b': ['13']}
    """

    def __init__(self, paramd=None):
        self.d = {}
        self.locked = 0
        if paramd is not None:
            self.append(paramd)
    
    def __delitem__(self, key):
        try:
            del self.d[key]
        except (KeyError, TypeError):
            pass
        
    def __getitem__(self, key):
        try:
            v = self.d[key]
            # v is always a sequence
            if v and len(v) == 1:
                return v[0]
            return v
        except (KeyError, TypeError):
            # @@@ for this behavior, we should use d.get() instead.
            return None
    
    def set(self, key, item):
        #
        #    Overwrite any existing value under key by item
        #    Make we store it as a sequence
        #
        if not isinstance(item, (tuple, list)):
            item = [item]
        self.d[key] = item
        
    def get(self, key, default=None):
        if key in self.d and self[key]:
            return self[key]
        else:
            return default
    
    def clear(self):
        u"""
        
        The ``clear`` clears the internal data, e.g. to be used when logging out.
        
        """
        self.d = {}
        
    def __setitem__(self, key, item):
        #
        #    This is a special dict behavior: if the value already exist in self.d[key]
        #    the value is a list of values. This way the values of multiple url 
        #    parameters with are converted into a list of values.
        #    This is e.g. used for the manage forms that generate e.form['idlist'] values.
        #
        if self.locked:
            raise ValueError, '[FormDict.__setitem__] Formdict is locked and cannot be changed'
        if not isinstance(item, (tuple, list)):
            item = [item]
        d = self.d
        if not d.has_key(key):
            d[key] = []
        d[key] += item
    
    def __repr__(self):
        return repr(self.d)

    def append(self, params):
        u"""
        
        The ``append`` method appends the content of ``params`` to self. If the attribute
        is a string, then split it on ``'/'``. Otherwise we assume that it is already a list.
        
        """
        if not params:
            params = []
        elif isinstance(params, basestring):
            params = params.split('/')

        for param in params:
            if not param:
                continue
            keyvalue = param.split('-')
            if len(keyvalue) == 1:
                key = keyvalue[0]
                value = '1'
            else:
                key = keyvalue[0]
                value = '-'.join(keyvalue[1:])
            self[key] = value
        
    def has_key(self, key):
        return self.d.has_key(key)

    __contains__ = has_key
    
    def keys(self):
        return self.d.keys()
        
    def items(self):
        return self.d.items()

    def __iter__(self):
        return iter(self.d)

    def dict(self):
        return self.d

    def getList(self, key):
        #
        #    Return a list (even when it is empty) of form parameters with name 'key'
        #
        value = self[key]
        if not isinstance(value, list):
            return [value]
        return value

