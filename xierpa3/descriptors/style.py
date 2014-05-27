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
#   style.py
#
#   Implements Style(), Media() and 
import weakref
import hashlib
from xierpa3.descriptors.state import State
from xierpa3.descriptors.media import Media

class Style(State):
    u"""The <b>Style</b> holds a set of style values for a components and the constructors inside the component block builders."""
    
    def __init__(self, selector=None, parent=None, component=None, **kwargs):
        u"""
        Constructor of a new style. The self.media holds a list of styles related to a specific @media size range of self.
        """
        assert parent is None or isinstance(parent, Style)
        State.__init__(self, **kwargs)
        self._uid = None
        self.selector = selector # If omitted, then just build the block, not the selector open/close.
        self.component = component
        self.parent = parent # Parent, can be None, will be filled when style is attached to a parent.
        self.media = [] # Can be overwritten by key/value in kwargs.
        self.styles = [] # Children styles of this style

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.selector or self.name or self.id or 'Untitled')

    def addMedia(self, selector, min=None, max=None, expression=None, **kwargs):
        u"""
        Create a new Media instance for @media content. The parameters @condition, @min and @max are expected 
        in the arguments as parameters for the @media. They are ignored in the content of the @media block. 
        Set to same selector and component, so CSS knows context. 
        Answer the created media style for convenience.
        """
        media = Media(selector, self, min, max, expression, **kwargs)
        self.media.append(media)
        return media

    def addStyle(self, selector=None, **kwargs):
        u"""
        Selector can be omitted, then just the block will be send to output. Answer the created style instance for
        convenience.
        """
        style = Style(selector, parent=self, component=self.component, **kwargs)
        self.styles.append(style)
        return style

    def add(self, d):
        for key, value in d.items():
            self[key] = value

    def isEmpty(self):
        u"""
        Answer the boolean flag if this Style instance is empty.
        """
        return len(self.styles) == 0

    # self.parent

    def _get_parent(self):
        if self._parent is not None:
            return self._parent()
        return None

    def _set_parent(self, parent):
        if parent is not None:
            if isinstance(parent, int):
                pass
            parent = weakref.ref(parent)
        self._parent = parent
        # Now we have a parent style, forget about any current component reference.
        self._component = None

    parent = property(_get_parent, _set_parent)

    # self.hashedID

    def _get_hashedID(self):
        u"""
        Calculate the unique hashed ID based on the content. This ID can be compared between components to decide if they
        are identical. This is used by the CSS builder to decide of styles can be skipped then they are identical. Note that
        the value is cache, so alterations to the content of children don't reflect in the ID, once it is established.
        """
        if self._hashedID is None:
            m = hashlib.md5()
            if self.selector:
                m.update(self.selector)
            for media in self.media:
                m.update(media.hashedID)
            for style in self.styles:
                m.update(style.hashedID)
            self._hashedID = m.digest()
        return self._hashedID

    hashedID = property(_get_hashedID)

    # self.component

    def _set_component(self, component):
        if component is not None:
            self._component = weakref.ref(component)
        else:
            self._component = None

    def _get_component(self):
        parent = self.parent
        if parent is not None:
            return parent.component
        # His happens when the style is a root. The self._component should be defined then.
        if self._component is not None:
            return self._component()
        return None # No component or parent style defined

    component = property(_get_component, _set_component)

    # self.components

    def _get_components(self):
        u"""
        Answer the list of parents (=component, not style). If there is no parent, answer an empty list.
        """
        component = self.component
        if component is not None:
            return component.parents + [component]
        return []

    components = property(_get_components)

    # self.selector   Answer the value of self._selector
    # Note that there is a difference between self.selector and self.component.selector

    def _get_selector(self):
        return self._selector

    def _set_selector(self, selector):
        self._selector = selector

    selector = property(_get_selector, _set_selector)

class StyleSet(Style):
    u"""The <i>StyleSet</i> class is a wrapper set around a set of classes. It behaves like
    a <i>Style</i> instance, but it does not show up as selector. The open and close
    output code is ignore, because <b>self.selector</b> always answers <b>None</b>."""

    def _get_selector(self):
        return None

    def _set_selector(self, selector):
        pass # Ignore the selector

    selector = property(_get_selector, _set_selector)

