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
import plistlib


class A(object):

    @classmethod
    def _getListClass(cls):
        return AList

    @classmethod
    def _getDictClass(cls):
        return ADict

    def __repr__(self):
        """
            >>> td = ADict(dict(a=1, b=2))
            >>> td
            <ADict:{'a': 1, 'b': 2}>
            >>> tl = AList([2, 3, 4])
            >>> tl
            <AList:[2, 3, 4]>
        """
        return u'<%s:%s>' % (self.__class__.__name__, self._data_)

    def __len__(self):
        """
            >>> td = ADict(dict(a=1, b=2))
            >>> len(td)
            2
            >>> tl = AList([2, 3, 4])
            >>> len(tl)
            3
        """
        return len(self._data_)

    def __setitem__(self, indexOrKey, value):
        """
            >>> tl = AList([2, 3, 4])
            >>> tl[1] = 33
            >>> tl[1]
            33
            >>> tl[-1] = 44
            >>> tl[-1]
            44
            >>> tl[4] = 123
            Traceback (most recent call last):
                ...
            IndexError: list assignment index out of range
        """
        self._data_[indexOrKey] = value

    def __getitem__(self, indexOrKey):
        """
            >>> tl = AList([2, 3, 4])
            >>> tl[1]
            3
            >>> tl[-1]
            4
            >>> tl[4]
            Traceback (most recent call last):
                ...
            IndexError: list index out of range
        """
        value = self._data_[indexOrKey]
        if isinstance(value, dict):
            value = self._getDictClass()(value)
        elif isinstance(value, (list, tuple)): # In case the index result is a slice
            value = self._getListClass()(value)
        return value

    def __eq__(self, other):
        u"""Answer whether self is equal to other.

            >>> td1 = ADict(dict(a=12))
            >>> td2 = ADict(dict(a=12))
            >>> td1 == td2
            True
            >>> td1 != td2
            False
            >>> td2 = ADict(dict(a=13))
            >>> td1 == td2
            False
            >>> td1 != td2
            True
            >>> tl1 = AList([1, 2, 3])
            >>> tl2 = AList([1, 2, 3])
            >>> tl1 == tl2
            True
            >>> tl1 != tl2
            False
            >>> tl2 = AList([1, 2, 4])
            >>> tl1 == tl2
            False
            >>> tl1 != tl2
            True
            >>> td1 = ADict(dict(a=13, b=dict(c=12, d=[1, 2, dict(e=14)])))
            >>> td2 = ADict(dict(a=13, b=dict(c=12, d=[1, 2, dict(e=14)])))
            >>> td1 == td2
            True
            >>> td1 != td2
            False
            >>> td2.b.d[2].e = 15
            >>> td1 == td2
            False
            >>> td1 != td2
            True
            >>> td2 = ADict(dict(a=13, b=dict(c=12, d=[1, 2, ADict(dict(e=14))])))
            >>> td1 == td2
            True
            >>> td2 = ADict(dict(a=13, b=dict(c=12, d=AList([1, 2, ADict(dict(e=14))]))))
            >>> td1 == td2
            True
            >>> td2 = ADict(dict(a=13, b=dict(c=12, d=AList([1, 2, ADict(dict(e=17))]))))
            >>> td1 == td2
            False
        """
        if isinstance(other, A):
            other = other._data_
        return self._data_ == other

    def __ne__(self, other):
        u"""Answer whether self is not equal to other."""
        return not self.__eq__(other)

    def asPList(self):
        u"""
            >>> tl = AList([2, 3, 4])
            >>> print tl.asPList().strip().replace("\t", "    ")
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
            <plist version="1.0">
            <array>
                <integer>2</integer>
                <integer>3</integer>
                <integer>4</integer>
            </array>
            </plist>
            >>> tl._data_
            [2, 3, 4]
        """
        return plistlib.writePlistToString(self._data_)

    @classmethod
    def fromPList(cls, s):
        u"""
            >>> tl = AList([2, 3, 4])
            >>> pl = tl.asPList()
            >>> tl2 = A.fromPList(pl)
            >>> tl2
            <AList:[2, 3, 4]>
            >>> td = ADict(dict(a=1, b=2))
            >>> pl = td.asPList()
            >>> td2 = A.fromPList(pl)
            >>> td2
            <ADict:{'a': 1, 'b': 2}>
            >>> x = A.fromPList("<integer>4</integer>")
            Traceback (most recent call last):
                ...
            TypeError: Top level plist object must be list or dict, not int
        """
        obj = plistlib.readPlistFromString(s)
        if isinstance(obj, dict):
            return cls._getDictClass()(obj)
        elif isinstance(obj, (list, tuple)):
            return cls._getListClass()(obj)
        raise TypeError("Top level plist object must be list or dict, not %s" % type(obj).__name__)

    def asSource(self):
        """
            >>> tl = AList([2, 3, 4])
            >>> tl.asSource()
            '[2, 3, 4]'
        """
        return repr(self._data_)

    @classmethod
    def fromSource(cls, s):
        """
            >>> tl = A.fromSource('[2, 3, 4]')
            >>> tl
            <AList:[2, 3, 4]>
            >>> td = A.fromSource('{"a": 2, "b": 3}')
            >>> td
            <ADict:{'a': 2, 'b': 3}>
        """
        compiled = eval(s)  # XXX not safe
        if isinstance(compiled, dict):
            return cls._getDictClass()(compiled)
        if isinstance(compiled, (list, tuple)):
            return cls._getListClass()(compiled)
        return compiled

class AList(A):
    u"""The AList (AttributeList) is the replacement of any list, to make sure that the
    replacement of dicts by ADicts (AttributeDicts) keeps working down the line of
    cascading attribute names."""

    def __init__(self, data=None):
        """
            >>> tl = AList([1, 2, 3])
            >>> tl
            <AList:[1, 2, 3]>
            >>> tl = AList(tl)
            >>> tl
            <AList:[1, 2, 3]>
        """
        if data is None:
            data = []
        elif isinstance(data, AList):
            data = data._data_
        self._data_ = data

    def clear(self):
        u"""
            >>> t1 = AList([1, 2, 3])
            >>> t1.clear()
            >>> len(t1)
            0
        """
        self._data_ = []

    def asList(self):
        u"""Return the contents as a list.

            >>> tl = AList([1, 2, 3])
            >>> tl.asList()
            [1, 2, 3]
        """
        return self._data_

    def append(self, o):
        u"""
            >>> tl = AList([1, 2, 3])
            >>> tl.append(900)
            >>> tl
            <AList:[1, 2, 3, 900]>
        """
        self._data_.append(o)

    def readFrom(self, o, clear=True):
        u"""
            >>> t1 = AList([1, 2, 3, ['a', 'b', 'c']])
            >>> t2 = AList()
            >>> t2.readFrom(t1)
            >>> t1[0] = 100
            >>> t2[0] # Original list changed, t2 should not.
            1
        """
        from copy import deepcopy
        if clear:
            self.clear()
        for e in o:
            if isinstance(e, ADict):
                e = e.asDict()
            elif isinstance(e, AList):
                e = e.asList()
            self.append(deepcopy(e))

class ADict(A):
    u"""The ADict (AttributeDict) is an improved version of State.  The main
    problem with the State class is that it needs to be recursively converted from
    and to a dictionary. This can be a time consuming conversion, e.g. when storing
    data in font.lib, glyph.lib or a database.

    Note: all attribute names are allowed, as long as they don't start with an
    underscore and are not in the set _RESERVEDNAMES.
    """
    _RESERVEDNAMES = set(('_data_', 'asDict', 'fromDict', 'asSource', 'fromSource',
        'get', 'has_key', 'keys', 'items', 'values', '_RESERVEDNAMES'))

    def __init__(self, d=None):
        u"""Set the internal dict to *d*. This is assumed to be an instance with dictionary behavior.
        If *d* is omitted, then create an empty dictionary. If *d* is an instance of @ADict@, then
        take that @d.asDict()@ as attribute.

            >>> td = ADict({'a': 2})
            >>> td
            <ADict:{'a': 2}>
            >>> td = ADict({"asDict": 2})
            Traceback (most recent call last):
                ...
            ValueError: [ADict] "str" (asDict) not allowed as key.
            >>> td = ADict({"_someName": 2})
            Traceback (most recent call last):
                ...
            ValueError: [ADict] "str" (_someName) not allowed as key.
            >>> td = ADict({1: 2})
            Traceback (most recent call last):
                ...
            TypeError: [ADict] "int" (1) not allowed as key.
        """
        if d is None:
            d = {}
        elif isinstance(d, self._getDictClass()):
            d = d.asDict()
        else:
            for k in d:
                self._assertValidName(k)
        self._data_ = d

    def _assertValidName(self, name):
        if not isinstance(name, basestring):
            raise TypeError('[%s] "%s" (%s) not allowed as key.' % (self.__class__.__name__, type(name).__name__, name))
        if name in self._RESERVEDNAMES or name.startswith('_'):
            raise ValueError('[%s] "%s" (%s) not allowed as key.' % (self.__class__.__name__, type(name).__name__, name))

    def asDict(self):
        u"""Answer the internal dictionary.
            >>> td = ADict(dict(a=1, b=[2, 3]))
            >>> td.asDict()
            {'a': 1, 'b': [2, 3]}
        """
        return self._data_


    def clear(self):
        u"""
            >>> t1 = ADict(dict(a=1, b=2, c=3))
            >>> t1.clear()
            >>> len(t1)
            0
        """
        self._data_ = {}

    def readFrom(self, o, clear=False):
        u"""
            >>> t1 = ADict(dict(a=1, b=2, c=3, d=['a', 'b', 'c']))
            >>> t2 = ADict()
            >>> t2.readFrom(t1)
            >>> t1.a = 100
            >>> t2.a # Original dictionary should not change.
            1
        """
        from copy import deepcopy
        if clear:
            self.clear()
        for key in o:
            e = o[key]
            if isinstance(e, ADict):
                e = e.asDict()
            elif isinstance(e, AList):
                e = e.asList()
            self[key] = deepcopy(e)

    @classmethod
    def fromCopy(cls, d):
        u"""
            >>> td = dict(a=1, b=2, c=dict(x=10, y=20, z=30))
            >>> ad = ADict.fromCopy(td)
            >>> td['a'] = 100
            >>> td['c']['x'] = 200 # Make change to original nested dict.
            >>> ad.a
            1
            >>> ad.c.x
            10
        """
        td = cls()
        td.readFrom(d)
        return td


    @classmethod
    def fromDict(cls, d):
        u"""Constructor from dictionary *d*."""
        # XXX Redundant, ADict(adict) works, too.
        return cls(d)

    def __iter__(self):
        """
            >>> td = ADict(dict(a=1, b=2))
            >>> for k in td:
            ...   k
            'a'
            'b'
            >>>
        """
        return iter(self._data_)

    def keys(self):
        u"""Answer the keys of the internal dictionary.

            >>> td = ADict(dict(a=1, b=2))
            >>> td.keys()
            ['a', 'b']
        """
        return self._data_.keys()

    def items(self):
        u"""Answer the items of the internal dictionary, where dict and list values are wrapped.

            >>> td = ADict(dict(a=1, b=[2, 3]))
            >>> td.items()
            [('a', 1), ('b', <AList:[2, 3]>)]
        """
        wrapped = {}
        for key in self._data_.keys(): # Need to copy this, to make sure that dict and list values get a wrapper.
            wrapped[key] = self[key]
        return wrapped.items()

    def values(self):
        u"""Answer the values of the internal dictionary, where dict and list values are wrapped.

            >>> td = ADict(dict(a=1, b=[2, 3]))
            >>> td.values()
            [1, <AList:[2, 3]>]
        """
        values = []
        for key in self._data_.keys():
            values.append(self[key])
        return values

    def get(self, name, default=None):
        u"""Answer the value of *name*. Answer *default* of the key does not exist. Dict and list values are wrapped.

            >>> td = ADict()
            >>> print td.get("123")
            None
            >>> print td.get("123", 456)
            456
            >>> td["a"] = [1, 2, 3]
            >>> td["a"]
            <AList:[1, 2, 3]>
        """
        try:
            return self[name]
        except KeyError:
            return default

    def __contains__(self, name):
        u"""Answer the has_key of the internal dictionary.

            >>> td = ADict(dict(a=12))
            >>> "a" in td
            True
            >>> "b" in td
            False
        """
        return self._data_.has_key(name)

    def has_key(self, name):
        u"""Answer the has_key of the internal dictionary.

            >>> td = ADict(dict(a=12))
            >>> td.has_key("a")
            True
            >>> td.has_key("b")
            False
        """
        return self.__contains__(name)

    def __getitem__(self, name):
        u"""Answer the named value. Internal dict, tuple and list instances get translated to
        *ADict* and *AList* respectively.

            >>> td = ADict(dict(a=12))
            >>> td["a"]
            12
            >>> td[12]
            Traceback (most recent call last):
                ...
            KeyError: 12
        """
        value = self._data_[name]
        if isinstance(value, dict):
            value = self._getDictClass()(value)
        elif isinstance(value, (tuple, list)):
            value = self._getListClass()(value)
        return value

    def __setitem__(self, name, value):
        u"""Set the named value in the internal dictionary. If the (external) value
        is an *ADict* or *AList*, then store the enclosed data instead.

            >>> td = ADict()
            >>> td["a"] = 14
            >>> td["a"]
            14
            >>> td[12] = 14
            Traceback (most recent call last):
                ...
            TypeError: [ADict] "int" (12) not allowed as key.
        """
        self._assertValidName(name)
        if isinstance(value, self.__class__):
            value = value._data_
        elif isinstance(value, AList):
            value = value.asList()
        self._data_[name] = value

    def __getattr__(self, name):
        u"""Answer the named attribute. If the answered value is a dictionary,
        then create a new ADict (AttributeDict) as wrapper around that dictionary.
        This allows a chained attribute query. Otherwise answer the plain value.

            >>> td = ADict()
            >>> td["a"] = 123
            >>> td.a
            123
            >>> td.b = 125
            >>> td.b
            125
            >>> td["b"]
            125
            >>> td.c
            Traceback (most recent call last):
                ...
            AttributeError: 'c'
        """
        try:
            return self[name]
        except KeyError:
            raise AttributeError(repr(name))

    def __setattr__(self, name, value):
        u"""Set the named attribute. If the value is an ADict, then copy the value by name.
        Otherwise set the plain value. Actively check if keys are strings, which is necessary
        to convert the internal dict into JSON or PLIST.

            >>> td = ADict()
            >>> td.a = 12
            >>> td.a
            12
            >>> td._a = 12
            >>> td.items = 13
            Traceback (most recent call last):
                ...
            ValueError: [ADict] "str" (items) not allowed as key.
        """
        if name.startswith('_'):
            self.__dict__[name] = value
        else:
            self._assertValidName(name)
            if isinstance(value, A):
                self._data_[name] = value._data_
            else:
                self._data_[name] = value

    def __delitem__(self, key):
        r"""
            >>> td = ADict(dict(a=12))
            >>> del td["a"]
            >>> td
            <ADict:{}>
            >>> del td["aaaa"]
            Traceback (most recent call last):
                ...
            KeyError: 'aaaa'
        """
        del self._data_[key]

    def __delattr__(self, key):
        r"""
            >>> td = ADict(dict(a=12))
            >>> del td.a
            >>> td
            <ADict:{}>
            >>> del td.aaaa
            Traceback (most recent call last):
                ...
            AttributeError: 'aaaa'
        """
        try:
            self.__delitem__(key)
        except KeyError:
            raise AttributeError(repr(key))


def _test():
    r"""
        >>> td = ADict(dict(aa=123, bb=[234, dict(yy=2, zz=4)], cc=dict(ddd=456, eee=dict(ffff=3333))))
        >>> td
        <ADict:{'cc': {'eee': {'ffff': 3333}, 'ddd': 456}, 'aa': 123, 'bb': [234, {'yy': 2, 'zz': 4}]}>
        >>> td.asDict()
        {'cc': {'eee': {'ffff': 3333}, 'ddd': 456}, 'aa': 123, 'bb': [234, {'yy': 2, 'zz': 4}]}
        >>> ADict.fromSource(td.asSource())
        <ADict:{'cc': {'eee': {'ffff': 3333}, 'ddd': 456}, 'aa': 123, 'bb': [234, {'yy': 2, 'zz': 4}]}>
        >>> td.aa, td.bb, td.cc.ddd, td.cc.eee.ffff
        (123, <AList:[234, {'yy': 2, 'zz': 4}]>, 456, 3333)
        >>> td.bb
        <AList:[234, {'yy': 2, 'zz': 4}]>
        >>> td.bb[1]
        <ADict:{'yy': 2, 'zz': 4}>
        >>> td.bb[1].yy
        2
        >>> td.cc.eee.ffff = 12345
        >>> td.cc.eee.ffff
        12345
        >>> td.cc.eee.ffff = dict(QQQQ=111, RRRR=222)
        >>> td.cc.eee.ffff.QQQQ
        111
        >>> td.asDict()
        {'cc': {'eee': {'ffff': {'QQQQ': 111, 'RRRR': 222}}, 'ddd': 456}, 'aa': 123, 'bb': [234, {'yy': 2, 'zz': 4}]}
        >>> td.cc['zzz'] = 888
        >>> td.asDict()
        {'cc': {'eee': {'ffff': {'QQQQ': 111, 'RRRR': 222}}, 'zzz': 888, 'ddd': 456}, 'aa': 123, 'bb': [234, {'yy': 2, 'zz': 4}]}
        >>> td.cc.zzz
        888
        >>> print td.cc.sss
        Traceback (most recent call last):
            ...
        AttributeError: 'sss'
        >>> td.aa = (1,2,3,4,5,6,7,8)
        >>> td.aa
        <AList:(1, 2, 3, 4, 5, 6, 7, 8)>
        >>> td
        <ADict:{'cc': {'eee': {'ffff': {'QQQQ': 111, 'RRRR': 222}}, 'zzz': 888, 'ddd': 456}, 'aa': (1, 2, 3, 4, 5, 6, 7, 8), 'bb': [234, {'yy': 2, 'zz': 4}]}>
        >>> td = ADict()
        >>> td.aa = 123
        >>> td
        <ADict:{'aa': 123}>
        >>> print td["unknownkey"]
        Traceback (most recent call last):
            ...
        KeyError: 'unknownkey'
        >>> tl  = AList([2, 3, 4])
        >>> tl
        <AList:[2, 3, 4]>
        >>> len(tl)
        3
        >>> tl[1]
        3
        >>> tl[-1]
        4
        >>> tl[4]
        Traceback (most recent call last):
            ...
        IndexError: list index out of range
        >>> print tl.asPList().strip().replace("\t", "    ")
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <array>
            <integer>2</integer>
            <integer>3</integer>
            <integer>4</integer>
        </array>
        </plist>
        >>> tl._data_
        [2, 3, 4]
    """


def _runDocTests():
    import doctest
    import fbits.toolbox.storage.adict
    return doctest.testmod(fbits.toolbox.storage.adict)


if __name__ == '__main__':
    _runDocTests()
