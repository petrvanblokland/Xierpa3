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
from xierpa3.attributes import Em, Perc, Color
#from xierpa3.descriptors.media import Media
from xierpa3.descriptors.blueprint import BluePrint

class Logo(Component):

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Component.C 

    BLUEPRINT = BluePrint(
        # Layout stuff
        colWidth=4, doc_colWidth=u'Default amount of columns for this component.', 
        maxWidth=Perc(100), doc_maxWidth=u'Maximal width of the component',
        minWidth=Perc(100), doc_minWidth=u'Minimal width of the component',
        # Logo data can be set as through text/style attribute or through the adapter.
        # The optional url creates a link from the logo, e.g. to the home page.
        text=None, doc_text=u'Optional text of the logo. Otherwise query the adapter.',
        src=None, doc_src=u'Optional src for logo image. Otherwise query the adapter.',
        url=None, doc_url=u'Optional url for logo link. Otherwise query the adapter.',
        # Logo stuff
        width=280, doc_logoWidth=u'Logo width',
        height=C.AUTO, doc_height=u'Logo height', 
        marginTop=0, doc_marginTop=u'Logo margin top', 
        marginLeft=0, doc_marginLeft=u'Logo margin left',
        marginRight=Perc(1.8), doc_marginRight=u'Logo margin right', 
        fontSize=Em(2.9), doc_fontSize=u'Logo font size',
        marginBottom=0, doc_marginBottom=u'Logo margin bottom', 
        logoFloat=C.LEFT, doc_logoFloat=u'Logo div float',
        # H2
        h2FontFamily=C.LOGOFAMILY, doc_h2FontFamily=u'h2 font family', 
        h2Size=Em(2.8), doc_h2Size=u'h2 size',
        h2LineHeight=Em(1.4), doc_h2LineHeight=u'h2 leading',
        h2Weight=C.BOLD, doc_h2Weight=u'h2 weight',
        h2Style=None, doc_h2Style=u'h2 style',
        h2PaddingTop=Em(0.2), doc_h2PaddingTop=u'h2 padding top',
        h2PaddingBottom=Em(0.2), doc_h2PaddingBottom=u'h2 padding bottom',
        h2Color=Color('#323A47'), doc_h2Color=u'h2 color',
    )
    def buildBlock(self, b):
        s = self.style
        colClass = self.getColClass(s.colWidth)
        b.div(class_=colClass, float=s.logoFloat, marginleft=s.marginLeft,
            marginright=s.marginRight, margintop=s.marginTop, marginbottom=s.marginBottom)
        # @text: text to show instead of the logo image.
        # @url: url of href link. If None no link is made
        # @src: url of the image source.
        data = self.adapter.getLogo()
        if s.text:
            data.text = s.text
            data.src = None
        if s.src:
            data.src = s.src
            data.text = None
        if s.url:
            data.url = s.url

        if data.url:
            b.a(href=data.url)
        if data.src:
            b.img(src=data.src, width=s.width, maxwidth=s.maxWidth, height=s.height)
        else:
            b.h2(fontsize=s.h2Size, lineheight=s.h2LineHeight, 
                 fontweight=s.h2Weight, fontstyle=s.h2Style, color=s.h2Color,
                 paddingtop=s.h2PaddingTop, paddingbottom=s.h2PaddingBottom,
            )
            b.text(data.text)
            b._h2()
        if data.url:
            b._a()
        b._div(comment=colClass)
