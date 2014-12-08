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
from xierpa3.attributes import Em, Perc, Color
from xierpa3.descriptors.blueprint import BluePrint

class Menu(Component):
    u"""The @Menu@ supports a generic menu, setup as a list of links. The menu items are supplied
    by adapter id @C.ADAPTER_MENU@."""
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Component.C 
    
    BLUEPRINT = BluePrint(
        # Block stuff
        colWidth=8, doc_colWidth=u'Default amount of columns for this component.', 
        # nav stuff
        navWidth=Perc(100), doc_navWidth=u'Default with of the nav-tag.',
        navFloat=C.RIGHT, doc_navFloat=u'Float menu navigation left or right. Default is @C.RIGHT@.',
        navDisplay=C.INLINE, doc_navDisplay=u'Type of display for menu navigation. Default is @C.INLINE@.',
        navMargin=0, doc_navMargin=u'Margin of menu navigation. Default is @0@.',
        navFontSize=Em(1.5), doc_navFontSize=u'Font size of the menu navigation. Default is @Em(1.5)@.',
        # Menu list stuff
        listStyleType=C.NONE, doc_listStyleType=u'List style type of the menu. One of "W3SChools":http://www.w3schools.com/cssref/pr_list-style-type.asp',
        listDisplay=C.INLINE, doc_listDisplay=u'Direction of hte menu list. One of @(C.INLINE, C.BLOCK)@. Default is @C.INLINE@.',
        listFloat=C.RIGHT, doc_listFloat=u'Default float of the menu list.',
        listPadding=10, doc_listPadding=u'Padding of the menu list. Default is @Px(10)@.',
        # Link stuff
        linkColor=Color('#4890BE'), doc_linkColor=u"Link color of a menu item. Default is @Color('#4890BE')@.",
        linkTextDecoration=C.NONE, doc_linkTextDecoration=u'Link text decoration of a menu item. Default is @C.NONE@@.',
        linkPadding=Em(0.3), doc_linkPadding=u'Link padding of a menu item. Default is @Em(0.3)@.',
        linkTransition=None, doc_linkTransition=u'Link transition. Default is no transition.',
    )
    def buildBlock(self, b):
        u"""Build the menu from the articles in the menu tags of the @home.xml@ document."""
        s = self.style
        colClass = self.getColClass(s.colWidth)
        b.div(class_=colClass)
        b.nav(id=self.C.ID_NAVIGATIONWRAP, width=s.navWidth, float=s.navFloat,
            display=s.navDisplay, margin=s.navMargin, fontsize=s.navFontSize)
        b.ol(liststyletype=s.listStyleType, display=s.listDisplay)
        # Make separate build for CSS, since there may not be home menu items available when
        # rendering in CSS mode.
        if b.isType(('css', 'sass')):
            self.buildMenuStyle(b)
        else:
            self.buildMenuItems(b)
        b._ol()
        b._nav()
        b._div(comment=colClass)

    def buildMenuStyle(self, b):
        u"""Build the CSS/SASS style type of the menu, even if the home does not have a menu defined."""
        s = self.style
        b.li(float=s.listFloat, padding=s.listPadding)
        b.a(href='/dummy', color=s.linkColor, textdecoration=s.linkTextDecoration,
                padding=s.linkPadding, transition=s.linkTransition)
        b._a()
        b._li()

    def buildMenuItems(self, b):
        for menuItem in self.adapter.getMenuArticles(id=self.C.ID_HOME): # Main menu is defined on the home page.
            b.li()
            if menuItem.url:
                url = menuItem.url[0] # Get first of list of related urls or None
            else:
                url = '/%s-%s' % (self.C.PARAM_ARTICLE, menuItem.id)
            b.a(href=url)
            b.text(menuItem.tag or menuItem.name or 'Untagged menu article')
            b._a()
            b._li()
