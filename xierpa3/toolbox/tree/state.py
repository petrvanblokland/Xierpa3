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
from copy import copy
from xierpa3.toolbox.parsers.c_json import cjson
from basenode import BaseNode
from xierpa3.toolbox.transformer import TX

class State(BaseNode):
    u"""
    A ``State`` instance holds the current state of style parameters while rendering a set of styles
    in a canvas or CSS. If the state refers to a style, then this is used to get cascading values from, in case
    the current set of attributes does not contain the requested name. Setting values, however, only takes
    place on the state attribute set, so the styles set will never be written.<br/>
    
    The ``State`` as final <quote>leaf</quote> underneath a cascading ``Style`` tree, can be
    seen as a sketch pad that hold the rendered values and stores any changed value, so it  will not damage the
    fixed styles.<br/>
    
    ``State`` instances are used in various places where several sides need to share the save values
    and where the set of values is undefined or expanding in the future. Examples are the state sharing between
    ``ImageBuilder`` and ``Canvas`` or the sharing between the main ``SiteBuilder``
    application and window instances.
    """

    def __init__(self, attributes=None, form=None, **args):
        u"""
        The ``__init__`` constructor takes the optional ``style`` attribute and stores is. If
        it is defined, then this reference to the style node is used a default source if the name of an
        attribute request does not exist in the current attribute set.<br/>
        
        If the ``form`` is defined, then copy all form attribute in/over the
        ``self._attributes`` values. This is convenient if a state needs to be populated with values
        from ``self.e.form``.
        """
        self._attributes = self.getNewAttributes(attributes, (args, form))

    def __getattr__(self, name):
        u"""
        The ``state.name`` (``__getattr__``) interprets the ``name`` attribute. If
        it does not exist, then the content of ``self._style`` is tested. If it does not exist, then
        ``None`` is answered, so it does not have to be initialized.
        """
        if name.startswith('_'):
            return self.__dict__.get(name)
        return self[name]

    def __setattr__(self, name, value):
        if name.startswith('_'):
            self.__dict__[name] = value
        self[name] = value

    def __setitem__(self, name, value):
        u"""
        The ``set`` (or ``state[name] = value``) method sets the attribute ``name`` to
        ``value``. This value is stored locally in the attributes dictionary of the state instance. It will not
        alter the style it may reference. Also it will block any further searching in the cascading set of style values,
        since the locally stored value is found on any next request for that name.
        """
        self._attributes[name] = value

    set = __setitem__

    def __getitem__(self, name):
        u"""
        The ``get`` (or ``state[name]``) method answers the state attribute named ``name
        ``.
        """
        value = self._attributes.get(name)
        return value

    get = __getitem__

    def getState(self):
        u"""
        The ``getState`` method is allowed for compatibility reasons with ``Style`` instances.
        The behavior is to answers a copy of ``self``.
        """
        return self.__class__(attributes=copy(self.getAttributes()))

    _copy = getState

    def _getUniqueAttrsId(self):
        u"""
        The ``_getUniqueAttrsId`` method answers the semi-unique id of the ``self`` attributes
        dictionary. This can be used to get a kind-of unique parameter for a given set of attribute values.
        """
        return hash(`self._attributes`)

    @classmethod
    def _fromDict(cls, d):
        return cls(d)

    @classmethod
    def _fromObject(cls, o):
        if isinstance(o, (list, tuple)):
            result = [] # Answer a list of states
            for d in o:
                result.append(cls._fromObject(d))
        elif isinstance(o, dict):
            result = cls() # Answer a single state
            for key, value in o.items():
                result[key] = cls._fromObject(value)
        else:
            result = o
        return result

    @classmethod
    def _asObject(cls, o):
        if isinstance(o, basestring):
            result = o
        elif isinstance(o, (long, int, float)):
            result = o
        elif o is None:
            result = 'None'
        elif isinstance(o, cls):
            result = {}
            for name, attr in o.getAttributes().items():
                result[name] = cls._asObject(attr)
        elif isinstance(o, (list, tuple)):
            result = []
            for oo in o:
                result.append(cls._asObject(oo))
        elif isinstance(o, dict):
            result = {}
            for key, item in o.items():
                result[TX.asString(key)] = cls._asObject(item)
        else:
            result = `o`
        return result

    @classmethod
    def _fromJson(cls, s):
        u"""
        If s evaluates to a list, then assume that the contents are dictionaries, which all convert to a single
        state. If s evaluates to a dict, then create a single state.
        """
        assert isinstance(s, basestring)
        return cls._fromObject(cjson.encode(s))

    def _asJson(self):
        u"""
        Convert self to an object of standard Python instances, so it can be dumped by JSON.
        """
        return cjson.decode(self._asObject(self))

