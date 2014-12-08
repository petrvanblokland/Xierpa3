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
from xierpa3.toolbox.coloring import Color
from xierpa3.attributes.attribute import Attribute
from xierpa3.attributes.values import asValue

class Shadow(Attribute):
    
    def __init__(self, x=0, y=0, blur=None, color=None, **kwargs):
        #
        # The Shadow class builds the prefix dependent CSS syntax for a shadow attribute.
        #
        #    boxshadow=Shadow(0, 4, 10, -2, '#333'),
        #
        #    box-shadow: 0 4px 10px #333;
        #    -webkit-box-shadow: 0 4px 10px #333;
        #    -ms-box-shadow: 0 4px 10px #333;
        #    -moz-box-shadow: 0 4px 10px #333;
        #    -o-box-shadow: 0 4px 10px #333;
        #
        #    With different prefix values
        #    boxshadow=Shadow(0, 4, 10, '#333', webkit=Shadow(0, 8, 10, '#FFF')),
        #
        #    box-shadow: 0 4px 10px #333;
        #    -webkit-box-shadow: 0 8px 10px #FFF;
        #    -ms-box-shadow: 0 4px 10px #333;
        #    -moz-box-shadow: 0 4px 10px #333;
        #    -o-box-shadow: 0 4px 10px #333;
        #
        self.x = x or 0
        self.y = y or 4
        self.blur = blur or 10
        self.color = color or Color('#333')
        self.initializePrefixes(kwargs) # Initialize any child prefix attributes
    
    # self.value
       
    def _get_value(self):
        return '%s %s %s %s' % (asValue(self.x), asValue(self.y), asValue(self.blur), self.color)
        
    value = property(_get_value)        

    def _get_raw(self):
        return self.id, self.x, self.y, self.blur, self.color
    
    raw = property(_get_raw)

    def build(self, name, builder, prefix=None):
        # Build the instance output on the (sass/css) builder
        if prefix is None: # This is the top call, do the other prefixes
            for prefix in self.C.PREFIXES:
                shadow = self.prefixes.get(prefix) or self.__class__(self.x, self.y, self.blur, self.color, prefix=prefix)
                shadow.build(name, builder, prefix)
            sprefix = ''
        else:
            sprefix = '-%s-' % prefix
        builder.output('%s%s: %s;' % (sprefix, name, self.value))
        builder.tabs()
            
