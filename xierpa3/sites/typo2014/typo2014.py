# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     xierpa server
#     Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#
#     X I E R P A  3
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    doingbydesignID.py
#
#    Demo application exporting to InDesign
#
#    http://localhost:8013/course/how-to-deal-with-customers
#
from xierpa3.themes.shop.shop import Shop
from xierpa3.adapters.textilefileadapter import TextileFileAdapter
#from xierpa3.descriptors.style import StyleSet
from xierpa3.attributes import Em, Perc
from xierpa3.components import Logo, SocialMedia, Header, MobileNavigation, Featured, Footer, Menu
from xierpa3.components import ItemGroup, Page, FeaturedByText, FeaturedByTextList, Article, Container
from xierpa3.components import FeaturedByDiapText, FeaturedByImage, Documentation, ArticleSideBar
#from xierpa3.constants.constants import C
#from xierpa3.toolbox.transformer import TX
#from xierpa3.sites import typo2014

FOOTERBACKGROUNDCOLOR = '#E1E1E1'
       
# Adapter

class Typo2014Adapter(TextileFileAdapter):
    pass
# Cache the adapter, initialized automatic.
#ADAPTER = Typo2014Adapter(root=TX.module2Path(typo2014) + '/files/articles')

class Typo2014(Shop):
    u"""The <b>Shop</b> class implements the standard example shop
    with content based on files."""
    TITLE = 'Doing by Design'
    SUBTITLE = 'Notes on design and education.'

    # LOGO = 'http://%s/%s/logo.png' % (HOST, IMAGES_PATH)
    # LOGO = 'http://data.doingbydesign.com.s3.amazonaws.com/_images/logo.png'
    LOGO = 'Typo 2014'
    SRCLOGO = 'http://data.xierpa.com.s3.amazonaws.com/_images/examples/typo2014.png'
    
    TEMPLATE_COURSES = 'courses'
    TEMPLATE_CATEGORY = 'category'
    TEMPLATE_PRODUCTS = 'products'
    
    URL_BACKGROUNDIMAGE = '//data.doingbydesign.com.s3.amazonaws.com/_images/articlebackground.png'
    URL_JAVASCRIPT = ['//ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js', 'js/toggle.js']

    CSS_BODYSIZE = 13 # Fixed anchor for relative Em-based body sizes
    CSS_BODYLEADING = Em(1.4)
    CSS_BGCOLOR = '#FFFFFF'
    CSS_ALINKCOLOR = '#888888'
    CSS_AVISITEDCOLOR = '+60%'
    CSS_AHOVERCOLOR = '-60%'
    CSS_ACTIVECOLOR = '+60%'

    MAXWIDTH = 1140
    MINWIDTH = 755

    def _get_css(self):
        # Force building of CSS with valid set of parameters
        force = ''
        if self.e.form['force']:
            force = '/force'
        return ['%s/css/site.css' % force]

    def _set_css(self, urls):
        # Ignore for now?
        pass

    css = property(_get_css, _set_css)

    def baseStyle(self):
        s = self.style # Answer root style without selector
        s.addStyle('body', fontfamily=s.bodyFamily, fontsize=self.CSS_BODYSIZE,
            backgroundcolor=self.CSS_BGCOLOR, lineheight=self.CSS_BODYLEADING)
        s.addStyle('h1, h2, h3, h4, h5, p.lead', fontfamily=self.CSS_HEADFONT)
        s.addStyle('h6', fontfamily=s.bodyFamily)
        s.addStyle('div', float=self.FLOAT_LEFT, width=Perc(100))
        s.addStyle('a, a:link', color=self.CSS_ALINKCOLOR)
        s.addStyle('a:visited', color=self.CSS_AVISITEDCOLOR)
        s.addStyle('a:hover', color=self.CSS_AHOVERCOLOR)
        s.addStyle('a:active', color=self.CSS_AACTIVECOLOR)
        s.addStyle('div.' + self.C.CLASS_1COL, margin=Em(0.5), float=self.C.LEFT, width='%d%%' % (98 / 12))
        s.addStyle('div.' + self.C.CLASS_2COL, margin=Em(0.5), float=self.C.LEFT, width='%d%%' % (98 * 2 / 12))
        s.addStyle('div.' + self.C.CLASS_4COL, margin=Em(0.5), float=self.C.LEFT, width='%d%%' % 30) #(98 * 4 / 12))
        s.addStyle('div.' + self.C.CLASS_8COL, margin=Em(0.5), float=self.C.LEFT, width='%d%%' % (98 * 8 / 12))
        s.addStyle('div.' + self.C.CLASS_12COL, margin=Em(0.5), float=self.C.LEFT, width=Perc(100))
        s.addStyle('div.' + self.C.CLASS_LAST, marginright=Em(0))
        s.addStyle('ul', display=self.C.BLOCK)
        s.addStyle('li', display=self.C.BLOCK)
        s.addStyle('ol', liststyletype=self.C.DECIMAL)
        return s

    def baseComponents(self):
        logo = Logo(logoSrc=self.SRCLOGO)
        menu = Menu()
        socialmedia = SocialMedia(twitterAccount='doingbydesign', facebookAccount='doingbydesign') 

        header = Header(components=(logo,menu), mobileContainerDisplay=self.NONE)
        mobileNavigation = MobileNavigation(title=self.TITLE) # Is container by itself. Change??
        # Articles featured by image
        featuredByImage = FeaturedByImage() # Featured article on a page. Main photo+link
        featuredByImage100 = FeaturedByImage(colWidth=9) # Featured article as group item
        #featuredByImageList = FeaturedByImageList() # Featured article on a page. List of related links
        # Articles featured by summary text
        featuredSideText = FeaturedByDiapText(colWidth=4, itemStart=1, label='Featured course')
        featuredByText = FeaturedByText(itemStart=2, showPoster=False)
        featuredByTextList = FeaturedByTextList(itemStart=5)
        # Featured black container
        bgColor = '#323A47'
        featuredImages = Featured(class_='featuredImages', 
            components=(featuredByImage, featuredSideText),
            #components=(featuredSideText, featuredByImage),
            containerBackgroundColor=bgColor)
        # Featured text container
        bgColor = '#E8E8E8'
        featuredTexts = Featured(class_='featuredTexts', 
            components=(featuredByText, featuredByTextList),
            containerBackgroundColor=bgColor)
        # Footer group
        footer = Footer(components=(menu,), containerBackgroundColor=FOOTERBACKGROUNDCOLOR)

        # Article
        featuredByTextList = FeaturedByTextList() # Default start a featured index 0
        article = Container(class_=self.C.CLASS_ARTICLE, 
            containerBackgroundImage=self.URL_BACKGROUNDIMAGE, containerBackgroundRepeat=self.C.REPEAT, 
            components=(Article(), socialmedia, ArticleSideBar(), featuredByTextList))
    
        # Floating items
        thumbnails = ItemGroup(components=(featuredByImage100,))

        # Documentation
        documentation = Documentation()
        
        homePage = Page(name=self.C.TEMPLATE_INDEX,
            components=(mobileNavigation, header, featuredImages, featuredTexts, footer),
            css=self.URL_CSS, fonts=self.URL_FONTS, js=self.URL_JAVASCRIPT, favicon=self.URL_FAVICON)

        articlePage = Page(name=self.C.TEMPLATE_ARTICLE,
            components=(mobileNavigation, header, article, footer),
            css=self.URL_CSS, fonts=self.URL_FONTS, js=self.URL_JAVASCRIPT, favicon=self.URL_FAVICON)

        thumbnailPage = Page(name=self.C.TEMPLATE_COURSES,
            components=(mobileNavigation, header, featuredImages, footer),
            css=self.URL_CSS, fonts=self.URL_FONTS, js=self.URL_JAVASCRIPT, favicon=self.URL_FAVICON)

        productsPage = Page(name=self.C.TEMPLATE_PRODUCTS,
            components=(mobileNavigation, header, thumbnails, footer),
            css=self.URL_CSS, fonts=self.URL_FONTS, js=self.URL_JAVASCRIPT, favicon=self.URL_FAVICON)

        categoryPage = Page(name=self.C.TEMPLATE_CATEGORY,
            components=(mobileNavigation, header, footer),
            css=self.URL_CSS, fonts=self.URL_FONTS, js=self.URL_JAVASCRIPT, favicon=self.URL_FAVICON)

        # Automatic documentation about Xierpa3
        documentationPage = Page(name=self.C.TEMPLATE_DOCUMENTATION,
            components=(mobileNavigation, header, documentation, footer),
            css=self.URL_CSS, fonts=self.URL_FONTS, js=self.URL_JAVASCRIPT, favicon=self.URL_FAVICON)

        return [homePage, articlePage, productsPage, thumbnailPage, categoryPage, documentationPage]
