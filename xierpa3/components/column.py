# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#    column.py
#
from xierpa3.components.container import Container
from xierpa3.attributes import Em
from xierpa3.descriptors.style import Media

class Column(Container):

    def buildBlock(self, b):
        u"""Build the block of a column. Note that for clarity fontsize and lineheight are defined
        for each part separated, relation the overall container fontsize and lineheight.
        Classes inheriting from <b>Column</b> should implement <b>self.buildBlock</b>."""
        s = self.style
        colClass = self.getColClass(s.colWidth)
        b.block(self)
        b.div(class_=colClass, marginright=s.colMarginRight, marginleft=s.colMarginLeft,
            margintop=s.colMarginTop or Em(1),
            paddingleft=s.paddingLeft or 0, float=s.colFloat, display=s.colDisplay,
            minheight=s.colMinHeight,   
            media=Media(max=self.M_MOBILE_MAX, display=self.BLOCK, float=self.NONE, width=self.AUTO,
                marginleft=0, marginright=0, paddingleft=Em(0.5), paddingright=Em(0.5))
            )
        self.buildColumn(b)
        b._div(comment=colClass)
        b._block(self) 
        
    def buildColumn(self, b):
        b.error('Classes inheriting from <b>Column</b> should implement <b>self.buildColumn(b)</b>.')
        
