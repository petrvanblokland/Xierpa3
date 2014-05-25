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
#    gradient.py
#
from xierpa3.attributes.attribute import Attribute

class Gradient(Attribute):
    """
    background-image: linear-gradient(left , rgb(213, 213, 213) 35%, rgb(248, 248, 248) 82%);
    background-image: -o-linear-gradient(left , rgb(213, 213, 213) 35%, rgb(248, 248, 248) 82%);
    background-image: -moz-linear-gradient(left , rgb(213, 213, 213) 35%, rgb(248, 248, 248) 82%);
    background-image: -webkit-linear-gradient(left , rgb(213, 213, 213) 35%, rgb(248, 248, 248) 82%);
    background-image: -ms-linear-gradient(left , rgb(213, 213, 213) 35%, rgb(248, 248, 248) 82%);
    background-image: -webkit-gradient(
        linear,
        left top,
        right top,
        color-stop(0.35, rgb(213, 213, 213)),
        color-stop(0.82, rgb(248, 248, 248))
        );     
    """
    def __init__(self, side, c1, p1, c2, p2, type=None, **kwargs):
        # The Shadow class builds the prefix dependent CSS syntax for a linear gradient attribute.
        #
        #    backgroundimage=LinearGradient('left', 'rgb(179,179,181)', 35, 'rgb(130,132,135)', 82), 
        #
        self.type = type
        self.side = side
        self.c1 = c1 # Start color
        self.p1 = p1 # Percentage in 100 of start
        self.c2 = c2 # End color
        self.p2 = p2 # Percentage in 100 of end
        self.initializePrefixes(kwargs) # Initialize any child prefix attributes
    
    def _get_value(self):
        if self.side == 'left':
            side1, side2 = 'left', 'right'
        else:
            side2, side1 = 'right', 'left'
        return '%s, %s top, %s top, color-stop(%0.2f, %s), color-stop(%0.2f, %s)' % \
            (self.type or '', side1, side2, self.p1/100.0, self.c1, self.p2/100.0, self.c2)

    value = property(_get_value)
    
    def _get_raw(self):
        return self.id, self.type, self.side, self.c1, self.p1, self.c2, self.p2
    
    raw = property(_get_raw)
              
    def build(self, name, builder, prefix=None):
        # Build the instance output on the (sass/css) builder
        if prefix is None: # This is the top call, do the other prefixes
            for prefix in self.PREFIXES:
                gradient = self.prefixes.get(prefix) or self.__class__(self.side, self.c1, self.p1, self.c2, self.p2, self.type, prefix=prefix)
                gradient.build(name, builder, prefix)
            sprefix = ''
        else:
            sprefix = '-%s-' % prefix
        builder.output('%s: %sgradient(%s);' % (name, sprefix, self.value))
        builder.tabs()
        
class LinearGradient(Gradient):
    
    # self.value
       
    def _get_value(self):
        return '%s, %s, %s%%, %s, %s%%' % (self.side, self.c1, self.p1, self.c2, self.p2)
        
    value = property(_get_value)        

    def build(self, name, builder, prefix=None):
        hook = 'build_' + builder.ID
        if hasattr(self, hook):
            getattr(self, hook)(name, builder, prefix)
            
    def build_css(self, name, builder, prefix=None):
        # Build the instance output on the (sass/css) builder
        if prefix is None:
            sprefix = ''
        else:
            sprefix = '-%s-' % prefix
        builder.output('%s: %slinear-gradient(%s);' % (name, sprefix, self.value))
        builder.tabs()
        if prefix is None: # This is the top call, do the other prefixes
            for prefix in self.PREFIXES:
                linearGradient = self.prefixes.get(prefix) or self.__class__(self.side, self.c1, self.p1, self.c2, self.p2, None, prefix=prefix)
                linearGradient.build(name, builder, prefix)
                if prefix == 'webkit':
                    gradient = Gradient(self.side, self.c1, self.p1, self.c2, self.p2, 'linear', prefix=prefix)
                    gradient.build(name, builder, prefix)

    def build_html(self, name, builder, prefix=None):
        u"""Html gradient must be inside an svg canvas
        self.c1 = c1 # Start color
        self.p1 = p1 # Percentage in 100 of start
        self.c2 = c2 # End color
        self.p2 = p2 # Percentage in 100 of end
        """
        return """
          <defs>
            <linearGradient id="%(name)s" x1="%(x1)s%%" y1="%(y1)s%%" x2="%(x2)s%%" y2="%(y2)s%%">
              <stop offset="0%%" style="stop-color:%(c1)s;stop-opacity:1" />
              <stop offset="100%%" style="stop-color:%(c2)s;stop-opacity:1" />
            </linearGradient>
          </defs>            
        """ % dict(name=name, c1=self.c1, c2=self.c2, x1=0, x2=100, y1=0, y2=100 )
