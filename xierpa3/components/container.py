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
#    container.py
#
from xierpa3.components import Component
from xierpa3.attributes import Perc, Margin
from xierpa3.descriptors.blueprint import BluePrint
from xierpa3.descriptors.media import Media # Include type of Style that holds @media parameters.

class Container(Component):
    u"""The *Container* is the generic component that holds most other components on a page.
    Containers are always two-layered: a container @div@ to position on a page with a row @div@ inside
    that handles the responsive behavior of the content."""

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Component.C

    BLUEPRINT = BluePrint(
        # Page/Column
        paddingLeft=10, doc_paddingLeft=u'Padding left of main container.',
        paddingRight=10, doc_paddingRight=u'Padding left of main container.',
        # Row
        rowWidth=Perc(100), doc_rowWidth=u'Default width of a row inside a container.',
        rowMargin=Margin(0, C.AUTO), doc_margin=u'Row margin. This makes the main container (page) center on maxwidth.',
        rowMinWidth=C.M_MOBILE_MAX, doc_rowMinWidth=u'Minimum width of the row inside a container. Default is %d.' % C.M_MOBILE_MAX,
        rowMinWidthMobile=0, doc_rowMinWidthMobile=u'Minimum width of the row inside a container for mobile.',
        rowMaxWidth=C.MAXWIDTH, doc_rowMaxWidth=u'Maximum width of the row inside a container. Default is %d.' % C.MAXWIDTH,
        rowMaxWidthMobile=Perc(100), doc_rowMaxWidthMobile=u'Maximum width of the row inside a container for mobile.',
        rowOverflow=C.HIDDEN, doc_rowOverflow=u'Default overflow hidden inside a row inside a container.',
        rowFloat=C.NONE, doc_rowFloat=u'Default float none inside a row inside a container.',
    )

    def buildBlock(self, b):
        u"""Build the container-div with a row-div inside."""
        s = self.style
        b.div(class_=self.getClassName(), paddingleft=s.paddingLeft, paddingright=s.paddingRight,
              media=Media(max=self.C.M_MOBILE_MAX, paddingleft=0, paddingright=0)
        )
        b.div(class_=self.C.CLASS_ROW, width=s.rowWidth, margin=s.rowMargin, float=s.rowFloat,
            overflow=s.rowOverflow, maxwidth=s.rowMaxWidth, minwidth=s.rowMinWidth,
            media= # Container row has width 100% in media!
               Media(max=self.C.M_MOBILE_MAX, width=Perc(100), minwidth=s.rowMinWidthMobile,
                    maxwidth=s.rowMaxWidthMobile, float=s.rowFloat),
        )
        for component in self.components:
            component.build(b)
        b._div(comment='.'+self.C.CLASS_ROW) # Comment class at end of row
        b._div(comment='.'+self.getClassName()) # Comment the class at end of container

