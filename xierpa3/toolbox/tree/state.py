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
    A <code>State</code> instance holds the current state of style parameters while rendering a set of styles
    in a canvas or CSS. If the state refers to a style, then this is used to get cascading values from, in case
    the current set of attributes does not contain the requested name. Setting values, however, only takes
    place on the state attribute set, so the styles set will never be written.<br/>
    
    The <code>State</code> as final <quote>leaf</quote> underneath a cascading <code>Style<code> tree, can be
    seen as a sketch pad that hold the rendered values and stores any changed value, so it  will not damage the
    fixed styles.<br/>
    
    <code>State</code> instances are used in various places where several sides need to share the save values
    and where the set of values is undefined or expanding in the future. Examples are the state sharing between
    <code>ImageBuilder</code> and <code>Canvas</code> or the sharing between the main <code>SiteBuilder</code>
    application and window instances.
    """

    def __init__(self, attributes=None, form=None, **args):
        u"""
        The <code>__init__</code> constructor takes the optional <attr>style</attr> attribute and stores is. If
        it is defined, then this reference to the style node is used a default source if the name of an
        attribute request does not exist in the current attribute set.<br/>
        
        If the <attr>form</attr> is defined, then copy all form attribute in/over the
        <code>self._attributes</code> values. This is convenient if a state needs to be populated with values
        from <code>self.e.form</code>.
        """
        self._attributes = self.getNewAttributes(attributes, (args, form))

    def __getattr__(self, name):
        u"""
        The <code>state.name</code> (<code>__getattr__</code>) interprets the <attr>name</attr> attribute. If
        it does not exist, then the content of <code>self._style</code> is tested. If it does not exist, then
        <code>None</code> is answered, so it does not have to be initialized.
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
        The <code>set</code> (or <code>state[name] = value</code>) method sets the attribute <attr>name</attr> to
        <attr>value</attr>. This value is stored locally in the attributes dictionary of the state instance. It will not
        alter the style it may reference. Also it will block any further searching in the cascading set of style values,
        since the locally stored value is found on any next request for that name.
        """
        self._attributes[name] = value

    set = __setitem__

    def __getitem__(self, name):
        u"""
        The <code>get</code> (or <code>state[name]</code>) method answers the state attribute named <attr>name
        </attr>.
        """
        value = self._attributes.get(name)
        return value

    get = __getitem__

    def getState(self):
        u"""
        The <code>getState</code> method is allowed for compatibility reasons with <code>Style</code> instances.
        The behavior is to answers a copy of <code>self</code>.
        """
        return self.__class__(attributes=copy(self.getAttributes()))

    _copy = getState

    def _getUniqueAttrsId(self):
        u"""
        The <code>_getUniqueAttrsId</code> method answers the semi-unique id of the <code>self</code> attributes
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

