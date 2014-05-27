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
#    logo.py
#
from xierpa3.components.component import Component
from xierpa3.constants.constants import C
from xierpa3.attributes import Em
from xierpa3.descriptors.media import Media

class Logo(Component):

    STYLE_DEFAULT = dict(
        # Layout stuff
        logoWidth=280, colWidth=4, height=C.AUTO, marginTop=0, marginLeft=0,
        marginRight='1.8%', fontSize=Em(2.9), marginBottom=0, logoFloat=C.LEFT,
        # H2
        h2Size=Em(2.8), h2LineHeight=Em(1.4), h2fontWeight=C.BOLD, h2PaddingTop=Em(0.2), h2PaddingBottom=Em(0.2),
        h2Color='#323A47',
    )
    def buildBlock(self, b):
        s = self.style
        colClass = self.getColClass(s.colWidth)
        b.block(self)
        b.div(class_=colClass, float=s.logoFloat, marginleft=s.marginLeft,
            marginright=s.marginRight, margintop=s.marginTop, marginbottom=s.marginBottom)
        # @url: url of href link. If None no link is made
        # @src: url of the image source.
        data = self.getAdapterData(self.ADAPTER_LOGO) 
        if data.url:
            b.a(href=data.url)
        #b.img(src=data.src, width=s.logoWidth, maxwidth=self.C100, height=s.height)
        b.h2(fontsize=s.h2Size, lineheight=s.h2LineHeight, 
             fontweight=s.h2fontWeight,
             fontstyle=s.h2FontStyle, color=s.h2Color,
             paddingtop=s.h2PaddingTop, paddingbottom=s.h2PaddingBottom,
        )
        b.text('Doing by Design')
        b._h2()
        if data.url:
            b._a()
        b._div(comment=colClass)
        b._block(self)
