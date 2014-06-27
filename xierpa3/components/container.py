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
from xierpa3.attributes import Perc, Margin, Em
from xierpa3.descriptors.blueprint import BluePrint
from xierpa3.descriptors.media import Media # Include type of Style that holds @media parameters.

class Container(Component):
    u"""The <b>Container</b> is the generic component that hold most other components on a page.
    Containers are always two-layered: a component div to position on a page with a row-div inside
    that handles the responsive behavior of the content."""
    CC = Component # Access of constants through parent class.

    BLUEPRINT = BluePrint( 
        # Page/Column
        paddingLeft=Em(1), doc_paddingLeft=u'Padding left of main container.',
        paddingRight=Em(1), doc_paddingRight=u'Padding left of main container.',
        # Row
        rowMargin=Margin(0, CC.AUTO), doc_margin=u'Row margin. This makes the main container (page) center on maxwidth.', 
        rowMinWidth=CC.M_MOBILE_MAX, doc_rowMinWidth=u'Minimum width of the row inside a container. Default is %d.' % CC.M_MOBILE_MAX,
        rowMaxWidth=CC.MAXWIDTH, doc_rowMaxWidth=u'Maximum width of the row inside a container. Default is %d.' % CC.MAXWIDTH,     
        rowWidth=Perc(100), doc_rowWidth=u'Default width of a row inside a container.',
    )
    
    def buildBlock(self, b):
        u"""Build the container-div with a row-div inside."""
        s = self.style
        b.div(class_=self.getClassName(), paddingleft=s.paddingLeft, paddingright=s.paddingRight) 
        b.div(class_=self.CLASS_ROW, margin=s.rowMargin, width=s.rowWidth, 
            maxwidth=s.rowMaxWidth, minwidth=s.rowMinWidth, 
            media=(
               Media(max=self.M_MOBILE_MAX, width=Perc(100), minwidth=0),
        ))
        for component in self.components:
            component.build(b)
        b._div(comment='.'+self.CLASS_ROW) # Comment class at end of row
        b._div(comment='.'+self.getClassName()) # Comment the class at end of container
        
