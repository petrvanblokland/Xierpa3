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
#    sidebar.py
#
from xierpa3.components.component import Component

class Sidebar(Component):
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Component.C 
