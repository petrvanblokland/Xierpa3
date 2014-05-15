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
#    theme.py
#
#    Example theme to build a blog site.
#
#    TODO
#    Make it work (including auto install) with Amazon database + CMS functions
#    Make example templates and components
#    Make payed Udemy course how to use/implement/build
#    Blog/site/store of components with specific tasks
#
import os
from xierpa3.components.theme import Theme
from xierpa3.attributes import * 
from xierpa3.components import *
from xierpa3.descriptors.style import Style, StyleSet
from xierpa3.constants.constants import C

# Subclasses to force naming in HTML and CSS classes.
class Subtitle(Group):
    pass

class IconBar(Group):
    pass

class MainContent(Group):
    pass

class SimpleBlog(Theme):
    u"""The <b>SimpleBlog</b> class implements the standard example blog."""
    TITLE = 'Blog Petr van Blokland + Claudia Mens'
    SUBTITLE = 'Notes on design and education.'

    UNIT = 8
    UNIT2 = UNIT/4
    CSS_PADDING = UNIT
    # Relative column sizes
    C1 = '20%'
    C2 = '40%'
    C3 = '60%'
    C4 = '80%'
    C5 = C100 = '100%'
    # Typographic measures
    CSS_BODYSIZE = 11
    CSS_BODYLEADING = '1.4em'
    CSS_HEADLEADING = '1.2em'
    CSS_SUBHEADLEADING = '1.2em'
    CSS_TITLESIZE = CSS_BODYSIZE*2
    CSS_SUBTITLESIZE = CSS_BODYSIZE*1.5
    CSS_ITALIC = 'italic'
    CSS_VERTICAL = 'vertical' # Menu
    CSS_BLOCK = 'block'
    CSS_NONE = 'none'
    # Links
    CSS_BGCOLOR = 'white' # Gray background with white page?
    CSS_ALINKCOLOR = '#201010'
    CSS_AVISITEDCOLOR = '#202030'
    CSS_AHOVERCOLOR = '#202020'
    CSS_AACTIVECOLOR = CSS_ALINKCOLOR
    # Float
    FLOAT_LEFT = 'left'
    FLOAT_RIGHT = 'right'
    FLOAT_NONE = 'none'
    # Media ranges
    M_MOBILE = 500
    M_IPAD = 650
    M_DESKTOP = 900
    M_LARGESCREEN = 1200
    
    WEBFONTS = 'http://cloud.webtype.com/css/7aa22aa1-1709-4b55-b95c-3413d3e5280a.css'
    CSS_BODYFONT = 'BentonSansRE, Verdana, sans'
    CSS_HEADFONT = 'MillerDisplay Semibold, Georgia, serif'
    CSS_SUBHEADFONT = 'MillerDisplay RomanItalic, Georgia, serif'
    CSS_TAGCLOUDFONT = 'AmplitudeComp Medium, Impact'
    
    CSS_H3FONTSIZE = CSS_BODYSIZE*1.3
    CSS_H3LEADING = CSS_SUBHEADLEADING
    CSS_H3FONTFAMILY = CSS_HEADFONT
            
    def baseStyle(self):
        s = StyleSet() # Answer root style without selector
        s.addStyle('body', fontfamily=self.CSS_BODYFONT, fontsize=self.CSS_BODYSIZE, 
            backgroundcolor=self.CSS_BGCOLOR, leading=self.CSS_BODYLEADING)
        s.addStyle('div', float=self.FLOAT_LEFT, width=self.C100)
        s.addStyle('a:link', color=self.CSS_ALINKCOLOR)
        s.addStyle('a:visited', color=self.CSS_AVISITEDCOLOR)
        s.addStyle('a:hover', color=self.CSS_AHOVERCOLOR)
        s.addStyle('a:active', color=self.CSS_AACTIVECOLOR)
        return s
    
    def baseComponents(self):
        # Header
        title = Link(Title(self.TITLE, class_='title', fontsize=self.CSS_TITLESIZE, 
            fontfamily=self.CSS_HEADFONT, leading=self.CSS_HEADLEADING))
        title.addMedia(min=self.M_DESKTOP, fontsize=self.CSS_TITLESIZE*1.3)
        title.addMedia(min=self.M_MOBILE, max=self.M_IPAD, fontsize=self.CSS_TITLESIZE*0.7)
        title.addMedia(max=self.M_MOBILE, fontsize=self.CSS_TITLESIZE*0.9)
        
        subtitle = Subtitle(self.SUBTITLE, class_='subtitle', fontsize=self.CSS_SUBTITLESIZE, 
            fontfamily=self.CSS_SUBHEADFONT, leading=self.CSS_SUBHEADLEADING)
        
        logo = Logo(contentID=C.ADAPTER_LOGOURL, width=self.C1)
        logo.addMedia(max=self.M_MOBILE, display='none')
        
        header = Header((title, subtitle), id=self.ID_HEADER, width=self.C3)
        header.addMedia(max=self.M_MOBILE, width=self.C100) 
        
        menu = Menu(width=self.C1, type=self.CSS_VERTICAL, display=self.CSS_BLOCK)
        menu.addMedia(max=self.M_MOBILE, width=self.C100)  
        
        headerbar = Group((logo, header, menu), width=self.C100)
        
        # Iconbar
        socialmedia = SocialMedia(width=self.C1, float=self.FLOAT_LEFT)
        socialmedia.addMedia(max=self.M_MOBILE, width=self.C100)
        icons = Thumbnails(contentID=C.ADAPTER_FEATUREDARTICLETHUMBS, width=self.C4, 
            count=8, height=42)
        icons.addMedia(max=self.M_MOBILE, display=self.CSS_NONE)
        iconbar = IconBar((socialmedia, icons), width=self.C100, marginbottom=6)

        # Sidebar
        message = Message(contentID=C.ADAPTER_MESSAGE, width=self.C100)
        message.addMedia(max=self.M_MOBILE, display='none')
        tagCloud = TagCloud(width=self.C100, 
            fontfamily=self.CSS_TAGCLOUDFONT, color=Color('#888888'), fontsize=18)
        tagCloud.addMedia(max=self.M_MOBILE, display='none')
        #sidebar = Sidebar((message, tagCloud), width=self.C1)
        sidebar = Sidebar((message,), width=self.C1)
        sidebar.addMedia(max=self.M_MOBILE, width=self.C100, backgroundcolor='#F0F0F0')

        # #article
        article = Article(contentID=C.ADAPTER_ARTICLE, id='article', width=self.C3, editable=True)
        article.addMedia(max=self.M_MOBILE, width=self.C100, fontsize=self.CSS_BODYSIZE*1.2)

        # Home thumbs
        homeThumbs = ThumbnailGrid(width=self.C4, count=20)
        homeThumbs.addStyle(selector='h3', fontfamily=self.CSS_H3FONTFAMILY, 
            fontsize=self.CSS_H3FONTSIZE, leading=self.CSS_H3LEADING, marginbottom=self.UNIT2, 
            margintop=self.UNIT2) 
        homeThumbs.addMedia(min=self.M_LARGESCREEN, headsize=self.CSS_TITLESIZE)
        homeThumbs.addMedia(max=self.M_MOBILE, width=self.C100)
        
        # Footer
        footer = Footer(contentID=C.ADAPTER_FOOTER, backgroundcolor=self.CSS_BGCOLOR, 
            width=self.C100, float=self.FLOAT_LEFT)
         
        # MainContent
        thumbnailMain = MainContent((sidebar, homeThumbs), width=self.C5, float=self.FLOAT_LEFT) 
            
        # ArticleMain
        articleMain = MainContent((sidebar, article), width=self.C5, float=self.FLOAT_LEFT)
         
        # P A G E S
        
        # Home page: Main = Grid of sidebar + thumbnails               
        homePage = Page(name=C.TEMPLATE_INDEX, components=(headerbar, iconbar, thumbnailMain, footer), 
            padding=self.UNIT, width=self.C100,
            css=self.URL_CSS, js=self.URL_JAVASCRIPT,
            webfonts=self.URL_WEBFONTS,
            favIcon=self.URL_FAVICON)
        homePage.addMedia(min=self.LARGESCREEN, width=self.M_LARGESCREEN, float=self.FLOAT_NONE,
            margin=Margin(0,'auto'), backgroundcolor='pink')
        
        # Article page        
        articlePage = Page(name=C.TEMPLATE_ARTICLE, components=(headerbar, iconbar, articleMain, footer),
            padding=self.UNIT, width=self.C100,
            css=self.URL_CSS, js=self.URL_JAVASCRIPT,
            webfonts=self.URL_WEBFONTS,
            favIcon=self.URL_FAVICON)
        articlePage.addMedia(min=self.LARGESCREEN, width=self.M_LARGESCREEN, float=self.FLOAT_NONE,
            margin=Margin(0,'auto'), backgroundcolor='pink')

        return [homePage, articlePage]
