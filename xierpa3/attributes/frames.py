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
#    frames.py
#
from xierpa3.constants.constants import C
from xierpa3.toolbox.transformer import TX 
from xierpa3.attributes.attribute import Attribute
from xierpa3.attributes.values import asValue

class Frame(Attribute):
    
    def __init__(self, t, r=None, b=None, l=None):
        # Margin(2)
        # Margin(2,3,4,5)
        self.t = t
        self.r = r
        self.b = b
        self.l = l
        
    def _get_value(self):
        if self.r is not None and (self.b is None or self.l is None):
            return '%s %s' % (asValue(self.t), asValue(self.r))
        if self.r is None or self.b is None or self.l is None:
            return asValue(self.t)
        return '%s %s %s %s' % (asValue(self.t), asValue(self.r),asValue(self.b), asValue(self.l))
        
    value = property(_get_value)

    def build(self, name, builder, prefix=None):
        builder.output(self.value)

    def _get_raw(self):
        return self.id, self.t, self.r, self.b, self.l
    
    raw = property(_get_raw)
    
class Margin(Frame):
    pass
    
class Padding(Frame):
    pass

class Border(Frame):
    def __init__(self, v1, v2=None, v3=None):
        # Border('solid', 2, Color('E1E2E2'))
        # @@@ Can be extended by parsing the values.
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        
    def _get_value(self):
        return '%s %s %s' % (self.v1, self.v2 or '', self.v3 or '')
        
    value = property(_get_value)

    def _get_raw(self):
        return self.id, self.v1, self.v2, self.v3
    
    raw = property(_get_raw)
    
