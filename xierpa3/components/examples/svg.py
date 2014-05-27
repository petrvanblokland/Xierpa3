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
from xierpa3.constants.constants import C
#from xierpa3.attributes import Em
from xierpa3.attributes import LinearGradient

CHAPTERCOLOR = '#202020'
CHAPTERTITLECOLOR0 = '#1F1F1F'
AUTHORCOLOR = '#828487'
CATEGORYCOLOR = '#828487'
LABELCOLOR = '#828487'
LEADCOLOR = '#828487'
NAMECOLOR= '#66696C'
TITLECOLOR= '#66696C'
SUMMARYCOLOR= '#202020'
H2COLOR = '#828487'

class SvgExample(Component):

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
        b.svg(width='100%', height=250)
        b.rect(width='100%', height=50, fill=LinearGradient('left', '#000', 0, '#FFF', 100))
        b.rect(y=50, width='100%', height=200, fill='green')
        # Perspective line
        b.line(x1=30, y1='100%', x2='50%', y2=50, stroke='yellow', strokewidth=3)
        b.line(x1='70%', y1='100%', x2='50%', y2=50, stroke='yellow', strokewidth=3, display=C.NONE)

        b.ellipse(x=80, y=150, rx=40, ry=10, fill='black', fillopacity=0.2)
        b.filter('frozenLiquid')
        b.circle(x=80, y=80, r=40, strokewidth=3, stroke='black', fill='red', fillopacity=0.5)
        b.circle(x=80, y=80, r=20, fill='green', fillopacity=0.5)
        b._filter()
        b.circle(x=65, y=65, r=10, fill='white', fillopacity=0.2)

        b.ellipse(x='50%', y='50%', rx=40, ry=10, fill='black', fillopacity=0.5)
        b.circle(x='50%', y=50, r=40, strokewidth=3, stroke='black', fill='red', fillopacity=0.5)
        b.circle(x='50%', y=50, r=20, fill='green', fillopacity=0.5)
        b.circle(x='48%', y=35, r=10, fill='white', fillopacity=0.6) 

        #b.text('Xierpa3', fill='#FFF', fontsize=45, fontfamiy='Verdana', x=100, y=100)

        b._svg()
        
    def demoSvgDrawing2(self, b):
        # Draw a responsive image in SVG
        #b.div(class_='svgDemo', display=C.NONE, margintop=Em(0.5), marginbottom=Em(0.5),
        #    media=Media(max=C.M_MOBILE_MAX, display=C.BLOCK))
        b.svg(width='100%', height=250)
        b.rect(width='100%', height=100, fill='cyan')
        b.rect(y=100, width='100%', height=150, fill='green')
        # Polygons don't work in %, so they cannot be positioned responsive to the container width
        b.rect(x='5%', y=20, width='8%', height=200, fill='yellow', fillopacity=0.5)
        b.filter('blur', blur=4)
        b.rect(x='20%', y=20, width='8%', height=200, fill='yellow')
        b._filter()
        # Neon
        b.filter('neon')
        b.rect(x='35%', y=20, rx=12, ry=12, width=32, height=200, fill=C.NONE, stroke='red', strokewidth=6)
        b._filter()
        b.filter('neon')
        b.rect(x='50%', y=20, rx=16, ry=16, width=32, height=200, fill=C.NONE, 
            fillopacity=0.5, stroke='blue', strokewidth=20)
        b._filter()
        b.filter('frozenLiquid') # @@@ Should not change the overall color of the image.
        b.rect(x='68%', y=20, rx=16, ry=16, width=32, height=200, fill='#D0D0D0', 
            fillopacity=0.5, stroke='blue', strokewidth=20)
        b._filter()
        b._svg()

        #b.polygon(points="140,40 160,40 180,210 130,210", fill='yellow')

