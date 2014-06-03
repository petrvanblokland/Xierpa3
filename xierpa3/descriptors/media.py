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
#   media.py
#
import weakref
from xierpa3.descriptors.state import State
from xierpa3.toolbox.transformer import TX

class Media(State):
    def __init__(self, selector=None, parent=None, min=None, max=None, expression=None, **kwargs):
        assert parent is None or isinstance(parent, State)
        State.__init__(self, **kwargs)
        self.selector = selector
        self.min = min
        self.max = max
        self.expression = expression
        self.parent = parent

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

    parent = property(_get_parent, _set_parent)

    # self.expression     @media selector expression

    def _get_expression(self):
        expressions = []
        if self.min:
            expressions.append('(min-width:%s)' % TX.px(self.min))
        if self.max:
            expressions.append('(max-width:%s)' % TX.px(self.max))
        if self.device or expressions:
            return (self.device or 'all') + ' and ' + ' and '.join(expressions)
        return None # Raising error, style as media needs a defined expression

    def _set_expression(self, expression):
        self._expression = expression

    expression = property(_get_expression, _set_expression)

