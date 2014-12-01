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
#   doingbydesign.py
#
#   Kirsten examples
#
#   http://www.kirstenlangmuur.com/doingbydesign/nl/
#   http://www.kirstenlangmuur.com/doingbydesign/nl/articles
#   http://www.kirstenlangmuur.com/doingbydesign/nl/products
#   http://www.kirstenlangmuur.com/doingbydesign/nl/course
#
#   http://localhost:8013/course/how-to-deal-with-customers
#
#   Newspaper responsive example
#   http://www.liquidreplica.com/newspapers/
#
#   @@@ Temporary out of order. Needs update of some functions.
#   @@@ Wait for github commit.
#
#   The typical structure of a Xierpa3 site is:
#   body
#       div.page
#           div.top
#               div.row
#                   div.fiveCol          <-- Display is none for mobile
#                       Logo content
#                   div.(sevenCol last)  <-- Display is none for mobile
#                       Menu content
#                   div.(twelveCol last) <-- Display is none for desktop
#                       Mobile navigation content
#
#           div.featured
#               div.row
#                   div.eightCol
#                       Feature content
#                   div.(fourCol last)
#                       Feature content
#           div.section
#               div.row
#                   div.sixCol
#                       Feature content
#                   div.(sixCol last)
#                       Feature content
#           div.mainContent
#               div.row
#                   div.eightCol
#                       Article content
#                   div.(fourCol last)
#                       Article sidebar content
#           div.footer
#               div.row
#                   div.eightCol
#                       Menu content
#                   div.(fourCol last)
#                       Contact content
#
#   The xxCol widths always add up to 12, if they are visible at the same time.
#   The widths are set by the individual components.
#
#
from xierpa3.toolbox.transformer import TX
from xierpa3.themes.shop.shop import Shop
from xierpa3.adapters import TextileFileAdapter
from xierpa3.attributes import Em, Color, Perc
from xierpa3.components import Page, Container, Logo, MobileNavigation, Article, Menu, FeaturedByImage,\
    FeaturedByText
from xierpa3.descriptors.blueprint import BluePrint
from xierpa3.descriptors.media import Media

# Adapter

class DbDAdapter(TextileFileAdapter):
    def getDescription(self):
        return self.newData(text=u"""Doing by Design, information about design, design technology, design process and education. Physical and digital.""")
     
    def getKeyWords(self):
        return self.newData(text=u"""Doing, design, design process, programming, design education""")

# Components

class DbDMobileNavigation(MobileNavigation):
    BLUEPRINT = BluePrint(MobileNavigation.BLUEPRINT,
        # Layout alternatives
    )

class Top(Container):
    BLUEPRINT = BluePrint(MobileNavigation.BLUEPRINT,
        # Layout alternatives
    )

class Featured(Container):
    BLUEPRINT = BluePrint(MobileNavigation.BLUEPRINT,
        # Layout alternatives
    )

class Section(Container):
    BLUEPRINT = BluePrint(MobileNavigation.BLUEPRINT,
        # Layout alternatives
    )

class MainContent(Container):
    BLUEPRINT = BluePrint(MobileNavigation.BLUEPRINT,
        # Layout alternatives
    )

class Footer(Container):
    BLUEPRINT = BluePrint(MobileNavigation.BLUEPRINT,
        # Layout alternatives
    )

class DoingByDesign(Shop):
    u"""The DoingByDesign class implements extended file (textile) based blog site.
    It is identical to the site that is on doingbydesign.com."""

    C = Shop.C

    TITLE = 'Doing by Design'
    SUBTITLE = 'Learn by doing your own design'

    URL_JAVASCRIPT = ['//ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js'] #, 'js/toggle.js']

    def baseStyle(self):
        s = self.newStyle() # Answer root style without selector
        return s

    def baseComponents(self):        
        # Import current example site, as anchor for the article files.
        from xierpa3.sites import doingbydesign
        # Root path where to find the article Simples wiki file for this example page.
        articleRoot = TX.module2Path(doingbydesign) + '/files/articles/'
        adapter = DbDAdapter(articleRoot) # Preferred adapter class for articles in this site.

        logo = Logo(text='Doing by Design', fontFamily='Impact', color=Color('#888'), fontSize=Em(1.8))
        menu = Menu()
        mobileNavigation = DbDMobileNavigation()
        article = Article()

        featuredByImage = FeaturedByImage(start=0, width=Perc(65.4), showTitle=False,
            showHeadline=False, showTopic=False)
        featuredByText = FeaturedByText(start=0, width=Perc(30.75))

        # Containers
        top = Top(components=(logo, menu), backgroundColor=Color('yellow'), media=Media(max=self.C.M_MOBILE_MAX, display=self.C.NONE))
        featured = Featured(components=(featuredByImage, featuredByText))
        section = Section(components=(featuredByImage,))
        mainContent = MainContent(components=article)
        footer = Footer(components=(menu))

        homePage = Page(name=self.C.TEMPLATE_INDEX,
            components=(mobileNavigation, top, featured, section, mainContent, footer),
            css=self.C.URL_CSS, fonts=self.C.URL_FONTS, js=self.URL_JAVASCRIPT,
            favicon=self.C.URL_FAVICON, adapter=adapter)

        articlePage = Page(name=self.C.TEMPLATE_ARTICLE,
            comoonents=(mobileNavigation, top, article, footer),
            css=self.C.URL_CSS, fonts=self.C.URL_FONTS, js=self.URL_JAVASCRIPT,
            favicon=self.C.URL_FAVICON, adapter=adapter)

        return [homePage, articlePage]
