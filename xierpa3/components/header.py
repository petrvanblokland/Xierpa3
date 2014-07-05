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
#    header.py
#
from xierpa3.components.container import Container

class Header(Container):
    u"""The header only shows in desktop mode."""

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Container.C 

