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
        backgroundColor=None, doc_backgroundColor=u'Background color of the logo component.',
        height=C.AUTO, doc_height=u'Logo height', 
        marginTop=0, doc_marginTop=u'Logo margin top', 
        marginLeft=0, doc_marginLeft=u'Logo margin left',
        marginRight=Perc(1.8), doc_marginRight=u'Logo margin right', 
        marginBottom=0, doc_marginBottom=u'Logo margin bottom',
        logoFloat=C.LEFT, doc_logoFloat=u'Logo div float',
        # H2 heading, in case style.text is defined and not style.src (for an image)
        fontFamily=C.LOGOFAMILY, doc_fontFamily=u'h2 font family',
        fontSize=Em(2.9), doc_fontSize=u'h2 Logo font size',
        lineHeight=Em(1.4), doc_lineHeight=u'h2 leading',
        fontWeight=C.BOLD, doc_fontWeight=u'h2 font weight',
        fontStyle=None, doc_fontStyle=u'h2 font style',
        paddingTop=Em(0.2), doc_paddingTop=u'h2 padding top',
        paddingBottom=Em(0.2), doc_paddingBottom=u'h2 padding bottom',
        color=Color('#323A47'), doc_color=u'h2 color',
    )
    def buildBlock(self, b):
        s = self.style
        colClass = self.getColClass(s.colWidth)
        b.div(class_=colClass, float=s.logoFloat, marginleft=s.marginLeft, backgroundcolor=s.backgroundColor,
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
            b.h2(fontsize=s.fontSize, lineheight=s.lineHeight, fontfamily=s.fontFamily,
                 fontWeight=s.h2Weight, fontStyle=s.h2Style, color=s.color,
                 paddingtop=s.paddingTop, paddingbottom=s.paddingBottom,
            )
            b.text(data.text)
            b._h2()
        if data.url:
            b._a()
        b._div(comment=colClass)
