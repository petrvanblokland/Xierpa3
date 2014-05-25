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
#    menu.py
#
from xierpa3.components.component import Component
from xierpa3.attributes import Em
from xierpa3.constants.constants import C

class Menu(Component):
    u"""The <b>Menu</b> supports a generic menu, setup as a list of links. The menu items are supplied
    by adapter id <b>C.ADAPTER_MENU</b>."""
    STYLE_DEFAULT = dict(
        # Block stuff
        navWidth=C.C100, navFloat=C.RIGHT, navDisplay=C.INLINE, navMargin=0, colWidth=8,
        navFontSize=Em(1.5),
        # Menu list stuff
        listStyleType=C.NONE, listDisplay=C.BLOCK, listFloat=C.RIGHT, listPadding=10,
        # Link stuff
        linkColor='#4890be', linkTextDecoration=C.NONE, linkPadding=Em(0.3), 
        linkTransition=None, #Transition(),
    )
    def buildBlock(self, b):
        u"""Build the menu from the articles in the menu tags of the home.xml document."""
        data = self.getAdapterData(self.ADAPTER_MENU, id='home')
        if data.menuItems is not None and len(data.menuItems):
            s = self.style
            b.block(self)
            colClass = self.getColClass(s.colWidth)
            b.div(class_=colClass)
            b.nav(id=self.ID_NAVIGATIONWRAP, width=s.navWidth, float=s.navFloat, display=s.navDisplay, 
                margin=s.navMargin, fontsize=s.navFontSize)
            b.ol(styletype=s.listStyleType, display=s.listDisplay)
            for menu in data.menuItems:
                b.li(float=s.listFloat, padding=s.listPadding)
                url = menu.url
                if url is None:
                    url = '/%s-%s' % (self.PARAM_ARTICLE, menu.id)
                b.a(href=url, color=s.linkColor, textdecoration=s.linkTextDecoration, 
                    padding=s.linkPadding, transition=s.linkTransition)
                b.text(menu.tag or menu.name)
                b._a()
                b._li()
            b._ol()
            b._nav()
            b._div(comment=colClass)
            b._block(self)
