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
#    example/svg.py
#
from xierpa3.components.component import Component
from xierpa3.attributes import Px, Perc, Color
from xierpa3.attributes import LinearGradient
from xierpa3.descriptors.blueprint import BluePrint

CHAPTERCOLOR = Color('#202020')
SUMMARYCOLOR= CHAPTERCOLOR
CHAPTERTITLECOLOR0 = Color('#1F1F1F')
H2COLOR = Color('#828487')
AUTHORCOLOR = H2COLOR
CATEGORYCOLOR = AUTHORCOLOR
LABELCOLOR = AUTHORCOLOR
LEADCOLOR = AUTHORCOLOR
NAMECOLOR= Color('#66696C') 
TITLECOLOR= NAMECOLOR

class SvgExample(Component):

    C = Component.C
    
    BLUEPRINT = BluePrint(
        height=Px(250), doc_height=u'Svg canvas height', 
        width=Perc(100), doc_width=u'Svg canvas width',               
    )
    def build_html(self, b):
        u"""Do all as build for CSS."""
        # if b.isType('scss'): # If generating CSS, there are no selected banners. Add some fake data here for 2 columns.
        self.demoSvgDrawing1(b)
        self.demoSvgDrawing2(b)

    def draw(self, b, drawingId):
        u"""Simple direct draw if used inside the liquid of a text columns, e.g. through 
        XML transformer part of a builder."""
        hook = 'demoSvgDrawing%s' % drawingId
        if hasattr(self, hook):
            b.div(class_='svgDemo')
            getattr(self, hook)(b)
            b._div()
        
    def demoSvgDrawing1(self, b):
        # Draw a responsive image in SVG, only in 
        #b.div(class_='svgDemo', display=C.BLOCK, margintop=Em(0.5), marginbottom=Em(0.5),
        #    media=Media(max=C.M_MOBILE_MAX, display=C.NONE))
        s = self.style
        b.svg(width=s.width, height=s.height)
        b.rect(width=Perc(100), height=50, fill=LinearGradient('left', '#000', 0, '#FFF', 100))
        b.rect(y=50, width=Perc(100), height=200, fill='green')
        # Perspective line
        b.line(x1=30, y1=Perc(100), x2=Perc(50), y2=50, stroke='yellow', strokewidth=3)
        b.line(x1=Perc(70), y1=Perc(100), x2=Perc(50), y2=50, stroke=Color('yellow'), strokewidth=3, display=self.C.NONE)

        b.ellipse(x=80, y=150, rx=40, ry=10, fill='black', fillopacity=0.2)
        b.filter('frozenLiquid')
        b.circle(x=80, y=80, r=40, strokewidth=3, stroke='black', fill='red', fillopacity=0.5)
        b.circle(x=80, y=80, r=20, fill=Color('green'), fillopacity=0.5)
        b._filter()
        b.circle(x=65, y=65, r=10, fill=Color('white'), fillopacity=0.2)

        b.ellipse(x=Perc(50), y=Perc(50), rx=40, ry=10, fill='black', fillopacity=0.5)
        b.circle(x=Perc(50), y=50, r=40, strokewidth=3, stroke='black', fill=Color('red'), fillopacity=0.5)
        b.circle(x=Perc(50), y=50, r=20, fill=Color('green'), fillopacity=0.5)
        b.circle(x=Perc(48), y=35, r=10, fill=Color('white'), fillopacity=0.6) 

        #b.text('Xierpa3', fill='#FFF', fontsize=45, fontfamily='Verdana', x=100, y=100)

        b._svg()
        
    def demoSvgDrawing2(self, b):
        # Draw a responsive image in SVG
        #b.div(class_='svgDemo', display=C.NONE, margintop=Em(0.5), marginbottom=Em(0.5),
        #    media=Media(max=C.M_MOBILE_MAX, display=C.BLOCK))
        s = self.style
        b.svg(width=s.width, height=s.height)
        b.rect(width=Perc(100), height=100, fill=Color('cyan'))
        b.rect(y=100, width=Perc(100), height=150, fill=Color('green'))
        # Polygons don't work in %, so they cannot be positioned responsive to the container width
        b.rect(x=Perc(5), y=20, width=Perc(8), height=200, fill=Color('yellow'), fillopacity=0.5)
        b.filter('blur', blur=4)
        b.rect(x=Perc(20), y=20, width=Perc(5), height=200, fill=Color('yellow'))
        b._filter()
        # Neon
        b.filter('neon')
        b.rect(x=Perc(35), y=20, rx=12, ry=12, width=32, height=200, fill=self.C.NONE, stroke='red', strokewidth=6)
        b._filter()
        b.filter('neon')
        b.rect(x=Perc(50), y=20, rx=16, ry=16, width=32, height=200, fill=self.C.NONE, 
            fillopacity=0.5, stroke=Color('blue'), strokewidth=20)
        b._filter()
        b.filter('frozenLiquid') # @@@ Should not change the overall color of the image.
        b.rect(x='68%', y=20, rx=16, ry=16, width=32, height=200, fill=Color('#D0D0D0'), 
            fillopacity=0.5, stroke=Color('blue'), strokewidth=20)
        b._filter()
        b._svg()

        #b.polygon(points="140,40 160,40 180,210 130,210", fill='yellow')

