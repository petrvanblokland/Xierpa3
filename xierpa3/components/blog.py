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
from xierpa3.attributes import Perc, Color
from xierpa3.descriptors.blueprint import BluePrint
from xierpa3.descriptors.media import Media

class BlogResponse(Component):
    u"""The <b>Menu</b> supports a generic menu, setup as a list of links. The menu items are supplied
    by adapter id <b>C.ADAPTER_MENU</b>."""
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Component.C 
    
    BLUEPRINT = BluePrint(
        # Block stuff
        width=Perc(100), doc_width=u'Width of the component.',
        backgroundColor=Color('#DDD'), doc_backgroundColor=u'Background color of the component.',
    )
    def buildBlock(self, b):
        u"""Build the @BlogResponse@ component."""
        s = self.style
        b.div(class_=self.getClassName(), backgroundcolor=s.backgroundColor, float=self.C.LEFT, 
            width=s.width, 
            media=Media(max=self.C.M_MOBILE_MAX, width=Perc(100), display=self.C.BLOCK, 
                float=self.C.NONE),
        )
        # TODO: Add blog response form here.
        b.text('[Develop Blog Response here] ' * 20)
        b._div(comment=self.getClassName())
