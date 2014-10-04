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
#    nothing.py
#
from xierpa3.components import Component

class Nothing(Component):
    u"""Place holder component, doing nothing. Can be used to debug pages with multiple components."""

    def build(self, b):
        pass
