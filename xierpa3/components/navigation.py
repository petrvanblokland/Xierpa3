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
from xierpa3.components.component import Component
from xierpa3.attributes import Perc, Px, Em, Border, Z, Margin
from xierpa3.descriptors.media import Media
from xierpa3.descriptors.blueprint import BluePrint

class Navigation(Component):
    u"""See also Menu component."""
    pass

class MobileNavigation(Navigation):

    CC = Navigation # Get constants through super class
    
    BLUEPRINT = BluePrint(
        colWidth=12,
        # Display stuff
        display=CC.NONE, doc_display=u'Display type',
        displayMobile=CC.BLOCK, doc_displayMobile=u'Display type for mobile.',
        # Container stuff
        width=None, doc_width=u'Mobile navigation container width.', 
        minWidth=0, doc_minWidth=u'Mobile navigation container minimal width', 
        # Navigation stuff
        backgroundColor='#323A47', doc_backgroundColor='Mobile navigation background color.',
        fontSize=Em(1.4), doc_fontSize=u'Mobile navigation font size.', 
        lineHeight=Em(1.1), doc_lineHeight=u'Mobile navigation leading.',
        marginLeft=0, doc_marginLeft=u'Mobile navigation margin left.',
        marginRight=0, doc_marginRight=u'Mobile navigation margin right.',
        paddingLeft=0, doc_paddingLeft=u'Mobile navigation padding left.',
        # Row
        rowClass=CC.CLASS_12COL, doc_rowClass=u'Class of the row.',
        # Item stuff
        itemCount=20, doc_itemCount=u'Preferred/max amount of pages, suggestion to the adapter.',
        menuHeight=Px(44), doc_menuHeight=u'Menu height.',
        menuMargin=0, doc_menuMargin=u'Menu margin.', 
        menuBackgroundColor='#323A47', doc_menuBackgroundColor=u'Menu background color.',
        menuZIndex=Z(1000), doc_menuZIndex='Menu Z index', 
        menuBorderBottom=Border('1 solid white'), doc_menuBorderBottom=u'Menu border bottom.',
        menuWidth=Perc(100), doc_menuWidth=u'Menu width.', 
        # Nav stuff
        navWidth=Perc(30), doc_navWidth='Navigation width.', 
        navDisplay=CC.INLINEBLOCK, doc_navDisplay=u'Navigation display type.',
        navZIndex=Z(1000), doc_navZIndex='Navigation Z index.',
        # List item stuff
        listFontSize=None,
        # Menu
        menuType=CC.LIST, doc_menuType=u'Default is plain navigation list. Set to “menu” for menu.',
        menuListBackgroundColor='#828487',
        menuIconUrl='//data.doingbydesign.com.s3.amazonaws.com/_images/menu_icon.png', doc_menuIconUrl=u'Url of the menu icon',
        # Link stuff
        linkColor=CC.WHITE, doc_linkColor=u'Link color',
    )                      
    def buildBlock(self, b):
        s = self.style
        data = self.getAdapterData(self.ADAPTER_MENU, id='home') # Get data for home page from adapter.
        b.block(self) # div.mobileNavigation
        b.div(class_=(self.CLASS_CONTAINER, self.className), display=s.display,
            backgroundcolor=s.backgroundColor, width=s.width,
            marginleft=s.marginLeft, marginright=s.marginRight,
            paddingleft=s.paddingLeft, paddingright=s.paddingRight,
            media=(
                Media(max=self.M_MOBILE_MAX, display=s.displayMobile),
            )
        )
        b.snippet(self, 'navigation-mobile') # Allow PHP to create a snippet file from this block.

        b.div(class_=self.CLASS_ROW, minwidth=0, paddingleft=0, paddingright=0, 
            overflow=self.HIDDEN, margin=Margin(0, self.AUTO))
        colClass = self.getColClass(s.colWidth)
        #b.text(data.loop) # In case there is PHP looping code. Skip for CSS
        b.div(class_=colClass, width=self.AUTO, float=self.NONE, marginleft=Em(0.5),
            marginright=Em(0.5), paddingleft=Em(0.5), paddingright=Em(0.5))
        b.div(id=self.ID_MOBILENAVWRAP, width=s.navWidth, display=s.navDisplay, zindex=s.navZIndex)
        b.div(id=self.ID_MENUICON, class_=self.CLASS_MENU, color=self.WHITE, height=26, width=56,
            paddingtop=0.6, cursor='pointer',
            display=self.INLINEBLOCK, marginright=0, top=0, left=0, fontsize=13)
        b.img(src=s.menuIconUrl,
            padding=0, margin=0, verticalalign=self.MIDDLE, maxwidth='50%', height=self.AUTO)
        b._div(comment='#'+self.ID_MENUICON) # #menu-icon
        if data.menuItems is None:
            b.error('No items in the adapter')
        else:
            b.ul(id=self.ID_NAV, backgroundcolor=s.menuListBackgroundColor,
                display=self.NONE, clear=self.BOTH, position=self.ABSOLUTE, top=s.menuHeight-5, 
                width=self.C100, zindex=Z(2000), padding=0, margin=0, liststyletype=self.NONE, left=0,
                textalign=self.CENTER)
        
            for menu in data.menuItems:
                url = menu.url
                if url is None:
                    url = '/%s-%s' % (self.PARAM_ARTICLE, menu.id)
                b.li(fontsize=s.listFontSize, paddingtop=Em(1.2), width=self.C100, liststyletype=self.NONE,
                    borderbottom=Border('1 solid white'), height=36, backgroundcolor='#4890BC')
                b.a(href=url, color='#E8E8E8')
                b.text(menu.name) # Show full name, otherwise use b.text(menu.tag or menu.name)
                b._a()
                b._li()
            b._ul()
        b._div(comment=self.ID_MOBILENAVWRAP)
        #b.a(href='/home', color='#E8E8E8')
        #b.text('Doing by Design')
        #b._a()
        b._div(comment=self.CLASS_12COL)
        #b.text(data._loop) # In case there is PHP looping code. Skip for CSS
        b._div(comment=self.CLASS_ROW)

        b._snippet(self) # In case PHP saved this block as snippet.
        b._div() # Final comment is automatic from component.selector
        b._block(self) # div.mobileNavigation
