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
#    shadow.py
#
from xierpa3.constants.constants import C
from xierpa3.attributes.attribute import Attribute
from xierpa3.attributes.values import asValue

class Shadow(Attribute):
    
    def __init__(self, t, r, b, l, color, **kwargs):
        #
        # The Shadow class builds the prefix dependent CSS syntax for a shadow attribute.
        #
        #    boxshadow=Shadow(0, 4, 10, -2, '#333'),
        #
        #    box-shadow: 0 4px 10px -2px #333;
        #    -webkit-box-shadow: 0 4px 10px -2px #333;
        #    -ms-box-shadow: 0 4px 10px -2px #333;
        #    -moz-box-shadow: 0 4px 10px -2px #333;
        #    -o-box-shadow: 0 4px 10px -2px #333;
        #
        #    Width different prefix values
        #    boxshadow=Shadow(0, 4, 10, -2, '#333', webkit=Shadow(0, 8, 10, -2, '#FFF')),
        #
        #    box-shadow: 0 4px 10px -2px #333;
        #    -webkit-box-shadow: 0 8px 10px -2px #FFF;
        #    -ms-box-shadow: 0 4px 10px -2px #333;
        #    -moz-box-shadow: 0 4px 10px -2px #333;
        #    -o-box-shadow: 0 4px 10px -2px #333;
        #
        self.t = t
        self.r = r
        self.b = b
        self.l = l
        self.color = color
        self.initializePrefixes(kwargs) # Initialize any child prefix attributes
    
    # self.value
       
    def _get_value(self):
        return '%s %s %s %s %s' % (asValue(self.t), asValue(self.r), asValue(self.b), asValue(self.l), self.color)
        
    value = property(_get_value)        

    def _get_raw(self):
        return self.id, self.t, self.r, self.b, self.l, self.color
    
    raw = property(_get_raw)

    def build(self, name, builder, prefix=None):
        # Build the instance output on the (sass/css) builder
        if prefix is None: # This is the top call, do the other prefixes
            for prefix in C.PREFIXES:
                shadow = self.prefixes.get(prefix) or self.__class__(self.t, self.r, self.b, self.l, self.color, prefix=prefix)
                shadow.build(name, builder, prefix)
            sprefix = ''
        else:
            sprefix = '-%s-' % prefix
        builder.output('%s%s: %s;' % (sprefix, name, self.value))
        builder.tabs()
            
