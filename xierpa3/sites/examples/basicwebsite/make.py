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
#    make.py
#
#    Demo site for the simple "BasicWebsite" example.
#    Each of the builders takes the information from the theme to build its
#    own type of file.
#
import webbrowser
from xierpa3.attributes import Color, Em, Perc
from xierpa3.components import Theme, Page, Column, Container, Article, Footer
from xierpa3.toolbox.transformer import TX
from xierpa3.adapters.textilefileadapter import TextileFileAdapter

# Load @fontface fonts for this example from www.webtype.com
BODYFAMILY = '"Benton Sans RE", Verdana, sans'
HEADFAMILY = '"Hermes FB Semibold", Impact, Verdana, sans'

class Navigation(Column):

    def buildBlock(self, b):
        b.div(class_='navigation', marginbottom=Em(2), width=Perc(100), backgroundcolor=Color('#EEE'))
        for article in self.adapter.getRankedArticles():
            if article.title:
                b.a(href='/article-%s' % article.id, fontsize=Em(0.8), color=Color('#888'))
                b.text(article.title)
                b._a()
            else:
                b.text('No title for article "%s"' % article.id)
            b.br()
        b._div()

class BasicWebsite(Theme):
    u"""The *BasicWebsite* generates a basic website from a given adapter with all navigation
    and content in place. The styling is not different from default (no additional styling added,
    except what is already defined the @component.BLUEPRINT@."""
    C = Theme.C

    TITLE = u'Basic website.' # Use as title of window.
    XIERPA3_DEMOFONTS = "//cloud.webtype.com/css/34d3e5fe-7dee-4122-9e87-ea5ee4a90a05.css"
    URL_FONTS = [
        # Note that this package contains the a set of latest featured font, and may be changed in the future.
        # If using the font in this package, safest is to refer to the functional constant names below,
        # instead of making a direct reference to the family name.
        # Of course, taking your own account at //www.webtype.com is even better :)
        XIERPA3_DEMOFONTS, # Webtype @fontface fonts, to be used for localhost demo purposes.
    ]    
    # The single column is filled by the self.adapter article query result and standard navigation.
    # The default b.adapter taks the articles from the DbD site.

    def baseStyle(self):
        u"""Answer the single basis style that will be defined as overall CSS, before
        specific block definitions start."""
        s = Article.BLUEPRINT
        root = self.newStyle() # Create root style
        root.addStyle('body', fontfamily=BODYFAMILY, fontsize=s.fontSize,
            backgroundcolor=s.pageBackgroundColor, lineheight=s.lineHeight)
        s.addStyle('h1, h2, h3, h4, h5, p.lead', fontfamily=HEADFAMILY)
        s.addStyle('h6', fontfamily=BODYFAMILY)
        s.addStyle('b', fontweight=self.C.BOLD)
        return root

    def getSiteAdapter(self):
        u"""Answer the adapter for this site, including all articles of the DbD site."""
        from xierpa3.sites import doingbydesign
        # Root path where to find the article Simples wiki file for this example page.
        articleRoot = TX.module2Path(doingbydesign) + '/files/articles/'
        return TextileFileAdapter(articleRoot) # Preferred adapter class for articles in this site.

    def baseComponents(self):
        u"""Create a theme site with just one single template home page. Answer a list
        of page instances that are used as templates for this site."""
        # Create an instance (=object) of components to be placed on the page.
        # Import current example site, as anchor for the article files.
        adapter = self.getSiteAdapter()

        navigation = Navigation()
        column = Article()
        footer = Footer()
        container = Container(components=(navigation, column, footer))
        # Create an instance (=object) of the page, containing the navigation components.
        # The class is also the page name in the url.
        homePage = Page(class_=self.C.TEMPLATE_INDEX, components=container, adapter=adapter,
            title=self.TITLE, fonts=self.URL_FONTS)
        # Answer a list of types of pages for this site. In this case just one template.
        return [homePage]
    
