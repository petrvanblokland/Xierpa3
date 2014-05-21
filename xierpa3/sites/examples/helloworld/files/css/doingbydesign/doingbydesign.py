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
#    doingbydesignID.py
#
#    Demo application exporting to InDesign
#
#    http://localhost:8013/course/how-to-deal-with-customers
#
from xierpa3.themes.shop.shop import Shop
from xierpa3.adapters.fileadapter import FileAdapter
from xierpa3.descriptors.style import StyleSet
from xierpa3.attributes import Em
from xierpa3.components import Logo, Menu, SocialMedia, FeaturedByImage,\
    Article, ArticleSideBar, FeaturedByText, FeaturedByTextList, FeaturedByDiapText,\
    MobileNavigation, Container, Header, Footer, Page, Documentation, \
    ItemGroup, Featured
from xierpa3.constants.constants import C
from xierpa3.toolbox.transformer import TX
from xierpa3.sites import doingbydesign

# Adapter

class DbDAdapter(FileAdapter):
    pass

class DoingByDesign(Shop):
    u"""The <b>Shop</b> class implements the standard example shop
    with content based on files."""
    TITLE = 'Doing by Design'
    SUBTITLE = 'Notes on design and education.'

    # LOGO = 'http://%s/%s/logo.png' % (HOST, IMAGES_PATH)
    # LOGO = 'http://data.doingbydesign.com.s3.amazonaws.com/_images/logo.png'
    LOGO = 'Doing by Design'
    
    TEMPLATE_COURSES = 'courses'
    TEMPLATE_CATEGORY = 'category'
    TEMPLATE_PRODUCTS = 'products'
    
    URL_BACKGROUNDIMAGE = 'http://data.doingbydesign.com.s3.amazonaws.com/_images/articlebackground.png'
    
    URL_FONTS = (
        # Google
        'http://fonts.googleapis.com/css?family=Bree+Serif',
        #'http://fonts.googleapis.com/css?family=Droid+Sans:400,700'
        # Webtype project Poynter
        #'http://cloud.webtype.com/css/0d2e9f93-9866-45e1-8119-9b678ba5ce23.css'
        # Webtype project Doing by Design (Proforma & Rocky)
        #'http://cloud.webtype.com/css/d5663b37-b395-4934-9f68-2f7ccd9e8c87.css',
        # Topaz (Benton Sans RE)
        'http://cloud.webtype.com/css/7aa22aa1-1709-4b55-b95c-3413d3e5280a.css',
    )
    URL_JAVASCRIPT = ['http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js', 'js/toggle.js']

    # Cache the adapter, initialized automatic.
    ADAPTER = DbDAdapter(root=TX.module2Path(doingbydesign) + '/files/articles')

    CSS_BODYFONT = '"BentonSansRE"'
    CSS_HEADFONT = '"BentonSansCond Medium"'
    CSS_BODYSIZE = 13 # Fixed anchor for relative Em-based body sizes
    CSS_BODYLEADING = Em(1.4)
    CSS_BGCOLOR = '#FFFFFF'
    CSS_FOOTERBGCOLOR = '#E1E1E1'
    CSS_ALINKCOLOR = '#888888'
    CSS_AVISITEDCOLOR = '+60%'
    CSS_AHOVERCOLOR = '-60%'
    CSS_ACTIVECOLOR = '+60%'
    
    MAXWIDTH = 1140
    MINWIDTH = 755

    def _get_css(self):
        u"""Force building of CSS with valid set of parameters if "/force" is somewhere
        in the url of the requested page."""
        force = ''
        if self.e.form['force']:
            force = '/force'
        return ['%s/css/site.css' % force]

    def _set_css(self, urls):
        u"""Ignore for now."""
        pass

    css = property(_get_css, _set_css)

    def baseStyle(self):
        s = StyleSet() # Answer root style without selector
        s.addStyle('body', fontfamily=self.CSS_BODYFONT, fontsize=self.CSS_BODYSIZE,
            backgroundcolor=self.CSS_BGCOLOR, lineheight=self.CSS_BODYLEADING)
        s.addStyle('h1, h2, h3, h4, h5, p.lead', fontfamily=self.CSS_HEADFONT)
        s.addStyle('h6', fontfamily=self.CSS_BODYFONT)
        s.addStyle('div', float=self.FLOAT_LEFT, width=self.C100)
        s.addStyle('a, a:link', color=self.CSS_ALINKCOLOR)
        s.addStyle('a:visited', color=self.CSS_AVISITEDCOLOR)
        s.addStyle('a:hover', color=self.CSS_AHOVERCOLOR)
        s.addStyle('a:active', color=self.CSS_AACTIVECOLOR)
        s.addStyle('div.' + C.CLASS_1COL, margin=Em(0.5), float=C.LEFT, width='%d%%' % (98 / 12))
        s.addStyle('div.' + C.CLASS_2COL, margin=Em(0.5), float=C.LEFT, width='%d%%' % (98 * 2 / 12))
        s.addStyle('div.' + C.CLASS_4COL, margin=Em(0.5), float=C.LEFT, width='%d%%' % 30) #(98 * 4 / 12))
        s.addStyle('div.' + C.CLASS_8COL, margin=Em(0.5), float=C.LEFT, width='%d%%' % (98 * 8 / 12))
        s.addStyle('div.' + C.CLASS_12COL, margin=Em(0.5), float=C.LEFT, width=C.C100)
        s.addStyle('div.' + C.CLASS_LAST, marginright=Em(0))
        s.addStyle('ul', display=C.BLOCK)
        s.addStyle('li', display=C.BLOCK)
        s.addStyle('ol', liststyletype=C.DECIMAL)
        return s

    def baseComponents(self):        
        logo = Logo()
        menu = Menu()
        socialmedia = SocialMedia(twitterAccount='doingbydesign', facebookAccount='doingbydesign') 

        header = Header(components=(logo,menu), mobileContainerDisplay=C.NONE)
        mobileNavigation = MobileNavigation() # Is container by itself. Change??
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
            containerBackgroundColor=bgColor)
        # Featured text container
        bgColor = '#E8E8E8'
        featuredTexts = Featured(class_='featuredTexts', 
            components=(featuredByText, featuredByTextList),
            containerBackgroundColor=bgColor)
        # Footer group
        footer = Footer(components=(menu,), containerBackgroundColor=self.CSS_FOOTERBGCOLOR)

        # Documentation
        # The documentation class knows how to collect methods and their attrbutes
        # from components, adapters and builders and build them in an automated
        # documentation site.
        documentation = Documentation()
        
        # Article
        featuredByTextList = FeaturedByTextList() # Default start a featured index 0
        article = Container(class_=C.CLASS_ARTICLE, 
            containerBackgroundImage=self.URL_BACKGROUNDIMAGE, containerBackgroundRepeat=C.REPEAT, 
            components=(Article(), socialmedia, ArticleSideBar(), featuredByTextList))
    
        # Floating items
        thumbnails = ItemGroup(components=(featuredByImage100,))
        
        homePage = Page(name=C.TEMPLATE_INDEX,
            components=(mobileNavigation, header, featuredImages, featuredTexts, footer),
            css=self.URL_CSS, fonts=self.URL_FONTS, js=self.URL_JAVASCRIPT, favicon=self.URL_FAVICON)
    
        articlePage = Page(name=C.TEMPLATE_ARTICLE,
            components=(mobileNavigation, header, article, footer),
            css=self.URL_CSS, fonts=self.URL_FONTS, js=self.URL_JAVASCRIPT, favicon=self.URL_FAVICON)

        thumbnailPage = Page(name=self.TEMPLATE_COURSES,
            components=(mobileNavigation, header, featuredImages, footer),
            css=self.URL_CSS, fonts=self.URL_FONTS, js=self.URL_JAVASCRIPT, favicon=self.URL_FAVICON)

        productsPage = Page(name=self.TEMPLATE_PRODUCTS,
            components=(mobileNavigation, header, thumbnails, footer),
            css=self.URL_CSS, fonts=self.URL_FONTS, js=self.URL_JAVASCRIPT, favicon=self.URL_FAVICON)

        categoryPage = Page(name=self.TEMPLATE_CATEGORY,
            components=(mobileNavigation, header, footer),
            css=self.URL_CSS, fonts=self.URL_FONTS, js=self.URL_JAVASCRIPT, favicon=self.URL_FAVICON)

        # Automatic documentation about Xierpa3
        documentationPage = Page(name=C.TEMPLATE_DOCUMENTATION,
            components=(mobileNavigation, header, documentation, footer),
            css=self.URL_CSS, fonts=self.URL_FONTS, js=self.URL_JAVASCRIPT, favicon=self.URL_FAVICON)

        return [homePage, articlePage, productsPage, thumbnailPage, categoryPage, documentationPage]
