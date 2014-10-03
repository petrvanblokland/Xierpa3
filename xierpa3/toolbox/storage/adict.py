# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Font Bureau
#
#     F B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     adict.py
#
class AList(object):
    u"""The AList (AttributeList) is the replacement of any list, to make sure that the
    replacement of dicts by ADicts (AttributeDicts) keeps working down the line of
    cascading attribute names."""

    def __init__(self, l=None):
        if l is None:
            l = []
        self._l = l

    def __repr__(self):
        return u'AList%s' % self._l

    def __len__(self):
        return len(self._l)

    def __getitem__(self, index):
        value = self._l[index]
        if isinstance(value, dict):
            value = ADict(value)
        elif isinstance(value, (list, tuple)): # In case the index result is a slice
            value = AList(value)
        return value

    def __setitem__(self, index, value):
        self._l[index] = value

    def asList(self):
        return self._l

    def append(self, o):
        self._l.append(o)

class ADict(object):
    u"""The ADict (AttributeDict) is an improved version of the old State.
    The main problem with the State class is that it needs to be recursively converted
    from and to a dictionary. This can be a time consuming conversion, e.g. when storing
    data in font.lib, glyph.lib or a database.

    Note: all attribute names are allowed, as long as they don't start with an underscore and
    when they are not in the set _RESERVEDNAMES.
    """
    _RESERVEDNAMES = set(('_ddd', 'asDict', 'fromDict', 'get', 'has_key', 'keys', 'items', 'values', '_RESERVEDNAMES'))

    def __init__(self, d=None):
        u"""Set the internal dict to *d*. This is assumed to be an instance with dictionary behavior."""
        if d is None:
            d = {}
        self.__dict__['_ddd'] = d

    def asDict(self):
        u"""Answer the internal dictionary."""
        return self._ddd

    @classmethod
    def fromDict(cls, d):
        u"""Constructor from dictionary *d*."""
        return cls(d)

    def keys(self):
        u"""Answer the keys of the internal dictionary."""
        return self._ddd.keys()

    def items(self):
        u"""Answer the items of the internal dictionary."""
        return self._ddd.items()

    def values(self):
        u"""Answer the values of the internal dictionary."""
        return self._ddd.values()

    def get(self, name):
        u"""Answer the value of *name*. Answer *None* of the key does not exist."""
        return self[name]

    def has_key(self, name):
        u"""Answer the has_key of the internal dictionary."""
        assert not name in self._RESERVEDNAMES, ('[%s] "%s" not allowed as key.' % (self.__class__.__name__, name))
        assert not isinstance(name, basestring) or not name.startswith('_')
        return self._ddd.has_key(name)

    def __repr__(self):
        return u'ADict%s' % self._ddd

    def __getitem__(self, name):
        u"""Answer the named value. Answer *None* of the key does not exist.
        Internal dict, tuple and list instances get translated to respectively
        @ADict@ and @AList."""
        assert not name in self._RESERVEDNAMES, ('[%s] "%s" not allowed as key.' % (self.__class__.__name__, name))
        assert not isinstance(name, basestring) or not name.startswith('_')
        value = self._ddd.get(name)
        if isinstance(value, dict):
            value = ADict(value)
        elif isinstance(value, (tuple, list)):
            value = AList(value)
        return value

    def __setitem__(self, name, value):
        u"""Set the named value in the internal dictionary. If the (external) value
        is an *ADict* or *AList*, then store the enclosed data instead."""
        assert not name in self._RESERVEDNAMES, ('[%s] "%s" not allowed as key.' % (self.__class__.__name__, name))
        assert not isinstance(name, basestring) or not name.startswith('_')
        if isinstance(value, ADict):
            value = value._ddd
        elif isinstance(value, AList):
            value = value.asList()
        self._ddd[name] = value

    def __getattr__(self, name):
        u"""Answer the named attribute. If the answered value is a dictionary,
        then create a new ADict (AttributeDict) as wrapper around that dictionary.
        This allows a chained attribute query. Otherwise answer the plain value.
        Answer *None* if the key does not exist."""
        if name.startswith('_'):
            return self.__dict__.get(name)
        value = self[name]
        if isinstance(value, dict):
            value = ADict(value)
        elif isinstance(value, (tuple, list)):
            value = AList(value)
        return value

    def __setattr__(self, name, value):
        u"""Set the named attribute. If the value is an ADict, then
        copy the value by name. Otherwise set the plain value."""
        assert not name in self._RESERVEDNAMES, ('[%s] "%s" not allowed as key.' % (self.__class__.__name__, name))
        if name.startswith('_'):
            self.__dict__[name] = value
        elif isinstance(value, ADict):
            self._ddd[name] = value[name]
        else:
            self._ddd[name] = value

    def __delitem__(self, key):
        if self._ddd.has_key(key):
            del self._ddd[key]

if __name__ == '__main__':
    td = ADict(dict(aa=123, bb=[234, dict(yy=2, zz=4)], cc=dict(ddd=456, eee=dict(ffff=3333))))
    print td
    print td.asDict()

    '''
    Attribute references are dynamically chained. So, even while td.asDict() answers
    the untouched td._ddd, the result of a chain is that all values are available
    as attribute values. No batch conversion is needed. The dictionaries are transformed
    on the fly if the first dictionary wrapper inherits from AttributeDict.
    '''

    print td.aa, td.bb, td.cc.ddd, td.cc.eee.ffff
    print td.bb[1].yy
    td.cc.eee.ffff = 12345
    print td.cc.eee.ffff
    td.cc.eee.ffff = dict(QQQQ=111, RRRR=222)
    print td.cc.eee.ffff.QQQQ
    print td.asDict()
    td.cc['zzz'] = 888
    print td.asDict()
    print td.cc.zzz
    print td.cc.sss # Answer None
    td.aa = (1,2,3,4,5,6,7,8)
    print td
    # Initialize without dict make empty internal dict.
    td = ADict()
    td.aaa = 123
    print td.aaa
