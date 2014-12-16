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
#    navigation.py
#
from xierpa3.toolbox.transformer import TX
from xierpa3.components.component import Component
from xierpa3.attributes import Perc, Px, Em, Border, Z, Color
from xierpa3.descriptors.media import Media
from xierpa3.descriptors.blueprint import BluePrint

class Navigation(Component):
    u"""See also Menu component."""
    pass

class MobileNavigation(Navigation):
    u"""The **MobileNavigation** only shows in mobile screen mode."""
    
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Navigation.C 
    
    BLUEPRINT = BluePrint(
        colWidth=12,
        # Display stuff
        display=C.NONE, doc_display=u'Display type',
        displayMobile=C.BLOCK, doc_displayMobile=u'Display type for mobile.',
        # Container stuff
        width=None, doc_width=u'Mobile navigation container width.', 
        minWidth=0, doc_minWidth=u'Mobile navigation container minimal width', 
        # Navigation stuff
        backgroundColor=Color('#323A47'), doc_backgroundColor='Mobile navigation background color.',
        fontSize=Em(1.4), doc_fontSize=u'Mobile navigation font size.', 
        lineHeight=Em(1.1), doc_lineHeight=u'Mobile navigation leading.',
        marginLeft=0, doc_marginLeft=u'Mobile navigation margin left.',
        marginRight=0, doc_marginRight=u'Mobile navigation margin right.',
        paddingLeft=0, doc_paddingLeft=u'Mobile navigation padding left.',
        # Row
        rowClass=C.CLASS_12COL, doc_rowClass=u'Class of the row.',
        # Item stuff
        start=0, doc_start=u'Start of the index of selected pages. Suggestion to the adapter.',
        count=20, doc_count=u'Preferred/max amount of pages, suggestion to the adapter.',
        menuHeight=Px(44), doc_menuHeight=u'Menu height.',
        menuMargin=0, doc_menuMargin=u'Menu margin.', 
        menuBackgroundColor=Color('#323A47'), doc_menuBackgroundColor=u'Menu background color.',
        menuZIndex=Z(1000), doc_menuZIndex='Menu Z index', 
        menuBorderBottom=Border('1 solid white'), doc_menuBorderBottom=u'Menu border bottom.',
        menuWidth=Perc(100), doc_menuWidth=u'Menu width.', 
        # Nav stuff
        navWidth=Perc(30), doc_navWidth='Navigation width.', 
        navDisplay=C.INLINEBLOCK, doc_navDisplay=u'Navigation display type.',
        navZIndex=Z(1000), doc_navZIndex='Navigation Z index.',
        # List item stuff
        listFontSize=None,
        # Menu
        menuType=C.LIST, doc_menuType=u'Default is plain navigation list. Set to “menu” for menu.',
        menuListBackgroundColor=Color('#828487'),
        menuIconUrl='//data.doingbydesign.com.s3.amazonaws.com/_images/menu_icon.png', doc_menuIconUrl=u'Url of the menu icon',
        # Link stuff
        linkColor=C.WHITE, doc_linkColor=u'Link color',
    )                      
    def buildBlock(self, b):
        s = self.style
        menuArticles = self.adapter.getMenu(id=self.C.ID_HOME) # Get data for home page from adapter.
        b.div(class_=(self.C.CLASS_CONTAINER, self.className), display=s.display,
            backgroundcolor=s.backgroundColor, width=s.width,
            marginleft=s.marginLeft, marginright=s.marginRight,
            paddingleft=s.paddingLeft, paddingright=s.paddingRight,
            media=(
                Media(max=self.C.M_MOBILE_MAX, display=s.displayMobile),
            )
        )
        b.snippet(self, 'navigation-mobile') # Allow PHP to create a snippet file from this block.

        colClass = self.getColClass(s.colWidth)
        #b.text(data.loop) # In case there is PHP looping code. Skip for CSS
        b.div(class_=colClass, width=self.C.AUTO, float=self.C.NONE, marginleft=Em(0.5),
            marginright=Em(0.5), paddingleft=Em(0.5), paddingright=Em(0.5))
        b.div(id=self.C.ID_MOBILENAVWRAP, width=s.navWidth, display=s.navDisplay, zindex=s.navZIndex)
        b.div(id=self.C.ID_MENUICON, class_=self.C.CLASS_MENU, color=Color(self.C.WHITE), 
            height=26, width=56, paddingtop=Em(0.6), cursor='pointer',
            display=self.C.INLINEBLOCK, marginright=0, top=0, left=0, fontsize=Px(13))
        b.img(src=s.menuIconUrl,
            padding=0, margin=0, verticalalign=self.C.MIDDLE, maxwidth=Perc(50), height=self.C.AUTO)
        b._div(comment='#'+self.C.ID_MENUICON) # #menu-icon
        if menuArticles is None:
            b.error('No items in the adapter')
        else:
            b.ul(id=self.C.ID_NAV, backgroundcolor=s.menuListBackgroundColor,
                display=self.C.NONE, clear=self.C.BOTH, position=self.C.ABSOLUTE, top=s.menuHeight-5, 
                width=Perc(100), zindex=Z(2000), padding=0, margin=0, liststyletype=self.C.NONE, left=0,
                textalign=self.C.CENTER)
            homeArticle = self.adapter.getArticle(id=self.C.ID_HOME)
            for menuArticle in menuArticles:
                url = menuArticle.url
                if url is None:
                    url = '/%s-%s' % (self.C.PARAM_ARTICLE, menuArticle.id)
                b.li(fontsize=s.listFontSize, paddingtop=Em(1.2), width=Perc(100), liststyletype=self.C.NONE,
                    borderbottom=Border('1 solid white'), height=36, backgroundcolor=Color('#4890BC'))
                b.a(href=url, color=Color('#E8E8E8'))
                b.text(menuArticle.name or 'Untitled') # Show full name, otherwise use b.text(menu.tag or menu.name)
                b._a()
                b._li()
            b._ul()
        b._div(comment=self.C.ID_MOBILENAVWRAP)
        #b.a(href='/home', color='#E8E8E8')
        #b.text('Doing by Design')
        #b._a()
        b._div(comment=self.C.CLASS_12COL)
        #b.text(data._loop) # In case there is PHP looping code. Skip for CSS

        b._snippet(self) # In case PHP saved this block as snippet.
        b._div() # Final comment is automatic from component.selector
