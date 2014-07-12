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
#    blog.py
#
from xierpa3.components.component import Component
from xierpa3.attributes import Perc
from xierpa3.descriptors.blueprint import BluePrint

class BlogResponse(Component):
    u"""The <b>Menu</b> supports a generic menu, setup as a list of links. The menu items are supplied
    by adapter id <b>C.ADAPTER_MENU</b>."""
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Component.C 
    
    BLUEPRINT = BluePrint(
        # Block stuff
        width=Perc(100), doc_width=u'Width of the component.',
    )
    def buildBlock(self, b):
        u"""Build the @BlogResponse@ component."""
        s = self.style
        b.block(self)
        colClass = self.getColClass(s.colWidth)
        b.div(class_=colClass)
        # TODO: Add blog response form here.
        b.text('AAAAAAAAAAA')
        b._div(comment=colClass)
        b._block(self)
