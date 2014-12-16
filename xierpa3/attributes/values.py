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
#    values.py
#
from xierpa3.toolbox.transformer import TX 
from xierpa3.attributes.attribute import Attribute

def asValue(value):
    if isinstance(value, Value):
        return value.value
    return TX.px(value)

class Value(Attribute):
    def __repr__(self):
        return '%s' % self.value

class Named(Value):
    u"""Show as Sass variable $name from the optional <i>name</i> or from the attribute name 
    instead of the value."""
    def __init__(self, value, name=None):
        self.value = value
        self.name = name

class Selection(Value):
    u"""If <i>param</i> exists as attributes in the <i>params</i>, and its value exists in 
    <i>values</i> as key, then use that value as selection. Otherwise the value of key "default"
    is used, which can be **None**, so it gets ignored by the builder."""
    def __init__(self, param, values):
        self.param = param
        self.values = values
        
    def selectFromParams(self, params):
        key = params.get(self.param)
        if key is not None:
            return self.values.get(key) or self.values.get('default')
        return None

class Z(Value):
    # Z-index shows plain number
    def __init__(self, value):
        self.value = value

class BaseCalculator(Value):
    u"""Abstract **BaseCalculator** class to support arithmetic with measurements of the same type."""
    def rawValue(self):
        return self._value
     
    def __add__(self, value):
        if isinstance(value, self.__class__):
            value = value.rawValue()
        if TX.isNumber(value):
            return self.__class__(self.rawValue() + value)
        return None
    
    def __sub__(self, value):
        if isinstance(value, self.__class__):
            value = value.rawValue()
        if TX.isNumber(value):
            return self.__class__(self.rawValue() - value)
        return None

    def __mul__(self, value):
        if isinstance(value, self.__class__):
            value = value.rawValue()
        if TX.isNumber(value):
            return self.__class__(self.rawValue() * value)
        return None

    def __div__(self, value):
        if isinstance(value, self.__class__):
            value = value.rawValue()
        if TX.isNumber(value):
            return self.__class__(self.rawValue() / value)
        return None
    
class Px(BaseCalculator):
    u"""Answer 100px"""
    def __init__(self, value):
        self._value = value
        
    def _get_value(self):
        if TX.isFloat(self._value):
            return '%0.2fpx' % self._value
        if TX.isInt(self._value):
            return '%dpx' % self._value
        return self._value

    value = property(_get_value)

class Perc(BaseCalculator):
    u"""Answer 100%"""
    def __init__(self, value):
        self._value = value
        
    def _get_value(self):
        if TX.isFloat(self._value):
            return '%0.2f%%' % self._value
        if TX.isInt(self._value):
            return '%d%%' % self._value
        return self._value
    
    value = property(_get_value)
    
class Em(BaseCalculator):
    
    def __init__(self, value):
        #
        # Em(0.2)
        # Em(2)
        # Em('$MyValue')      
        #
        self._value = value
        
    def _get_value(self):
        if TX.isFloat(self._value):
            return '%0.2fem' % self._value
        if TX.isInt(self._value):
            return '%dem' % self._value
        return self._value

    value = property(_get_value)
