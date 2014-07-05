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
#    attribute.py
#
from xierpa3.constants.constants import Constants

class Attribute(object):

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Constants 
           
    def initializePrefixes(self, d):
        self.prefixes = {}
        for prefix, attribute in d.items():
            if prefix in self.C.PREFIXES:
                assert isinstance(attribute, self.__class__)
                self.prefixes[prefix] = attribute

    def _get_raw(self):
        return self.id, self._value
    
    raw = property(_get_raw)
        
    def _get_id(self):
        return self.__class__.__name__
    
    id = property(_get_id)
    
