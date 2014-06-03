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
from xierpa3.components.component import Component
from xierpa3.attributes import Margin
from xierpa3.descriptors.media import Media
from xierpa3.descriptors.blueprint import BluePrint

class Container(Component):

    BLUEPRINT = BluePrint( 
        maxColumns=Component.MAXCOL, doc_maxColumns=u'Maximum number of columns in this component.',
    )
    def initialize(self):
        s = self.style
        self.addMedia(max=self.M_MOBILE_MAX, display=s.mobileDisplay) # No header in Mobile layout
        # Check on the total width of all components and issue an error or warning if the total does not fit.
        totalWidth = 0
        for component in self.components:
            totalWidth += component.style.colWidth or 0
        if self.DEBUG: # If debugging, show some analysis about the use of columns.
            if totalWidth > s.maxColumns:
                print '### Column error ###', totalWidth, self.components  
            elif 0 < totalWidth < self.s.maxColumns:
                print '### Column warning ###', totalWidth, self.components  

    def buildBlock(self, b):
        u"""The Container is used to group components together. It shows the components combined in a single row.
        The components know their own column widths."""
        s = self.style
        b.block(self)
        containerClass = s.class_ or self.class_ or self.className
        b.div(class_=(self.CLASS_CONTAINER, containerClass), display=s.containerDisplay or self.BLOCK,
            width=s.containerWidth, height=s.containerHeight,
            marginleft=s.containerMarginLeft, margintop=s.containerMarginTop,
            paddingleft=s.containerPaddingLeft or 20, paddingright=s.containerPaddingRight or 20,
            backgroundcolor=s.containerBackgroundColor, backgroundimage=s.containerBackgroundImage,
            backgroundrepeat=s.containerBackgroundRepeat,
            media=Media(max=self.M_MOBILE_MAX, width=s.mobileContainerWidth or self.C100, 
                display=s.mobileContainerDisplay or self.BLOCK,
                minwidth=s.mobileMinWidth or 0, paddingleft=s.mobilePaddingLeft or 0,
                paddingright=s.mobilePaddingRight or 0)
            )
        self.buildBlockRow(b)
        b._div(comment=self.className)
        b._block(self)

    def buildBlockRow(self, b):
        s = self.style
        b.div(class_=self.CLASS_ROW, width=s.rowWidth or self.C100, minwidth=s.rowMinWidth or 755,
            maxwidth=s.rowMaxWidth or 1140, margin=s.rowMargin or Margin(0, self.AUTO), 
            overflow=s.rowOverflow or self.HIDDEN,
            media=Media(max=self.M_MOBILE_MAX, display=s.mobileRowDisplay or self.BLOCK,
                minwidth=0, width=self.C100, paddingleft=0, paddingright=0, margin=0)
            )
        self.buildContainerBlock(b)
        b._div(comment=self.CLASS_ROW)
        
    def buildContainerBlock(self, b):
        """Default is to build all child components. This method can be redefined by inheriting container
        components that need different behavior."""
        for component in self.components:
            component.build(b)
    