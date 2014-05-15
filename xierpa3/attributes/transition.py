# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#    shadow.py
#
from xierpa3.constants.constants import C
from xierpa3.toolbox.transformer import TX 
from xierpa3.attributes.attribute import Attribute

class Transition(Attribute):
    
    def __init__(self, **kwargs):
        #
        # The Transition class builds the prefix dependent CSS syntax for a transition attribute.
        #
        #    boxshadow=Transition(width=2, height=2)       
        #
        self.attributes = {}
        for key, value in kwargs.items():
            if key in C.PREFIXES or key == 'prefix':
                continue
            self.attributes[key] = value
        self.initializePrefixes(kwargs)

    def _get_raw(self):
        return self.id, self.width, self.height
    
    raw = property(_get_raw)

    def build(self, name, builder, prefix=None):
        # Build the instance output on the (sass/css) builder
        if prefix is None: # This is the top call, do the other prefixes
            for prefix in C.PREFIXES:
                shadow = self.prefixes.get(prefix) or self.__class__(prefix=prefix, **self.attributes)
                shadow.build(name, builder, prefix)
            sprefix = ''
        else:
            sprefix = '-%s-' % prefix
        output = []
        for attribute, value in self.attributes.items():
            if attribute in ('transition',):
                attribute = sprefix + attribute
            output.append('%s %s' % (attribute, value))
        builder.output('%s%s: %s;' % (sprefix, name, ', '.join(output)))
        builder.tabs()
            
