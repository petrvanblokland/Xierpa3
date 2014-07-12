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
from xierpa3.attributes import Em, Perc
from xierpa3.descriptors.blueprint import BluePrint

class Menu(Component):
    u"""The <b>Menu</b> supports a generic menu, setup as a list of links. The menu items are supplied
    by adapter id <b>C.ADAPTER_MENU</b>."""
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Component.C 
    
    BLUEPRINT = BluePrint(
        # Block stuff
        colWidth=8, doc_colWidth=u'Default amount of columns for this component.', 
        # nav stuff
        navWidth=Perc(100), # ...
        navFloat=C.RIGHT, 
        navDisplay=C.INLINE, 
        navMargin=0, 
        navFontSize=Em(1.5),
        # Menu list stuff
        listStyleType=C.NONE, doc_listStyleType=u'List style type. One of "W3SChools":http://www.w3schools.com/cssref/pr_list-style-type.asp',
        listDisplay=C.INLINE, doc_listDisplay=u'Direction of hte menu list. One of @(C.INLINE, C.BLOCK)@.',
        listFloat=C.RIGHT, 
        listPadding=10,
        # Link stuff
        linkColor='#4890be', doc_linkColor=u'Link color',
        linkTextDecoration=C.NONE, 
        linkPadding=Em(0.3), doc_linkPadding=u'Link padding',
        linkTransition=None, #Transition(),
    )
    def buildBlock(self, b):
        u"""Build the menu from the articles in the menu tags of the @home.xml@ document."""
        data = self.adapter.getMenu(id='home') # Main menu is defined on the home page.
        if data.items:
            s = self.style
            b.block(self)
            colClass = self.getColClass(s.colWidth)
            b.div(class_=colClass)
            b.nav(id=self.C.ID_NAVIGATIONWRAP, width=s.navWidth, float=s.navFloat, 
                display=s.navDisplay, margin=s.navMargin, fontsize=s.navFontSize)
            b.ol(styletype=s.listStyleType, display=s.listDisplay)
            for menuItem in data.items:
                b.li(float=s.listFloat, padding=s.listPadding)
                print 'wererwerw', menuItem.url
                if menuItem.url:
                    url = menuItem.url[0] # Get first of list of related urls or None
                else:
                    url = '/%s-%s' % (self.C.PARAM_ARTICLE, menuItem.id)
                b.a(href=url, color=s.linkColor, textdecoration=s.linkTextDecoration, 
                    padding=s.linkPadding, transition=s.linkTransition)
                b.text(menuItem.tag or menuItem.name)
                b._a()
                b._li()
            b._ol()
            b._nav()
            b._div(comment=colClass)
            b._block(self)
