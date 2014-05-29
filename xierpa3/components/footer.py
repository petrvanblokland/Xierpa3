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
#    footer.py
#
from xierpa3.components.container import Container
from xierpa3.constants.constants import C
from xierpa3.attributes import Em
from xierpa3.descriptors.blueprint import BluePrint

class Footer(Container):

    BLUEPRINT = BluePrint( 
        # Layout stuff
        colDisplay=C.BLOCK, 
        colClear=C.BOTH, 
        colMarginBottom=Em(0.5), 
        colColor=None,
        colMarginRight='1.8%', 
        colMarginLeft=0, 
        colFloat=C.LEFT, 
        colMinHeight=1,  
        # Layout stuff
        colWidth=12, # Default amount of columns for this component       
        # Mobile stuff
        mobileDisplay=C.NONE,
        mobilePaddingTop=Em(2), 
        mobilePaddingBottom=Em(0.5), 
        mobilePaddingLeft=Em(0.5), 
        mobilePaddingRight=Em(0.5),
        mobileMarginTop=Em(2), 
        mobileMarginBottom=Em(0.5), 
        mobileMarginLeft=Em(0.5), 
        mobileMarginRight=Em(0.5),
        mobileFloat=C.NONE, 
        mobileWidth=C.AUTO,
    )
    def buildBlock(self, b):
        s = self.style
        colClass = self.getColClass(s.colWidth)
        b.block(self)
        b.div(class_=colClass, float=s.logoFloat, marginleft=s.marginLeft, marginright=s.marginRight, margintop=s.marginTop, marginbottom=s.marginBottom)
        b._div(comment=colClass)
        b._block(self)
