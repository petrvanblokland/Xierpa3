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
from xierpa3.constants.constants import C
from xierpa3.attributes import Em, Border, Z, Margin
from xierpa3.descriptors.style import Media

class Navigation(Component):
    u"""See also Menu component."""
    pass

class MobileNavigation(Navigation):

    # TODO: Default style will become a Style, where all default values
    # also hold the description. This way the documentation for of the 
    # component API can be automated.
    STYLE_DEFAULT = dict(
        colWidth=12,
        # Container stuff
        containerDisplay=C.NONE, containerBackgroundColor='#323A47',
        containerFontSize=Em(1.4), containerLineHeight=Em(1.1), containerMarginLeft=0,
        containerMarginRight=0, containerPaddingLeft=0, containerPaddingRight=0,
        containerMenuHeight=48, containerZIndex=Z(1000),
        containerBorderBottom=Border('1 solid white'), containerWidth=C.C100, containerMinWidth=0,
        # Item stuff
        itemCount=20, # Preferred/max amount of page, suggestion to the adapter.
        menuHeight=44, menuMargin=0, menuBackgroundColor='#323A47',
        menuZIndex=Z(1000), menuBorderBottom=Border('1 solid white'), menuWidth=C.C100,
        menuMinWidth=0, 
        # Nav stuff
        navWidth='30%', navDisplay=C.INLINEBLOCK, navZIndex=Z(1000),
        # List item stuff
        listFontSize=None,
        # Menu
        menuListBackgroundColor='#828487',
        menuIconUrl='http://data.doingbydesign.com.s3.amazonaws.com/_images/menu_icon.png',
        # Link stuff
        linkColor=C.WHITE, 
        # Mobile stuff
        mobileContainerDisplay=C.BLOCK, 
    )
    def initialize(self):
        s = self.style
        self.menuType = 'list' # Default is plain navigation list. Set to 'menu' for menu.
        self.rowClass = self.CLASS_12COL
                      
    def buildBlock(self, b):
        s = self.style
        data = self.getAdapterData(self.ADAPTER_MENU, id='home')
        b.block(self) # div.mobileNavigation
        b.div(class_=(self.CLASS_CONTAINER, self.className), display=s.containerDisplay,
            backgroundcolor=s.containerBackgroundColor,
            marginleft=s.containerMarginLeft, marginright=s.containerMarginRight,
            paddingleft=s.containerPaddingLeft, paddingright=s.comtainerPaddingRight,
            media=Media(max=self.M_MOBILE, display=s.mobileContainerDisplay))
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
